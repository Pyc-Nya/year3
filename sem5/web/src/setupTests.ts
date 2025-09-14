import fs from 'fs';
import path from 'path';

const testUsersFile = path.join(process.cwd(), 'test-users.json');

beforeEach(() => {
  if (fs.existsSync(testUsersFile)) {
    fs.unlinkSync(testUsersFile);
  }
});

afterEach(() => {
  if (fs.existsSync(testUsersFile)) {
    fs.unlinkSync(testUsersFile);
  }
});