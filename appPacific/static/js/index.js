
let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');

btn.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});