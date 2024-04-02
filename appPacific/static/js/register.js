function showHiddenElement(elementId, input) {
    let hiddenElement = document.getElementById(elementId);
    hiddenElement.style.display = "block";

    document.addEventListener("click", function(event) {
        let inputElement = document.getElementById(input);
        if (event.target !== inputElement && event.target !== hiddenElement) {
            hiddenElement.style.display = "none";
        }
    });
}

showHiddenElement('nameHidden','nombre');
showHiddenElement('apellidoHidden','apellidos');
showHiddenElement('usuarioHidden','username');
showHiddenElement('correoHidden','correo');
showHiddenElement('celularHidden','celular');
showHiddenElement('pass1Hidden','password1');
showHiddenElement('pass2Hidden','password2');


function hideAllHiddenElements() {
    let hiddenElements = document.querySelectorAll("[id$='Hidden']"); // Select all elements ending with "Hidden"
    hiddenElements.forEach(function(element) {
        element.style.display = "none";
    });
}

// Event listener for form submission
document.addEventListener("DOMContentLoaded", function() {
    let form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Hide all hidden elements
        hideAllHiddenElements();

        // Submit the form
        form.submit();
    });
});