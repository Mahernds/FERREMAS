const re = /A.+/;
console.log("hola!");
console.log(re.test("Asdfsdf"));

// funciones de estilo CSS
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

function resetCSSInputs() {
  $("input").removeClass("es-campo-valido es-campo-invalido");
}

// funciones validadoras
function validar(id, regex) {
  let esValido = false;
  const re = regex;

  let val = $(id).val();
  esValido = re.test(val);

  //cambiamos el estilo CSS segun corresponda
  if (esValido) {
    setCampoValido(id);
  } else {
    setCampoInvalido(id);
  }

  return esValido;
}

// a. Rut: largo entre 9 y 10 caracteres.
function validarRut() {
  const re = /^([0-9]{7,9}-([0-9]|k|K))/;
  let id = "#rutInput";
  return validar(id, re);
}
// ! el regex acepta numeros
// b. Nombre: largo entre 3 y 20 caracteres.
function validarNombre() {
  const re = /^([^0-9]{3,20})/;
  let id = "#nombreInput";
  return validar(id, re);
}

//! el regex acepta numeros
// c. Apellido paterno: largo entre 3 y 20 caracteres.
function validarApPaterno() {
  const re = /^([^0-9]{3,20})/;
  let id = "#apellidoPaternoInput";
  return validar(id, re);
}

//! el regex acepta numeros
// d. Apellido materno: largo entre 3 y 20 caracteres.
function validarApMaterno() {
  const re = /^([^0-9]{3,20})/;
  let id = "#apellidoMaternoInput";
  return validar(id, re);
}

// e. Edad: entre 18 y 35 años.
function validarEdad() {
  const re = /^(((1[8-9])|(2[0-9])|(3[0-5])))$/;
  let id = "#edadInput";
  return validar(id, re);
}

// f. Género: que sea seleccionado un género de la lista.
function validarGenero() {
  const re = /^(([1-9]))$/;
  let id = "#generoInput";
  return validar(id, re);
}

// g. Celular: largo 8
// +56 9 XXXX XXXX
function validarCelular() {
  const re = /^([1-9]{8})$/;
  let id = "#celularInput";
  return validar(id, re);
}

// formato email xxx@xxx.xxx
function validarEmail() {
  const re = /^(.+@.+\..+)/;
  let id = "#emailInput";
  return validar(id, re);
}

// que sea no vacio
function validarMensaje() {
  let esValido = false;
  let mensaje = $("#textAreaInput").val();
  let n = mensaje.trim().length;
  if (n > 0) {
    esValido = true;
  }
  if (esValido) {
    setCampoValido("#textAreaInput");
  } else {
    setCampoInvalido("#textAreaInput");
  }
  return esValido;
}

$(document).ready(function () {
  // al apretar el boton en formulario validamos todo
  $(".form-trabaja-con-nosotros button").click(function (e) {
    resetCSSInputs();
    console.log(e);
    let esFormularioValido = false;

    //validar rut 
    let esRutValido = validarRut();
    //validar nombre
    let esNombreValido = validarNombre();
    //validar apellido paterno
    let esApPaternoValido = validarApPaterno();
    //validar materno
    let esApMaternoValido = validarApMaterno();
    //validar edad
    let esEdadValido = validarEdad();
    //validar genero
    let esGeneroValido = validarGenero();
    //validar celular
    let esCelularValido = validarCelular();
    //validar email
    let esEmailValido = validarEmail();
    //validar mensaje
    let esMensajeValido = validarMensaje();

    esFormularioValido =
      esRutValido &&
      esNombreValido &&
      esApPaternoValido &&
      esApMaternoValido &&
      esEdadValido &&
      esGeneroValido &&
      esCelularValido &&
      esEmailValido &&
      esMensajeValido;

    if (esFormularioValido) {
      console.log("formulario valido!");
    } else {
      console.log("algo esta invalido");
    }
  });
});