//Enma
async function cargarGastos() {
    try {
        const response = await fetch("http://127.0.0.1:8000/gastos-recurrentes/");

        if (!response.ok) {
            throw new Error("Error al obtener los datos del servidor");
        }

        const data = await response.json();
        console.log("Datos recibidos:", data);

        const tabla = document.getElementById("tablaGastos");

        if (!tabla) {
            console.error("No se encontró el elemento tablaGastos");
            return;
        }

        // Limpiar tabla antes de llenar
        tabla.innerHTML = "";

        data.forEach(gasto => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${gasto.IdGastoRecurrente}</td>
                <td>${gasto.Concepto}</td>
                <td>Q${gasto.Monto}</td>
                <td>${gasto.FechaInicio}</td>
                <td>${gasto.Frecuencia}</td>
                <td>
                    <button onclick="editarGasto(${gasto.IdGastoRecurrente})">
                        ✏️Editar
                    </button>

                    <button class="btn-eliminar" onclick="eliminarGasto(${gasto.IdGastoRecurrente})">
                        Eliminar
                    </button>
                </td>
            `;

            tabla.appendChild(fila);
        });

    } catch (error) {
        console.error("Error real:", error);
    }
}


function editarGasto(id) {
    if (!id) return;
    window.location.href = `editar_gasto_recurrente.html?id=${id}`;
}
// Función para desactivar (eliminar lógico)
async function eliminarGasto(id) {
    if (!confirm("¿Seguro que deseas desactivar este gasto?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/gastos-recurrentes/desactivar/${id}`, {
            method: "PUT"
        });

        if (response.ok) {
            alert("Gasto desactivado correctamente");
            cargarGastos(); // recargar tabla
        } else {
            alert("Error al desactivar gasto");
        }

    } catch (error) {
        console.error("Error:", error);
    }
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", cargarGastos);