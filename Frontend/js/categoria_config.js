const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", listarCategorias);
function getIconoMovimiento(tipo) {
    if (tipo === "Ingreso") return "💰 Ingreso";
    if (tipo === "Egreso") return "💸 Egreso";
    return tipo;
}

function getIconoCategoria(tipo) {
    if (tipo === "Fijo") return "📌 Fijo";
    if (tipo === "Variable") return "🔄 Variable";
    if (tipo === "Hormiga") return "🐜 Hormiga";
    if (tipo === "Inversion") return "📈 Inversión";
    return tipo;
}

async function listarCategorias() {
    try {
        const response = await fetch(`${API_URL}/categorias/`);
        const categorias = await response.json();

        const lista = document.getElementById('lista-categorias');
        lista.innerHTML = "";

        categorias.forEach(cat => {

            const idCat = cat.id;
            const nombre = cat.nombre;
            const tipoMov = cat.tipo_movimiento;
            const clasificacion = cat.tipo_categoria;

            lista.innerHTML += `
                <tr>
                    <td><strong>${nombre}</strong></td>
                    <td>${getIconoMovimiento(tipoMov)}</td>
                    <td>${getIconoCategoria(clasificacion)}</td>
                    <td>
                        <button class="btn-edit" style="border:none; background:none;" 
                            onclick="prepararEdicion(${idCat}, '${nombre}', '${tipoMov}', '${clasificacion}')">
                            ✏️
                        </button>
                        <button class="btn-delete" onclick="eliminarCategoria(${idCat}, '${nombre}')">
                          🗑️
                        </button>
                    </td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Error al listar:", error);
    }
}

// --- PREPARAR EDICIÓN ---
function prepararEdicion(id, nombre, tipoMov, tipoCat) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nombre').value = nombre;

    // 🔹 Convertir texto → valor del select
    const mapMov = {
        "Ingreso": 1,
        "Egreso": 2
    };

    const mapCat = {
        "Fijo": 1,
        "Variable": 2,
        "Hormiga": 3,
        "Inversion": 4
    };

    document.getElementById('edit-tipo-mov').value = mapMov[tipoMov] || "";
    document.getElementById('edit-tipo-cat').value = mapCat[tipoCat] || "";

    mostrarSeccion('editar');
}

// --- ACTUALIZAR ---
document.getElementById('form-edit-categoria').addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('edit-id').value;

    const bodyData = {
        nombre_categoria: document.getElementById('edit-nombre').value,
        id_tipo_movimiento: parseInt(document.getElementById('edit-tipo-mov').value),
        id_tipo_categoria: parseInt(document.getElementById('edit-tipo-cat').value)
    };

    const response = await fetch(`${API_URL}/categorias/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
    });

    if (response.ok) {
        mostrarMensaje("✏️ Categoría actualizada correctamente", "success");
        listarCategorias();
        ocultarSecciones();
    }else {
    mostrarMensaje("❌ Error al actualizar categoría", "error");
    }
});

// --- CREAR ---
document.getElementById('form-categoria').addEventListener('submit', async (e) => {
    e.preventDefault();

    const bodyData = {
        nombre_categoria: document.getElementById('cat-nombre').value,
        id_tipo_movimiento: parseInt(document.getElementById('cat-tipo-mov').value),
        id_tipo_categoria: parseInt(document.getElementById('cat-tipo-cat').value)
    };

    const response = await fetch(`${API_URL}/categorias/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
    });

    if (response.ok) {
        mostrarMensaje("🌟 Categoría creada correctamente", "success");
        e.target.reset();
        listarCategorias();
        ocultarSecciones();
    }else {
    mostrarMensaje("❌ Error al crear categoría", "error");
    }
});

// --- UI ---
function mostrarSeccion(tipo) {
    ocultarSecciones();

    if (tipo === 'crear')
        document.getElementById('seccion-crear').classList.remove('hidden');

    if (tipo === 'editar')
        document.getElementById('seccion-editar').classList.remove('hidden');
}

function ocultarSecciones() {
    document.getElementById('seccion-crear').classList.add('hidden');
    document.getElementById('seccion-editar').classList.add('hidden');
}

async function eliminarCategoria(id, nombre) {
    const confirmar = confirm(`¿Seguro que deseas eliminar "${nombre}"?`);
    if (!confirmar) return;

    try {
        const response = await fetch(`${API_URL}/categorias/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        // 🔴 Si el backend manda error → mostrarlo
        if (data.error) {
            mostrarMensaje(data.error, "error");
            return;
        }

        // 🟢 Si todo salió bien
        mostrarMensaje("Categoría eliminada correctamente", "success");
        listarCategorias();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión", "error");
    }
}

function mostrarMensaje(texto, tipo) {
    const mensaje = document.createElement("div");
    mensaje.className = `toast ${tipo}`;
    mensaje.textContent = texto;

    document.body.appendChild(mensaje);

    setTimeout(() => {
        mensaje.remove();
    }, 3000);
}