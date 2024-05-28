/*
    AL MODAL SE LE PUEDE APLICAR LAS SIGUIENTES CLASES:

    modal-back: active
    Para presentar el modal.

    modal-response: exito || error
    -El "exito" es para un modal que tiene un icon con la etiqueta i y la clase
    "bx bx-check-circle" de check o visto, le da un estilo verde al modal
    para marcar como exitosa alguna acción, así con el error, tendrá un icon con 
    la etiqueta i con su clase "bx bx-x-circle" de x, esto 
    para denotar una acción errónea.

*/
const modalBack = document.querySelector('.modal-back');
const closeModal = modalBack.querySelector('.bx.bx-x');

closeModal.addEventListener('click', (e) =>{
    modalBack.classList.remove('active')
});
