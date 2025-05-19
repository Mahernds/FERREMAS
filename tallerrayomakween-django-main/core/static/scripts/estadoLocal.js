const diaSemana = {
    1: "Lunes",
    2: "Martes",
    3: "Miercoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sabado",
    0: "Domingo"
}

const horarioLaboral = {
    "semana": "8AM - 6PM",
    "sabado": "9AM - 2PM"
}

const mensajeAbierto = "Ven a nuesto taller! Estamos atendiendo";
const mensajeCerrado = "Nuesto taller esta cerrado :(";

const horaAperturaSemana = "08:00";
const horaCierreSemana = "18:00";
const horaAperturaSabado = "09:00";
const horaCierreSabado = "14:00";

// funcion del reloj
function actualizarHora() {
    // obtenemos fecha actual del sistema
    let hora, minutos, segundos;
    let dateTime = new Date();
    hora = dateTime.getHours();
    minutos = dateTime.getMinutes();
    segundos = dateTime.getSeconds();

    // arreglamos el formato de 1 digito a 2 para mantener consistencia
    if (segundos < 10) {
        segundos = "0" + segundos;
    }
    if (minutos < 10) {
        minutos = "0" + minutos;
    }

    // de formato 24hrs a 12hrs AM y PM
    if (hora = 0) {
        horaActual = "12" + ":" + minutos + " AM";
    }
    if (hora = 12) {
        horaActual = hora + ":" + minutos + " PM";
    }
    else if (hora > 12) {
        horaActual = hora % 12 + ":" + minutos + " PM";
    }
    else {
        horaActual = hora % 12 + ":" + minutos + " AM";
    }
    console.log(horaActual);
    $(".hora-actual").text(horaActual);
}

// funcion de calculo del estado de apertura del taller
function setApertura(dateTime) {

    // true si dateTime esta entre las fechas de apertura y cierre
    // false en otro caso
    function fechaEntre(fechaApertura, fechaCierre) {
        let fechaActual = dateTime;

        let apertura = new Date();
        apertura.setHours(fechaApertura.substr(0, 2));
        apertura.setMinutes(fechaApertura.substr(3, 2))
        apertura.setSeconds(0);

        let cierre = new Date();
        cierre.setHours(fechaCierre.substr(0, 2));
        cierre.setMinutes(fechaCierre.substr(3, 2))
        cierre.setSeconds(0);

        if (apertura < fechaActual && fechaActual < cierre) {
            return true;
        }
        return false;
    }

    function actualizarIcono(esAbierto){
        $(".icono-apertura").css("display", "flex");
        if(esAbierto){
            $(".icono-apertura").text("Abierto");
            $(".icono-apertura").addClass("abierto");
        }
        else{
            $(".icono-apertura").text("Cerrado");
            $(".icono-apertura").addClass("cerrado");
        }
    }

    // aasignamos mensajes sobre horarios y estado de apertura segun la fecha
    let mensajeAtencion = "";
    let mensajeApertura = "";
    let estaAbierto = false;

    switch (dateTime.getDay()) {
        case 0: //domingo
            mensajeAtencion = "Hoy es Domingo. Solo atendemos de Lunes a Sabado."
            estaAbierto = false;
            break;
        case 6: //sabado
            mensajeAtencion = `Hoy Sabado atendemos de ${horarioLaboral["sabado"]}`;
            estaAbierto = fechaEntre(horaAperturaSabado, horaCierreSabado);
            break;
        default: //dia de semana
            mensajeAtencion = `Hoy ${diaSemana[dateTime.getDay()]} atendemos de ${horarioLaboral["semana"]}`;
            estaAbierto = fechaEntre(horaAperturaSemana, horaCierreSemana);
            break;
    }

    if (estaAbierto) {
        mensajeApertura = mensajeAbierto;
    } else {
        mensajeApertura = mensajeCerrado;
    }
    
    // escribimos mensajes en el HTML
    $(".mensaje-atencion").text(mensajeAtencion);
    $(".mensaje-apertura").text(mensajeApertura);

    // actualizamos icono de estado de apertura del taller
    actualizarIcono(estaAbierto);
}

// API hora global
$(document).ready(function () {
    urlZonaHoraria = "https://worldtimeapi.org/api/timezone/America/Santiago";
    console.log("test");
    $.ajax({
        type: "get",
        url: urlZonaHoraria,
        success: function (response) {
            // obtenemos la hora de Chile y la procesamos
            let dateTime = new Date(response.datetime);
            // dateTime.setDate(11)
            // console.log(response);
            setApertura(dateTime);
        }
    });
});

// Reloj
$(document).ready(function () {
    setInterval(() => {
        actualizarHora();
    }, 1000);
});