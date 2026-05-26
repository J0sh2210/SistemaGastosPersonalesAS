const API_RESUMEN_URL = "http://127.0.0.1:8000/presupuestos/resumen";

// CORREGIDO: Buscamos la clave exacta que tu login guarda en el navegador
const ID_USUARIO_ACTUAL = localStorage.getItem("IdCliente");

document.addEventListener("DOMContentLoaded", () => {
    // Validación de seguridad real usando los datos de tu sesión
    if (!ID_USUARIO_ACTUAL) {
        console.error("No se detectó un usuario con sesión activa.");
        const bloqueBarras = document.getElementById("bloque-barras-consumo");
        if (bloqueBarras) {
            bloqueBarras.innerHTML = `<tr><td colspan="3" class="loading-text" style="color: #dc2626; text-align: center;">⚠️ Error: Sesión no válida. Inicie sesión nuevamente.</td></tr>`;
        }
        return;
    }

    // Si hay sesión activa, ejecuta el monitoreo automáticamente
    actualizarMonitoreo();
    
    const btnActualizar = document.getElementById("btn-actualizar");
    if (btnActualizar) {
        btnActualizar.addEventListener("click", actualizarMonitoreo);
    }
});

async function actualizarMonitoreo() {
    const bloqueBarras = document.getElementById("bloque-barras-consumo");
    const panelAlertas = document.getElementById("panel-alertas-criticas");
    const listaAlertas = document.getElementById("lista-alertas-detalladas");

    bloqueBarras.innerHTML = `<tr><td colspan="3" class="loading-text" style="text-align: center;">Calculando porcentajes en tiempo real...</td></tr>`;
    listaAlertas.innerHTML = "";
    panelAlertas.style.display = "none";

    try {
        // NOTA: Es crucial usar backticks (``) para mapear correctamente la URL con el ID dinámico
        const response = await fetch(`${API_RESUMEN_URL}/${ID_USUARIO_ACTUAL}`);
        
        if (!response.ok) throw new Error("Error en la respuesta del servidor.");

        const resumenes = await response.json();
        bloqueBarras.innerHTML = ""; 

        // Si el usuario seleccionado no tiene nada en la base de datos, mostrará esto:
        if (!resumenes || resumenes.length === 0) {
            bloqueBarras.innerHTML = `<tr><td colspan="3" class="loading-text" style="text-align: center;">No posees presupuestos activos este mes.</td></tr>`;
            return;
        }

        let tieneAlertas = false;

        resumenes.forEach(item => {
            let colorClase = "color-success"; 
            if (item.estado === "ALERTA") colorClase = "color-warning"; 
            if (item.estado === "EXCEDIDO") colorClase = "color-error"; 

            const porcentajeAcotado = item.porcentaje > 100 ? 100 : item.porcentaje;

            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td style="font-weight: 600; text-align: left; padding-left: 15px;">${item.categoria}</td>
                <td style="padding: 12px 10px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 3px;">
                        <strong>${item.porcentaje}%</strong>
                        <span>Límite: Q ${parseFloat(item.limite).toFixed(2)}</span>
                    </div>
                    <div class="progress-bar-wrapper">
                        <div class="progress-bar-fill ${colorClase}" style="width: ${porcentajeAcotado}%;"></div>
                    </div>
                </td>
                <td style="font-weight: 700; color: ${item.estado === 'EXCEDIDO' ? '#dc2626' : 'var(--text-main)'}">
                    Q ${parseFloat(item.gastado).toFixed(2)}
                </td>
            `;
            bloqueBarras.appendChild(fila);

            if (item.estado === "ALERTA" || item.estado === "EXCEDIDO") {
                tieneAlertas = true;
                const tarjeta = document.createElement("div");
                
                if (item.estado === "EXCEDIDO") {
                    tarjeta.className = "alert-box";
                    tarjeta.innerHTML = `🚨 <strong>Presupuesto Excedido:</strong> El rubro de <strong>${item.categoria}</strong> ha superado el tope financiero asignado. Consumo actual: <strong>Q ${parseFloat(item.gastado).toFixed(2)}</strong> de un límite de <strong>Q ${parseFloat(item.limite).toFixed(2)}</strong>.`;
                } else {
                    tarjeta.className = "alert-box warning";
                    tarjeta.innerHTML = `⚠️ <strong>Alerta de Proximidad:</strong> El rubro de <strong>${item.categoria}</strong> consumió más del 80% previsto. Consumo actual: <strong>Q ${parseFloat(item.gastado).toFixed(2)}</strong> de un límite de <strong>Q ${parseFloat(item.limite).toFixed(2)}</strong>.`;
                }
                listaAlertas.appendChild(tarjeta);
            }
        });

        if (tieneAlertas) {
            panelAlertas.style.display = "block";
        }

    } catch (error) {
        console.error("Detalle del error:", error);
        bloqueBarras.innerHTML = `<tr><td colspan="3" class="loading-text" style="text-align: center; color: #dc2626;">⚠️ Error en la conexión con la API de monitoreo.</td></tr>`;
    }
}