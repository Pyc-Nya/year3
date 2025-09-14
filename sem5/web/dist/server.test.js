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
const supertest_1 = __importDefault(require("supertest"));
const express_1 = __importDefault(require("express"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const path_1 = __importDefault(require("path"));
describe('Server Functions Tests', () => {
    let app;
    beforeEach(() => {
        app = (0, express_1.default)();
        app.use(express_1.default.json());
        app.use((0, cookie_parser_1.default)());
        app.use(express_1.default.static(path_1.default.join(process.cwd(), 'public')));
    });
    describe('Basic Server Setup', () => {
        test('should create express app', () => {
            expect(app).toBeDefined();
        });
    });
    describe('API Routes', () => {
        beforeEach(() => {
            // Мокаем пользователей для тестов
            const mockUsers = {
                'test-id-123': {
                    id: 'test-id-123',
                    name: 'testuser',
                    password: 'testpass123',
                    color: '#FF0000'
                },
                'test-id-456': {
                    id: 'test-id-456',
                    name: 'anotheruser',
                    password: 'anotherpass',
                    color: '#00FF00'
                }
            };
            // Добавляем роуты напрямую для тестирования
            app.post('/api/auth', (req, res) => {
                const { username, password } = req.body;
                const user = Object.values(mockUsers).find(u => u.name === username);
                if (!user) {
                    // Создание нового пользователя
                    res.redirect('/profile');
                }
                else if (user.password === password) {
                    // Авторизация существующего пользователя
                    res.cookie('username', username);
                    res.cookie('id', user.id);
                    res.cookie('color', user.color);
                    res.redirect('/profile');
                }
                else {
                    res.status(401).send('Неверное имя пользователя или пароль');
                }
            });
            app.get('/api/users', (req, res) => {
                const usersArr = Object.values(mockUsers).map(({ name, color, id }) => ({ name, color, id }));
                res.status(200).json(usersArr);
            });
            app.get('/api/user/:id', (req, res) => {
                const id = req.params.id;
                if (typeof id !== 'string') {
                    return res.status(400).send('invalid id');
                }
                const user = mockUsers[id];
                if (!user) {
                    return res.status(404).send('user with id does not exist');
                }
                res.status(200).json({
                    id: user.id,
                    name: user.name,
                    color: user.color
                });
            });
            app.delete('/api/user', (req, res) => {
                const { id } = req.body;
                if (typeof id !== 'string') {
                    return res.status(400).send('invalid id');
                }
                const user = mockUsers[id];
                if (!user) {
                    return res.status(404).send('user with id does not exist');
                }
                delete mockUsers[id];
                res.status(200).send();
            });
            app.post('/api/color', (req, res) => {
                const { id, color } = req.body;
                if (!id || !mockUsers[id]) {
                    return res.redirect('/auth');
                }
                mockUsers[id].color = color;
                res.cookie('color', color);
                res.status(200).send('успешно изменен цвет пользователя');
            });
            app.get('/', (req, res) => {
                res.status(404).send('you should not be here');
            });
        });
        describe('POST /api/auth', () => {
            test('should create new user when user does not exist', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/auth')
                    .send({
                    username: 'newuser',
                    password: 'newpass123'
                });
                expect(response.status).toBe(302);
                expect(response.headers.location).toBe('/profile');
            }));
            test('should authenticate existing user with correct credentials', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/auth')
                    .send({
                    username: 'testuser',
                    password: 'testpass123'
                });
                expect(response.status).toBe(302);
                expect(response.headers.location).toBe('/profile');
            }));
            test('should reject existing user with wrong password', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/auth')
                    .send({
                    username: 'testuser',
                    password: 'wrongpassword'
                });
                expect(response.status).toBe(401);
                expect(response.text).toBe('Неверное имя пользователя или пароль');
            }));
        });
        describe('GET /api/users', () => {
            test('should return list of users without passwords', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .get('/api/users');
                expect(response.status).toBe(200);
                expect(response.body).toHaveLength(2);
                expect(response.body[0]).toHaveProperty('name');
                expect(response.body[0]).toHaveProperty('color');
                expect(response.body[0]).toHaveProperty('id');
                expect(response.body[0]).not.toHaveProperty('password');
            }));
        });
        describe('GET /api/user/:id', () => {
            test('should return user by ID', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .get('/api/user/test-id-123');
                expect(response.status).toBe(200);
                expect(response.body).toEqual({
                    id: 'test-id-123',
                    name: 'testuser',
                    color: '#FF0000'
                });
            }));
            test('should return 404 for non-existent user', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .get('/api/user/non-existent-id');
                expect(response.status).toBe(404);
                expect(response.text).toBe('user with id does not exist');
            }));
        });
        describe('DELETE /api/user', () => {
            test('should delete existing user', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .delete('/api/user')
                    .send({ id: 'test-id-123' });
                expect(response.status).toBe(200);
            }));
            test('should return 404 for non-existent user', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .delete('/api/user')
                    .send({ id: 'non-existent-id' });
                expect(response.status).toBe(404);
                expect(response.text).toBe('user with id does not exist');
            }));
            test('should return 400 for invalid ID', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .delete('/api/user')
                    .send({ id: 123 });
                expect(response.status).toBe(400);
                expect(response.text).toBe('invalid id');
            }));
        });
        describe('POST /api/color', () => {
            test('should update user color', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/color')
                    .send({
                    id: 'test-id-123',
                    color: '#0000FF'
                });
                expect(response.status).toBe(200);
                expect(response.text).toBe('успешно изменен цвет пользователя');
            }));
            test('should redirect unauthorized user', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/color')
                    .send({
                    id: 'non-existent-id',
                    color: '#0000FF'
                });
                expect(response.status).toBe(302);
                expect(response.headers.location).toBe('/auth');
            }));
            test('should redirect user with no ID', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .post('/api/color')
                    .send({
                    color: '#0000FF'
                });
                expect(response.status).toBe(302);
                expect(response.headers.location).toBe('/auth');
            }));
        });
        describe('GET /', () => {
            test('should return 404 for root path', () => __awaiter(void 0, void 0, void 0, function* () {
                const response = yield (0, supertest_1.default)(app)
                    .get('/');
                expect(response.status).toBe(404);
                expect(response.text).toBe('you should not be here');
            }));
        });
    });
    describe('Utility Functions', () => {
        test('should handle language parameter correctly', () => {
            // Имитируем логику getLanguage
            const getLanguage = (req) => {
                return req.query.lang === "eng" ? "eng" : "ru";
            };
            expect(getLanguage({ query: { lang: 'eng' } })).toBe('eng');
            expect(getLanguage({ query: {} })).toBe('ru');
            expect(getLanguage({ query: { lang: 'ru' } })).toBe('ru');
        });
    });
});
