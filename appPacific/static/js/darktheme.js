const swith = document.querySelector(".switch");

document.addEventListener("DOMContentLoaded", e => {
    // con esta funcion se compueba si ya hay algo guardado
    cargarDarkModeDesdeLocalStorage()
    swith.addEventListener("click", toggleDarkMode);
})

function toggleDarkMode() {
    swith.classList.toggle("active");
    document.body.classList.toggle("active");
    //console.log(swith.classList.contains("active")) -> true or false
    guardarDarkModeEnLocalStorage(swith.classList.contains("active"));
}

// verificar que el estado true o false, 
// donde localstore permite guardar información

function guardarDarkModeEnLocalStorage(estado){
    localStorage.setItem("darkMode", estado)
}

// obtener el valor de local storage para conservar los cambios de la web

function cargarDarkModeDesdeLocalStorage(){
    // para evitar el valor de null hay que identificarlo con un true:
    const darkModeGuardado = localStorage.getItem("darkMode") === "true"
    if(darkModeGuardado){
        swith.classList.add("active");
        document.body.classList.add("active"); 
    }
}









