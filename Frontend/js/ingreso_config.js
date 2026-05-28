// js/ingreso_config.js
const API_URL = "http://127.0.0.1:8000";
let idUsuarioActual = null; // Variable global para guardar el ID del cliente una vez obtenido
let categoriasDisponibles = []; // Variable global para guardar las categorías

// 1. Verificar sesión y cargar datos al entrar a la página
document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    // Primero pedimos el perfil para saber quién es el usuario
    try {
        const resPerfil = await fetch(`${API_URL}/usuarios/perfil`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (resPerfil.ok) {
            const datosUsuario = await resPerfil.json();
            idUsuarioActual = datosUsuario.IdCliente;
            
            // Cargamos las categorías disponibles
            await cargarCategorias();
            
            // Ahora que sabemos quién es, cargamos su tabla de movimientos
            cargarListaMovimientos();
        }
    } catch (error) {
        console.error("Error obteniendo el perfil al cargar la página", error);
    }
});

// --------------------------------------------------------
// 👉 CARGAR CATEGORÍAS DESDE LA BD
// --------------------------------------------------------
async function cargarCategorias() {
    const token = localStorage.getItem("token");
    const selectCategoria = document.getElementById("categoria");
    
    if (!token || !selectCategoria) return;
    
    try {
        const response = await fetch(`${API_URL}/categorias/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // El backend devuelve directamente el array
            let categorias = Array.isArray(data) ? data : [];
            
            categoriasDisponibles = categorias;
            
            console.log("Categorías cargadas:", categoriasDisponibles);
            
            selectCategoria.innerHTML = '<option value="">Selecciona una categoría</option>';
            
            categoriasDisponibles.forEach(cat => {
                const option = document.createElement('option');
                // Usar 'id' como valor y 'nombre' como texto
                option.value = cat.id;
                option.textContent = cat.nombre;
                selectCategoria.appendChild(option);
            });
        } else {
            console.error("Error en la respuesta:", response.status);
        }
    } catch (error) {
        console.error("Error al cargar las categorías:", error);
    }
}

// --------------------------------------------------------
// 👉 NUEVAS FUNCIONES PARA CONTROLAR LA PANTALLA
// --------------------------------------------------------
function mostrarFormulario() {
    document.getElementById("panel-formulario").style.display = "block"; // Muestra el form
    document.getElementById("btnMostrarFormulario").style.display = "none"; // Oculta el botón
}

function ocultarFormulario() {
    document.getElementById("panel-formulario").style.display = "none"; // Oculta el form
    document.getElementById("btnMostrarFormulario").style.display = "block"; // Muestra el botón
    
    // Limpiamos los campos y los mensajes al cerrar
    document.getElementById("formMovimiento").reset();
    document.getElementById("msg-status").innerText = "";
}

// 2. FUNCIÓN PARA OBTENER Y MOSTRAR LOS MOVIMIENTOS EN LA TABLA
async function cargarListaMovimientos() {
    const cuerpoTabla = document.getElementById("cuerpo-tabla-movimientos");
    const token = localStorage.getItem("token");

    if (!idUsuarioActual || !token) return;

    try {
        const response = await fetch(`${API_URL}/ingresos/${idUsuarioActual}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const movimientos = await response.json();
            cuerpoTabla.innerHTML = "";

            const misMovimientos = movimientos.filter(mov => mov.IdCliente === idUsuarioActual);

            if (misMovimientos.length === 0) {
                cuerpoTabla.innerHTML = "<tr><td colspan='4' style='text-align: center;'>No tienes movimientos registrados aún.</td></tr>";
                return;
            }

            misMovimientos.forEach(mov => {
                console.log("Datos del movimiento:", mov);
                const idTipo = parseInt(mov.IdTipo || mov.IdMovimiento);
                const esIngreso = idTipo === 1; 
                
                const tipoTexto = esIngreso ? "Ingreso" : "Egreso";
                const colorTexto = esIngreso ? "#10b981" : "#ef4444";

                // Obtener el nombre de la categoría usando 'id' en lugar de 'IdCategoria'
                const categoria = categoriasDisponibles.find(cat => cat.id === mov.IdCategoria);
                const nombreCategoria = categoria ? categoria.nombre : "Sin categoría";

                const fila = `
                    <tr>
                        <td>${mov.Concepto}</td>
                        <td>Q${mov.Monto}</td>
                        <td>${nombreCategoria}</td>
                        <td style="color: ${colorTexto}; font-weight: bold;">${tipoTexto}</td>
                    </tr>
                `;
                cuerpoTabla.innerHTML += fila;
            });
        }
    } catch (error) {
        console.error("Error al cargar la lista de movimientos:", error);
    }
}

// 3. Evento al darle clic en "Guardar Movimiento"
document.getElementById('formMovimiento').addEventListener('submit', async (e) => {
    e.preventDefault();

    const msg = document.getElementById('msg-status');
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    if (!idUsuarioActual) {
        msg.style.color = "var(--error)";
        msg.innerText = "✖ Error: No se ha cargado el ID del usuario. Recarga la página.";
        return;
    }

    const idCategoria = document.getElementById('categoria').value;
    if (!idCategoria) {
        msg.style.color = "var(--error)";
        msg.innerText = "✖ Error: Debes seleccionar una categoría.";
        return;
    }

    msg.innerText = "Registrando...";
    msg.style.color = "var(--text-muted)";

    try {
        const ingresoData = {
            Concepto: document.getElementById('concepto').value,
            Monto: parseFloat(document.getElementById('monto').value),
            IdCliente: parseInt(idUsuarioActual),
            IdCategoria: parseInt(idCategoria),
            IdMovimiento: parseInt(document.getElementById('tipo').value)
        };

        console.log("Datos a enviar:", ingresoData);

        const response = await fetch(`${API_URL}/ingresos/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify(ingresoData)
        });

        if (response.ok) {
            // 👉 MAGIA: Si se guardó bien, recargamos la tabla y ocultamos el formulario
            msg.style.color = "#10b981"; // Color verde
            msg.innerText = "✅ Movimiento registrado con éxito";
            cargarListaMovimientos();
            document.getElementById("formMovimiento").reset();
            ocultarFormulario();
            
        } else {
            const errorData = await response.json();
            msg.style.color = "var(--error)"; 
            msg.innerText = "✖ Error: " + (errorData.detail || "Datos inválidos");
        }

    } catch (error) {
        console.error("Error detallado:", error);
        msg.style.color = "var(--error)";
        msg.innerText = "✖ " + error.message;
    }
});
