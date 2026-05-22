// Ajusta esto si en tu main.py le pusiste un prefix="/gastos" a tu router
const URL_API = "http://127.0.0.1:8000"; 

document.addEventListener('DOMContentLoaded', obtenerGastos);

async function obtenerGastos() {
    const estado = document.getElementById('mensaje-estado');
    const tabla = document.getElementById('tabla-gastos');
    const tbody = document.getElementById('cuerpo-tabla');

    try {
        // Hace match con @router.get("/VerGastos")
        const respuesta = await fetch(`${URL_API}/VerGastos`); 
        
        if (!respuesta.ok) {
            throw new Error(`Error en el servidor: ${respuesta.status}`);
        }

        const gastos = await respuesta.json();

        tbody.innerHTML = '';

        if (gastos.length === 0) {
            estado.textContent = "Aún no tienes gastos registrados.";
            estado.style.display = 'block';
            tabla.style.display = 'none';
            return;
        }

        gastos.forEach(gasto => {
            const tr = document.createElement('tr');
            
            // Usamos los campos exactos de tu clase Movimiento en movimiento_model.py
            const idGasto = gasto.IdMovimiento;
            const concepto = gasto.Concepto;
            const monto = parseFloat(gasto.Monto).toFixed(2);
            // Formatear fecha si existe, de lo contrario mostrar texto por defecto
            const fecha = gasto.FechaMovimiento ? new Date(gasto.FechaMovimiento).toLocaleDateString() : 'Sin fecha';

            tr.innerHTML = `
                <td>${idGasto}</td>
                <td>${fecha}</td>
                <td>${concepto}</td>
                <td class="monto gasto">- Q ${monto}</td>
                <td>
                    <button class="btn-eliminar" onclick="eliminarGasto(${idGasto})">
                        🗑️ Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        estado.style.display = 'none';
        tabla.style.display = 'table';

    } catch (error) {
        console.error("Error al cargar gastos:", error);
        estado.textContent = "Error al conectar con el servidor.";
        estado.style.color = "red";
    }
}

async function eliminarGasto(idGasto) {
    const confirmar = confirm(`¿Estás seguro de que deseas eliminar el gasto #${idGasto}?`);
    
    if (!confirmar) return;

    try {
        // Tu ruta es @router.delete("/BorrarGasto") y recibe id_gasto como query param
        const respuesta = await fetch(`${URL_API}/BorrarGasto?id_gasto=${idGasto}`, {
            method: 'DELETE',
        });

        if (respuesta.ok) {
            alert("Gasto eliminado exitosamente");
            obtenerGastos(); // Recarga la tabla
        } else {
            const errorData = await respuesta.json();
            alert(`Error al eliminar: ${errorData.detail || 'Problema en el servidor'}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("No se pudo conectar con el servidor para eliminar.");
    }
}