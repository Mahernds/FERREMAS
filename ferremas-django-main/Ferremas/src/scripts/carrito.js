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
      imagen: producto.imagen || '',
      cantidad: 1
    });
  }
  localStorage.setItem('carrito', JSON.stringify(carrito));
  if (window.actualizarContadorCarrito) window.actualizarContadorCarrito(true);
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

  if (!tbody || !totalSpan || !vacioDiv || !contenidoDiv) return;

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

  renderizarBotonPaypal(); // ← ¡Aquí se renderiza PayPal!
}

// Renderizar botón PayPal solo si no ha sido renderizado
function renderizarBotonPaypal() {
  const paypalContainer = document.getElementById('paypal-button-container');
  if (!paypalContainer || paypalContainer.children.length > 0) return;

  const totalElement = document.getElementById('carrito-total');
  const total = parseFloat(totalElement.textContent.replace(/[^\d]/g, '') || "0");

  paypal.Buttons({
    createOrder: function (data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            currency_code: "CLP",
            value: total.toFixed(0)
          }
        }]
      });
    },
    onApprove: function (data, actions) {
      return actions.order.capture().then(function (details) {
        localStorage.removeItem('carrito'); // Vacía el carrito al pagar
        window.location.href = 'gracias.html';
      });
    },
    onError: function (err) {
      console.error('Error en el pago:', err);
      alert('Hubo un error al procesar el pago.');
    }
  }).render('#paypal-button-container');
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

// Ya no se usa 'btn-pagar'
// Se eliminó la función onclick de btn-pagar

// Renderizar al cargar
document.addEventListener('DOMContentLoaded', renderizarCarrito);
