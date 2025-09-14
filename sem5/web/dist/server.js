"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const promises_1 = __importDefault(require("fs/promises"));
const cors_1 = __importDefault(require("cors"));
const uuid_1 = require("uuid");
const users_FILE = path_1.default.join(process.cwd(), 'users.json');
const loadUsersSync = () => {
    try {
        const data = fs_1.default.readFileSync(users_FILE, 'utf8');
        console.log('Пользователи загружены из users.json');
        return JSON.parse(data);
    }
    catch (error) {
        console.log('Файл users.json не найден, создаем пустой объект пользователей');
        return {};
    }
};
const getLanguage = (req) => {
    return req.query.lang === "eng" ? "eng" : "ru";
};
const saveUsers = (users) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        yield promises_1.default.writeFile(users_FILE, JSON.stringify(users, null, 2));
        console.log('Пользователи сохранены в users.json');
    }
    catch (error) {
        console.error('Ошибка сохранения пользователей:', error);
    }
});
const checkAuthMiddleware = (req, res, next) => {
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
    }
    else if (!doesUserExist && req.path !== "/auth") {
        console.log("пользователь не был авторизован ранее, перенаправление на /auth");
        return res.redirect(`/auth${queryParams}`);
    }
    else {
        return next();
    }
};
const app = (0, express_1.default)();
app.use(express_1.default.static(path_1.default.join(process.cwd(), 'public')));
app.use((0, cookie_parser_1.default)());
app.use(express_1.default.json());
app.use((0, cors_1.default)({
    origin: 'https://localhost:12345', // nginx сервер
    credentials: true // для передачи кук
}));
app.use(checkAuthMiddleware);
const port = 8000;
const users = loadUsersSync();
console.log(`Загружено ${Object.keys(users).length} пользователей`);
app.get('/', (req, res) => {
    res.status(404).send('you should not be here');
});
app.get('/profile', (req, res) => {
    const lang = getLanguage(req);
    res.status(200).sendFile(path_1.default.join(process.cwd(), "public", "html", lang, "index.html"));
});
app.get('/auth', (req, res) => {
    const lang = getLanguage(req);
    res.status(200).sendFile(path_1.default.join(process.cwd(), "public", "html", lang, "auth.html"));
});
app.get('/admin-panel', (req, res) => {
    const lang = getLanguage(req);
    res.status(200).sendFile(path_1.default.join(process.cwd(), "public", "html", lang, "adminPanel.html"));
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
    }
    else {
        let findedUser = user;
        if (usersWithName.length === 0) {
            const id = (0, uuid_1.v4)();
            findedUser = {
                name: name,
                password: password,
                color: "#000000",
                id: id,
            };
            users[id] = findedUser;
            console.log("сохраняю нового пользователя");
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
        };
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
        return res.redirect("/auth");
    }
    else {
        users[id].color = color;
        res.cookie("color", color);
        console.log("успешно изменен цвет пользователя");
        res.status(200).send("успешно изменен цвет пользователя");
    }
});
app.get("/api/users", (req, res) => {
    console.log("/api/users");
    const usersArr = Object.values(users).map(({ name, color, id }) => ({ name, color, id }));
    res.status(200).send(usersArr);
});
app.get("/api/user/:id", (req, res) => {
    const id = req.params.id;
    console.log("get: /api/user/", id);
    console.log("looking for id", id);
    if (typeof id !== "string") {
        console.log("invalid id");
        return res.status(400).send("invalid id");
    }
    else {
        if (users[id] === undefined) {
            console.log("user with id", id, "does not exist");
            return res.status(404).send("user with id does not exist");
        }
        else {
            res.status(200).send({
                id: users[id].id,
                name: users[id].name,
                color: users[id].color
            });
        }
    }
});
app.delete("/api/user", (req, res) => {
    console.log("delete: /api/user");
    const id = req.body.id;
    if (typeof id !== "string") {
        console.log("invalid id");
        return res.status(400).send("invalid id");
    }
    else {
        if (users[id] === undefined) {
            console.log("user with id", id, "does not exist");
            return res.status(404).send("user with id does not exist");
        }
        else {
            delete users[id];
            saveUsers(users);
            res.status(200).send();
        }
    }
});
app.listen(port, () => {
    console.log(`Сервер запущен на http://localhost:${port}`);
});
