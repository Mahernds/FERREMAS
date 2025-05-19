$(document).ready(function () {
  // variables de animacion del contador
  let contador = $("#contadorCarrito");
  let posY = contador.css("top");
  let posY2 = posY;
  let posY1 = (parseInt(posY.substr(0, 2)) + 3) + "px";

  actualizarContador();
  // para probar borramos la data persistente
  //   sessionStorage.removeItem("numProductos");

  $(".btn-agregar-producto").click(function () {
    agregarProducto();
    actualizarContador();
    animarContador();
  });

  function agregarProducto() {
    let numProductos = sessionStorage.getItem("numProductos");

    if (numProductos == null) {
      numProductos = 1;
    } else {
      numProductos = parseInt(numProductos) + 1;
    }

    sessionStorage.setItem("numProductos", numProductos);
  }

  function actualizarContador() {
    let numProductos = sessionStorage.getItem("numProductos");

    if (numProductos == null) {
      numProductos = 0;
    }

    $("#contadorCarrito").text(numProductos);

    if (numProductos == 0) {
      $("#contadorCarrito").css("display", "none");
    } else {
      $("#contadorCarrito").css("display", "block");
    }
  }

  function animarContador() {
    // console.log(posY1, posY2);
    contador.animate({ top: posY1 }, 150);
    contador.animate({ top: posY2 }, 100);
  }
});