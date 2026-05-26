const API_URL = "http://127.0.0.1:8000";
let categoriasMap = {};

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");

    // 🔒 CONTROL REAL: Si no hay token, se le expulsa. No dependemos de IDs fijos.
    if (!token) {
        alert("Sesión inválida o expirada. Por favor, inicia sesión de nuevo.");
        window.location.href = "./usuario_index.html";
        return;
    }

    await cargarCategorias();
    await listarPresupuestos();
});

// ======================
// CARGAR CATEGORÍAS
// ======================
async function cargarCategorias() {
    try {
        const response = await fetch(`${API_URL}/categorias/`);
        const categorias = await response.json();

        const selectCrear = document.getElementById("pres-categoria");
        const selectEditar = document.getElementById("edit-categoria");

        if (selectCrear) selectCrear.innerHTML = '<option value="">Seleccione una categoría</option>';
        if (selectEditar) selectEditar.innerHTML = '<option value="">Seleccione una categoría</option>';

        categorias.forEach(cat => {
            categoriasMap[cat.id] = cat.nombre;
            if (selectCrear) selectCrear.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
            if (selectEditar) selectEditar.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
        });
    } catch (error) {
        console.error("Error cargando categorías:", error);
    }
}

// ======================
// LISTAR PRESUPUESTOS (100% DINÁMICO Y MULTIUSUARIO)
// ======================
async function listarPresupuestos() {
    const token = localStorage.getItem("token");
    
    // 👥 DINÁMICO: Recuperamos el ID que el login guardó en el LocalStorage para el usuario actual.
    const idUsuarioActual = localStorage.getItem("IdCliente"); 

    try {
        const response = await fetch(`${API_URL}/presupuestos/`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Cache-Control": "no-store"
            }
        });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }

        const data = await response.json();
        
        if (data.detail) {
            console.error("Detalle del servidor:", data.detail);
            return;
        }

        const lista = document.getElementById("lista-presupuestos");
        const contenedor = document.getElementById("contenedor-barras");

        if (lista) lista.innerHTML = "";
        if (contenedor) contenedor.innerHTML = "";

        // Si tu backend filtra automáticamente por Token, usamos "data" directo. 
        // Si tu backend devuelve todo, lo filtramos dinámicamente con el ID del usuario logueado.
        let presupuestosFiltrados = [];
        if (Array.isArray(data)) {
            if (idUsuarioActual) {
                presupuestosFiltrados = data.filter(p => {
                    const campoCliente = p.id_usuario || p.id_cliente || p.IdCliente || p.cliente || p.id_usuario_id;
                    return String(campoCliente) === String(idUsuarioActual);
                });
            } else {
                // Si por alguna razón no se ha guardado el ID local, mostramos lo que devuelva el token
                presupuestosFiltrados = data;
            }
        }

        if (presupuestosFiltrados.length === 0) {
            if (lista) {
                lista.innerHTML = `<tr><td colspan="4" style="text-align:center;">No tienes presupuestos creados en tu cuenta.</td></tr>`;
            }
            return;
        }

        presupuestosFiltrados.forEach(p => {
            if (lista) {
                lista.innerHTML += `
                    <tr id="fila-${p.id_presupuesto}">
                        <td>Q ${p.monto_presupuesto}</td>
                        <td>${p.categoria || 'Sin Categoría'}</td>
                        <td>${p.mes_aplicacion}</td>
                        <td>
                            <button onclick="prepararEdicion(${p.id_presupuesto}, ${p.monto_presupuesto}, '${p.categoria}', '${p.mes_aplicacion}')">✏️</button>
                            <button onclick="eliminarPresupuesto(${p.id_presupuesto})">🗑️</button>
                        </td>
                    </tr>
                `;
            }

            if (contenedor) {
                contenedor.innerHTML += `
                    <div style="margin-bottom: 15px;">
                        <strong>${p.categoria || 'Sin Categoría'}</strong>
                        <div class="barra-container" style="background-color: #e0e0e0; border-radius: 4px; overflow: hidden; height: 22px; width: 100%; margin-top: 5px;">
                            <div id="barra-${p.id_presupuesto}" class="barra" style="width: 0%; height: 100%; text-align: center; color: white; font-size: 12px; font-weight: bold; line-height: 22px; transition: width 0.5s ease; background-color: #888;">0%</div>
                        </div>
                    </div>
                `;
            }

            // Detectar el ID de usuario dinámicamente desde el presupuesto o la sesión
            const idParaProgreso = idUsuarioActual || p.id_usuario || p.id_cliente;
            const idCategoria = p.id_categoria;
            if (idCategoria && idParaProgreso) {
                cargarProgresoPresupuesto(idParaProgreso, idCategoria, `barra-${p.id_presupuesto}`);
            }
        });
    } catch (error) {
        console.error("Error al listar presupuestos:", error);
    }
}

// ======================
// CREAR PRESUPUESTO (ENVÍO DINÁMICO SIN CAMPOS QUEMADOS)
// ======================
const formPresupuesto = document.getElementById("form-presupuesto");
if (formPresupuesto) {
    formPresupuesto.addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        const idUsuarioActual = localStorage.getItem("IdCliente");

        // Construimos el cuerpo mandando el ID dinámico en el formato numérico que exige Pydantic
        const bodyData = {
            monto_presupuesto: parseFloat(document.getElementById("pres-monto").value),
            id_categoria: document.getElementById("pres-categoria").value ? parseInt(document.getElementById("pres-categoria").value) : null,
            mes_aplicacion: document.getElementById("pres-mes").value
        };

        // 🧠 Si tu backend exige el ID explícito en el JSON y no lo saca del token, se lo inyectamos dinámicamente aquí:
        if (idUsuarioActual) {
            const numericId = parseInt(idUsuarioActual);
            bodyData.id_usuario = numericId;
            bodyData.id_cliente = numericId;
            bodyData.IdCliente = numericId;
        }

        try {
            const response = await fetch(`${API_URL}/presupuestos/`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(bodyData)
            });

            if (response.ok) {
                mostrarMensaje("🌟 Presupuesto creado correctamente", "success");
                await listarPresupuestos();
                e.target.reset();
                ocultarSecciones();
            } else {
                const errorData = await response.json();
                console.error("Detalle del error 422 en el backend:", errorData.detail);
                
                // Si el error dice qué campo falta, te lo mostrará en la consola del navegador (F12)
                mostrarMensaje(`❌ Error de validación: Verifica el formato de los datos`, "error");
            }
        } catch (error) {
            console.error("Error en submit crear:", error);
        }
    });
}

// ======================
// PREPARAR EDICIÓN
// ======================
function prepararEdicion(id, monto, categoria, mes) {
    document.getElementById("edit-id").value = id;
    document.getElementById("edit-monto").value = monto;
    document.getElementById("edit-mes").value = mes;

    const categoriaSelect = document.getElementById("edit-categoria");
    if (categoriaSelect) {
        for (let option of categoriaSelect.options) {
            if (option.text === categoria) {
                categoriaSelect.value = option.value;
                break;
            }
        }
    }
    mostrarSeccion("editar");
}

// ======================
// ACTUALIZAR PRESUPUESTO
// ======================
const formEditPresupuesto = document.getElementById("form-edit-presupuesto");
if (formEditPresupuesto) {
    formEditPresupuesto.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = document.getElementById("edit-id").value;
        const token = localStorage.getItem("token");
        const idUsuarioActual = localStorage.getItem("IdCliente");

        const bodyData = {
            monto_presupuesto: parseFloat(document.getElementById("edit-monto").value),
            id_categoria: document.getElementById("edit-categoria").value ? parseInt(document.getElementById("edit-categoria").value) : null,
            mes_aplicacion: document.getElementById("edit-mes").value
        };

        if (idUsuarioActual) {
            const numericId = parseInt(idUsuarioActual);
            bodyData.id_usuario = numericId;
            bodyData.id_cliente = numericId;
        }

        try {
            const response = await fetch(`${API_URL}/presupuestos/${id}`, {
                method: "PUT",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(bodyData)
            });

            if (response.ok) {
                await listarPresupuestos(); 
                ocultarSecciones();
                mostrarMensaje("✏️ Presupuesto actualizado", "success");
            } else {
                mostrarMensaje("❌ Error al actualizar", "error");
            }
        } catch (error) {
            console.error("Error en submit editar:", error);
        }
    });
}

// ======================
// ELIMINAR PRESUPUESTO
// ======================
async function eliminarPresupuesto(id) {
    const confirmar = confirm("¿Eliminar presupuesto?");
    if (!confirmar) return;

    const token = localStorage.getItem("token");

    try {
        const response = await fetch(`${API_URL}/presupuestos/${id}`, { 
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (response.ok) {
            mostrarMensaje("🗑️ Eliminado correctamente", "success");
            await listarPresupuestos();
        } else {
            mostrarMensaje("❌ Error al eliminar", "error");
        }
    } catch (error) {
        console.error("Error al eliminar:", error);
    }
}

// ======================
// CONTROL DE INTERFAZ (UI)
// ======================
function mostrarSeccion(tipo) {
    ocultarSecciones();
    if (tipo === "crear") document.getElementById("seccion-crear")?.classList.remove("hidden");
    if (tipo === "editar") document.getElementById("seccion-editar")?.classList.remove("hidden");
}

function ocultarSecciones() {
    document.getElementById("seccion-crear")?.classList.add("hidden");
    document.getElementById("seccion-editar")?.classList.add("hidden");
}

function mostrarMensaje(texto, tipo) {
    const mensaje = document.createElement("div");
    mensaje.className = `toast ${tipo}`;
    mensaje.textContent = texto;
    document.body.appendChild(mensaje);
    setTimeout(() => { mensaje.remove(); }, 3000);
}

// ======================
// BARRA DE PROGRESO
// ======================
async function cargarProgresoPresupuesto(idUsuario, idCategoria, elementoId) {
    const barra = document.getElementById(elementoId);
    if (!barra) return;

    try {
        if (!idCategoria || !idUsuario) {
            EstablecerBarraVacia(barra);
            return;
        }
        
        const response = await fetch(`${API_URL}/presupuestos/validar/${idUsuario}/${idCategoria}`);
        
        // Si el endpoint da error (porque no hay gastos registrados aún)
        if (!response.ok) {
            EstablecerBarraVacia(barra);
            return;
        }

        const data = await response.json();
        
        // Validamos que venga un porcentaje numérico real
        if (data == null || data.porcentaje_usado == null || isNaN(data.porcentaje_usado)) {
            EstablecerBarraVacia(barra);
            return;
        }

        const porcentaje = Number(data.porcentaje_usado);
        barra.style.width = Math.min(porcentaje, 100) + "%";
        barra.textContent = porcentaje.toFixed(2) + "%";
        
        // Colores de alerta según consumo
        if (porcentaje >= 100) {
            barra.style.backgroundColor = "#dc3545"; // Rojo (Excedido)
            barra.style.color = "#fff";
        } else if (porcentaje >= 80) {
            barra.style.backgroundColor = "#ffc107"; // Naranja (Advertencia)
            barra.style.color = "#000";
        } else {
            barra.style.backgroundColor = "#28a745"; // Verde (Seguro)
            barra.style.color = "#fff";
        }

    } catch (error) {
        console.error("Error cargando progreso, usando estado por defecto:", error);
        EstablecerBarraVacia(barra);
    }
}

// Función auxiliar: Si el usuario no tiene gastos, la barra se muestra verde en 0%
function EstablecerBarraVacia(elementoBarra) {
    elementoBarra.style.width = "100%"; // La expandimos para que el texto sea legible
    elementoBarra.style.backgroundColor = "#28a745"; // Verde (0% gastado es totalmente seguro)
    elementoBarra.style.color = "#fff";
    elementoBarra.textContent = "0.00% usado";
}

function logout() {
    localStorage.clear();
    window.location.href = "./usuario_index.html";
}