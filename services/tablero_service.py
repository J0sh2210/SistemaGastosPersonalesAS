from database import engine  # Importamos el motor que tienes en tu database.py
from fastapi import HTTPException
from sqlalchemy import text  # Necesario para ejecutar texto SQL plano en SQLAlchemy

class ResumenService:
    @staticmethod
    def obtener_resumen_presupuestos_sp9(id_usuario: int):
        try:
            # 1. Abrimos una conexión usando el motor de tu database.py
            with engine.connect() as connection:
                
                # 2. Preparamos la llamada al procedimiento almacenado de forma segura
                query = text("EXEC sp_ObtenerResumenPresupuestos @IdUsuario = :id_usuario")
                
                # 3. Ejecutamos pasando el parámetro
                result = connection.execute(query, {"id_usuario": id_usuario})
                
                resumen_presupuestos = []
                
                # 4. Mapeamos las filas que devuelve el SP a nuestro arreglo JSON
                for row in result:
                    resumen_presupuestos.append({
                        "categoria": row.categoria,     
                        "limite": float(row.limite),     
                        "gastado": float(row.gastado),   
                        "porcentaje": float(row.porcentaje), 
                        "estado": row.estado            
                    })
                
                return resumen_presupuestos

        except Exception as e:
            print(f"Error en ResumenService (SP9 con SQLAlchemy): {str(e)}")
            raise HTTPException(status_code=500, detail="Error interno al procesar el SP9")