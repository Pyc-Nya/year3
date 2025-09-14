import express from 'express';
import cookieParser from 'cookie-parser';
import path from 'path';
import fs from 'fs';   
import fsAsync from 'fs/promises';
import cors from "cors"
import { v4 as uuidv4 } from 'uuid';

const users_FILE = path.join(process.cwd(), 'users.json');
type Tusers = {[key: string]: {name: string, password: string, color: string, id: string}}

const loadUsersSync = (): Tusers => {
  try {
    const data = fs.readFileSync(users_FILE, 'utf8');
    console.log('Пользователи загружены из users.json');
    return JSON.parse(data);
  } catch (error) {
    console.log('Файл users.json не найден, создаем пустой объект пользователей');
    return {};
  }
};

const getLanguage = (req: express.Request): "ru" | "eng" => {
  return req.query.lang === "eng" ? "eng" : "ru";
};

const saveUsers = async (users: Tusers) => {
  try {
    await fsAsync.writeFile(users_FILE, JSON.stringify(users, null, 2));
    console.log('Пользователи сохранены в users.json');
  } catch (error) {
    console.error('Ошибка сохранения пользователей:', error);
  }
};

const checkAuthMiddleware: express.RequestHandler = (req, res, next) => {
  if (req.path.startsWith("/api")) {
    return next();
  }

  const username = req.cookies.username;
  console.log("запрос на ", req.path, "от ", username);
  const doesUserExist = Object.values(users).some(user => user.name === username); 

  const lang = getLanguage(req);
  const queryParams = `?lang=${lang}`;

  if (req.path === "/admin-panel") {
    return next();
  }

  // я исключаю здесь роуты /profile и /auth, т.к. если юзер уже на них, то нет смысла редиректить
  // иначе был бы бесконечный цикл, т к эта middleware используется во всех запросах
  if (doesUserExist && req.path !== "/profile" && req.path !== "/auth") {
    console.log("пользователь уже был авторизован ранее, перенаправление на /profile");
    return res.redirect(`/profile${queryParams}`);
  } else if (!doesUserExist && req.path !== "/auth") {
    console.log("пользователь не был авторизован ранее, перенаправление на /auth");
    return res.redirect(`/auth${queryParams}`);
  } else {
    return next();
  }
};

const app = express();
app.use(express.static(path.join(process.cwd(), 'public')));
app.use(cookieParser());
app.use(express.json());
app.use(cors({
  origin: 'https://localhost:12345',  // nginx сервер
}));
app.use(checkAuthMiddleware);
const port = 8000;

const users: Tusers = loadUsersSync();
console.log(`Загружено ${Object.keys(users).length} пользователей`);

app.get('/', (req, res) => {
  res.status(404).send('you should not be here');
});

app.get('/profile', (req, res) => {
  const lang = getLanguage(req);
  res.status(200).sendFile(path.join(process.cwd(), "public", "html", lang, "index.html"));
});

app.get('/auth', (req, res) => {
  const lang = getLanguage(req);
  res.status(200).sendFile(path.join(process.cwd(), "public", "html", lang, "auth.html"));
});

app.get('/admin-panel', (req, res) => {
  const lang = getLanguage(req);
  res.status(200).sendFile(path.join(process.cwd(), "public", "html", lang, "adminPanel.html"));
});

app.post("/api/auth", (req, res) => {
  console.log("/api/auth", req.body);
  const body = req.body;
  const name = body.username;
  const password = body.password;
  const usersWithName = Object.values(users).filter(user => user.name === name);
  const user = usersWithName.find(user => {
    return user.name === name && user.password === password;
  });
  if (!user && usersWithName.length > 0) {
    console.log("Неверное имя пользователя или пароль");
    return res.status(401).send("Неверное имя пользователя или пароль");
  } else {
    let findedUser = user;
    if (usersWithName.length === 0) {
      const id = uuidv4();
      findedUser = {
        name: name,
        password: password,
        color: "#000000",
        id: id,
      };
      users[id] = findedUser;
      console.log("сохраняю нового пользователя")
      saveUsers(users);
    }
    if (!findedUser) {
      return res.status(500).send();
    }
    console.log("сохраняю куки ", name, users[findedUser.id].color);

    const cookieProps = {
      httpOnly: false,
      domain: "localhost",
      path: "/"
    }
    
    res.cookie("username", name, cookieProps);
    res.cookie("id", findedUser.id, cookieProps);
    res.cookie("color", users[findedUser.id].color, cookieProps);

    console.log("перенаправление на /profile");
    return res.redirect("/profile");
  }
});

app.post("/api/color", (req, res) => {
  console.log("/api/color", req.body);
  const body = req.body;
  const id = body.id; 
  const color = body.color;
  console.log(id, color);
  if (!id || users[id] === undefined) {
    console.log("неавторизованный пользователь, перенаправление на /auth");
    return res.status(401).send("Не найден пользователь с указанным id");
  } else {
    users[id].color = color;
    saveUsers(users);
    res.cookie("color", color);
    console.log("успешно изменен цвет пользователя");
    res.status(200).send("успешно изменен цвет пользователя");
  }
});

app.get("/api/users", (req, res) => {
  console.log("/api/users");
  const usersArr = Object.values(users).map(({name, color, id}) => ({name, color, id}));
  res.status(200).send(usersArr);
});

app.get("/api/user/:id", (req, res) => {
  const id = req.params.id;

  console.log("get: /api/user/", id)
  console.log("looking for id", id);
  if (typeof id !== "string") {
    console.log("invalid id");
    return res.status(400).send("invalid id");
  } else {
    if (users[id] === undefined) {
      console.log("user with id", id, "does not exist");
      return res.status(404).send("user with id does not exist");
    } else {
      res.status(200).send({
        id: users[id].id,
        name: users[id].name,
        color: users[id].color
      });
    }
  }
});

app.delete("/api/user", (req, res) => {
  console.log("delete: /api/user")

  const id = req.body.id;
  if (typeof id !== "string") {
    console.log("invalid id");
    return res.status(400).send("invalid id");
  } else {
    if (users[id] === undefined) {
      console.log("user with id", id, "does not exist");
      return res.status(404).send("user with id does not exist");
    } else {
      delete users[id];
      saveUsers(users);
      res.status(200).send();
    }
  }
});



app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});