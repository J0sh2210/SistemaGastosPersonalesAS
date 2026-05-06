const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "usuario_index.html"; 
        return;
    }
    cargarPerfil(token);
});

async function cargarPerfil(token) {
    try {
        const response = await fetch(`${API_URL}/usuarios/perfil`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('prof-user').innerText = data.usuario;
            document.getElementById('prof-name').innerText = `${data.nombre} ${data.segundoNombre || ''}`.trim();
            document.getElementById('prof-lastname').innerText = `${data.apellido} ${data.segundoApellido || ''}`.trim();
        } else {
            logout();
        }
    } catch (error) {
        console.error("Error cargando el perfil", error);
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "usuario_index.html";
}