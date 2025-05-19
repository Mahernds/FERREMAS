// id de los selectores
let idNombre = "#inputNombreContacto";
let idCorreo = "#inputCorreoContacto";
let idFono = "#inputFonoContacto";
let idTexto = "#inputTextoContacto";

// funciones de estilo de campos validos e invalidos
function setCampoValido(id) {
  $(id).addClass("is-valid");
  $(id).removeClass("is-invalid");
}

function setCampoInvalido(id) {
  $(id).addClass("is-invalid");
  $(id).removeClass("is-valid");
}

function setCampoNeutro(id) {
  $(id).removeClass("is-valid");
  $(id).removeClass("is-invalid");
}

function actualizarCSS(esValido, id) {
  if (esValido) {
    setCampoValido(id);
  } else {
    setCampoInvalido(id);
  }
}

// validacion de nombre
function validarNombre(nombre) {
  let esValido = false;
  if (nombre.length > 0) {
    esValido = true;
  }
  actualizarCSS(esValido, idNombre);
}

$(idNombre).on("focusout", function () {
  let val = $(idNombre).val();
  if (val.length > 0) {
    validarNombre(val);
  } else {
    setCampoNeutro(idNombre);
  }
});

// validacion de correo
function validarCorreo(correo) {
  let esValido = false;
  if (correo.length > 0) {
    esValido = true;
  }
  actualizarCSS(esValido, idCorreo);
}

$(idCorreo).on("focusout", function () {
  let val = $(idCorreo).val();
  if (val.length > 0) {
    validarCorreo(val);
  } else {
    setCampoNeutro(idCorreo);
  }
});

// validacion de fono
function validarFono(fono) {
  let esValido = false;
  if (fono.length > 0) {
    esValido = true;
  }
  actualizarCSS(esValido, idFono);
}

$(idFono).on("focusout", function () {
  let val = $(idFono).val();
  if (val.length > 0) {
    validarFono(val);
  } else {
    setCampoNeutro(idFono);
  }
});

// validacion de texto
function validarTexto(texto) {
  let esValido = false;
  if (texto.length > 0) {
    esValido = true;
  }
  actualizarCSS(esValido, idTexto);
}

$(idTexto).on("focusout", function () {
  let val = $(idTexto).val();
  if (val.length > 0) {
    validarTexto(val);
  } else {
    setCampoNeutro(idTexto);
  }
});

// al hacer click en enviar revisamos que este todo valido
$("form button").on("click", function () {
  let esFormularioValido = true;
  $(".form-group input, textarea").each(function (index, element) {
    // console.log($(element).hasClass("is-valid"));
    if (!$(element).hasClass("is-valid")) {
      esFormularioValido = false;
    }
  });

  if (esFormularioValido) {
    console.log("formulario valido!");
    alert("formulario valido!")
    resetForm();
  } else {
    console.log("formulario invalido!");
  }
});
