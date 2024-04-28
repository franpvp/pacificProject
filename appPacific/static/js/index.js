
// SideBar
let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');

btn.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});
// Buscador Selector Hab, Cant Adultos y Niños
let btn_huespedes = document.querySelector('.btn-huespedes');
let contenedor_huespedes = document.querySelector('.contenedor-huespedes');
let btn_minus_adultos = document.querySelector('#btn-minus-adultos');
let btn_plus_adultos = document.querySelector('#btn-plus-adultos');
let btn_minus_ninos = document.querySelector('#btn-minus-ninos');
let btn_plus_ninos = document.querySelector('#btn-plus-ninos');
var btnFiltro = document.querySelector('.filtro');
var contenedorFiltro = document.querySelector('.filtro-opciones');
var contadorAdultosInput = document.getElementById('contador_adultos_input');
var contadorNinosInput = document.getElementById('contador_ninos_input');

// Event listener para el clic en cualquier parte del documento
document.addEventListener('click', function(event) {
    // Verificar si el clic no ocurrió dentro del contenedor de huéspedes y no fue en el botón de huéspedes
    if (!contenedor_huespedes.contains(event.target) && event.target !== btn_huespedes) {
        // Ocultar el contenedor de huéspedes
        contenedor_huespedes.classList.remove('active');
    }
});

// Event listener para el clic en el botón de huéspedes
btn_huespedes.addEventListener('click', function(event) {
    // Evitar que el clic se propague al documento y active el listener del documento
    event.stopPropagation();
    // Alternar la clase activa del contenedor de huéspedes
    contenedor_huespedes.classList.toggle('active');
});

// Event listener para el clic dentro del contenedor de huéspedes
contenedor_huespedes.addEventListener('click', function(event) {
    // Evitar que el clic se propague al documento y active el listener del documento
    event.stopPropagation();
});

let contador_adultos = document.querySelector('.contador-adultos');
let contador_ninos = document.querySelector('.contador-ninos');
let contador_1 = 0;
let contador_2 = 0;

// Función para actualizar el estilo del botón de restar de adultos
function actualizarEstiloBotonRestarAdultos() {
    if (contador_1 === 0) {
        btn_minus_adultos.style.opacity = '0.5';
        btn_minus_adultos.style.pointerEvents = 'none'; // Desactivar eventos de puntero (hover, clic)
    } else {
        btn_minus_adultos.style.opacity = '1';
        btn_minus_adultos.style.pointerEvents = 'auto'; // Activar eventos de puntero
    }
}

// Función para actualizar el estilo del botón de restar de niños
function actualizarEstiloBotonRestarNinos() {
    if (contador_2 === 0) {
        btn_minus_ninos.style.opacity = '0.5';
        btn_minus_ninos.style.pointerEvents = 'none'; // Desactivar eventos de puntero (hover, clic)
    } else {
        btn_minus_ninos.style.opacity = '1';
        btn_minus_ninos.style.pointerEvents = 'auto'; // Activar eventos de puntero
    }
}

// Función para actualizar el contenido del botón con los resultados de los contadores
function actualizarContenidoBoton() {
    let textoBoton = "Adulto" + (contador_1 !== 1 ? "s" : "") + ": " + contador_1 + ", Niño" + (contador_2 !== 1 ? "s" : "") + ": " + contador_2;
    btn_huespedes.textContent = textoBoton;
    actualizarEstiloBotonRestarAdultos(); // Actualizar estilo del botón de restar de adultos
    actualizarEstiloBotonRestarNinos(); // Actualizar estilo del botón de restar de niños
}

// Contador Adultos
btn_minus_adultos.addEventListener('click', function() {
    if(contador_1 > 0){
        contador_1--;
        contador_adultos.textContent = contador_1;
        contadorAdultosInput.value = contador_1;
        actualizarContenidoBoton();
    }
});

btn_plus_adultos.addEventListener('click', function() {
    contador_1++;
    contador_adultos.textContent = contador_1;
    contadorAdultosInput.value = contador_1;
    actualizarContenidoBoton();
});

// Contador Niños
btn_minus_ninos.addEventListener('click', function() {
    if(contador_2 > 0){
        contador_2--;
        contador_ninos.textContent = contador_2;
        contadorNinosInput.value = contador_2;
        actualizarContenidoBoton();
    }
});

btn_plus_ninos.addEventListener('click', function() {
    contador_2++;
    contador_ninos.textContent = contador_2;
    contadorNinosInput.value = contador_2;
    actualizarContenidoBoton();
});

// Llama a estas funciones al principio para establecer el estilo inicial de los botones de restar
actualizarEstiloBotonRestarAdultos();
actualizarEstiloBotonRestarNinos();

// Botones Filtrar
// Función para filtrar habitaciones por tipo
document.querySelectorAll('.btn-filtrar').forEach(btn => {
    btn.addEventListener('click', function() {
        const idTipoHab = this.getAttribute('data-id-tipo-hab');

        // Mostrar solo las habitaciones del tipo seleccionado y habilitar las que estaban ocultas
        document.querySelectorAll('.habitacion').forEach(hab => {
            if (hab.classList.contains('tipo-' + idTipoHab)) {
                hab.style.display = 'block';
            } else {
                hab.style.display = 'none';
            }
        });
    });
});

btnFiltro.addEventListener('click', function() {
    var contenedorFiltro = document.querySelector('.filtro-opciones');
    if (contenedorFiltro.classList.contains('active')) {
        contenedorFiltro.classList.remove('active');
    } else {
        contenedorFiltro.classList.add('active');
    }
});

document.addEventListener('click', function(event) {
    var contenedorFiltro = document.querySelector('.filtro-opciones');
    if (!contenedorFiltro.contains(event.target) && event.target !== btnFiltro) {
        contenedorFiltro.classList.remove('active');
    }
});

// Detectar clics fuera del botón
window.addEventListener('click', function(event) {
    // Verificar si el clic no se realizó dentro del contenedor del botón o su contenido
    if (!btn_huespedes.contains(event.target)) {
        // Ocultar el contenido aquí
        contenedor_huespedes.classList.remove('active');
    } else{
        contenedor_huespedes.classList.add('active');
    }
    // if (!btnFiltro.contains(event.target)) {
    //     contenedorFiltro.classList.remove('active');
    // } else{
    //     contenedorFiltro.classList.add('active');
    // }
});

// Botón Filtrar (Más económicos, más caros)
// Función para ordenar las habitaciones por precio de mayor a menor
function ordenarPorPrecioMayorAMenor() {
    const habitacionesArray = Array.from(document.querySelectorAll('.habitacion'));
    const row = document.querySelector('.row.mt-2.justify-content-center'); // Seleccionamos la fila existente
    habitacionesArray.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.card-text[data-precio]').getAttribute('data-precio').replace('$', '').replace(' CLP', ''));
        const precioB = parseFloat(b.querySelector('.card-text[data-precio]').getAttribute('data-precio').replace('$', '').replace(' CLP', ''));
        return precioB - precioA;
    });
    habitacionesArray.forEach(habitacion => {
        row.appendChild(habitacion); // Añadimos cada habitación ordenada a la fila existente
    });
}

// Agregar event listener al botón para ordenar de mayor a menor precio
document.querySelector('.mas-caros').addEventListener('click', function() {
    ordenarPorPrecioMayorAMenor();
    // Mostrar todas las habitaciones nuevamente
    document.querySelectorAll('.habitacion').forEach(hab => {
        hab.style.display = 'block';
    });
});


// Función para ordenar las habitaciones por precio de menor a mayor
function ordenarPorPrecioMenorAMayor() {
    const habitacionesArray = Array.from(document.querySelectorAll('.habitacion'));
    const row = document.querySelector('.row.mt-2.justify-content-center'); // Seleccionamos la fila existente
    habitacionesArray.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.card-text[data-precio]').getAttribute('data-precio').replace('$', '').replace(' CLP', ''));
        const precioB = parseFloat(b.querySelector('.card-text[data-precio]').getAttribute('data-precio').replace('$', '').replace(' CLP', ''));
        return precioA - precioB; // Cambiamos el orden de la resta para ordenar de menor a mayor
    });
    habitacionesArray.forEach(habitacion => {
        row.appendChild(habitacion); // Añadimos cada habitación ordenada a la fila existente
    });
}

// Agregar event listener al botón para ordenar de menor a mayor precio
document.querySelector('.mas-economicos').addEventListener('click', function() {
    ordenarPorPrecioMenorAMayor();
    // Mostrar todas las habitaciones nuevamente
    document.querySelectorAll('.habitacion').forEach(hab => {
        hab.style.display = 'block';
    });
});

// Se guardar los campos del buscador
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('form-busqueda').addEventListener('submit', function(event) {
        // Obtener los valores de los campos de entrada
        var fechaLlegada = document.getElementById('fecha_llegada').value;
        var fechaSalida = document.getElementById('fecha_salida').value;
        var contadorAdultos = parseInt(document.getElementById('contador-adultos').innerText);
        var contadorNinos = parseInt(document.getElementById('contador-ninos').innerText);
        
        // Validar que las fechas de llegada y salida estén ingresadas y que al menos un adulto esté seleccionado
        if (fechaLlegada.trim() === '' || fechaSalida.trim() === '') {
            alert('Por favor ingrese las fechas de llegada y salida.');
            event.preventDefault(); // Evitar el envío del formulario si hay campos vacíos
        } else if (contadorAdultos < 1) {
            alert('Debe seleccionar al menos 1 adulto.');
            event.preventDefault(); // Evitar el envío del formulario si no hay adultos seleccionados
        }
    });
});

var btnFiltro = document.querySelector('.filtro');
var iconoFiltro = document.getElementById('icono-filtro');

// Añadimos un evento de clic al botón de filtro
btnFiltro.addEventListener('click', function() {
    // Alternamos la clase 'rotated' en el icono
    iconoFiltro.classList.toggle('rotated');
});

// Volvemos al estado original cuando se hace clic en cualquier lugar de la página excepto en el botón de filtro
document.addEventListener('click', function(event) {
    if (!event.target.matches('.filtro')) {
        // Eliminamos la clase 'rotated' del icono si no se hizo clic en el botón de filtro
        iconoFiltro.classList.remove('rotated');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los elementos de precio
    const precios = document.querySelectorAll('.precio');
    
    // Definir la traducción de "noche" según el idioma actual
    const traduccionNoche = idioma === "en" ? "night" : "noche";

    // Iterar sobre cada elemento de precio
    precios.forEach(function(precioElement) {
        // Obtener el precio sin formato de los datos del atributo data
        const precioSinFormato = precioElement.getAttribute('data-precio');

        // Convertir el precio sin formato a un número y formatearlo con el formato 99.999
        const precioFormateado = parseFloat(precioSinFormato).toLocaleString('es-CL');

        // Actualizar el contenido del elemento con el precio formateado y la traducción de "noche"
        precioElement.innerHTML = `<strong>$${precioFormateado} CLP </strong>${traduccionNoche}`;
    });
});

function mostrarMensaje() {
    alert("Debe iniciar sesión antes de realizar una reserva.");
    window.location.href = "/iniciosesion";
}


const btnBuscador = document.getElementById('btn-buscador');
const textoBuscador = document.getElementById('texto-buscador');
const iconoBuscador = document.getElementById('icono-buscador');

btnBuscador.addEventListener('mouseover', function() {
    textoBuscador.textContent = 'Buscar';
});

btnBuscador.addEventListener('mouseout', function() {
    textoBuscador.textContent = '';
});
