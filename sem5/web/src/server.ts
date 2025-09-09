import express from 'express';
import cookieParser from 'cookie-parser';
import path from 'path';
import fs from 'fs';   
import fsAsync from 'fs/promises';

const users_FILE = path.join(process.cwd(), 'users.json');
type Tusers = {[key: string]: {name: string, password: string, color: string}}

const loadUsersSync = (): {[key: string]: {name: string, password: string, color: string}} => {
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

  const lang = getLanguage(req);
  const queryParams = `?lang=${lang}`;
  
  // я исключаю здесь роуты /profile и /auth, т.к. если юзер уже на них, то нет смысла редиректить
  // иначе был бы бесконечный цикл, т к эта middleware используется во всех запросах
  if (username && req.path !== "/profile" && req.path !== "/auth") {
    console.log("пользователь уже был авторизован ранее, перенаправление на /profile");
    return res.redirect(`/profile${queryParams}`);
  } else if (!username && req.path !== "/auth") {
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
app.use(checkAuthMiddleware);
const port = 8000;

const users: {[key: string]: {name: string, password: string, color: string}} = loadUsersSync();
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

app.post("/api/auth", (req, res) => {
  console.log("/api/auth", req.body);
  const body = req.body;
  const name = body.username;
  const password = body.password;

  if (users[name] !== undefined && users[name].password !== password) {
    console.log("Неверное имя пользователя или пароль");
    res.status(401).send("Неверное имя пользователя или пароль");
  } else {
    if (users[name] === undefined) {
      users[name] = {
        name: name,
        password: password,
        color: "#000000"
      };
      saveUsers(users);
    }
    res.cookie("username", name);
    res.cookie("color", users[name].color);
    console.log("перенаправление на /profile");
    return res.redirect("/profile");
  }
});

app.post("/api/color", (req, res) => {
  console.log("/api/color", req.body);
  const body = req.body;
  const username = req.cookies.username; 
  const color = body.color;
  console.log(username, color);
  if (!username || users[username] === undefined) {
    console.log("неавторизованный пользователь, перенаправление на /auth");
    return res.redirect("/auth");
  } else {
    users[username].color = color;
    res.cookie("color", color);
    console.log("успешно изменен цвет пользователя");
    res.status(200).send("успешно изменен цвет пользователя");
  }
})

app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});