const API_URL = "http://127.0.0.1:8000";
let categoriasMap = {};

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Sesión inválida o expirada. Por favor, inicia sesión de nuevo.");
        window.location.href = "./usuario_index.html";
        return;
    }

    // Inyecta automáticamente el año y mes actual en los inputs readonly
    fijarMesActual();

    await cargarCategorias();
    await listarPresupuestos();
});

// =========================================================================
// FIJAR MES ACTUAL EN LOS FORMULARIOS (Mayo 2026)
// =========================================================================
function fijarMesActual() {
    const inputMesCrear = document.getElementById("pres-mes");
    const inputMesEditar = document.getElementById("edit-mes");

    const fecha = new Date();
    const anio = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const mesFormateado = `${anio}-${mes}`; // Resultado dinámico: "2026-05"

    if (inputMesCrear) inputMesCrear.value = mesFormateado;
    if (inputMesEditar) inputMesEditar.value = mesFormateado;
}

// =========================================================================
// CARGAR CATEGORÍAS
// =========================================================================
async function cargarCategorias() {
    try {
        const response = await fetch(`${API_URL}/categorias/`);
        const categoriesData = await response.json();

        const selectCrear = document.getElementById("pres-categoria");
        const selectEditar = document.getElementById("edit-categoria");

        if (selectCrear) selectCrear.innerHTML = '<option value="">Seleccione una categoría</option>';
        if (selectEditar) selectEditar.innerHTML = '<option value="">Seleccione una categoría</option>';

        categoriesData.forEach(cat => {
            const idCat = cat.id || cat.id_categoria || cat.IdCategoria;
            const nombreCat = cat.nombre || cat.nombre_categoria || cat.NombreCategoria;
            
            categoriasMap[idCat] = nombreCat;
            if (selectCrear) selectCrear.innerHTML += `<option value="${idCat}">${nombreCat}</option>`;
            if (selectEditar) selectEditar.innerHTML += `<option value="${idCat}">${nombreCat}</option>`;
        });
    } catch (error) {
        console.error("Error cargando categorías:", error);
    }
}

// =========================================================================
// LISTAR PRESUPUESTOS (CORREGIDO)
// =========================================================================
async function listarPresupuestos() {
    const token = localStorage.getItem("token");
    const idUsuarioActual = localStorage.getItem("IdCliente"); 

    try {
        const response = await fetch(`${API_URL}/presupuestos/`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Cache-Control": "no-store"
            }
        });

        if (!response.ok) throw new Error("Error en la respuesta del servidor");
        const data = await response.json();

        const lista = document.getElementById("lista-presupuestos");
        if (lista) lista.innerHTML = "";

        let presupuestosFiltrados = [];
        if (Array.isArray(data)) {
            if (idUsuarioActual) {
                presupuestosFiltrados = data.filter(p => {
                    const campoCliente = p.id_usuario || p.id_cliente || p.IdCliente || p.cliente;
                    return String(campoCliente) === String(idUsuarioActual);
                });
            } else {
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
                // CORREGIDO: Añadido el signo '$' faltante para renderizar correctamente la variable en el HTML
                lista.innerHTML += `
                    <tr id="fila-${p.id_presupuesto}">
                        <td>Q ${p.monto_presupuesto}</td>
                        <td>${p.categoria || 'Sin Categoría'}</td>
                        <td>${p.mes_aplicacion}</td>
                        <td>
                            <button onclick="prepararEdicion(${p.id_presupuesto}, ${p.monto_presupuesto}, '${p.categoria ? p.categoria.replace(/'/g, "\\'") : ''}', '${p.mes_aplicacion}')">✏️</button>
                            <button onclick="eliminarPresupuesto(${p.id_presupuesto})">🗑️</button>
                        </td>
                    </tr>
                `;
            }
        });
    } catch (error) {
        console.error("Error al listar presupuestos:", error);
    }
}

// =========================================================================
// CREAR PRESUPUESTO
// =========================================================================
const formPresupuesto = document.getElementById("form-presupuesto");
if (formPresupuesto) {
    formPresupuesto.addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        const idUsuarioActual = localStorage.getItem("IdCliente");

        const bodyData = {
            monto_presupuesto: parseFloat(document.getElementById("pres-monto").value),
            id_categoria: document.getElementById("pres-categoria").value ? parseInt(document.getElementById("pres-categoria").value) : null,
            mes_aplicacion: document.getElementById("pres-mes").value
        };

        if (idUsuarioActual) {
            bodyData.id_usuario = parseInt(idUsuarioActual);
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
                alert("Presupuesto creado correctamente");
                await listarPresupuestos();
                e.target.reset();
                fijarMesActual(); // Evita que el reset borre el mes bloqueado
                ocultarSecciones();
            } else {
                // Captura el mensaje HTTP 400 personalizado enviado desde FastAPI
                const errorData = await response.json();
                alert(errorData.detail || "Error al crear el presupuesto.");
            }
        } catch (error) {
            console.error("Error en submit crear:", error);
        }
    });
}

// =========================================================================
// PREPARAR EDICIÓN
// =========================================================================
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

// =========================================================================
// ACTUALIZAR PRESUPUESTO
// =========================================================================
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
            bodyData.id_usuario = parseInt(idUsuarioActual);
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
                alert("Presupuesto actualizado con éxito");
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Error al actualizar el presupuesto");
            }
        } catch (error) {
            console.error("Error en submit editar:", error);
        }
    });
}

// =========================================================================
// ELIMINAR PRESUPUESTO
// =========================================================================
async function eliminarPresupuesto(id) {
    const confirmar = confirm("¿Está seguro de que desea eliminar este presupuesto?");
    if (!confirmar) return;

    const token = localStorage.getItem("token");

    try {
        const response = await fetch(`${API_URL}/presupuestos/${id}`, { 
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (response.ok) {
            alert("Presupuesto eliminado");
            await listarPresupuestos();
        } else {
            alert("Error al eliminar el presupuesto");
        }
    } catch (error) {
        console.error("Error al eliminar:", error);
    }
}

// =========================================================================
// CONTROL DE INTERFAZ (UI)
// =========================================================================
function mostrarSeccion(tipo) {
    ocultarSecciones();
    if (tipo === "crear") document.getElementById("seccion-crear")?.classList.remove("hidden");
    if (tipo === "editar") document.getElementById("seccion-editar")?.classList.remove("hidden");
}

function ocultarSecciones() {
    document.getElementById("seccion-crear")?.classList.add("hidden");
    document.getElementById("seccion-editar")?.classList.add("hidden");
}

function logout() {
    localStorage.clear();
    window.location.href = "./usuario_index.html";
}