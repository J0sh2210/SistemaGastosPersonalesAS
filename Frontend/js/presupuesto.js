const API_URL = "http://127.0.0.1:8000";

let categoriasMap = {};

document.addEventListener("DOMContentLoaded", async () => {

    await cargarCategorias();

    listarPresupuestos();

});

// ======================
// CARGAR CATEGORÍAS
// ======================
async function cargarCategorias() {

    try {

        const response =
            await fetch(`${API_URL}/categorias/`);

        const categorias =
            await response.json();

        const selectCrear =
            document.getElementById("pres-categoria");

        const selectEditar =
            document.getElementById("edit-categoria");

        categorias.forEach(cat => {

            categoriasMap[cat.id] = cat.nombre;

            selectCrear.innerHTML += `
                <option value="${cat.id}">
                    ${cat.nombre}
                </option>
            `;

            selectEditar.innerHTML += `
                <option value="${cat.id}">
                    ${cat.nombre}
                </option>
            `;
        });

    } catch (error) {

        console.error(
            "Error cargando categorías:",
            error
        );
    }
}

// ======================
// LISTAR
// ======================
async function listarPresupuestos() {

    try {

        const response =
            await fetch(`${API_URL}/presupuestos/`);

        const presupuestos =
            await response.json();

        const lista =
            document.getElementById("lista-presupuestos");

        lista.innerHTML = "";

        presupuestos.forEach(presupuesto => {

            lista.innerHTML += `
                <tr>

                    <td>
                        Q ${presupuesto.monto_presupuesto}
                    </td>

                    <td>
                        ${
                            presupuesto.id_categoria
                            ? categoriasMap[presupuesto.id_categoria]
                            : "General"
                        }
                    </td>

                    <td>
                        ${presupuesto.mes_aplicacion}
                    </td>

                    <td>

                        <button
                            style="border:none;background:none;cursor:pointer;"
                            onclick="prepararEdicion(
                                ${presupuesto.id_presupuesto},
                                ${presupuesto.monto_presupuesto},
                                '${presupuesto.id_categoria ?? ""}',
                                '${presupuesto.mes_aplicacion}'
                            )">

                            ✏️

                        </button>

                        <button
                            style="border:none;background:none;cursor:pointer;"
                            onclick="eliminarPresupuesto(
                                ${presupuesto.id_presupuesto}
                            )">

                            🗑️

                        </button>

                    </td>

                </tr>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}

// ======================
// CREAR
// ======================
document.getElementById("form-presupuesto")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const bodyData = {

        monto_presupuesto: parseFloat(
            document.getElementById("pres-monto").value
        ),

        id_categoria:
            document.getElementById("pres-categoria").value
            ? parseInt(
                document.getElementById("pres-categoria").value
              )
            : null,

        mes_aplicacion:
            document.getElementById("pres-mes").value,

        id_usuario: parseInt(
            document.getElementById("id-usuario").value
        )
    };

    try {

        const response = await fetch(
            `${API_URL}/presupuestos/`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(bodyData)
            }
        );

        if (response.ok) {

            mostrarMensaje(
                "🌟 Presupuesto creado correctamente",
                "success"
            );

            listarPresupuestos();

            e.target.reset();

            ocultarSecciones();

        } else {

            mostrarMensaje(
                "❌ Error al crear",
                "error"
            );
        }

    } catch (error) {

        console.error(error);
    }
});

// ======================
// PREPARAR EDICIÓN
// ======================
function prepararEdicion(
    id,
    monto,
    categoria,
    mes
) {

    document.getElementById("edit-id").value = id;

    document.getElementById("edit-monto").value = monto;

    document.getElementById("edit-categoria").value = categoria;

    document.getElementById("edit-mes").value = mes;

    mostrarSeccion("editar");
}

// ======================
// ACTUALIZAR
// ======================
document.getElementById("form-edit-presupuesto")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const id =
        document.getElementById("edit-id").value;

    const bodyData = {

        monto_presupuesto: parseFloat(
            document.getElementById("edit-monto").value
        ),

        id_categoria:
            document.getElementById("edit-categoria").value
            ? parseInt(
                document.getElementById("edit-categoria").value
              )
            : null,

        mes_aplicacion:
            document.getElementById("edit-mes").value,

        id_usuario: 1
    };

    try {

        const response = await fetch(
            `${API_URL}/presupuestos/${id}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(bodyData)
            }
        );

        if (response.ok) {

            mostrarMensaje(
                "✏️ Presupuesto actualizado",
                "success"
            );

            listarPresupuestos();

            ocultarSecciones();

        } else {

            mostrarMensaje(
                "❌ Error al actualizar",
                "error"
            );
        }

    } catch (error) {

        console.error(error);
    }
});

// ======================
// ELIMINAR
// ======================
async function eliminarPresupuesto(id) {

    const confirmar =
        confirm("¿Eliminar presupuesto?");

    if (!confirmar) return;

    try {

        const response = await fetch(
            `${API_URL}/presupuestos/${id}`,
            {
                method: "DELETE"
            }
        );

        if (response.ok) {

            mostrarMensaje(
                "🗑️ Eliminado correctamente",
                "success"
            );

            listarPresupuestos();

        } else {

            mostrarMensaje(
                "❌ Error al eliminar",
                "error"
            );
        }

    } catch (error) {

        console.error(error);
    }
}

// ======================
// UI
// ======================
function mostrarSeccion(tipo) {

    ocultarSecciones();

    if (tipo === "crear") {

        document.getElementById("seccion-crear")
        .classList.remove("hidden");
    }

    if (tipo === "editar") {

        document.getElementById("seccion-editar")
        .classList.remove("hidden");
    }
}

function ocultarSecciones() {

    document.getElementById("seccion-crear")
    .classList.add("hidden");

    document.getElementById("seccion-editar")
    .classList.add("hidden");
}

// ======================
// TOAST
// ======================
function mostrarMensaje(texto, tipo) {

    const mensaje = document.createElement("div");

    mensaje.className = `toast ${tipo}`;

    mensaje.textContent = texto;

    document.body.appendChild(mensaje);

    setTimeout(() => {

        mensaje.remove();

    }, 3000);
}