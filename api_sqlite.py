from flask import Flask, request, jsonify, g
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

app = Flask(__name__)

# SQLite - Runs immediately, no build tools needed
DATABASE_URL = "sqlite:///gastos.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# Gasto table
class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    monto = Column(Integer)

# Create tables
Base.metadata.create_all(engine)

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@app.before_request
def before_request():
    g.db = None

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy - SQLite", "db": DATABASE_URL})

@app.route("/gastos", methods=["GET"])
def ver_gastos():
    try:
        db = get_db()
        gastos = db.query(Gasto).all()
        return jsonify([{"id": g.id, "descripcion": g.descripcion, "monto": g.monto} for g in gastos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gastos", methods=["POST"])
def agregar_gasto():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400
    data = request.json
    descripcion = (data.get("descripcion") or "").strip()
    monto = data.get("monto")
    if not descripcion or not isinstance(monto, (int, float)) or monto <= 0:
        return jsonify({"error": "Invalid data"}), 400
    try:
        db = get_db()
        nuevo = Gasto(descripcion=descripcion, monto=int(monto))
        db.add(nuevo)
        db.commit()
        return jsonify({"mensaje": "Added", "id": nuevo.id}), 201
    except Exception as e:
        if 'db' in locals():
            db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/gastos/<int:id>", methods=["DELETE"])
def eliminar_gasto(id):
    try:
        db = get_db()
        gasto = db.get(Gasto, id)
        if not gasto:
            return jsonify({"error": "Not found"}), 404
        db.delete(gasto)
        db.commit()
        return jsonify({"mensaje": "Deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gastos/<int:id>", methods=["PUT"])
def editar_gasto(id):
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400
    data = request.json
    descripcion = (data.get("descripcion") or "").strip()
    monto = data.get("monto")
    if not descripcion or not isinstance(monto, (int, float)) or monto <= 0:
        return jsonify({"error": "Invalid data"}), 400
    try:
        db = get_db()
        gasto = db.get(Gasto, id)
        if not gasto:
            return jsonify({"error": "Not found"}), 404
        gasto.descripcion = descripcion
        gasto.monto = int(monto)
        db.commit()
        return jsonify({"mensaje": "Updated"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
