import { listenLangChange } from './changeLange.js';
import { listenExitClick } from './listenExitClick.js';
import { makeFetch } from './myfetch.js';

document.addEventListener('DOMContentLoaded', () => {
	listenLangChange();
	listenExitClick();

	const userName = document.getElementById("username") as HTMLInputElement;
	const sendButton = document.querySelector('.send-button') as HTMLButtonElement;
	const colorInput = document.getElementById("color") as HTMLInputElement;

	const cookies: any = {};
	document.cookie.split(";").map(cookie => {
		const [name, value] = cookie.trim().split("=");
		if (typeof name !== "string") return;
		cookies[name] = decodeURIComponent(value);
	})

	userName.textContent = cookies["username"];
	colorInput.value = cookies["color"];

	const handleClick = () => {
		if (colorInput.value !== "") {
			makeFetch(
				"/color",
				{
					method: "POST",
					body: JSON.stringify({
						color: colorInput.value,
						id: cookies["id"]
					})
				},
				() => {},
				() => {}
			)
		}
	}

	sendButton.addEventListener('click', handleClick);
});