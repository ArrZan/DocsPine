// document.addEventListener("DOMContentLoaded", event => {
    
//     const wrapper = document.querySelector('.wrapper');
    
//     document.addEventListener('click', (e) => {
//         if (e.target.matches('#perfil') || e.target.matches('.wrapper')) {
//             wrapper.classList.toggle('show-wrapper');
//         }
        
//         // const ulidiomas = document.querySelector('.ul-idiomas'),
//         // btnIdioma = document.getElementById('idioma'); 
        
//         if (e.target.matches('.select-bt') || e.target.matches('.select-bt span') || e.target.matches('.select-bt i')) {
//             let btnSelect = e.target;
//             if(btnSelect.className.includes('select-bt')) {
//                 btnSelect = btnSelect.parentNode;
//                 console.log(btnSelect);
//             };
//             const ulSelect = btnSelect.nextElementSibling;
            
//             ulSelect.style.display = (ulSelect.style.display == 'none') ? 'block': 'none';
//             btnSelect.classList.toggle('rotated');  

//         } else {
//             if (document.querySelectorAll('.select-bt.rotated').length != 0) {

//                 const selectsActivos = document.querySelectorAll('.select-bt.rotated');
                
//                 selectsActivos.forEach((select) =>{
//                     select.classList.remove('rotated');
//                     select.nextElementSibling.style.display = 'none';
//                 })
    
    
//             }
//         }
        
        
//     })
//   });
  