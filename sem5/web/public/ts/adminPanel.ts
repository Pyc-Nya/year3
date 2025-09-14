import { listenLangChange } from './changeLange.js';
import { makeFetch } from './myfetch.js';

const handleClose = (button: HTMLButtonElement, userId: string, e: MouseEvent) => {
  e.stopPropagation();
  makeFetch(
    "/user",
    {
      method: "DELETE",
      body: JSON.stringify({
        id: userId,
      })
    },
    () => {
      button.parentElement?.remove();
    },
    () => {}
  )
}

const handleClick = (userId: string, modal: HTMLDivElement, userName: HTMLDivElement, userColor: HTMLInputElement) => {

  makeFetch(
    "/user/" + userId,
    {},
    (d: {name: string, color: string}) => {
      userName.textContent = d.name;
      userColor.value = d.color;
      modal.style.display = "flex";
    },
    () => {
    }
  )
}

const useUsersListItem = (item: HTMLDivElement, id: string) => {
  const modal = document.querySelector(".modal") as HTMLDivElement;
  if (!modal) return;

  const userName = document.getElementById("username") as HTMLDivElement;
  const userColor = modal.querySelector(".main-info__color") as HTMLInputElement;

  if (!userName || !userColor) return;

  userColor.disabled = true;

  item.addEventListener("click", () => handleClick(id, modal, userName, userColor));
}

const createUsersListItem = (userName: string, userColor: string, id: string) => {
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
  })
  
  item.appendChild(name);
  item.appendChild(color);
  item.appendChild(closeButton);
  
  return item;
}

const refresh = () => {
  makeFetch(
    "/users",
    {},
    (data: {name: string, color: string, id: string}[]) => {
      const usersList = document.querySelector(".users-list__list");
      if (!usersList) return;
      usersList.innerHTML = "";
      data.forEach(({name, color, id}) => {
        const item = createUsersListItem(name, color, id);
        usersList.appendChild(item);
      });
    },
    () => {}
  );
}

document.addEventListener('DOMContentLoaded', () => {
	listenLangChange();
  refresh();
  const modal = document.querySelector(".modal") as HTMLDataElement;
  modal.style.display = "none";
  modal.addEventListener("mousedown", () => {
    modal.style.display = "none";
  })
  const modalContent = document.getElementById("modal-content") as HTMLDataElement;
  modalContent.addEventListener("mousedown", (e) => {
    e.stopPropagation();
  }, true);
  const refreshButton = document.querySelector(".users-list__refresh") as HTMLButtonElement;
  refreshButton.addEventListener("click", refresh);
});