/**
 * carrito.js
 * Lógica para mostrar y gestionar el carrito de compras
 * Usa localStorage con la clave 'carrito'
 * Estructura de cada producto: {id, nombre, precio, cantidad, imagen}
 */

/**
 * Agrega un producto al carrito en localStorage.
 * @param {Object} producto - Debe tener id, nombre, precio, imagen.
 */
function agregarAlCarrito(producto) {
  let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const idx = carrito.findIndex(p => p.id == producto.id);
  if (idx !== -1) {
    carrito[idx].cantidad += 1;
  } else {
    carrito.push({
      id: producto.id,
      nombre: producto.nombre,
      precio: producto.precio,
      imagen: producto.imagen || '', // Opcional
      cantidad: 1
    });
  }
  localStorage.setItem('carrito', JSON.stringify(carrito));
  if (window.actualizarContadorCarrito) window.actualizarContadorCarrito(true); // true para animar
}

function obtenerCarrito() {
  return JSON.parse(localStorage.getItem('carrito')) || [];
}

function guardarCarrito(carrito) {
  localStorage.setItem('carrito', JSON.stringify(carrito));
}

function renderizarCarrito() {
  const carrito = obtenerCarrito();
  const tbody = document.getElementById('carrito-items');
  const totalSpan = document.getElementById('carrito-total');
  const vacioDiv = document.getElementById('carrito-vacio');
  const contenidoDiv = document.getElementById('carrito-contenido');

  if (!tbody || !totalSpan || !vacioDiv || !contenidoDiv) return; // Si no estamos en carrito.html

  tbody.innerHTML = '';
  let total = 0;

  if (carrito.length === 0) {
    vacioDiv.style.display = 'block';
    contenidoDiv.style.display = 'none';
    totalSpan.textContent = '0';
    if (window.actualizarContadorCarrito) window.actualizarContadorCarrito();
    return;
  } else {
    vacioDiv.style.display = 'none';
    contenidoDiv.style.display = 'block';
  }

  carrito.forEach((producto, idx) => {
    const subtotal = producto.precio * producto.cantidad;
    total += subtotal;

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <img src="${producto.imagen || '../../imagenes/logo-auto-negro.svg'}" alt="" width="50" class="me-2">
        ${producto.nombre}
      </td>
      <td>$${producto.precio.toLocaleString()}</td>
      <td>
        <input type="number" min="1" value="${producto.cantidad}" data-idx="${idx}" class="form-control cantidad-input" style="width:80px;">
      </td>
      <td>$${subtotal.toLocaleString()}</td>
      <td>
        <button class="btn btn-danger btn-sm eliminar-btn" data-idx="${idx}">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  totalSpan.textContent = total.toLocaleString();
  if (window.actualizarContadorCarrito) window.actualizarContadorCarrito();
}

// Cambiar cantidad
document.addEventListener('input', function (e) {
  if (e.target.classList.contains('cantidad-input')) {
    const idx = parseInt(e.target.dataset.idx);
    let carrito = obtenerCarrito();
    let nuevaCantidad = parseInt(e.target.value);
    if (nuevaCantidad < 1 || isNaN(nuevaCantidad)) nuevaCantidad = 1;
    carrito[idx].cantidad = nuevaCantidad;
    guardarCarrito(carrito);
    renderizarCarrito();
  }
});

// Eliminar producto
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('eliminar-btn')) {
    const idx = parseInt(e.target.dataset.idx);
    let carrito = obtenerCarrito();
    carrito.splice(idx, 1);
    guardarCarrito(carrito);
    renderizarCarrito();
  }
});

// Vaciar carrito
document.addEventListener('click', function (e) {
  if (e.target.id === 'btn-vaciar-carrito') {
    if (confirm('¿Seguro que quieres vaciar el carrito?')) {
      localStorage.removeItem('carrito');
      renderizarCarrito();
    }
  }
});

// Proceder al pago (puedes enlazar a la integración de PayPal después)
document.addEventListener('click', function (e) {
  if (e.target.id === 'btn-pagar') {
    alert('Aquí irá la integración con PayPal.');
    // window.location.href = 'pago.html'; // Si tienes una página de pago
  }
});

// Renderizar al cargar
document.addEventListener('DOMContentLoaded', renderizarCarrito);