// Botones Filtrar (Suite, Premium, Twin)
document.querySelectorAll('.btn-filtrar').forEach(btn => {
    btn.addEventListener('click', function() {
        const idTipoHab = this.getAttribute('data-id-tipo-hab');

        // Ocultar todas las habitaciones
        document.querySelectorAll('.habitacion').forEach(hab => {
            hab.style.display = 'none';
        });

        // Mostrar solo las habitaciones del tipo seleccionado
        document.querySelectorAll('.tipo-' + idTipoHab).forEach(hab => {
            hab.style.display = 'block';
        });
    });
});

// Contenedor Botón Filtrar
var btnFiltro = document.getElementById('filtro');
var contenedorFiltro = document.querySelector('.filtro-op');
btnFiltro.addEventListener('click', function() {
    contenedorFiltro.classList.toggle('active');
    
})

// Detectar clics fuera del botón
window.addEventListener('click', function(event) {
    // Verificar si el clic no se realizó dentro del contenedor del botón o su contenido
    if (!btnFiltro.contains(event.target)) {
        // Ocultar el contenido aquí
        contenedorFiltro.classList.remove('active');
    } else{
        contenedorFiltro.classList.add('active');
    }
});
