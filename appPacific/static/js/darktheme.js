// const swith = document.querySelector(".switch");

// document.addEventListener("DOMContentLoaded", e => {
//     // con esta funcion se compueba si ya hay algo guardado
//     cargarDarkModeDesdeLocalStorage()
//     swith.addEventListener("click", toggleDarkMode);
// })

// function toggleDarkMode() {
//     swith.classList.toggle("active");
//     document.body.classList.toggle("active");
//     //console.log(swith.classList.contains("active")) -> true or false
//     guardarDarkModeEnLocalStorage(swith.classList.contains("active"));
// }

// // verificar que el estado true o false, 
// // donde localstore permite guardar información

// function guardarDarkModeEnLocalStorage(estado){
//     localStorage.setItem("darkMode", estado)
// }

// // obtener el valor de local storage para conservar los cambios de la web

// function cargarDarkModeDesdeLocalStorage(){
//     // para evitar el valor de null hay que identificarlo con un true:
//     const darkModeGuardado = localStorage.getItem("darkMode") === "true"
//     if(darkModeGuardado){
//         swith.classList.add("active");
//         document.body.classList.add("active"); 
//     }
// }

const switchButton = document.querySelector(".switch");

document.addEventListener("DOMContentLoaded", () => {
    // Check if dark mode is saved in local storage
    cargarDarkModeDesdeLocalStorage();
    switchButton.addEventListener("click", toggleDarkMode);
});

function toggleDarkMode() {
    const isDarkMode = !switchButton.classList.contains("active");
    switchButton.classList.toggle("active");
    document.body.classList.toggle("active");

    // Add transition class to body for smooth transition
    document.body.classList.add("mode-transition");

    // Save dark mode state to local storage
    guardarDarkModeEnLocalStorage(isDarkMode);

    // Remove the transition class after a short delay
    setTimeout(() => {
        document.body.classList.remove("mode-transition");
    }, 300); // Adjust the duration to match your CSS transition duration
}

function guardarDarkModeEnLocalStorage(estado) {
    localStorage.setItem("darkMode", estado);
}

function cargarDarkModeDesdeLocalStorage() {
    // Check local storage for dark mode state
    const darkModeGuardado = localStorage.getItem("darkMode") === "true";
    if (darkModeGuardado) {
        // Apply dark mode styles if it's enabled
        switchButton.classList.add("active");
        document.body.classList.add("active");
    }
}







