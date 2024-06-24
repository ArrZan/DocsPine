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

document.addEventListener('DOMContentLoaded', function() {
    // --------------------------------------------------------------------------------------------- Abrir Wrapper
    const wrapper = document.querySelector('.wrapper');
    const perfil = document.getElementById('perfil');
    const v_Show = 'show-wrapper';
    
    document.addEventListener('click', e => {
        // --------------------------------------------------------------------------------------------- Cerrar Wrapper
        if (perfil && e.target == perfil) {
            wrapper.classList.toggle(v_Show);
        };
        
        // --------------------------------------------------------------------------------------------- Cerrar Wrapper
        if (wrapper && !wrapper.contains(e.target) && e.target !== perfil) {
            wrapper.classList.remove(v_Show);
        };


        // --------------------------------------------------------------------------------------------- Select Genérico
        const v_btnSe = '.select-btn'; // Botón del select o select mismo
        let classbtn = 'rotated';
    
        if (e.target.matches(v_btnSe) || e.target.matches(`${v_btnSe} span`) || e.target.matches(`${v_btnSe} i`)) {
            
            let btnSelect = e.target;
            if(!btnSelect.className.includes(v_btnSe)) {
                btnSelect = btnSelect.parentNode; // Tomamos al padre 
            };

            if(btnSelect.className == 'select-box') {
                btnSelect = btnSelect.children[0]; // Tomamos al options
            };
            
            const ulSelect = btnSelect.nextElementSibling;
            ulSelect.style.display = (ulSelect.style.display == 'none') ? 'block': 'none';
            btnSelect.classList.toggle(classbtn);
    
        } else {
            
            // Preguntamos si existe al menos 1 elemento con la clase select-btn.rotated,
            // Es decir, si hay un select activo
            if (document.querySelectorAll(`${v_btnSe}.${classbtn}`).length != 0) {
                
                // Ocultamos los select que estén activos
                const selectsActivos = document.querySelectorAll(`${v_btnSe}.${classbtn}`);
                
                selectsActivos.forEach((select) =>{
                    select.classList.remove(`${classbtn}`);
                    select.nextElementSibling.style.display = 'none';
                })

                // Si estamos seleccionando alguna opción, lo mandamos al span del select-btn
                
                if (e.target.className == 'option') {
                    e.target.classList.add('selected');
                    let btnSelect = e.target.parentNode.parentNode;
                    let optionSelected = e.target.textContent;
                    
                    console.log(e.target);
                    console.log(e.target.textContent);
                    console.log(btnSelect);

                    btnSelect.querySelector('.select-btn span') = optionSelected; 
                }

            }
        };
    });


    
})