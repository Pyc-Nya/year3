import { listenLangChange } from './changeLange.js';
import { makeFetch } from './myfetch.js';
document.addEventListener('DOMContentLoaded', () => {
    listenLangChange();
    const userName = document.getElementById("username");
    const password = document.getElementById("password");
    const sendButton = document.querySelector('.send-button');
    const handleEnterDown = (e) => {
        if (e.key === "Enter") {
            handleClick();
        }
    };
    const handleChange = () => {
        userName.classList.remove("invalid");
        password.classList.remove("invalid");
        if (userName.value === "" || password.value === "") {
            sendButton.classList.add("inactive");
        }
        else {
            sendButton.classList.remove("inactive");
        }
    };
    const handleClick = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const currentLang = urlParams.get('lang') || 'ru';
        if (userName.value !== "" && password.value !== "") {
            makeFetch("/auth", {
                method: "POST",
                body: JSON.stringify({
                    username: userName.value,
                    password: password.value
                })
            }, () => {
                window.location.href = `/profile?lang=${currentLang}`;
            }, () => {
                userName.classList.add("invalid");
                password.classList.add("invalid");
            });
        }
    };
    sendButton.addEventListener('click', handleClick);
    userName.addEventListener('keydown', handleEnterDown);
    password.addEventListener('keydown', handleEnterDown);
    userName.addEventListener('input', handleChange);
    password.addEventListener('input', handleChange);
});
