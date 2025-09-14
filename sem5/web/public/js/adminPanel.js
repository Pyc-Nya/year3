import { listenLangChange } from './changeLange.js';
import { makeFetch } from './myfetch.js';
const handleClose = (button, userId, e) => {
    e.stopPropagation();
    makeFetch("/user", {
        method: "DELETE",
        body: JSON.stringify({
            id: userId,
        })
    }, () => {
        var _a;
        (_a = button.parentElement) === null || _a === void 0 ? void 0 : _a.remove();
    }, () => { });
};
const handleClick = (userId, modal, userName, userColor) => {
    makeFetch("/user/" + userId, {}, (d) => {
        userName.textContent = d.name;
        userColor.value = d.color;
        modal.style.display = "flex";
    }, () => {
    });
};
const useUsersListItem = (item, id) => {
    const modal = document.querySelector(".modal");
    if (!modal)
        return;
    const userName = document.getElementById("username");
    const userColor = modal.querySelector(".main-info__color");
    if (!userName || !userColor)
        return;
    userColor.disabled = true;
    item.addEventListener("click", () => handleClick(id, modal, userName, userColor));
};
const createUsersListItem = (userName, userColor, id) => {
    const item = document.createElement('div');
    item.classList.add("users-list__item");
    useUsersListItem(item, id);
    const name = document.createElement("div");
    name.classList.add("users-list__name");
    name.textContent = userName;
    const color = document.createElement("div");
    color.classList.add("users-list__color");
    color.style.backgroundColor = userColor;
    const closeButton = document.createElement("button");
    closeButton.classList.add("users-list__close");
    closeButton.textContent = "X";
    closeButton.addEventListener("click", (e) => {
        handleClose(closeButton, id, e);
    });
    item.appendChild(name);
    item.appendChild(color);
    item.appendChild(closeButton);
    return item;
};
const refresh = () => {
    makeFetch("/users", {}, (data) => {
        const usersList = document.querySelector(".users-list__list");
        if (!usersList)
            return;
        usersList.innerHTML = "";
        data.forEach(({ name, color, id }) => {
            const item = createUsersListItem(name, color, id);
            usersList.appendChild(item);
        });
    }, () => { });
};
document.addEventListener('DOMContentLoaded', () => {
    listenLangChange();
    refresh();
    const modal = document.querySelector(".modal");
    modal.style.display = "none";
    modal.addEventListener("mousedown", () => {
        modal.style.display = "none";
    });
    const modalContent = document.getElementById("modal-content");
    modalContent.addEventListener("mousedown", (e) => {
        e.stopPropagation();
    }, true);
    const refreshButton = document.querySelector(".users-list__refresh");
    refreshButton.addEventListener("click", refresh);
});
