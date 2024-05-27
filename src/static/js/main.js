document.querySelectorAll('.abrir_modal').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        const modalId = item.dataset.bsTarget; // Obtener el ID del modal desde el atributo data-bs-target
        const modal = document.querySelector(modalId);
        modal.classList.add('modal_show');
    });
});

document.querySelectorAll('.modal_cerrar').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        const modal = item.closest('.modal');
        modal.classList.remove('modal_show');
    });
});


// CALIFICAR
// Obtener todos los campos de radio
const radioButtons = document.querySelectorAll('input[type="radio"]');

// Agregar un evento onchange a cada campo de radio
radioButtons.forEach(radioButton => {
    radioButton.addEventListener('change', function () {
        // Obtener el valor seleccionado y el ID del proyecto
        const selectedValue = this.value;
        const proyectoID = this.getAttribute('name').replace('estrellas', ''); // Extraer el ID del proyecto del nombre del campo
        // Asignar el valor al campo oculto específico del proyecto
        document.getElementById('calificar_proyecto' + proyectoID).value = selectedValue;
        // Enviar automáticamente el formulario específico del proyecto
        document.getElementById('calificacion' + proyectoID).submit();
        alert('Gracias por tu calificación');
    });
});

