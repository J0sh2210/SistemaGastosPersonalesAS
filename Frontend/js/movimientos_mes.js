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

    // 👉 NUEVO: Convertimos el mes y año seleccionados en Fechas para el Backend
    const mesFormateado = mes.padStart(2, '0'); // Asegura que "5" se vuelva "05"
    const fechaInicio = `${anio}-${mesFormateado}-01`; // Siempre el día 1
    
    // El '0' en el día de Date nos da automáticamente el último día del mes
    const ultimoDia = new Date(anio, mes, 0).getDate(); 
    const fechaFin = `${anio}-${mesFormateado}-${ultimoDia}`;

    try {
        // 👉 AHORA ENVIAMOS fecha_inicio y fecha_fin en la URL
        const res = await fetch(`${API}/movimientos/filtrar?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Error al obtener movimientos");
        }
        
        const data = await res.json();
        
        console.log(`Buscando del ${fechaInicio} al ${fechaFin}`, data);
        
        actualizarVista(data, parseInt(mes), parseInt(anio));
    } catch (e) {
        document.getElementById("contenido-tabla").innerHTML =
            `<p class="empty-msg">❌ Error: ${e.message}</p>`;
    }
}

function actualizarVista(data, mes, anio) {
    // 1. Extraemos el arreglo sin importar cómo lo haya envuelto el backend
    const movimientos = Array.isArray(data) ? data : (data.movimientos || data.data || []);

    if (!movimientos || movimientos.length === 0) {
        document.getElementById("contenido-tabla").innerHTML =
            '<p class="empty-msg">No hay movimientos para este mes.</p>';
        document.getElementById("resumen").style.display = "none";
        return;
    }

    let totalIngresos = 0;
    let totalEgresos = 0;

    const filas = movimientos.map(m => {
        // 2. Prevenimos el error de undefined asegurando mayúsculas o minúsculas
        const idMovimiento = m.idMovimiento || m.IdMovimiento;
        const concepto = m.concepto || m.Concepto;
        const monto = parseFloat(m.monto || m.Monto);
        const idTipo = m.idTipo || m.IdTipo;
        const fecha = m.fechaMovimiento || m.FechaMovimiento;

        const esIngreso = idTipo === 1;
        if (esIngreso) totalIngresos += monto;
        else totalEgresos += monto;

        return `
            <tr>
                <td>${idMovimiento}</td>
                <td>${concepto}</td>
                <td>Q${monto.toFixed(2)}</td>
                <td>${new Date(fecha).toLocaleDateString("es-GT")}</td>
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
