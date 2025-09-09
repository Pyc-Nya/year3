export const listenExitClick = () => {
    const exitButton = document.getElementById("exit");
    exitButton.addEventListener("click", () => {
        const urlParams = new URLSearchParams(window.location.search);
        const currentLang = urlParams.get('lang') || 'ru';
        window.location.href = `/auth?lang=${currentLang}`;
    });
};
