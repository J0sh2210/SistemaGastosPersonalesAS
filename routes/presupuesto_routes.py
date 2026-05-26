from fastapi import APIRouter, HTTPException, status  # <-- MODIFICADO: Agregamos HTTPException y status
from datetime import datetime  # <-- NUEVO: Agregamos esto para obtener el mes actual

from models.presupuesto_model import (
    PresupuestoCreate,
    PresupuestoUpdate
)
from services.presupuesto_service import (
    crear_presupuesto_mensual,
    obtener_presupuestos,
    actualizar_presupuesto,
    eliminar_presupuesto
)
# CORREGIDO: Importamos la clase correcta que tienes mapeada
from services.tablero_service import ResumenService

router = APIRouter(
    prefix="/presupuestos",
    tags=["Presupuestos"]
)

# =========================================================================
# FUNCIÓN MODIFICADA CON LA VALIDACIÓN DEL MES ACTUAL
# =========================================================================
@router.post("/", response_model=None)
def crear_presupuesto(presupuesto_data: PresupuestoCreate):
    # 1. Capturamos el año y mes actual del sistema (Ej: '2026-05')
    mes_actual = datetime.now().strftime("%Y-%m")
    
    # 2. CORREGIDO: Cambiado '.mes' por '.mes_aplicacion' para coincidir con tu Pydantic y JS
    if presupuesto_data.mes_aplicacion != mes_actual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación denegada. Solo se permite ingresar presupuestos para el mes actual ({mes_actual})."
        )
        
    # 3. Si todo está bien, procede al Service y al SP
    return crear_presupuesto_mensual(presupuesto_data)

@router.get("/", response_model=None)
def listar_presupuestos():
    return obtener_presupuestos()

@router.put("/{id_presupuesto}", response_model=None)
def editar_presupuesto(id_presupuesto: int, data: PresupuestoUpdate):
    return actualizar_presupuesto(id_presupuesto, data)

@router.delete("/{id_presupuesto}")
def eliminar(id_presupuesto: int):
    return eliminar_presupuesto(id_presupuesto)

# =========================================================================
# RUTA DEL TABLERO CORREGIDA
# =========================================================================
@router.get("/resumen/{id_usuario}")
def obtener_resumen_tablero(id_usuario: int):
    # CORREGIDO: Cambiado TableroService por tu importación real ResumenService
    return ResumenService.obtener_resumen_presupuestos_sp9(id_usuario)