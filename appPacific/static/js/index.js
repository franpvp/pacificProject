
// SideBar
let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');

btn.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});
// Buscador Selector Hab, Cant Adultos y Niños
let btn_adultos = document.querySelector('.btn-adultos');
let btn_ninos = document.querySelector('.btn-ninos');
let box_adultos = document.querySelector('.box-btn-adultos');
let box_ninos = document.querySelector('.box-btn-ninos');
let btn_minus_adultos = document.querySelector('#btn-minus-adultos');
let btn_plus_adultos = document.querySelector('#btn-plus-adultos');
let btn_minus_ninos = document.querySelector('#btn-minus-ninos');
let btn_plus_ninos = document.querySelector('#btn-plus-ninos');
var btnFiltro = document.querySelector('.filtro');
var contenedorFiltro = document.querySelector('.filtro-opciones');
var contadorAdultosInput = document.getElementById('contador_adultos_input');
var contadorNinosInput = document.getElementById('contador_ninos_input');

btn_adultos.addEventListener('click', function() {
    // event.stopPropagation();
    box_adultos.classList.toggle('active');
});

btn_ninos.addEventListener('click', function() {
    // event.stopPropagation();
    box_ninos.classList.toggle('active');
});

let contador_adultos = document.querySelector('.contador-adultos');
let contador_ninos = document.querySelector('.contador-ninos');
let contador_1 = 0;
let contador_2 = 0;



// Contador Adultos
btn_minus_adultos.addEventListener('click', function() {
    if(contador_1 > 0){
        contador_1--;
        contador_adultos.textContent = contador_1;
        contadorAdultosInput.value = contador_1;
        if(contador_1 != 1){
            btn_adultos.textContent = "Adultos: " + contador_1;
        } else{
            btn_adultos.textContent = "Adulto: " + contador_1;
        }
        
    }
});

btn_plus_adultos.addEventListener('click', function() {
    contador_1++;
    contador_adultos.textContent = contador_1;
    contadorAdultosInput.value = contador_1;
    if(contador_1 != 1){
        btn_adultos.textContent = "Adultos: " + contador_1;
    } else{
        btn_adultos.textContent = "Adulto: " + contador_1;
    }
    
});

// Contador Niños
btn_minus_ninos.addEventListener('click', function() {
    if(contador_2 > 0){
        contador_2--;
        contador_ninos.textContent = contador_2;
        contadorNinosInput.value = contador_2;
        if(contador_2 != 1){
            btn_ninos.textContent = "Niños: " + contador_2;
        } else{
            btn_ninos.textContent = "Niño: " + contador_2;
        }
        
    }
});

btn_plus_ninos.addEventListener('click', function() {
    contador_2++;
    contador_ninos.textContent = contador_2;
    contadorNinosInput.value = contador_2;
    if(contador_2 != 1){
        btn_ninos.textContent = "Niños: " + contador_2;
    } else{
        btn_ninos.textContent = "Niño: " + contador_2;
    }
    
});

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
    if (!btn_adultos.contains(event.target)) {
        // Ocultar el contenido aquí
        box_adultos.classList.remove('active');
    } else{
        box_adultos.classList.add('active');
    }
    if(!btn_ninos.contains(event.target)){
        box_ninos.classList.remove('active');
    } else{
        box_ninos.classList.add('active');
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


function mostrarMensaje() {
    alert("Debe iniciar sesión antes de realizar una reserva.");
    window.location.href = "/iniciosesion";
}
