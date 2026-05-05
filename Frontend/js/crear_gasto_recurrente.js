//Enma
document.getElementById("formGasto").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        Concepto: document.getElementById("concepto").value,
        Monto: parseFloat(document.getElementById("monto").value),
        FechaInicio: new Date(document.getElementById("fechaInicio").value).toISOString().split("T")[0],
        Frecuencia: document.getElementById("frecuencia").value,
        IdCliente: parseInt(document.getElementById("idCliente").value)
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/gastos-recurrentes/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            document.getElementById("mensaje").innerText = "Gasto creado correctamente";
        } else {
            document.getElementById("mensaje").innerText = "Error al crear gasto";
        }

    } catch (error) {
        console.error(error);
        document.getElementById("mensaje").innerText = "Error de conexión";
    }
});

