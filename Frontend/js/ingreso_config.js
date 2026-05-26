// js/ingreso_config.js
const API_URL = "http://127.0.0.1:8000";

// Verificar que el usuario tenga sesión al entrar a la página
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "usuario_index.html";
    }
});

// Evento al darle clic en "Guardar Ingreso"
document.getElementById('form-ingreso').addEventListener('submit', async (e) => {
    e.preventDefault();

    const msg = document.getElementById('ing-msg');
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    msg.innerText = "Registrando...";
    msg.style.color = "var(--text-muted)";

    try {
        // 1. Pedimos los datos del perfil al servidor
        const resPerfil = await fetch(`${API_URL}/usuarios/perfil`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!resPerfil.ok) throw new Error("No se pudo obtener el perfil del usuario");
        const datosUsuario = await resPerfil.json();
        
        // Imprimimos en consola para confirmar que llega el IdCliente
        console.log("Datos recibidos del perfil:", datosUsuario);

        const idDelCliente = datosUsuario.IdCliente;

        // Validamos por si el backend aún no envía el IdCliente
        if (!idDelCliente) {
            throw new Error("El backend no devolvió el IdCliente. ¡Revisa que hayas guardado los cambios en Python!");
        }

        // 2. Preparamos la información que se enviará a la tabla Ingresos
        const ingresoData = {
            Concepto: document.getElementById('ing-concepto').value,
            Monto: parseFloat(document.getElementById('ing-monto').value),
            IdCliente: parseInt(idDelCliente), // Usamos el ID automático
            IdMovimiento: document.getElementById('tipo-movimiento').value === "egreso" ? 1 : 2
        };
        // 3. Enviamos la petición POST para guardar el ingreso
        const response = await fetch(`${API_URL}/ingresos/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify(ingresoData)
        });

        // 4. Mostramos el resultado en pantalla
        if (response.ok) {
            msg.style.color = "#10b981"; // Color verde
            msg.innerText = "Movimiento  registrado con éxito";
            document.getElementById('form-ingreso').reset(); // Limpiamos el formulario
        } else {
            const errorData = await response.json();
            msg.style.color = "var(--error)"; // Color rojo
            msg.innerText = "✖ Error: " + (errorData.detail || "Datos inválidos");
        }

    } catch (error) {
        console.error("Error detallado:", error);
        msg.style.color = "var(--error)";
        msg.innerText = "✖ " + error.message;
    }
});