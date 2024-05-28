// --------------------------------------------------------------------------------------------- MODAL GENÉRICO
{/* <div class="modal-back">
<div class="modal-response">
    <div class="modal-header">
        <p>Esto es el título</p>
        <i class='bx bx-x'></i>
    </div>
    <div class="modal-body">
        <div class="icon"><i class=''></i></div>
        <p class="text">Esto es el párrafo</p>
    </div>
    <div class="modal-footer">
    </div>
</div>
</div> */}
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

document.addEventListener('click', (e) => {
// --------------------------------------------------------------------------------------------- Wrapper de INCIO
    const wrapper = document.querySelector('.wrapper');
    const v_Show = 'show-wrapper';
    
if (e.target.matches('#perfil') || e.target.matches('.wrapper')) {
    wrapper.classList.toggle(v_Show);
} 
// else {
//     if (wrapper && wrapper.className.includes(v_Show)) {
//         wrapper.classList.remove(v_Show);
//     }
// };

// --------------------------------------------------------------------------------------------- Select Genérico
const v_btnSe = '.select-bt'; // Botón del select o select mismo
let classbtn = 'rotated';
if (e.target.matches(v_btnSe) || e.target.matches(`${v_btnSe} span`) || e.target.matches(`${v_btnSe} i`)) {
    let btnSelect = e.target;
    if(!btnSelect.className.includes('select-bt')) {
            btnSelect = btnSelect.parentNode;
        };
        const ulSelect = btnSelect.nextElementSibling;
        
        ulSelect.style.display = (ulSelect.style.display == 'none') ? 'block': 'none';
        btnSelect.classList.toggle(classbtn);  

} else {
    if (document.querySelectorAll(`${v_btnSe}.${classbtn}`).length != 0) {

        const selectsActivos = document.querySelectorAll(`${v_btnSe}.${classbtn}`);
        
        selectsActivos.forEach((select) =>{
            select.classList.remove(`${classbtn}`);
            select.nextElementSibling.style.display = 'none';
        })


    }
}

    
})