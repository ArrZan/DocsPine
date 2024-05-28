
document.addEventListener("DOMContentLoaded", event => {
    
    const btnLogin = document.querySelector('#header-form .seven.columns'),
    btnRegister = document.querySelector('#header-form .five.columns'),
    formLogin = document.getElementById('body-login'),
    formRegister = document.getElementById('body-register');

    document.addEventListener('click', (e) => {
        if (e.target.matches('.btn-register')) {

            // Activamos el botón del register y desactivamos el del login
            btnLogin.classList.remove('header-active');
            btnRegister.classList.add('header-active');

            // Mostramos el body del register y ocultamos el del login
            formRegister.classList.add('active');
            formLogin.classList.remove('active');
        }
        
        if (e.target.matches('.btn-login')) {

            // Activamos el botón del login y desactivamos el del register
            btnLogin.classList.add('header-active');
            btnRegister.classList.remove('header-active');

            // Mostramos el body del login y ocultamos el del register
            formRegister.classList.remove('active');
            formLogin.classList.add('active');
        }
    })
  });
  