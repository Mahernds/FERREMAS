/**
 * contadorCarrito.js
 * Actualiza el contador del carrito en el header usando localStorage
 * y anima el contador cuando se agrega un producto.
 * Debe incluirse en todas las páginas con el header del carrito.
 */

function actualizarContadorCarrito(animar = false) {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const contador = carrito.reduce((acc, prod) => acc + prod.cantidad, 0);
  const contadorDiv = document.getElementById('contadorCarrito');
  if (!contadorDiv) return;

  contadorDiv.textContent = contador;

  if (contador === 0) {
    contadorDiv.style.display = "none";
  } else {
    contadorDiv.style.display = "block";
    if (animar) {
      // Animación simple: "salta" el contador
      const originalTop = contadorDiv.style.top || "0px";
      contadorDiv.style.transition = "top 0.15s";
      contadorDiv.style.top = "3px";
      setTimeout(() => {
        contadorDiv.style.top = originalTop;
      }, 150);
    }
  }
}

// Permite que otros scripts llamen a actualizarContadorCarrito()
window.actualizarContadorCarrito = actualizarContadorCarrito;

// Actualiza el contador al cargar la página
document.addEventListener('DOMContentLoaded', () => actualizarContadorCarrito());