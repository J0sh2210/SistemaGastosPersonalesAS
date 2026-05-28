const API = "http://localhost:8000";

const MESES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

async function cargarMovimientos() {
    const mes = document.getElementById("selectMes").value;
    const anio = document.getElementById("inputAnio").value;
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    document.getElementById("contenido-tabla").innerHTML = '<p class="loading">⏳ Cargando...</p>';
    document.getElementById("resumen").style.display = "none";

    try {
        const res = await fetch(`${API}/movimientos/filtrar?mes=${mes}&anio=${anio}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Error al obtener movimientos");
        }
        const movimientos = await res.json();
        actualizarVista(movimientos, parseInt(mes), parseInt(anio));
    } catch (e) {
        document.getElementById("contenido-tabla").innerHTML =
            `<p class="empty-msg">❌ Error: ${e.message}</p>`;
    }
}

function actualizarVista(movimientos, mes, anio) {
    if (!movimientos || movimientos.length === 0) {
        document.getElementById("contenido-tabla").innerHTML =
            '<p class="empty-msg">No hay movimientos para este mes.</p>';
        document.getElementById("resumen").style.display = "none";
        return;
    }

    let totalIngresos = 0;
    let totalEgresos = 0;

    const filas = movimientos.map(m => {
        const monto = parseFloat(m.monto);
        const esIngreso = m.idTipo === 1;
        if (esIngreso) totalIngresos += monto;
        else totalEgresos += monto;

        return `
            <tr>
                <td>${m.idMovimiento}</td>
                <td>${m.concepto}</td>
                <td>Q${monto.toFixed(2)}</td>
                <td>${new Date(m.fechaMovimiento).toLocaleDateString("es-GT")}</td>
                <td><span class="badge ${esIngreso ? 'ingreso' : 'egreso'}">
                    ${esIngreso ? 'Ingreso' : 'Egreso'}
                </span></td>
            </tr>
        `;
    }).join("");

    const balance = totalIngresos - totalEgresos;

    document.getElementById("total-ingresos").textContent = `Q${totalIngresos.toFixed(2)}`;
    document.getElementById("total-egresos").textContent = `Q${totalEgresos.toFixed(2)}`;
    document.getElementById("balance").textContent = `Q${balance.toFixed(2)}`;
    document.getElementById("resumen").style.display = "flex";

    document.getElementById("contenido-tabla").innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Concepto</th>
                    <th>Monto</th>
                    <th>Fecha</th>
                    <th>Tipo</th>
                </tr>
            </thead>
            <tbody>${filas}</tbody>
        </table>
    `;
}

// Cargar mes actual al iniciar
window.onload = () => {
    const hoy = new Date();
    document.getElementById("selectMes").value = hoy.getMonth() + 1;
    document.getElementById("inputAnio").value = hoy.getFullYear();
    cargarMovimientos();
};
