document.addEventListener("DOMContentLoaded", event => {
    
    const wrapper = document.querySelector('.wrapper');
    
    document.addEventListener('click', (e) => {
        if (e.target.matches('#perfil') || e.target.matches('.wrapper')) {
            wrapper.classList.toggle('show-wrapper');
        }
        
        const ulidiomas = document.querySelector('.ul-idiomas'),
        btnIdioma = document.getElementById('idioma'); 
        
        if (e.target.matches('.bt-idioma')) {
            ulidiomas.style.display = (ulidiomas.style.display == 'none') ? 'block': 'none';
            btnIdioma.classList.toggle('rotated');  
        } else {
            ulidiomas.style.display = 'none';
            btnIdioma.classList.remove('rotated');
        }
        
        
    })
  });
  