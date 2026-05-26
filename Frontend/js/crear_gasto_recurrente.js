// URL base de tu API FastAPI
const API_URL = "http://127.0.0.1:8000";

// 1. CARGAR LA LISTA AL ABRIR LA PÁGINA
document.addEventListener("DOMContentLoaded", () => {
    cargarListaRecurrentes();
});

// 2. FUNCIÓN PARA OBTENER Y MOSTRAR LOS GASTOS DEL USUARIO
async function cargarListaRecurrentes() {
    const cuerpoTabla = document.getElementById("cuerpo-tabla-recurrentes");
    const idUsuarioActual = localStorage.getItem("IdCliente");

    // Si no hay usuario logueado, no intentamos cargar la tabla
    if (!idUsuarioActual) {
        cuerpoTabla.innerHTML = "<tr><td colspan='3'>Inicia sesión para ver tus gastos.</td></tr>";
        return;
    }

    try {
        // 👉 AHORA LE PASAMOS EL ID DIRECTAMENTE A LA RUTA DEL BACKEND
        const response = await fetch(`${API_URL}/gastos-recurrentes/${idUsuarioActual}`);
        
        if (response.ok) {
            const gastos = await response.json();
            
            // Limpiamos la tabla antes de llenarla
            cuerpoTabla.innerHTML = "";

            // Verificamos si el usuario tiene gastos registrados
            if (gastos.length === 0) {
                cuerpoTabla.innerHTML = "<tr><td colspan='3' style='text-align: center;'>No tienes gastos recurrentes registrados.</td></tr>";
                return;
            }

            // Recorremos los gastos y creamos una fila por cada uno
            gastos.forEach(gasto => {
                const fila = `
                    <tr>
                        <td>${gasto.Concepto}</td>
                        <td>Q${gasto.Monto}</td>
                        <td style="text-transform: capitalize;">${gasto.Frecuencia}</td>
                    </tr>
                `;
                cuerpoTabla.innerHTML += fila;
            });
        } else {
            console.error("Error al obtener los gastos del servidor.");
        }
    } catch (error) {
        console.error("Error de conexión al cargar la lista:", error);
    }
}

// 3. FUNCIÓN PARA CREAR UN NUEVO GASTO RECURRENTE
document.getElementById("formGasto").addEventListener("submit", async function(e) {
    e.preventDefault();

    const idUsuarioActual = localStorage.getItem("IdCliente");
    const mensaje = document.getElementById("mensaje");

    // Validación de seguridad por si expiró la sesión
    if (!idUsuarioActual) {
        alert("Tu sesión ha expirado o no has iniciado sesión. Por favor, vuelve a ingresar.");
        return; 
    }

    // Armamos los datos tal cual los espera tu modelo Pydantic
    const data = {
        Concepto: document.getElementById("concepto").value,
        Monto: parseFloat(document.getElementById("monto").value),
        FechaInicio: new Date(document.getElementById("fechaInicio").value).toISOString().split("T")[0],
        Frecuencia: document.getElementById("frecuencia").value, // Asegúrate de que tu HTML envíe "mensual" en minúsculas
        IdCliente: parseInt(idUsuarioActual)
    };

    try {
        const response = await fetch(`${API_URL}/gastos-recurrentes/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            mensaje.style.color = "green";
            mensaje.innerText = "Gasto recurrente creado correctamente";
            document.getElementById("formGasto").reset(); // Limpia el formulario
            
            // 👉 ACTUALIZAMOS LA TABLA AL INSTANTE
            cargarListaRecurrentes();

            // Quitamos el mensaje de éxito después de 3 segundos
            setTimeout(() => { mensaje.innerText = ""; }, 3000);
            
        } else {
            const errorData = await response.json();
            console.log("Error detallado del backend:", errorData);
            mensaje.style.color = "red";
            mensaje.innerText = "Error al crear gasto. Revisa los datos.";
        }

    } catch (error) {
        console.error(error);
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
    }
});