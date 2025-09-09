# Web Application - Project Overview

## 🏗️ Architecture
Full-stack web application with Node.js/Express backend and vanilla TypeScript frontend

## 📁 Project Structure
```
web/
├── src/                    # Server-side code
│   └── server.ts          # Main Express server
├── public/                # Client-side static files
│   ├── html/              # HTML templates (ru/eng localization)
│   ├── js/                # Compiled JavaScript (from TypeScript)
│   ├── ts/                # TypeScript source files
│   └── css/               # Stylesheets
├── dist/                  # Compiled server code
├── node_modules/          # Dependencies
├── package.json           # Project configuration
├── tsconfig.json          # TypeScript config for server
└── users.json            # User data storage
```

## 🛠️ Technology Stack
- **Backend**: Node.js, Express, TypeScript, ts-node
- **Frontend**: Vanilla TypeScript/JavaScript, HTML, CSS
- **Development**: nodemon for hot reload
- **Build**: TypeScript compiler with dual configs

## ⚙️ Features
- **Authentication System**: Cookie-based user authentication
- **Internationalization**: Russian/English language support
- **User Management**: Registration, login, profile customization
- **User Profiles**: Color themes for users
- **API Endpoints**: RESTful API for user operations

## 📋 Key Components

### Server (`src/server.ts`)
- Express server with cookie-parser middleware
- Authentication middleware for route protection
- User data management with JSON file storage
- Language detection and routing
- Static file serving

### Client TypeScript Files
- `auth.ts` - Authentication form handling
- `index.ts` - Profile page functionality  
- `myfetch.ts` - Custom fetch utility
- `changeLange.ts` - Language switching

### HTML Structure
- Localized templates in `/html/ru/` and `/html/eng/`
- Authentication page (`auth.html`)
- Profile page (`index.html`)

## 🔧 Build System
Dual TypeScript configuration:
- **Server**: `tsconfig.json` (src → dist, CommonJS)
- **Client**: `public/ts/tsconfig.json` (public/ts → public/js, ES6 modules)

## 📦 NPM Scripts
- `npm run dev` - Start development server with nodemon
- `npm run build:server` - Compile server TypeScript
- `npm run build:client` - Compile client TypeScript
- `npm run build` - Build both server and client
- `npm run watch:server` - Watch server files
- `npm run watch:client` - Watch client files

## 💾 Data Storage
- User data stored in `users.json`
- Structure: `{username: {name, password, color}}`
- Synchronous/asynchronous file operations

## 🌐 Routing & Middleware
- Authentication checks on all non-API routes
- Automatic redirects based on authentication status
- Language parameter handling (?lang=eng/ru)

## 🎨 User Experience
- Responsive design with color customization
- Form validation and error handling
- Keyboard navigation support (Enter key)
- Dynamic language switching