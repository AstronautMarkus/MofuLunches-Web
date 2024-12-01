# MofuLunches-Web

**MofuLunches-Web** is a front-end application built with Flask, designed to serve as the dashboard for administrators and cooks on the **MofuLunches** platform. This dashboard enables seamless interaction with the MofuLunches-API, providing an efficient interface for managing users, orders, and menu items.

## Features

- **Admin Dashboard**: Comprehensive tools for managing user accounts, viewing order statuses, and monitoring menu items.
- **Cocineros Dashboard**: Interactive tools for creating, updating, and managing menu items and ingredients.
- **Seamless Integration**: Built to work with the [MofuLunches-API](https://github.com/AstronautMarkus/MofuLunches-API) for backend data, ensuring smooth data exchange between the front end and back end.
- **Responsive Design**: Optimized for desktop use to ensure usability across different screen sizes.

## Dotenv File Variables

To configure the application, create a `.env` file in the root directory with the following variables:

```plaintext
SECRET_KEY=flask_secret_key
API_URL=API_MAIN_ENDPOINT/api
```

These variables are essential for the application to function correctly:

- `SECRET_KEY`: A secret key for Flask to handle sessions and security.
- `API_URL`: The main endpoint for the MofuLunches-API, including the `/api` path (e.g., `http://localhost:5000/api`).