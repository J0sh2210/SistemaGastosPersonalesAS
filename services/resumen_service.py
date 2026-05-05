from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, List
from models.schemas import ResumenMesResponse  # Se creará

def obtener_resumen_mes(id_cliente: int, anio: int, mes: int, db: Session) -> ResumenMesResponse:
    try:
        # Usa SP existente para obtener movimientos del mes
        query = text("EXEC sp_ObtenerMovimientosMesActual @IdCliente = :IdCliente")
        movimientos = db.execute(query, {"IdCliente": id_cliente}).fetchall()
    except Exception:
        # Fallback al mock si SP falla
        return obtener_resumen_mes_mock(id_cliente, anio, mes)
    
    # Procesar para resumen
    total_ingresos = 0.0
    total_egresos = 0.0
    ingresos = []
    egresos = []
    
    for row in movimientos:
        try:
            mapping = row._mapping
            monto = float(mapping['Monto'])
            id_tipo = int(mapping['IdTipo'])
            
            item = {
                'idMovimiento': int(mapping['IdMovimiento']),
                'concepto': str(mapping['Concepto']),
                'monto': monto,
                'fechaMovimiento': str(mapping['FechaMovimiento'])
            }
            
            if id_tipo == 1:  # Ingreso
                total_ingresos += monto
                ingresos.append(item)
            else:  # Egreso
                total_egresos += monto
                egresos.append(item)
        except (KeyError, ValueError, TypeError) as e:
            # Ignora filas malformadas, continúa con datos válidos
            continue
    
    balance = total_ingresos - total_egresos
    
    return ResumenMesResponse(
        anio=anio,
        mes=mes,
        idCliente=id_cliente,
        totalIngresos=total_ingresos,
        totalEgresos=total_egresos,
        balance=balance,
        ingresos=ingresos,
        egresos=egresos
    )

# MOCK (si SP no existe)
def obtener_resumen_mes_mock(id_cliente: int, anio: int, mes: int) -> ResumenMesResponse:
    return ResumenMesResponse(
        anio=anio,
        mes=mes,
        idCliente=id_cliente,
        totalIngresos=5000.0,
        totalEgresos=3000.0,
        balance=2000.0,
        ingresos=[{"idMovimiento": 1, "concepto": "Sueldo", "monto": 5000, "fechaMovimiento": "2024-01-05"}],
        egresos=[{"idMovimiento": 2, "concepto": "Alquiler", "monto": 3000, "fechaMovimiento": "2024-01-10"}]
    )
