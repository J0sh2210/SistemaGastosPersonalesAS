// js/categoria_config.js
const API_URL = "http://127.0.0.1:8000";

document.getElementById('form-categoria').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const msg = document.getElementById('cat-msg');
    msg.innerText = "Procesando...";
    msg.style.color = "var(--text-main)";

    // Preparamos los datos según CategoriaCreate
    const bodyData = {
        nombre_categoria: document.getElementById('cat-nombre').value,
        id_tipo_movimiento: parseInt(document.getElementById('cat-tipo-mov').value),
        id_tipo_categoria: parseInt(document.getElementById('cat-tipo-cat').value)
    };

    try {
        const response = await fetch(`${API_URL}/categorias/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();

        if (response.ok) {
            msg.style.color = "var(--primary)";
            // Retorna el mensaje definido en tu service
            msg.innerText = "✔ " + (data.mensaje || "Categoría guardada");
            document.getElementById('form-categoria').reset();
        } else {
            msg.style.color = "var(--error)";
            msg.innerText = "✖ " + (data.detail || "Error al procesar");
        }
    } catch (error) {
        msg.style.color = "var(--error)";
        msg.innerText = "Error: No se pudo conectar con la API.";
        console.error(error);
    }
});