document.addEventListener('DOMContentLoaded', function() {
    const tipoHabSelect = document.getElementById('tipo_hab_select');
    const tituloHabSelect = document.getElementById('titulo_hab_select');
    const precioElement = document.getElementById('precio');
    const pagoInicialElement = document.getElementById('pago_inicial');
    const pagoPendienteElement = document.getElementById('pago_pendiente');
    const precioInfoDiv = document.getElementById('precioInfo');
    const capacidadMaximaElement = document.getElementById('capacidad_maxima');

    // Ocultar el detalle de la reserva al cargar la página
    precioInfoDiv.style.display = 'none';

    // Función para mostrar el precio de la opción seleccionada
    function mostrarPrecioYPagos() {
        if (!tituloHabSelect) return; // Verificar si el elemento existe
        const selectedOption = tituloHabSelect.options[tituloHabSelect.selectedIndex];
        const precio = selectedOption ? selectedOption.getAttribute('data-precio') : null;
        precioElement.textContent = precio ? `Precio: $${precio} CLP` : '';
        
        // Calcular el pago inicial y pendiente
        const pagoInicial = precio ? parseInt(precio * 0.3) : 0;
        const pagoPendiente = precio ? parseInt(precio * 0.7) : 0;
        pagoInicialElement.textContent = `Pago inicial: $${pagoInicial} CLP`;
        pagoPendienteElement.textContent = `Pago pendiente: $${pagoPendiente} CLP`;
    }

    // Función para mostrar la capacidad máxima
    function mostrarCapacidadMaxima() {
        if (!tituloHabSelect || tituloHabSelect.options.length === 0) {
            capacidadMaximaElement.textContent = ''; // Si no hay opciones disponibles, eliminar el contenido
            return;
        }
        const selectedOption = tituloHabSelect.options[tituloHabSelect.selectedIndex];
        const capacidadMaxima = selectedOption ? selectedOption.getAttribute('data-capacidad') : null;
        capacidadMaximaElement.textContent = capacidadMaxima ? `Capacidad máxima: ${capacidadMaxima}` : '';
    }

    // Agregar evento de cambio al select de tipo de habitación
    tipoHabSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        console.log('Valor seleccionado:', selectedValue);
        
        // Realizar la solicitud Ajax para enviar los valores seleccionados a la vista Django
        fetch(`/crear_reserva_pacific/?id_tipo_hab=${selectedValue}`)
            .then(response => response.json())
            .then(data => {
                console.log("DATA: ", data);
                // Eliminar las opciones existentes del segundo select
                if (tituloHabSelect) {
                    tituloHabSelect.innerHTML = '';
                    
                    // Agregar las nuevas opciones al segundo select
                    data.habitaciones.forEach(habitacion => {
                        const option = document.createElement('option');
                        option.value = habitacion.id_tipo_hab; // Asignar el valor del ID de la habitación
                        option.text = `${habitacion.titulo_hab}  (Precio: $${habitacion.precio})`;
                        option.setAttribute('data-precio', habitacion.precio); // Concatenar el título y el precio
                        option.setAttribute('data-capacidad', habitacion.capacidad_max);
                        tituloHabSelect.appendChild(option);
                    });
                }
                // Mostrar el precio de la opción seleccionada
                mostrarPrecioYPagos();

                // Mostrar u ocultar el detalle de la reserva según si hay habitaciones disponibles
                if (tituloHabSelect.options.length == 0) {
                    precioInfoDiv.style.display = 'none';
                    mostrarCapacidadMaxima();
                } else {
                    precioInfoDiv.style.display = 'block';
                    mostrarCapacidadMaxima();
                }
                
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Agregar evento de clic al select de habitaciones
    if (tituloHabSelect) {
        tituloHabSelect.addEventListener('click', function() {
            mostrarCapacidadMaxima();
            
        });

<<<<<<< HEAD
        // Calcular el pago inicial y pendiente
        const pagoInicial = precio ? parseInt(precio * 0.3) : 0;
        const pagoPendiente = precio ? parseInt(precio * 0.7) : 0;
        pagoInicialElement.textContent = `Pago inicial: $${pagoInicial} CLP`;
        pagoPendienteElement.textContent = `Pago pendiente: $${pagoPendiente} CLP`;
=======
        // Agregar evento de cambio al select de habitaciones
        tituloHabSelect.addEventListener('change', function() {
            // Mostrar el precio y la capacidad máxima cuando cambia la selección
            mostrarPrecioYPagos();
            mostrarCapacidadMaxima();
        });
>>>>>>> rama-fran
    }
});
