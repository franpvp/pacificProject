
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


btn_adultos.addEventListener('click', function() {
    // event.stopPropagation();
    box_adultos.classList.toggle('active');
});

btn_ninos.addEventListener('click', function() {
    // event.stopPropagation();
    box_ninos.classList.toggle('active');
});

let btn_minus_adultos = document.querySelector('#btn-minus-adultos');
let btn_plus_adultos = document.querySelector('#btn-plus-adultos');
let btn_minus_ninos = document.querySelector('#btn-minus-ninos');
let btn_plus_ninos = document.querySelector('#btn-plus-ninos');


let contador_adultos = document.querySelector('.contador-adultos');
let contador_ninos = document.querySelector('.contador-ninos');
let contador_1 = 0;
let contador_2 = 0;

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
});
// Contador Adultos
btn_minus_adultos.addEventListener('click', function() {
    if(contador_1 > 0){
        contador_1--;
        contador_adultos.textContent = contador_1;
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
    if(contador_2 != 1){
        btn_ninos.textContent = "Niños: " + contador_2;
    } else{
        btn_ninos.textContent = "Niño: " + contador_2;
    }
    
});