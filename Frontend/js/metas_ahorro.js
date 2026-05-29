const API_URL = "http://127.0.0.1:8000";
const idUsuarioActual = localStorage.getItem("IdCliente"); // Ajustado a IdUsuario según lo corregimos

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token || !idUsuarioActual) {
        window.location.href = "usuario_index.html";
        return;
    }
    
    // Llamamos a la función al cargar la página para pintar la tabla
    cargarListaMetas(); 
});

// 👉 FUNCIÓN PARA OBTENER Y PINTAR LAS METAS EN LA TABLA
async function cargarListaMetas() {
    const cuerpoTabla = document.getElementById("cuerpo-tabla-metas");
    const token = localStorage.getItem("token");

    try {
        // Hacemos el GET al endpoint que acabas de crear
        const response = await fetch(`${API_URL}/api/metas/${idUsuarioActual}`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${token}` 
            }
        });

        if (response.ok) {
            const metas = await response.json();
            cuerpoTabla.innerHTML = ""; // Limpiamos el mensaje de "Aún no tienes metas"

            if (metas.length === 0) {
                cuerpoTabla.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 20px; color: #6b7280;">Aún no tienes metas registradas.</td></tr>`;
                return;
            }

            // Recorremos las metas y creamos las filas
            metas.forEach(meta => {
                const fila = document.createElement("tr");
                fila.style.borderBottom = "1px solid #ddd";

                // Formateamos los números a dos decimales
                const montoObjetivo = parseFloat(meta.MontoObjetivo).toFixed(2);
                const montoActual = parseFloat(meta.MontoActual).toFixed(2);

                fila.innerHTML = `
                    <td style="padding: 12px; font-weight: bold; color: #374151;">${meta.NombreMeta}</td>
                    <td style="padding: 12px; color: #1c9cf7; font-weight: bold;">
                        Q ${montoActual} <span style="color:#6b7280; font-size: 0.85em; font-weight: normal;">/ Q ${montoObjetivo}</span>
                    </td>
                    <td style="padding: 12px; color: #4b5563;">${meta.FechaLimite}</td>
                `;
                cuerpoTabla.appendChild(fila);
            });
        } else {
            cuerpoTabla.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 20px; color: red;">Error al cargar las metas.</td></tr>`;
        }
    } catch (error) {
        console.error("Error en el fetch de metas:", error);
        cuerpoTabla.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 20px; color: red;">Error de conexión con el servidor.</td></tr>`;
    }
}


// 👉 FUNCIONES PARA CONTROLAR LA ANIMACIÓN DEL FORMULARIO
function mostrarFormulario() {
    document.getElementById("panel-formulario").classList.remove("oculto"); 
    document.getElementById("btnMostrarFormulario").style.display = "none";
}

function ocultarFormulario() {
    document.getElementById("panel-formulario").classList.add("oculto"); 
    setTimeout(() => {
        document.getElementById("btnMostrarFormulario").style.display = "block"; 
    }, 300); 

    const form = document.getElementById("formMeta");
    if(form) form.reset();
    
    const msg = document.getElementById("mensaje");
    if(msg) msg.innerText = "";
}

// 👉 EVENTO GUARDAR META
document.getElementById('formMeta').addEventListener('submit', async (e) => {
    e.preventDefault();

    const mensaje = document.getElementById('mensaje');
    const token = localStorage.getItem("token");

    mensaje.style.color = "#6b7280";
    mensaje.innerText = "⏳ Guardando meta...";

    const dataPOST = {
        id_usuario: parseInt(idUsuarioActual),
        nombre_meta: document.getElementById("nombreMeta").value,
        monto_objetivo: parseFloat(document.getElementById("montoObjetivo").value),
        fecha_limite: document.getElementById("fechaLimite").value,
        monto_actual: 0.0 
    };

    try {
        const response = await fetch(`${API_URL}/api/metas/`, { 
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` 
            },
            body: JSON.stringify(dataPOST)
        });

        if (response.ok) {
            mensaje.style.color = "#10b981";
            mensaje.innerText = "✅ Meta creada con éxito";
            
            // 👉 Actualizamos la tabla inmediatamente sin recargar la página
            cargarListaMetas(); 
            
            setTimeout(() => ocultarFormulario(), 1500);
        } else {
            const errorData = await response.json();
            mensaje.style.color = "red";
            mensaje.innerText = "❌ Error: " + (errorData.detail || "Revisa los datos");
        }

    } catch (error) {
        console.error("Error en el fetch:", error);
        mensaje.style.color = "red";
        mensaje.innerText = "❌ Error de conexión al servidor.";
    }
});