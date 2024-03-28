// SideBar
let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');

btn.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});
// Buscador Selector Hab, Cant Adultos y Niños
let btn_sec = document.querySelector('.btn-sec');
let contenido = document.querySelector('.box-btn-sec');

btn_sec.addEventListener('click', function() {
    event.stopPropagation();
    contenido.classList.toggle('active');
});

let btn_minus = document.querySelector('#btn-minus');
let btn_plus = document.querySelector('#btn-plus');
let contador_adultos = document.querySelector('.contador-adultos');
let contador = 0;

// Detectar clics fuera del botón
window.addEventListener('click', function(event) {
    // Verificar si el clic no se realizó dentro del contenedor del botón o su contenido
    if (!btn_sec.contains(event.target)) {
        // Ocultar el contenido aquí
        contenido.classList.remove('active');
    }
});

btn_minus.addEventListener('click', function() {
    if(contador > 0){
        contador--;
        contador_adultos.textContent = contador;
        btn_sec.textContent = contador;

    }
});

btn_plus.addEventListener('click', function() {
    contador++;
    contador_adultos.textContent = contador;
    btn_sec.textContent = contador;
});