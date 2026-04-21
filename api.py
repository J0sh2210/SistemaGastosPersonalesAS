from flask import Flask, request, jsonify, g
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

app = Flask(__name__)

# -------- CONEXIÓN A SQL SERVER --------
DATABASE_URL = "mssql+pyodbc://@ARIATNA/gastosDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# -------- TABLA --------
class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    monto = Column(Integer)


# -------- MANEJO DE DB --------
def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# -------- HEALTH --------
@app.route("/health", methods=["GET"])
def health():
    try:
        db = get_db()
        db.execute(text("SELECT 1"))
        return jsonify({"status": "healthy"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# -------- GET --------
@app.route("/gastos", methods=["GET"])
def ver_gastos():
    try:
        db = get_db()
        gastos = db.query(Gasto).all()
        return jsonify([
            {"id": g.id, "descripcion": g.descripcion, "monto": g.monto}
            for g in gastos
        ])
    except Exception as e:
        return jsonify({"error": f"Error al obtener gastos: {str(e)}"}), 500

# -------- POST --------
@app.route("/gastos", methods=["POST"])
def agregar_gasto():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400

    data = request.json
    descripcion = (data.get("descripcion") or "").strip()
    monto = data.get("monto")

    if not descripcion:
        return jsonify({"error": "Descripción requerida"}), 400
    if not isinstance(monto, (int, float)) or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    try:
        db = get_db()
        nuevo = Gasto(descripcion=descripcion, monto=int(monto))
        db.add(nuevo)
        db.commit()
        return jsonify({"mensaje": "Gasto agregado", "id": nuevo.id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Error al agregar gasto: {str(e)}"}), 500

# -------- DELETE --------
@app.route("/gastos/<int:id>", methods=["DELETE"])
def eliminar_gasto(id):
    try:
        db = get_db()
        gasto = db.get(Gasto, id)

        if not gasto:
            return jsonify({"error": "Gasto no encontrado"}), 404

        db.delete(gasto)
        db.commit()
        return jsonify({"mensaje": "Gasto eliminado"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Error al eliminar gasto: {str(e)}"}), 500

# -------- PUT --------
@app.route("/gastos/<int:id>", methods=["PUT"])
def editar_gasto(id):
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400

    data = request.json
    descripcion = (data.get("descripcion") or "").strip()
    monto = data.get("monto")

    if not descripcion:
        return jsonify({"error": "Descripción requerida"}), 400
    if not isinstance(monto, (int, float)) or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    try:
        db = get_db()
        gasto = db.get(Gasto, id)

        if not gasto:
            return jsonify({"error": "Gasto no encontrado"}), 404

        gasto.descripcion = descripcion
        gasto.monto = int(monto)
        db.commit()
        return jsonify({"mensaje": "Gasto actualizado"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Error al actualizar gasto: {str(e)}"}), 500

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)