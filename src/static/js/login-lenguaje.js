
const langEl = document.querySelector('.lenguajeS');
const select = document.getElementById('langselect');
const titleEl = document.querySelector('.web');
const descrEl = document.querySelector('.info');
const loginEl = document.querySelector('.login');
const registerEl = document.querySelector('.register');
const log1El = document.querySelector('.log1');
const log2El = document.querySelector('.log2');
const usernameInput = document.getElementById('usernameImput');
const passInput = document.getElementById('passwordImput1');
const reg0El = document.querySelector('.reg0');
const usernameInput1 = document.getElementById('usernameImput1');
const passInput1 = document.getElementById('password1Imput');
const usernameInput2 = document.getElementById('fullnameImput');
const mailad = document.getElementById('emailInput');
const passcInput1 = document.getElementById('password2Imput');
const imgsEl = document.querySelector('.imgs');
const reg1El = document.querySelector('.reg1');
const message1 = document.getElementById('message1');
const message2 = document.getElementById('message2');
const message3 = document.getElementById('message3');
const message4 = document.getElementById('message4');

if (select) {

    select.addEventListener('change', () => {
        const selectedLanguage = select.value;
        changeLanguage(selectedLanguage);
    });


    function changeLanguage(language) {
        titleEl.textContent = data[language].title;
        descrEl.textContent = data[language].description;
        titleEl.textContent = data[language].web;
        descrEl.textContent = data[language].info;
        loginEl.textContent = data[language].login;
        registerEl.textContent = data[language].register;
        log1El.textContent = data[language].log1;
        log2El.textContent = data[language].log2;
        usernameInput.placeholder = data[language].username;
        passInput.placeholder = data[language].password;
        reg0El.textContent = data[language].reg0;
        usernameInput1.placeholder = data[language].username;
        passInput1.placeholder = data[language].password;
        usernameInput2.placeholder = data[language].username1;
        mailad.placeholder = data[language].emailInput;
        passcInput1.placeholder = data[language].passwordc;
        imgsEl.textContent = data[language].imgs;
        reg1El.textContent = data[language].reg1;
        message1.textContent = data[language].messages[0];
        message2.textContent = data[language].messages[1];
        message3.textContent = data[language].messages[2];
        message4.textContent = data[language].messages[3];

    }

    var data = {
        "español": {
            "web": "Nuestro sitio web",
            "info": "Información",
            "login": "Iniciar Sesión",
            "register": "Registrate",
            "log1":"¡Inicia sesión ya!",
            "log2":"Ingresar",
            "username": "Usuario",
            "password": "Contraseña",
            "reg0": "¡Regístrate ahora!",
            "username1": "Nombre y Apellido",
            "emailInput": "Correo electrónico",
            "passwordc": "Confirmar contraseña",
            "imgs": "Selecciona una imagen",
            "reg1":"Registrate",
            "messages": [
                "Dato no obligatorio.",
                "message3.textContent = data[language].messages[2];",
                "Tamaño máximo de 2MB.",
                "Tipo de imagen permitido JPEG, JPG, PNG."
            ],
        },
        "english": {
            "web": "Our website",
            "info": "Information",
            "login": "Log in",
            "register": "Sign up",
            "log1": "¡Sign in now!",
            "log2":"Enter",
            "username": "Username",
            "password": "Password",
            "reg0": "¡Register now!",
            "username1": "First and Last Name",
            "emailInput": "E-mail address",
            "passwordc": "Confirm password",
            "imgs": "Select image",
            "reg1":"Register",
            "messages": [
                "Not a required field.",
                "We recommend the photo to be square (e.g., 256x256px).",
                "Maximum size of 2MB.",
                "Allowed image types JPEG, JPG, PNG."
            ],
        },
        "frances": {
            "web": "Notre site web",
            "info": "Information",
            "login": "Connexion",
            "register": "Inscrivez-vous",
            "log1": "Connectez-vous maintenant!",
            "log2": "Entrer",
            "username": "Utilisateur",
            "password": "Mot de passe",
            "reg0": "¡Inscrivez-vous maintenant!",
            "username1": "Nom et prénom",
            "emailInput": "Adresse électronique",
            "passwordc": "Confirmer le mot de passe",
            "imgs": "Sélectionnez une image",
            "reg1": "Inscrivez-vous",
            "messages": [
                "Donnée non obligatoire.",
                "Nous recommandons que la photo soit carrée (ex: 256x256px).",
                "Taille maximale de 2MB.",
                "Type d'image autorisé JPEG, JPG, PNG."
            ]
        },
        "italiano": {
            "web": "Il nostro sito web",
            "info": "Informazione",
            "login": "Accedi",
            "register": "Registrati",
            "log1": "Accedi ora!",
            "log2": "Entra",
            "username": "Utente",
            "password": "Password",
            "reg0": "¡Registrati ora!",
            "username1": "Nome e cognome",
            "emailInput": "Indirizzo email",
            "passwordc": "Conferma password",
            "imgs": "Seleziona un'immagine",
            "reg1": "Registrati",
            "messages": [
                "Dato non obbligatorio.",
                "Raccomandiamo che la foto sia quadrata (es: 256x256px).",
                "Dimensione massima di 2MB.",
                "Tipo di immagine consentito JPEG, JPG, PNG."
            ]
        },
        "portugues": {
            "web": "Nosso site",
            "info": "Informação",
            "login": "Entrar",
            "register": "Cadastre-se",
            "log1": "Entre agora!",
            "log2": "Entrar",
            "username": "Usuário",
            "password": "Senha",
            "reg0": "¡Cadastre-se agora!",
            "username1": "Nome e Sobrenome",
            "emailInput": "Endereço de email",
            "passwordc": "Confirmar senha",
            "imgs": "Selecione uma imagem",
            "reg1": "Cadastre-se",
            "messages": [
                "Dado não obrigatório.",
                "Recomendamos que a foto seja quadrada (ex: 256x256px).",
                "Tamanho máximo de 2MB.",
                "Tipo de imagem permitido JPEG, JPG, PNG."
            ]
        },
        "aleman": {
            "web": "Unsere Website",
            "info": "Information",
            "login": "Anmelden",
            "register": "Registrieren",
            "log1": "Melden Sie sich jetzt an!",
            "log2": "Einloggen",
            "username": "Benutzername",
            "password": "Passwort",
            "reg0": "Jetzt registrieren!",
            "username1": "Vor- und Nachname",
            "emailInput": "E-Mail-Adresse",
            "passwordc": "Passwort bestätigen",
            "imgs": "Wählen Sie ein Bild aus",
            "reg1": "Registrieren",
            "messages": [
                "Daten sind optional.",
                "Wir empfehlen, dass das Foto quadratisch ist (z.B. 256x256px).",
                "Maximale Dateigröße 2MB.",
                "Erlaubtes Bildformat: JPEG, JPG, PNG."
            ]
        },
        "polaco": {
        "web": "Nasza strona internetowa",
        "info": "Informacje",
        "login": "Zaloguj się",
        "register": "Zarejestruj się",
        "log1": "Zaloguj się teraz!",
        "log2": "Zaloguj",
        "username": "Nazwa użytkownika",
        "password": "Hasło",
        "reg0": "Zarejestruj się teraz!",
        "username1": "Imię i nazwisko",
        "emailInput": "Adres e-mail",
        "passwordc": "Potwierdź hasło",
        "imgs": "Wybierz obraz",
        "reg1": "Zarejestruj się",
        "messages": [
            "Dane nie są wymagane.",
            "Zalecamy, aby zdjęcie było kwadratowe (np. 256x256px).",
            "Maksymalny rozmiar pliku 2MB.",
            "Dozwolony format obrazu: JPEG, JPG, PNG."
        ]
        },
        "ruso": {
        "web": "Наш веб-сайт",
        "info": "Информация",
        "login": "Войти",
        "register": "Зарегистрироваться",
        "log1": "Войдите сейчас!",
        "log2": "Войти",
        "username": "Имя пользователя",
        "password": "Пароль",
        "reg0": "Зарегистрируйтесь сейчас!",
        "username1": "Имя и фамилия",
        "emailInput": "Электронная почта",
        "passwordc": "Подтвердите пароль",
        "imgs": "Выберите изображение",
        "reg1": "Зарегистрироваться",
        "messages": [
            "Данные не обязательны.",
            "Рекомендуем, чтобы фотография была квадратной (например, 256x256px).",
            "Максимальный размер файла 2MB.",
            "Разрешённые форматы изображений: JPEG, JPG, PNG."
        ]
    }
    }



    }
    document.addEventListener('DOMContentLoaded', () => {
        updateSelectedLanguage(); // Initial update in case there's a default selected option
    });

    function updateSelectedLanguage() {
        if (document.getElementById('langselect')) {
            const selectElement = document.getElementById('langselect');
            const selectedOption = selectElement.options[selectElement.selectedIndex];

            // Display only the initials for the selected option
            const initials = selectedOption.value.toUpperCase().substring(0, 3);
            selectedOption.textContent = initials;
        }
    }

    function showFullNames() {
        const selectElement = document.getElementById('langselect');
        for (let i = 0; i < selectElement.options.length; i++) {
            const option = selectElement.options[i];
            option.textContent = option.getAttribute('data-fullname');
        }
    }




