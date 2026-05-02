# VUE FRONTEND APPLICATION

1. Create an .env in root and add this: 
`VITE_API_BASE_URL=http://localhost:8080`
2. To lunch the front-end in docker use this commands:
`docker build -t vue-app .`
`docker run -d --name vue-app -p 5173:5173 vue-app`


## DESCRIPTION
This is a Vue 3 frontend application built with Vite.

The project provides a user interface for a microservices-based system and communicates with backend services through an Nginx API Gateway.

Main features:

- Multi-language support (3 languages)
- Tailwind CSS styling
- DaisyUI component system
- Communication with backend via Nginx reverse proxy
- Integration with multiple microservices (users, projects, news, expenses, events, visits)

## TECH STACK

- Vue 3
- Vite
- Tailwind CSS
- DaisyUI
- Vue I18n
- Axios (via API Gateway)

RECOMMENDED SETUP

IDE
VS Code with:

- Vue (Official) extension (Volar)
- Disable Vetur if installed

Browser
Chromium-based browsers (Chrome, Edge, Brave):

- Vue Devtools extension
- Enable Custom Object Formatter in DevTools

Firefox:

- Vue Devtools extension
- Enable Custom Object Formatter

## PROJECT SETUP

Install dependencies:
```npm install```

## DEVELOPMENT SERVER

Run local development server:
```npm run dev```

Application will be available at:
http://localhost:5173

## PRODUCTION BUILD

Create optimized build:
```npm run build```

Preview production build:
```npm run preview```

## ARCHITECTURE NOTES

- Frontend does NOT communicate directly with microservices
- All API requests go through Nginx API Gateway
- Gateway handles routing to backend services
- Authentication and data access are handled via backend services
- Frontend only consumes REST API responses

## MICROSERVICES INTEGRATION

This frontend connects to the following services via API Gateway:

- Users service
- Projects service (Kanban and tasks)
- News service (articles and feeds)
- Expenses service (financial tracking)
- Events service (calendar and scheduling)
- Visits metrics service (analytics and tracking)

## NOTES

- Ensure API Gateway (Nginx) is running before frontend requests backend data
- Environment variables should point to gateway URL (not individual services)
- Supports multi-language UI out of the box (3 languages configured)