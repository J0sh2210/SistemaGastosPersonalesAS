from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from models.schemas import IngresoCreate, IngresoUpdate

class IngresoService:
    @staticmethod
    def registrar(db: Session, ingreso: IngresoCreate):
        query = text("""
            EXEC sp_RegistrarIngreso 
            @Concepto = :Concepto, 
            @Monto = :Monto, 
            @IdCliente = :IdCliente
        """)
        # Ejecutamos y extraemos la fila devuelta por el SP
        result = db.execute(query, {
            "Concepto": ingreso.Concepto,
            "Monto": ingreso.Monto,
            "IdCliente": ingreso.IdCliente
        }).fetchone()
        
        db.commit()
        return result._mapping if result else None

    @staticmethod
    def editar(db: Session, id_movimiento: int, ingreso: IngresoUpdate):
        query = text("""
            EXEC sp_EditarIngreso 
            @IdMovimiento = :IdMovimiento, 
            @Concepto = :Concepto, 
            @Monto = :Monto
        """)
        result = db.execute(query, {
            "IdMovimiento": id_movimiento,
            "Concepto": ingreso.Concepto,
            "Monto": ingreso.Monto
        }).fetchone()
        
        db.commit()
        
        # Si el SP no devuelve nada, significa que el ID no existe o no era un Ingreso
        if not result:
            raise HTTPException(
                status_code=404, 
                detail="Ingreso no encontrado o pertenece a un Egreso"
            )
            
        return result._mapping