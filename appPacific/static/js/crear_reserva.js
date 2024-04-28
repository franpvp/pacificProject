// document.getElementById('paypal-button').addEventListener('click', function(event) {
//     event.preventDefault(); // Evitar que el enlace redireccione

//     // Capturar el correo electrónico del usuario
//     var correoElectronico = document.getElementById('correo').value;

//     // Enviar el correo electrónico al backend a través de una solicitud AJAX
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/enviar_correo_paypal/', true);
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.onload = function() {
//         if (xhr.status === 200) {
//             // Manejar la respuesta del backend, si es necesario
//             console.log('Correo electrónico enviado con éxito.');
//         } else {
//             console.error('Error al enviar el correo electrónico.');
//         }
//     };
//     xhr.onerror = function() {
//         console.error('Error de red al enviar el correo electrónico.');
//     };
//     xhr.send(JSON.stringify({ correoElectronico: correoElectronico }));
// });


document.addEventListener('DOMContentLoaded', function() {
    const tipoHabSelect = document.getElementById('tipo_hab_select');
    const tituloHabSelect = document.getElementById('titulo_hab_select');
    const precioElement = document.getElementById('precio');
    const pagoInicialElement = document.getElementById('pago_inicial');
    const pagoPendienteElement = document.getElementById('pago_pendiente');
    const precioInfoDiv = document.getElementById('precioInfo');

    tipoHabSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        console.log('Valor seleccionado:', selectedValue);
        
        // Realiza la solicitud Ajax para enviar los valores seleccionados a la vista Django
        fetch(`/crear_reserva_pacific/?id_tipo_hab=${selectedValue}`)
            .then(response => response.json())
            .then(data => {
                console.log("DATA: ", data);
                // Elimina las opciones existentes del segundo select
                tituloHabSelect.innerHTML = '';
                
                // Agrega las nuevas opciones al segundo select
                data.habitaciones.forEach(habitacion => {
                    const option = document.createElement('option');
                    option.value = habitacion.id_tipo_hab; // Asigna el valor del ID de la habitación
                    option.text = `${habitacion.titulo_hab}  (Precio: $${habitacion.precio})`;
                    option.setAttribute('data-precio', habitacion.precio); // Concatena el título y el precio
                    option.setAttribute('data-capacidad', habitacion.capacidad_max);
                    tituloHabSelect.appendChild(option);
                });
                // Mostrar el precio de la opción seleccionada
                mostrarPrecioYPagos();
                precioInfoDiv.style.display = 'block';
                
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Función para mostrar el precio de la opción seleccionada
    function mostrarPrecioYPagos() {
        const selectedOption = tituloHabSelect.options[tituloHabSelect.selectedIndex];
        const precio = selectedOption.getAttribute('data-precio');
        precioElement.textContent = precio ? `Precio: $${precio} CLP` : '';

        // Calcular el pago inicial y pendiente
        const pagoInicial = precio ? parseInt(precio) * 0.3 : 0;
        const pagoPendiente = precio ? parseInt(precio) * 0.7 : 0;
        pagoInicialElement.textContent = `Pago inicial: $${pagoInicial} CLP`;
        pagoPendienteElement.textContent = `Pago pendiente: $${pagoPendiente} CLP`;
    }

    // Mostrar el precio al cargar la página
    mostrarPrecioYPagos();


    // Agregar evento de cambio al select
    tituloHabSelect.addEventListener('change', function() {
        // Mostrar el precio cuando cambia la selección
        mostrarPrecioYPagos();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const tituloHabSelect = document.getElementById('titulo_hab_select');
    const capacidadMaximaElement = document.getElementById('capacidad_maxima');

    // Función para mostrar la capacidad máxima
    function mostrarCapacidadMaxima() {
        const selectedOption = tituloHabSelect.options[tituloHabSelect.selectedIndex];
        const capacidadMaxima = selectedOption.getAttribute('data-capacidad');
        capacidadMaximaElement.textContent = capacidadMaxima ? `Capacidad máxima: ${capacidadMaxima}` : '';
    }

    // Mostrar la capacidad máxima al cargar la página
    mostrarCapacidadMaxima();

    // Agregar evento de clic al select
    tituloHabSelect.addEventListener('click', function() {
        // Mostrar la capacidad máxima al hacer clic en el select
        mostrarCapacidadMaxima();
    });

    // Agregar evento de cambio al select
    tituloHabSelect.addEventListener('change', function() {
        // Mostrar la capacidad máxima cuando cambia la selección
        mostrarCapacidadMaxima();
    });
});

