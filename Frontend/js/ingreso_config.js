// js/ingreso_config.js
const API_URL = "http://127.0.0.1:8000";
let idUsuarioActual = null;
let categoriasDisponibles = [];
let metasDisponibles = [];

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    try {
        const resPerfil = await fetch(`${API_URL}/usuarios/perfil`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (resPerfil.ok) {
            const datosUsuario = await resPerfil.json();
            idUsuarioActual = datosUsuario.IdCliente;
            
            await cargarCategorias();
            await cargarMetas(); // Cargar metas al iniciar
            cargarListaMovimientos();
        }
    } catch (error) {
        console.error("Error obteniendo el perfil al cargar la página", error);
    }
});

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
            let categorias = Array.isArray(data) ? data : [];
            
            categoriasDisponibles = categorias;
            
            selectCategoria.innerHTML = '<option value="">Selecciona una categoría</option>';
            
            categoriasDisponibles.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.nombre;
                selectCategoria.appendChild(option);
            });
            
            // Agregar evento para detectar cuando selecciona "Ahorro"
            selectCategoria.addEventListener('change', mostrarOcultarMeta);
        } else {
            console.error("Error en la respuesta:", response.status);
        }
    } catch (error) {
        console.error("Error al cargar las categorías:", error);
    }
}

// Nueva función para cargar las metas del usuario
async function cargarMetas() {
    const token = localStorage.getItem("token");
    const selectMeta = document.getElementById("meta");
    
    if (!token || !idUsuarioActual || !selectMeta) return;
    
    try {
        const response = await fetch(`${API_URL}/api/metas/${idUsuarioActual}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const metas = await response.json();
            metasDisponibles = metas;
            
            selectMeta.innerHTML = '<option value="">Selecciona una meta de ahorro (opcional)</option>';
            
            metasDisponibles.forEach(meta => {
                const option = document.createElement('option');
                option.value = meta.IdMeta;
                option.textContent = `${meta.NombreMeta} (Q${parseFloat(meta.MontoActual).toFixed(2)} / Q${parseFloat(meta.MontoObjetivo).toFixed(2)})`;
                selectMeta.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Error al cargar las metas:", error);
    }
}

// Nueva función para mostrar/ocultar el campo de metas
function mostrarOcultarMeta() {
    const selectCategoria = document.getElementById("categoria");
    const selectMeta = document.getElementById("meta");
    const categoriaSeleccionada = categoriasDisponibles.find(cat => cat.id === parseInt(selectCategoria.value));
    
    if (categoriaSeleccionada && (categoriaSeleccionada.nombre.toLowerCase().includes("ahorro") || categoriaSeleccionada.nombre === "Ahorro inversión")) {
        selectMeta.style.display = "block";
        selectMeta.setAttribute("data-obligatorio", "false"); // Opcional
    } else {
        selectMeta.style.display = "none";
        selectMeta.value = "";
        selectMeta.setAttribute("data-obligatorio", "false");
    }
}

// 👉 NUEVAS FUNCIONES PARA CONTROLAR LA PANTALLA
function mostrarFormulario() {
    document.getElementById("panel-formulario").classList.remove("oculto"); 
    document.getElementById("btnMostrarFormulario").style.display = "none"; 
}

function ocultarFormulario() {
    document.getElementById("panel-formulario").classList.add("oculto"); 
    
    setTimeout(() => {
        document.getElementById("btnMostrarFormulario").style.display = "block"; 
    }, 400);

    const form = document.getElementById("formMovimiento");
    if(form) form.reset();
    
    const msg = document.getElementById("mensaje");
    if(msg) msg.innerText = "";
}

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
    // 1. Imprimimos el movimiento en la consola para ver cómo se llaman exactamente los campos
    console.log("Movimiento recibido:", mov); 

    // 2. Tomamos directamente el IdTipo (Asegúrate de que la mayúscula/minúscula sea idéntica a lo que imprime el console.log)
    const idTipo = parseInt(mov.IdTipo); 
    
    // Si el tipo es 1 es Ingreso, de lo contrario (2) es Egreso
    const esIngreso = idTipo === 1; 
    
    const tipoTexto = esIngreso ? "Ingreso" : "Egreso";
    const colorTexto = esIngreso ? "#10b981" : "#ef4444"; // Verde para ingreso, Rojo para egreso

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

// Evento Submit (POST y PUT)
document.getElementById('formMovimiento').addEventListener('submit', async (e) => {
    e.preventDefault();

    const mensaje = document.getElementById('mensaje');
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "usuario_index.html";
        return;
    }

    if (!idUsuarioActual) {
        mensaje.style.color = "red";
        mensaje.innerText = "Error: No se ha cargado el ID del usuario. Recarga la página.";
        return;
    }

    const idCategoria = document.getElementById('categoria').value;
    if (!idCategoria) {
        mensaje.style.color = "red";
        mensaje.innerText = "Error: Debes seleccionar una categoría.";
        return;
    }

    const idMeta = document.getElementById('meta').value; // Puede ser vacío, y eso está bien

    const ingresoData = {
        Concepto: document.getElementById('concepto').value,
        Monto: parseFloat(document.getElementById('monto').value),
        IdCliente: parseInt(idUsuarioActual),
        IdCategoria: parseInt(idCategoria),
        IdMovimiento: parseInt(document.getElementById('tipo').value),
        IdMeta: idMeta ? parseInt(idMeta) : null, // Incluir IdMeta si fue seleccionado
        IdTipo: parseInt(document.getElementById('tipo').value) // Asegúrate de enviar el IdTipo también
    };

    try {
        const response = await fetch(`${API_URL}/ingresos/`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(ingresoData)
        });

        if (response.ok) {
            mensaje.style.color = "#10b981";
            mensaje.innerText = "✅ Movimiento registrado con éxito";
            cargarListaMovimientos(); 
            await cargarMetas(); // Recargar metas para actualizar los montos
            setTimeout(() => ocultarFormulario(), 1500);
            
        } else {
            const errorData = await response.json();
            console.error("Error del backend:", errorData);
            mensaje.style.color = "red";
            mensaje.innerText = "❌ Error en la operación. Revisa los datos.";
        }

    } catch (error) {
        console.error(error);
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
    }
});
