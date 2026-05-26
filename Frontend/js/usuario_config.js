const API_URL = "http://127.0.0.1:8000";

// --- LÓGICA DE INTERFAZ (TABS) ---
function showForm(formType) {
    document.getElementById('form-login').classList.remove('active');
    document.getElementById('form-register').classList.remove('active');
    document.getElementById('tab-login').classList.remove('active');
    document.getElementById('tab-register').classList.remove('active');

    if (formType === 'login') {
        document.getElementById('form-login').classList.add('active');
        document.getElementById('tab-login').classList.add('active');
    } else {
        document.getElementById('form-register').classList.add('active');
        document.getElementById('tab-register').classList.add('active');
    }
}

// --- VERIFICAR SESIÓN ACTIVA ---
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (token) {
        cargarPerfil();
    }
});

// --- INICIAR SESIÓN ---
document.getElementById('form-login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorMsg = document.getElementById('login-error');
    errorMsg.innerText = "";

    const formData = new URLSearchParams();
    formData.append("username", document.getElementById('login-username').value);
    formData.append("password", document.getElementById('login-password').value);

    try {
        const response = await fetch(`${API_URL}/usuarios/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("token", data.access_token);
            await cargarPerfil(); 
        } else {
            errorMsg.innerText = data.detail || "Error al iniciar sesión";
        }
    } catch (error) {
        errorMsg.innerText = "Error de conexión con el servidor";
    }
});

// --- REGISTRAR USUARIO ---
document.getElementById('form-register').addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = document.getElementById('reg-msg');
    msg.innerText = "";

    const bodyData = {
        username: document.getElementById('reg-username').value,
        password: document.getElementById('reg-password').value,
        primerNombre: document.getElementById('reg-nombre1').value,
        segundoNombre: document.getElementById('reg-nombre2').value || null,
        primerApellido: document.getElementById('reg-apellido1').value,
        segundoApellido: document.getElementById('reg-apellido2').value || null
    };

    try {
        const response = await fetch(`${API_URL}/usuarios/registro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();

        if (response.ok) {
            msg.style.color = "var(--primary)";
            msg.innerText = "Registro exitoso. Ahora puedes iniciar sesión.";
            setTimeout(() => showForm('login'), 2000);
        } else {
            msg.style.color = "var(--error)";
            msg.innerText = data.detail || "Error en el registro";
        }
    } catch (error) {
        msg.style.color = "var(--error)";
        msg.innerText = "Error de conexión con el servidor";
    }
});

// --- CARGAR PERFIL ---
async function cargarPerfil() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/usuarios/perfil`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            
            // Mapeo flexible del ID devuelto por tu BD para guardarlo de respaldo
            const idDetectado = data.id_usuario || data.id_cliente || data.IdCliente || data.id;
            if (idDetectado) {
                localStorage.setItem("IdCliente", String(idDetectado));
            }

            if (document.getElementById('prof-user')) document.getElementById('prof-user').innerText = data.usuario || data.username || "";
            if (document.getElementById('prof-name')) document.getElementById('prof-name').innerText = `${data.nombre || data.primerNombre || ''} ${data.segundoNombre || ''}`.trim();
            if (document.getElementById('prof-lastname')) document.getElementById('prof-lastname').innerText = `${data.apellido || data.primerApellido || ''} ${data.segundoApellido || ''}`.trim();
            
            window.location.href = "dashboard.html";
        } else {
            logout();
        }
    } catch (error) {
        console.error("Error cargando el perfil", error);
    }
}

// --- CERRAR SESIÓN ---
function logout() {
    localStorage.clear();
    window.location.href = "usuario_index.html";
}