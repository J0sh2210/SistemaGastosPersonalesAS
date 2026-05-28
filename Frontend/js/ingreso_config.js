// js/ingreso_config.js
const API_URL = "http://127.0.0.1:8000";
let idUsuarioActual = null;
let categoriasDisponibles = [];
let movimientoEditandoId = null;
let listaMovimientosGlobal = [];

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
        } else {
            console.error("Error en la respuesta:", response.status);
        }
    } catch (error) {
        console.error("Error al cargar las categorías:", error);
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
    
    movimientoEditandoId = null;
    const btnSubmit = document.getElementById("btnGuardarMovimiento");
    if(btnSubmit) btnSubmit.innerText = "Guardar Movimiento";
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
            listaMovimientosGlobal = movimientos;
            cuerpoTabla.innerHTML = "";

            const misMovimientos = movimientos.filter(mov => mov.IdCliente === idUsuarioActual);

            if (misMovimientos.length === 0) {
                cuerpoTabla.innerHTML = "<tr><td colspan='4' style='text-align: center;'>No tienes movimientos registrados aún.</td></tr>";
                return;
            }

            misMovimientos.forEach(mov => {
                const idDelMovimiento = mov.IdIngreso || mov.IdMovimiento;
                const idTipo = parseInt(mov.IdTipo || mov.IdMovimiento);
                const esIngreso = idTipo === 1; 
                
                const tipoTexto = esIngreso ? "Ingreso" : "Egreso";

                const categoria = categoriasDisponibles.find(cat => cat.id === mov.IdCategoria);
                const nombreCategoria = categoria ? categoria.nombre : "Sin categoría";

                const fila = `
                    <tr>
                        <td>${mov.Concepto}</td>
                        <td>Q${mov.Monto}</td>
                        <td>${nombreCategoria}</td>
                        <td style="text-align: center;">
                            <button class="btn-accion" onclick="prepararEdicion(${idDelMovimiento})" title="Editar">✏️</button>
                            <button class="btn-accion" onclick="eliminarMovimiento(${idDelMovimiento})" title="Eliminar">🗑️</button>
                        </td>
                    </tr>
                `;
                cuerpoTabla.innerHTML += fila;
            });
        }
    } catch (error) {
        console.error("Error al cargar la lista de movimientos:", error);
    }
}

async function eliminarMovimiento(idMovimiento) {
    if (!idMovimiento) return;

    if (confirm("¿Estás seguro de que deseas eliminar este movimiento?")) {
        try {
            const response = await fetch(`${API_URL}/ingresos/eliminar/${idMovimiento}`, {
                method: "DELETE"
            });

            if (response.ok) {
                alert("Movimiento eliminado correctamente");
                cargarListaMovimientos(); 
            } else {
                alert("Hubo un problema al intentar eliminar el movimiento.");
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
        }
    }
}

function prepararEdicion(idMovimiento) {
    const movimiento = listaMovimientosGlobal.find(m => (m.IdIngreso || m.IdMovimiento) === idMovimiento);
    if (!movimiento) return;

    mostrarFormulario();

    document.getElementById("concepto").value = movimiento.Concepto;
    document.getElementById("monto").value = movimiento.Monto;
    document.getElementById("categoria").value = movimiento.IdCategoria;
    document.getElementById("tipo").value = movimiento.IdTipo || movimiento.IdMovimiento;

    movimientoEditandoId = idMovimiento;
    const btnSubmit = document.getElementById("btnGuardarMovimiento");
    btnSubmit.innerText = "Actualizar Movimiento";
    btnSubmit.style.backgroundColor = "#f59e0b";
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

    const dataPUT = {
        Concepto: document.getElementById('concepto').value,
        Monto: parseFloat(document.getElementById('monto').value),
        IdCategoria: parseInt(idCategoria),
        IdTipo: parseInt(document.getElementById('tipo').value)
    };

    try {
        let response;

        if (movimientoEditandoId === null) {
            // MODO CREAR (POST)
            const dataPOST = {
                ...dataPUT,
                IdCliente: parseInt(idUsuarioActual)
            };

            response = await fetch(`${API_URL}/ingresos/`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(dataPOST)
            });
        } else {
            // MODO EDITAR (PUT)
            response = await fetch(`${API_URL}/ingresos/${movimientoEditandoId}`, {
                method: "PUT",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(dataPUT)
            });
        }

        if (response.ok) {
            cargarListaMovimientos(); 
            ocultarFormulario();
            
            alert(movimientoEditandoId ? "Movimiento actualizado con éxito" : "Movimiento creado con éxito");
            movimientoEditandoId = null;
            
        } else {
            const errorData = await response.json();
            console.error("Error del backend:", errorData);
            mensaje.style.color = "red";
            mensaje.innerText = "Error en la operación. Revisa los datos.";
        }

    } catch (error) {
        console.error(error);
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
    }
});
