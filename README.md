<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/frontend/public/logo-dark.svg?raw=true">
    <img src="/frontend/public/logo.svg?raw=true" width="400" alt="InStory logo">
  </picture>
</p>

A web app that represents a simplified analog of Instagram. The backend is written in Django 5 using DRF.
The frontend (SSR+SPA) is implemented using Nuxt 3, Tailwind 4 and Vuetify component library.
The database is PostgreSQL.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/docs/screenshots/profile-dark.png?raw=true">
    <img src="/docs/screenshots/profile.png?raw=true" alt="App Screenshot">
  </picture>
</p>

## Features

- Authorization
- Email confirmation via a link sent to it
- Basic account settings: change username, avatar, first and last name, email, password
- Creating a post with a photo and its description
- View any user's profile with their published photos
- Validation of all data sent to the Backend, differentiation of API access
- Dockerized setup for easy deployment

## Features still in progress

- Displaying a single post with its description, comments, and likes, etc.
- Creating post comments
- Liking posts
- Following on users
- User searching
- Post feed
- Removing posts and comments by administrators
- Mobile version (bottom and top bars)

## Requirements

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)

## Setup & Usage

### Initial Setup

Run the following command to perform initial setup:

```sh
make setup
```

### Start the app

Launch the app using:

```sh
make up
```

By default, the app will be accessible at: [http://localhost:3000](http://localhost:3000).

All emails are sent via the Mailpit service (Included in the Docker debug setup) by default and are available at
http://localhost:8025.

### Stop the app

To stop the service, run:

```sh
make down
```

## Environment Variables

The `.env` file contains the following configurations:

```env
APP_NAME='InStory'
APP_DEBUG=true
APP_SECRET_KEY=

# Leave this empty if the app is not publicly hosted, otherwise insert ip or domain.
# Setting the value enables HTTPS and SSL certificate auto-renewal.
APP_HOST=
# If empty, 80 will be used for the HTTP port.
HTTP_PORT=3000
# If empty, 443 will be used for the HTTPS port.
HTTPS_PORT=
# Update the URL when you change APP_HOST, HTTP_PORT or HTTPS_PORT.
APP_URL=http://localhost:3000

DB_HOST=postgres
DB_PORT=5432
DB_NAME=instory
DB_USER=instory_user
DB_PASSWORD=

GUNICORN_WORKERS=3

EMAIL_HOST=mailpit
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=false
EMAIL_FROM_USER="noreply@instory.local"
```
