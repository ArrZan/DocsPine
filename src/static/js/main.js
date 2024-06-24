document.querySelectorAll('.delete-project').forEach(element => {
    element.addEventListener('click', event => {
        event.preventDefault();

        const modal = document.querySelector('.modal-back');
        const modalFooter = modal.querySelector('.modal-footer');
        const modalResponse = modal.querySelector('.modal-response');
        
        modalResponse.classList.add('error');
        modalResponse.querySelector('.modal-header p').textContent = 'Eliminar Proyecto';
        
        modalResponse.querySelector('.modal-body .icon i').classList.add('bx', 'bx-x-circle');
        modalResponse.querySelector('.modal-body .text').innerHTML = `Estás seguro de que deseas eliminar el proyecto: <strong>${element.dataset.project}</strong>?`;
        

        modal.classList.add('active');
        
        modalFooter.innerHTML = '';

        modalFooter.innerHTML = `
            <a class="cont-a" href="${element.href}">
                Eliminar
            </a>
        `;
        })
})


if (document.getElementById('crear-proyecto')){
    document.getElementById('crear-proyecto').addEventListener('click', event => {
        event.preventDefault();
        window.location.href = '/crear_proyectos';
    });
}


document.querySelectorAll('.cont-btn').forEach(item => {
    if (item.id != 'crear-proyecto') {

        item.addEventListener('click', event => {
            event.preventDefault();
            const url = item.dataset.action; // Obtenemos la dirección de la vista
            const csrfToken = document.querySelector('[name="csrf_token"]').value;
    
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => {
                if (!response.ok) {
                    alert('Error en la solicitud');
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    // console.log(data.error);
                    alert(data.error);
                } else {
                    present_data(data, item.dataset.projectId, item.dataset.userId, item.dataset.fecha);
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                // Aquí puedes mostrar un mensaje de error al usuario si lo deseas
            });
            
            
            
            // modal.classList.add('modal_show');
    
    
    
        });
    
    
        function present_data(data, idProject, idUserSession, date) {
            document.querySelector('body').style.overflow  = 'hidden';
            const modal = document.querySelector('#modalProyectos');
            const autorProyecto = document.getElementById(`autor${idProject}`).textContent;
            const nombreProyecto = document.getElementById(`nombre${idProject}`).textContent;
            const imagenProyecto = document.getElementById(`imagen${idProject}`).src;
    
            const proyecto = data.proyecto[0];
            const rating = data.rating[0];
    
            // Colocación de datos del html en el modal
            document.getElementById('modalFoto').src = imagenProyecto;
            document.querySelector('.modalTitle').textContent = nombreProyecto;
            document.querySelector('.modalDesc').textContent = proyecto.DescripcionProyecto;
            document.querySelector('.modalFecha').textContent = date;
            document.querySelector('.modalAutor').textContent = autorProyecto;
            
            pushRating(rating, idProject);
    
            pushFiles(proyecto.Archivos, autorProyecto, nombreProyecto);
    
            pushComments(data.comentarios, data.users, idProject, idUserSession);
    
            modal.scrollTop = 0;
    
            modal.classList.add('modal_show');
        }
    
    
        function convert_str_date(str_date) {
            const dateObj = new Date(str_date);
    
            // Extraemos los componentes de la fecha
            const year = dateObj.getUTCFullYear();
            const month = ('0' + (dateObj.getUTCMonth() + 1)).slice(-2); // +1 porque los meses son indexados desde 0
            const day = ('0' + dateObj.getUTCDate()).slice(-2);
            const hours = ('0' + dateObj.getUTCHours()).slice(-2);
            const minutes = ('0' + dateObj.getUTCMinutes()).slice(-2);
            const seconds = ('0' + dateObj.getUTCSeconds()).slice(-2);
    
            // Formateamos la fecha y hora en el formato deseado
            return `${year}-${month}-${day} / ${hours}:${minutes}:${seconds}`;
        }
    
    
        function pushRating(rating, idProject) {
            let ratingForm = document.getElementById('calificacion');
    
            let radiosInput = ratingForm.querySelectorAll('input[type="radio"]');
            
            radiosInput.forEach((radio) => {
                radio.name = `estrellas${idProject}`;
                radio.checked =  false; // Reseteamos todos los radio
            })
    
            if (rating) {            
                if (rating.Calificacion > 0) {
                    // Damos la url de recalificar al action del form
                    ratingForm.action = `/re_calificar/${idProject}/${rating.ID}`
    
                    // Le damos el checked al input dado al rating que tenía
                    ratingForm.querySelector(`input[value="${rating.Calificacion}"]`).checked = true;
                
                }
    
            } else {
                ratingForm.action =`/calificar/${idProject}`
            }
        }
    
    
        function pushFiles(files, autorProyecto, nombreProyecto) {
            files.forEach((file) => {
                let nameFile = file.split('_');
                nameFile = nameFile[nameFile.length - 1];
    
                let formatFile = nameFile.split('.');
                formatFile = formatFile[formatFile.length - 1];
    
                const fileBoxHTML = `
                        <a download href="/archivo/${autorProyecto}/${nombreProyecto}/${file}">
                            <div class="showfilebox" data-index="0">
                                <div class="left">
                                    <span class="filetype">${formatFile}</span>
                                    <h3>
                                        ${nameFile}
                                    </h3>
                                </div>
            
                                <div class="right download">
                                    <i class='bx bxs-download'></i>
                                </div>            
                            </div>
                        </a>
                    `
                
                const filesDiv = document.getElementById('filewrapper');
                
                filesDiv.insertAdjacentHTML('beforeend', fileBoxHTML);
    
            })
    
        }
    
    
        function pushComments(comentarios, users, idProject, idUserSession) {
            const comentarioForm = document.querySelector('.agregar_comentario');
            comentarioForm.action = `/comentar/${idProject}`;
            const comentariosDiv = document.querySelector('.modal_apartado_coment');
            // const idUser = comentarioForm.dataset.userId;
    
            comentariosDiv.innerHTML = ''; // Reseteo de lo que haya en comentarios
    
            comentarios.forEach( objeto => {
                const comment = objeto.Comentario;
                const date = convert_str_date(objeto.Fecha);
                const userComment =  users[objeto.IDUsuario];
    
                let newComment = '';
    
                if (objeto.IDUsuario == idUserSession) {
                    newComment = `
                        <div class="row">
                            <div class="modal_coment col">
                                <div class="row">
                                    <div class="col"><b>${userComment.name}</b></div>
                                    <div class="col" style="text-align: end; font-size: 13px;"><b>${date}</b></div>
                                </div>
                                <p>${comment}</p>
                            </div>
                            <div style="margin-left: 20px;" class="col-2"><img class="foto_comentario centrar" src="${userComment.photo}" alt="Foto"></div>
                        </div>
                    `;
                } else {
                    newComment = `
                        <div class="row">
                            <div class="col-2"><img class="foto_comentario centrar" src="${userComment.photo}" alt="Foto"></div>
                            <div class="modal_coment col">
                                <div class="row">
                                    <div class="col"><b>${userComment.name}</b></div>
                                    <div class="col" style="text-align: end; font-size: 13px;"><b>${date}</b></div>
                                </div>
                                <p>${comment}</p>
                            </div>
                        </div>
                    `;
    
                }
                // Insertamos al final de todos los comentarios
                comentariosDiv.insertAdjacentHTML('beforeend', newComment);
    
            });
    
            comentariosDiv.scrollTop = 0; // Dejamos el scroll al comienzo de los comentarios (top)
        };
    }
});

document.querySelectorAll('.modal_cerrar').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        const modal = item.closest('.modal');
        document.querySelector('body').style.overflow  = 'auto';
        document.getElementById('filewrapper').innerHTML = ''; // Reseteamos el contenedor de archivos
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
        document.getElementById('calificar_proyecto').value = selectedValue;
        // Enviar automáticamente el formulario específico del proyecto
        document.getElementById('calificacion').submit();
        alert('Gracias por tu calificación');
    });
});


