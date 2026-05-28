const API_URL = "http://127.0.0.1:8000";
let gastoEditandoId = null;
let listaGastosGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
    cargarListaRecurrentes();
});

// 👉 NUEVAS FUNCIONES PARA CONTROLAR LA PANTALLA
function mostrarFormulario() {
    // Le quitamos la clase "oculto" para que se expanda suavemente
    document.getElementById("panel-formulario").classList.remove("oculto"); 
    
    // Ocultamos el botón verde (puedes dejar esto con display)
    document.getElementById("btnMostrarFormulario").style.display = "none"; 
}

function ocultarFormulario() {
    // Le agregamos la clase "oculto" para que se encoja suavemente
    document.getElementById("panel-formulario").classList.add("oculto"); 
    
    // Mostramos el botón verde de nuevo tras un pequeño retraso
    setTimeout(() => {
        document.getElementById("btnMostrarFormulario").style.display = "block"; 
    }, 400); // 400ms espera a que termine la animación de cierre

    // Limpiamos los campos
    const form = document.getElementById("form-ingreso") || document.getElementById("formGasto");
    if(form) form.reset();
    
    const msg = document.getElementById("ing-msg") || document.getElementById("mensaje");
    if(msg) msg.innerText = "";
}


async function cargarListaRecurrentes() {
    const cuerpoTabla = document.getElementById("cuerpo-tabla-recurrentes");
    const idUsuarioActual = localStorage.getItem("IdCliente");

    if (!idUsuarioActual) {
        cuerpoTabla.innerHTML = "<tr><td colspan='4'>Inicia sesión para ver tus gastos.</td></tr>";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/gastos-recurrentes/${idUsuarioActual}`);
        
        if (response.ok) {
            const gastos = await response.json();
            listaGastosGlobal = gastos; 
            cuerpoTabla.innerHTML = "";

            if (gastos.length === 0) {
                cuerpoTabla.innerHTML = "<tr><td colspan='4' style='text-align: center;'>No tienes gastos recurrentes registrados.</td></tr>";
                return;
            }

            gastos.forEach(gasto => {
                const idDelGasto = gasto.IdGasto || gasto.IdGastoRecurrente; 

                const fila = `
                    <tr>
                        <td>${gasto.Concepto}</td>
                        <td>Q${gasto.Monto}</td>
                        <td style="text-transform: capitalize;">${gasto.Frecuencia}</td>
                        <td style="text-align: center;">
                            <button class="btn-accion" onclick="prepararEdicion(${idDelGasto})" title="Editar">✏️</button>
                            <button class="btn-accion" onclick="eliminarGasto(${idDelGasto})" title="Eliminar">🗑️</button>
                        </td>
                    </tr>
                `;
                cuerpoTabla.innerHTML += fila;
            });
        }
    } catch (error) {
        console.error("Error de conexión al cargar la lista:", error);
    }
}

async function eliminarGasto(idGasto) {
    if (!idGasto) return;

    if (confirm("¿Estás seguro de que deseas eliminar este gasto recurrente?")) {
        const mensaje = document.getElementById("mensaje");
        try {
            const response = await fetch(`${API_URL}/gastos-recurrentes/eliminar/${idGasto}`, {
                method: "DELETE"
            });

            if (response.ok) {
                mensaje.style.color = "#10b981";
                mensaje.innerText = "✅ Gasto eliminado correctamente";
                cargarListaRecurrentes();
                setTimeout(() => {
                    mensaje.innerText = "";
                }, 2000);
            } else {
                mensaje.style.color = "red";
                mensaje.innerText = "❌ Hubo un problema al intentar eliminar el gasto.";
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
            mensaje.style.color = "red";
            mensaje.innerText = "❌ Error al eliminar el gasto.";
        }
    }
}

function prepararEdicion(idGasto) {
    // 1. Buscamos el gasto
    const gasto = listaGastosGlobal.find(g => (g.IdGasto || g.IdGastoRecurrente) === idGasto);
    if (!gasto) return;

    // 2. Mostramos el formulario por si estaba oculto
    mostrarFormulario();

    // 3. Llenamos los inputs
    document.getElementById("concepto").value = gasto.Concepto;
    document.getElementById("monto").value = gasto.Monto;
    document.getElementById("frecuencia").value = gasto.Frecuencia.toLowerCase();
    
    if (gasto.FechaInicio) {
        document.getElementById("fechaInicio").value = gasto.FechaInicio.split("T")[0];
    }

    // 4. Activamos modo edición
    gastoEditandoId = idGasto;
    const btnSubmit = document.getElementById("btnGuardarGasto");
    btnSubmit.innerText = "Actualizar Gasto";
    btnSubmit.style.backgroundColor = "#f59e0b"; // Naranja
}

// Evento Submit (POST y PUT)
document.getElementById("formGasto").addEventListener("submit", async function(e) {
    e.preventDefault();

    const idUsuarioActual = localStorage.getItem("IdCliente");
    const mensaje = document.getElementById("mensaje");

    if (!idUsuarioActual) {
        mensaje.style.color = "red";
        mensaje.innerText = "❌ Tu sesión ha expirado. Por favor inicia sesión de nuevo.";
        setTimeout(() => {
            window.location.href = "usuario_index.html";
        }, 2000);
        return; 
    }

    const dataPUT = {
        Concepto: document.getElementById("concepto").value,
        Monto: parseFloat(document.getElementById("monto").value),
        Frecuencia: document.getElementById("frecuencia").value
    };

    try {
        let response;

        if (gastoEditandoId === null) {
            // MODO CREAR (POST)
            const dataPOST = {
                ...dataPUT,
                FechaInicio: new Date(document.getElementById("fechaInicio").value).toISOString().split("T")[0],
                IdCliente: parseInt(idUsuarioActual)
            };

            response = await fetch(`${API_URL}/gastos-recurrentes/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dataPOST)
            });
        } else {
            // MODO EDITAR (PUT)
            response = await fetch(`${API_URL}/gastos-recurrentes/${gastoEditandoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dataPUT)
            });
        }

        if (response.ok) {
            const successMsg = gastoEditandoId ? "Gasto actualizado con éxito" : "Gasto creado con éxito";
            mensaje.style.color = "#10b981";
            mensaje.innerText = "✅ " + successMsg;
            cargarListaRecurrentes(); 
            setTimeout(() => ocultarFormulario(), 1500);
            
        } else {
            const errorData = await response.json();
            console.error("Error del backend:", errorData);
            mensaje.style.color = "red";
            mensaje.innerText = "❌ Error en la operación. Revisa los datos.";
        }

    } catch (error) {
        console.error(error);
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
    }
});