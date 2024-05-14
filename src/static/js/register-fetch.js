/* 
USERNAME1
Que el username1 tenga entre 3 y 12 caracteres (validado en la etiqueta mismo)
Puede contener mayus y minus, numeros y guiones bajos (_) pero no espacios u otros caracteres.

FULLNAME
Que tenga entre 3 y máx 25 caracteres 
Puede contener mayus y minus y espacios.

EMAIL
El type email ya valida el correo

PASSWORD'S
Deben coincidir :v
Al menos 4 caracteres y máx 16 (validado en la etiqueta mismo)
Puede contener cualquier tipo de caracter, incluyendo números y símbolos.

IMAGE
Validar el peso (si queremos) y el tipo de archivo.
*/
// Expresiones regulares para validar los input's
const expr = {
    username1: /^[a-zA-Z0-9\_]{3,12}$/, // Letras, numeros, guion y guion_bajo
	fullname: /^[a-zA-ZÀ-ÿ\s]{3,25}$/, // Letras y espacios, pueden llevar acentos.
	password: /^.{4,16}$/, // 4 a 16 digitos.
	email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/, // Por si el navegador no lo tiene
}

// Campos del form para darle un estado de válido (true) o inválido (false)
const fieldsForm = {
    'username1': false,
    'fullname': false,
    'password1': false,
    'password2': false,
    'email': false,
    'image': false
}

// Obtenemos el formulario de registro y sus input's
const formRegister = document.getElementById('body-register');
const inputs = document.querySelectorAll('#body-register input');

//----------------------------------------------------------------------------------------- VALIDACIONES DEL FORMULARIO

function isPassword(key) {
    return (key == 'password1') ? 'password': key;
}

/* Función para verificar el input a través de expresiones regulares
con test y le damos una clase exito o error al control-form */
function check_input(key, dato, padre) {
    let logos = padre.querySelectorAll('.control-form i');

    let keyRe = isPassword(key);
    
    if(expr[keyRe].test(dato)){
        // Muestro el icono preedeterminado del label
        logos[0].style.display = 'block';
        logos[1].style.display = 'none';

        // Doy la clase de exito y quito la de error
        padre.classList.add('exito');
        padre.classList.remove('error');

        // Guardo como validado este dato
        fieldsForm[key] = true;
    } else {
        // Oculto el icono predeterminado del label y presento el de error
        logos[0].style.display = 'none';
        logos[1].style.display = 'block';
        
        // Doy la clase de error y quito la de exito
        padre.classList.add('error');
        padre.classList.remove('exito');

        // Guardo como invalido este dato
        fieldsForm[key] = false;
    };
}

/* Función para verificar que las contraseñas coincidan*/
function check_pass2() {
    const password1 = document.getElementById('password1Imput'),
        password2 = document.getElementById('password2Imput'),
        padre = password2.parentNode;

    if(password1.value !== password2.value || password1.value == "") {
        padre.classList.add('error');
        padre.classList.remove('exito');

        // Guardo como inválido este dato
        fieldsForm['password2'] = false;
    } else {
        padre.classList.remove('error');
        padre.classList.add('exito');
        
        // Guardo como válido este dato
        fieldsForm['password2'] = true;
    };
}

/* Función para validar los inputs del formulario,
tomamos el valor afectado por el keyUp o el blur
y se lo cedemos acá para tomar su value que sería el dato,
el hijo que no es más que el mismo e.target y el padre del hijo
que es su contenedor, osea el control-form que lo contiene,
mandamos la expresión, el dato y el padre dependiendo del name del hijo */
const validForm = (e) => {
    let dato = e.target.value,
        hijo = e.target,
        padre = hijo.parentNode;

    // Si no es password el name, entonces se checkea los otros input's, image se valida por separado a esto
    if(hijo.name=='password1' || hijo.name=='password2') {
        check_input('password1', dato, padre);
        check_pass2(dato, padre);
    } else {
        check_input(hijo.name, dato, padre);
    }
}

/* Hacemos un forEach para controlar cada input
por medio de los eventos keyUp (tecla presionada) y
el blur (quitar focus del input) para que cada tecla que presione o
cada que el usuario haga clic afuera del input,
este se valide en el validForm  */
inputs.forEach((input) => {
    input.addEventListener('keyup', validForm);
    input.addEventListener('blur', validForm);
});

/* Al momento de subir una imagen se llevará a cabo el proceso
de validar el tipo y peso de la imagen seleccionada que es 2MB
y permite solo tipos JPEG, JPG y PNG.  */
inputs[6].addEventListener('change', e =>{
    console.log('Entra al evento change del image');
    let file = extractDataImageInput(e.target);

    if(file.image) {
        if (validImage(file.image)) {
            addImage(file);
        } else {
            trashImage(file);
        };
    } else {
        trashImage(file);
    }
});

//-------------------------------------------------------------------------------------- SUBIDA Y ELIMINACIÓN DE IMAGEN
// Al hacer click para subir una imagen, controlaremos si llega a subir o no una imagen
inputs[6].nextElementSibling.addEventListener('click', e => {
    let labelImage = e.target;
    let inputimage = inputs[6];

    if (labelImage.tagName != "BUTTON" && labelImage.tagName != "I"){
        if(!fieldsForm.image && inputimage.files.length == 1) {

            let file = extractDataImageInput(inputimage);
            if (validImage(file.image)) {addImage(file);}

        }
    }
})

// Mandamos el file para extraer datos de su archivo y padre contenedor
function extractDataImageInput(imageInput) {
    return {
        'image' : imageInput.files[0],
        'padre' : imageInput.parentNode
    }
};

// Lógica para validar los parámetros para la imagen
function validImage(imgFile) {
    const allowedType = ['image/jpeg', 'image/png', 'image/jpg'], // tipos de imagen permitidos
    sizeMax = 2 * 1024 * 1024; // 2MB en bytes máximos

    // Validamos peso de imagen
    if(imgFile.size > sizeMax) {
        return false
    }
    
    // Validamos tipo de imagen
    if(!allowedType.includes(imgFile.type)) {
        return false            
    }

    return true 
}

// Añadir presentación de selección de imagen en input estilizado
function addImage(DictFile) {
    let nameImage = DictFile.image.name,
    etiquetaStrong = DictFile.padre.querySelector('strong'),
    etiquetaName = DictFile.padre.querySelector('p'),
    buttonTrash = DictFile.padre.querySelector('.btn-trash');

    sizeFile = (DictFile.image.size/1024/1024).toFixed(2);

    /* Activamos botón para eliminar imagen,
    Ocultamos la etiqueta de presentación,
    Mostramos el peso y nombre de la imagen seleccionada
    y colocamos true en el image fieldsForm para indicar que hay imagen
    */
    buttonTrash.classList.add('active');
    etiquetaStrong.style.display='none';
    etiquetaName.textContent = `${sizeFile}MB / ${nameImage}`;

    fieldsForm.image = true;
}

// Función onclick para borrar la imagen
function trashImage(DictFile=extractDataImageInput(inputs[6])) {

    DictFile.padre.querySelector('.btn-trash').classList.remove('active');
    DictFile.padre.querySelector('strong').style.display='block';
    DictFile.padre.querySelector('p').textContent = "";
    
    fieldsForm.image = false;
}

//---------------------------------------------------------------------------------------- BOTÓN CLOSE MESSAGE DEL FORM
function closeMessage(form) {
    document.getElementById(`messages${form}`).classList.remove('show');
}


//-------------------------------------------------------------------------------------- ENVÍO DEL FORMULARIO POR FETCH
formRegister.addEventListener('submit', evt => {
    /* Debemos preguntar si todos los campos están válidos */
    evt.preventDefault();
    /*  Valores correspondientes a los inputs del formRegister
        0: token
        1: username1
        2: fullname
        3: email
        4: password1
        5: password2
        6: image
    */

    // Confirmamos que los campos hayan sido validados accediendo a sus estados
    if(fieldsForm.username1 && fieldsForm.fullname && fieldsForm.email && fieldsForm.password2 && fieldsForm.password1) {
        
        const formData = new FormData();

        let url_save = "/register"
        let csrf = document.querySelector('[name=csrf_token2]').value;
        
        formData.append('idioma', idioma); // Variable global (de idioma.js) momentánea hasta ver como aplicamos
        formData.append('username1', inputs[1].value);
        formData.append('fullname', inputs[2].value);
        formData.append('email', inputs[3].value);
        formData.append('password', inputs[5].value);

        // Confirmamos si el usuario puso o no una imagen
        if(fieldsForm.image) {
            formData.append('image', inputs[6].files[0]);
        }

        fetch(url_save,
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf,
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.error_message) {
                    ct_message = document.getElementById('messagesReg');
                    ct_message.querySelector('p').textContent = data.error_message;
                    ct_message.classList.add('show');
                } else {
                    const modalBack = document.querySelector('.modal-back'),
                    modalResponse = modalBack.querySelector('.modal-response'),
                    closeModal = modalBack.querySelector('.bx.bx-x');

                    const title = modalBack.querySelector('.modal-header p'),
                    icon = modalBack.querySelector('.modal-body i'),
                    parrafo = modalBack.querySelector('.modal-body p');
                    
                    closeModal.style.display = 'none'
                    modalResponse.classList.add('exito');
                    icon.classList.add('bx','bx-check-circle');
                    
                    title.textContent = 'Registro exitoso';
                    parrafo.textContent = data.message;

                    modalBack.classList.add('active');
                    console.log(data.redirectUrl);
                    
                    setTimeout(()=> {
                        urlActual = window.location.href;
                        // Separamos para obtener el url básico de la página y reemplazarlo por el que nos envía el backend
                        urlLi = urlActual.split('/');

                        window.location.href = urlActual.replace(urlLi[urlLi.length - 1], data.redirectUrl);
                    },3000);
                }
                
                // if (data.message === 'Recompensa reclamada exitosamente.') {
                //     alert(data.message, 'success', recompensaId);
                //     button.classList.add('inactivo');
                // }
            })
            .catch(error =>{
                console.log('-------------- SALIDA POR CATCH --------------');
                console.log('Error: ', error);
            });
    } else {
        // Iteramos los campos inválidos para denotarle al usuario que faltan de llenar o están incorrectos
        for (const key in fieldsForm) {
            if(fieldsForm[key]==false && key != "image") {
                console.log(key);
                controlForm = document.querySelector(`[name=${key}]`).parentNode;
                controlForm.classList.add('error-flush');
                
                setTimeout(()=> {
                    controlForm.classList.remove('error-flush');
                },1100);
            }
        }
    }
})