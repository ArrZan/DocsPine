document.addEventListener('DOMContentLoaded', function() {
    const socket = io();

    const comentarioForm = document.querySelector('.agregar_comentario');
    const redactar_comentario = document.querySelector('.redactar_comentario');

    if (comentarioForm) {

        redactar_comentario.addEventListener('keydown', e => {
            if (e.key == 'Enter') {
                document.querySelector('.enviar_comentario').click();
            };
        });

        comentarioForm.addEventListener('submit', function(event) {
            event.preventDefault();
    
            const formData = new FormData(comentarioForm);
    
            if (formData.get('redactar_comentario')) {
                const url = comentarioForm.action;
    
                formData.get('csrf_token');
    
                fetch(url, {
                    method: 'POST',
                    body: formData,
                })
                .then(response => {
                    if (!response.ok) {
                        alert('Error al enviar el comentario');
                        throw new Error('Error al enviar el comentario');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
    
                        socket.emit('new_comment', data);
                    }
                })
                .catch(error => {
                    console.error('Error al enviar el comentario:', error);
                    // Aquí puedes mostrar un mensaje de error al usuario si lo deseas
                });
            } else {
                alert('Ingrese un comentario!')
            }
        });
    
    
        // -------------------------------------------------------Función para comunicación bidirecciona
        // Escuchar el evento 'nuevo_comentario' del handle del servidor
        socket.on('new_comment', function(data) {
            generateComment(data);
        });
    
    
        function generateComment(data) {
            const comentarioForm = document.querySelector('.agregar_comentario');
            const idUser = comentarioForm.dataset.userId;
            
            
            const comentario = data.new_comment;
            
            let newComment = ''
    
            if (idUser == data.id_issuer) {
                newComment = `
                    <div class="row">
                        <div class="modal_coment col">
                            <div class="row">
                                <div class="col"><b>${comentario.NombreUsuario}</b></div>
                                <div class="col" style="text-align: end; font-size: 13px;"><b>${comentario.fecha}</b></div>
                            </div>
                            <p>${comentario.comentario}</p>
                        </div>
                        <div style="margin-left: 20px;" class="col-2"><img class="foto_comentario centrar" src="static/${comentario.Foto}" alt="Foto"></div>
                    </div>
                `;
            } else {
                newComment = `
                    <div class="row">
                        <div class="col-2"><img class="foto_comentario centrar" src="static/${comentario.Foto}" alt="Foto"></div>
                        <div class="modal_coment col">
                            <div class="row">
                                <div class="col"><b>${comentario.NombreUsuario}</b></div>
                                <div class="col" style="text-align: end; font-size: 13px;"><b>${comentario.fecha}</b></div>
                            </div>
                            <p>${comentario.comentario}</p>
                        </div>
                    </div>
                `;
    
            }
    
            const comentariosDiv = document.querySelector('.modal_apartado_coment');
            // Insertamos arriba de todos los comentarios
            comentariosDiv.insertAdjacentHTML('afterbegin', newComment);
    
            // Limpiar el campo de redactar comentario
            document.querySelector('.redactar_comentario').value = '';
    
            // Hacer scroll hacia arriba para mostrar el nuevo comentario
            scrollToTop(comentariosDiv);
        }
    
    
        function scrollToTop(element) {
            const startingY = element.scrollTop;
            const targetY = 0;
            const distance = targetY - startingY;
            const duration = 500; // Duración de la animación en milisegundos
            const startTime = performance.now();
    
            function easeInOutQuad(t, b, c, d) {
                t /= d / 2;
                if (t < 1) return c / 2 * t * t + b;
                t--;
                return -c / 2 * (t * (t - 2) - 1) + b;
            }
    
            function animateScroll(timestamp) {
                const currentTime = timestamp - startTime;
                element.scrollTop = easeInOutQuad(currentTime, startingY, distance, duration);
                if (currentTime < duration) {
                    requestAnimationFrame(animateScroll);
                } else {
                    element.scrollTop = targetY;
                }
            }
    
            requestAnimationFrame(animateScroll);
        }
        
    }

});
