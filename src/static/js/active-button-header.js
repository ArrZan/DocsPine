const currentURL = window.location.href,
home = "List_Proyectos", mPro = "misProyectos";

const bt_proy = document.getElementById('bt-pro'),
    bt_mproy = document.getElementById('bt-mpro');

// Activamos el boton del header en cuyo caso esté en esa url
if (currentURL.includes(home)) {
    bt_proy.classList.add('active');
    
} else if (currentURL.includes(mPro)) {
    bt_mproy.classList.add('active');
}
