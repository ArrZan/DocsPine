// Función para validar la extensión de un archivo de imagen
const validarExtImagen = (input) => {
    const archivoRuta = input.value;
    const extPermitidas = /(.png|.svg|.jpg|.jpeg)$/i; // extensiones permitidas
    // Verificar si la extensión está permitida
    if (!extPermitidas.test(archivoRuta)) {
        alert('Asegúrate de haber seleccionado una imagen con una extensión válida (png, svg, jpg, jpeg).');
        input.value = '';
        return false;
    }
    return true;
};

// Código para mostrar una imagen seleccionada en un elemento <img>
const file = document.getElementById('Imagen');
const img = document.getElementById('img');
file.addEventListener('change', e => {
    if (e.target.files[0]) {
        const reader = new FileReader(); // Crear un objeto FileReader para leer el contenido del archivo
        reader.onload = e => { //se ejecuta cuando la lectura es exitosa
            // Establecer el src del elemento <img> con la URL del archivo cargado
            img.src = e.target.result;
        };
        // Leer el contenido del archivo como una URL de datos
        reader.readAsDataURL(e.target.files[0]);
    }
});

// Evento que se ejecuta cuando la página se ha cargado completamente
window.addEventListener("load", () => {
    // Obtener el input de archivo
    const input = document.getElementById("file");
    // Obtener el contenedor de archivos
    const filewrapper = document.getElementById("filewrapper");
    let archivosSeleccionados = []; // Lista de archivos seleccionados
    let removedFiles = []; // Lista de archivos eliminados
    // Obtener archivos existentes en el contenedor
    const existingFiles = Array.from(document.querySelectorAll('.archivo-item'));

    // Mostrar archivos seleccionados cuando se selecciona uno nuevo
    input.addEventListener("change", (e) => {
        // Obtener los nuevos archivos seleccionados
        const newFiles = Array.from(e.target.files);
        // Agregar los nuevos archivos a la lista de seleccionados
        archivosSeleccionados = archivosSeleccionados.concat(newFiles);
        // Llamar a la función para mostrar los archivos
        mostrarArchivos();
    });

    // Función para mostrar archivos en el contenedor
    const mostrarArchivos = () => {
        // Limpiar el contenedor
        filewrapper.innerHTML = '';
        // Recorrer los archivos existentes en el contenedor
        existingFiles.forEach((fileElem, index) => {
            // Verificar si el archivo no ha sido eliminado
            if (!removedFiles.includes(index)) {
                // Mostrar archivos existentes en el contenedor
                filewrapper.appendChild(fileElem);
            }
        });
        // Recorrer los archivos seleccionados
        archivosSeleccionados.forEach((file, index) => {
            // Llamar a la función para mostrar cada archivo
            fileshow(file.name, file.name.split('.').pop(), index + existingFiles.length);
        });
    };

    // Función para mostrar un archivo en el contenedor
    const fileshow = (fileName, filetype, index) => {
        // Crear elementos HTML para mostrar la información del archivo
        const showfileboxElem = document.createElement("div");
        showfileboxElem.classList.add("showfilebox");
        showfileboxElem.dataset.index = index;
        const leftElem = document.createElement("div");
        leftElem.classList.add("left");
        const fileTypeElem = document.createElement("span");
        fileTypeElem.classList.add("filetype");
        fileTypeElem.innerHTML = filetype;
        leftElem.append(fileTypeElem);
        const filetitleElem = document.createElement("h3");
        filetitleElem.innerHTML = fileName;
        leftElem.append(filetitleElem);
        showfileboxElem.append(leftElem);
        const rightElem = document.createElement("div");
        rightElem.classList.add("right");
        showfileboxElem.append(rightElem);
        const crossElem = document.createElement("span");
        crossElem.innerHTML = "&#215;";
        rightElem.append(crossElem);
        filewrapper.append(showfileboxElem);

        // Manejar la eliminación de archivos
        crossElem.addEventListener("click", () => {
            // Quitar el archivo del contenedor
            filewrapper.removeChild(showfileboxElem);
            if (index < existingFiles.length) {
                // Agregar el archivo a la lista de eliminados si ya existe
                removedFiles.push(index);
            } else {
                // Quitar el archivo de la lista de seleccionados si es nuevo
                archivosSeleccionados = archivosSeleccionados.filter((_, i) => i !== (index - existingFiles.length));
            }
            // Actualizar la vista del contenedor
            mostrarArchivos();
        });
    };

    // Filtrar archivos eliminados antes de enviar el formulario
    const form = document.querySelector("form");
    form.addEventListener("submit", (e) => {
        // Crear un objeto DataTransfer para manejar los archivos
        const dataTransfer = new DataTransfer();
        archivosSeleccionados.forEach((file) => {
            dataTransfer.items.add(file);
        });
        // Asignar los archivos al input de archivo del formulario
        input.files = dataTransfer.files;
        // Crear un campo oculto que contenga la lista de archivos eliminados en formato JSON
        const removedInput = document.createElement("input");
        removedInput.type = "hidden";
        removedInput.name = "removedFiles";
        removedInput.value = JSON.stringify(removedFiles);
        // Agregar el campo oculto al formulario antes de enviarlo
        form.appendChild(removedInput);
    });

    // Manejar la eliminación de archivos existentes
    existingFiles.forEach((fileElem, index) => {
        const deleteBtn = fileElem.querySelector('.eliminar-archivo');
        deleteBtn.addEventListener('click', () => {
            // Quitar el archivo del contenedor
            filewrapper.removeChild(fileElem);
            // Agregar el archivo a la lista de eliminados
            removedFiles.push(index);
        });
    });
});
