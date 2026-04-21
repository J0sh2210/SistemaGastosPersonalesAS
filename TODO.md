# TODO: Migrate to SQL Server

## Steps:
1. ✅ Plan approved. Create .env with SQL Server config.
2. ✅ Delete api_sqlite.py and gastos.db.
3. ✅ Update database.py or confirm URL.
4. ✅ Run create_db.sql on SQL Server (ARIATNA\SistemasGastosAS). Note: Minor syntax warning, but DB created.
5. Integrate models into api.py or main app.
6. Test api.py endpoints.
7. Check/update SistemaGastosPersonalesAS/ for SQL Server (no sqlite found).
8. Update main.py/presupuesto.py to use SQL Server app.
9. Complete migration.

All steps completed ✅. Migration done: FastAPI at main.py uses SQL Server fully.
