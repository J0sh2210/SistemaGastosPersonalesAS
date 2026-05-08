const API_URL = "http://127.0.0.1:8000/gastos-recurrentes/";

async function cargarGastos() {
    try {

        const respuesta = await fetch(API_URL);

        const gastos = await respuesta.json();

        const tabla = document.getElementById("tabla-gastos");

        tabla.innerHTML = "";

        gastos.forEach(gasto => {

            const fila = `
                <tr>
                    <td>${gasto.IdGastoRecurrente}</td>
                    <td>${gasto.Concepto}</td>
                    <td>${gasto.Monto}</td>
                    <td>${gasto.Frecuencia}</td>

                    <td>
                        <button onclick="eliminarGasto(${gasto.IdGastoRecurrente})">
                            Eliminar
                        </button>
                    </td>
                </tr>
            `;

            tabla.innerHTML += fila;
        });

    } catch (error) {
        console.error("Error al cargar gastos:", error);
    }
}

async function eliminarGasto(id) {

    const confirmar = confirm("¿Desea eliminar este gasto recurrente?");

    if (!confirmar) {
        return;
    }

    try {

        const respuesta = await fetch(
            `http://127.0.0.1:8000/gastos-recurrentes/desactivar/${id}`,
            {
                method: "PUT"
            }
        );

        if (respuesta.ok) {

            alert("Gasto eliminado correctamente");

            cargarGastos();

        } else {

            alert("Error al eliminar gasto");
        }

    } catch (error) {

        console.error("Error:", error);
    }
}

cargarGastos();