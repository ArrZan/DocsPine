let idleTime = 0;

const [hours, minutes, seconds] = sessionTime.split(':').map(Number);

// Convertir horas, minutos y segundos a milisegundos
const totalMilliseconds = (hours * 60 * 60 + minutes * 60 + seconds) * 1000;

const maxIdleTime = totalMilliseconds; // El tiempo proviene del config, editar allá

function resetIdleTimer() {
    idleTime = 0;
}

function checkIdleTime() {
    idleTime += 1000; // Incrementa el tiempo de inactividad en 1 segundo
    if (idleTime >= maxIdleTime) {
        fetch('/logout', {
            method: 'GET'
        }).then(() => {
            window.location.href = '/login'; // Redirige a la página de inicio de sesión después de cerrar sesión
        });
    }
}

window.onload = function() {
    setInterval(checkIdleTime, 1000); // Revisa el tiempo de inactividad cada segundo

    // Resetea el temporizador de inactividad al realizar cualquier evento
    window.onmousemove = resetIdleTimer;
    window.onkeypress = resetIdleTimer;
    window.onclick = resetIdleTimer;
    window.onscroll = resetIdleTimer;
}

// document.addEventListener('DOMContentLoaded', function() {
//     const selectBtn = document.getElementById('selectBtn');
//     const optionsList = document.getElementById('optionsList');
//     const selectedValue = document.querySelector('.selected-value');

//     selectBtn.addEventListener('click', function() {
//         optionsList.classList.toggle('show-options');
//     });

//     optionsList.addEventListener('click', function(event) {
//         const lang = event.target.dataset.lang;
//         if (lang) {
//             selectedValue.textContent = event.target.textContent;
//             optionsList.classList.remove('show-options');
//             window.location.href = `/login?lang=${lang}`;
//         }
//     });

//     document.addEventListener('click', function(event) {
//         if (!optionsList.contains(event.target) && event.target !== selectBtn) {
//             optionsList.classList.remove('show-options');
//         }
//     });
// });