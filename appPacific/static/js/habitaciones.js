// Botones Filtrar (Suite, Premium, Twin)
document.querySelectorAll('.btn-filtrar').forEach(btn => {
    btn.addEventListener('click', function() {
        const idTipoHab = this.getAttribute('data-id-tipo-hab');

        if (!idTipoHab) {
            console.error('El botón no tiene el atributo data-id-tipo-hab.');
            return;
        }

        // Ocultar todas las columnas
        document.querySelectorAll('.habitacion').forEach(col => {
            col.style.display = 'none';
        });

        // Mostrar solo las columnas del tipo seleccionado
        document.querySelectorAll('.tipo-' + idTipoHab).forEach(col => {
            col.style.display = 'block';
        });
    });
});


// Contenedor Botón Filtrar
// var btnFiltro = document.querySelector('.filtro-hab');
// var contenedorFiltro = document.querySelector('.filtro-op');


// Detectar clics fuera del botón
// window.addEventListener('click', function(event) {
//     // Verificar si el clic no se realizó dentro del contenedor del botón o su contenido
//     if (!btnFiltro.contains(event.target)) {
//         // Ocultar el contenido aquí
//         contenedorFiltro.classList.remove('active');
//     } else{
//         contenedorFiltro.classList.add('active');
//     }
// });

// Filtrar por más ecónomicos o más caros
function ordenarHabitaciones(orden) {
    var preciosHabitaciones = document.querySelectorAll('.precio'); // Seleccionamos todos los elementos con la clase 'precio-hab'

    var habitacionesArray = Array.from(preciosHabitaciones).map(function(precioHabitacion) {
        return {
            elemento: precioHabitacion.closest('.habitacion'), // Obtenemos el elemento habitación más cercano
            precio: parseFloat(precioHabitacion.innerText.split('$ ')[1]) // Extraemos y convertimos el precio
        };
    });

    habitacionesArray.sort(function(a, b) {
        return orden === 'asc' ? a.precio - b.precio : b.precio - a.precio; // Ordenamos por precio ascendente o descendente
    });

    var habitacionesContainer = document.querySelector('.row.mt-2.habitacion'); // Seleccionamos el contenedor de habitaciones

    // Eliminamos todas las habitaciones del contenedor
    while (habitacionesContainer.firstChild) {
        habitacionesContainer.removeChild(habitacionesContainer.firstChild);
    }

    // Añadimos las habitaciones ordenadas al contenedor
    habitacionesArray.forEach(function(habitacion) {
        habitacionesContainer.appendChild(habitacion.elemento);
    });
}


// Mostrar info de las habitaciones
const enlaceMostrarInfo = document.getElementById('btn-mostrar-info');
const divMasInformacion = document.querySelector('.mas-informacion');
const divBtnClose = document.querySelector('.btn-close');
const fondoOpaco = document.querySelector('.fondo-opaco');

// Agregar evento de clic al botón de "Más Información"
enlaceMostrarInfo.addEventListener('click', function() {
    // Mostrar la ventana de información con un retraso pequeño para permitir que el fondo opaco se muestre primero
    setTimeout(function() {
        divMasInformacion.style.display = 'block';
        divMasInformacion.classList.add('active'); // Agregar la clase 'active' para mostrar la ventana de información
    }, 200);
    fondoOpaco.style.display = 'block'; // Mostrar el fondo semi-transparente
});

// Agregar evento de clic al botón de "Cerrar" en la ventana de información
divBtnClose.addEventListener('click', function() {
    // Ocultar la ventana de información
    divMasInformacion.classList.remove('active'); // Quitar la clase 'active' para ocultar la ventana de información
    setTimeout(function() {
        divMasInformacion.style.display = 'none';
    }, 300); // Retrasar un poco para que la transición tenga tiempo de completarse
    fondoOpaco.style.display = 'none'; // Ocultar el fondo semi-transparente
});


function mostrarMensaje() {
    alert("Debe iniciar sesión antes de realizar una reserva.");
    window.location.href = "/iniciosesion";
}











