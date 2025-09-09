import { listenLangChange } from './changeLange.js';
import { makeFetch } from './myfetch.js';
document.addEventListener('DOMContentLoaded', () => {
    listenLangChange();
    const userName = document.getElementById("username");
    const sendButton = document.querySelector('.send-button');
    const colorInput = document.getElementById("color");
    const cookies = {};
    document.cookie.split(";").map(cookie => {
        const [name, value] = cookie.trim().split("=");
        if (typeof name !== "string")
            return;
        cookies[name] = decodeURIComponent(value);
    });
    userName.textContent = cookies["username"];
    colorInput.value = cookies["color"];
    const handleClick = () => {
        if (colorInput.value !== "") {
            makeFetch("/color", {
                method: "POST",
                body: JSON.stringify({
                    color: colorInput.value,
                })
            }, () => { }, () => { });
        }
    };
    sendButton.addEventListener('click', handleClick);
});
