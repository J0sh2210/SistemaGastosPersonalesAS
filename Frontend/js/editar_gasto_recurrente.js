const API_URL = "http://127.0.0.1:8000";

// Obtener ID desde la URL
function obtenerId() {

    const params = new URLSearchParams(window.location.search);

    return params.get("id");
}

// Cargar gasto actual
async function cargarGasto() {

    const id = obtenerId();

    if (!id) {
        alert("ID inválido");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/gastos-recurrentes/${id}`
        );

        if (!response.ok) {
            throw new Error("No se pudo cargar el gasto");
        }

        const gasto = await response.json();

        console.log("Gasto cargado:", gasto);

        // Llenar formulario
        document.getElementById("expenseId").value =
            gasto.IdGastoRecurrente;

        document.getElementById("concepto").value =
            gasto.Concepto;

        document.getElementById("monto").value =
            gasto.Monto;

        document.getElementById("frecuencia").value =
            gasto.Frecuencia;

    } catch (error) {

        console.error("Error:", error);

        alert("Error al cargar gasto");
    }
}

// Guardar cambios
document.getElementById("editForm")
.addEventListener("submit", async function(e) {

    e.preventDefault();

    const id = document.getElementById("expenseId").value;

    const datosActualizados = {

        Concepto:
            document.getElementById("concepto").value,

        Monto:
            parseFloat(
                document.getElementById("monto").value
            ),

        Frecuencia:
            document.getElementById("frecuencia").value
    };

    try {

        const response = await fetch(
            `${API_URL}/gastos-recurrentes/${id}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(datosActualizados)
            }
        );

        if (!response.ok) {
            throw new Error("No se pudo actualizar");
        }

        alert(
            "✅ Gasto actualizado correctamente " +
            "(solo futuras recurrencias)"
        );

        // Regresar al listado
        window.location.href =
            "listar_gastos_recurrentes.html";

    } catch (error) {

        console.error("Error:", error);

        alert("Error al actualizar gasto");
    }

});

// Cancelar edición
function cancelar() {

    window.location.href =
        "listar_gastos_recurrentes.html";
}

// Inicializar página
document.addEventListener(
    "DOMContentLoaded",
    cargarGasto
);