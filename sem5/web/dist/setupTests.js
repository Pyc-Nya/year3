"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const testUsersFile = path_1.default.join(process.cwd(), 'test-users.json');
beforeEach(() => {
    if (fs_1.default.existsSync(testUsersFile)) {
        fs_1.default.unlinkSync(testUsersFile);
    }
});
afterEach(() => {
    if (fs_1.default.existsSync(testUsersFile)) {
        fs_1.default.unlinkSync(testUsersFile);
    }
});
