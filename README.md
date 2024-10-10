# Price Alerts
## Features

- As per Instruction Run on localhost:8000/...
## Installation

To set up and run this project locally, follow these steps:


### Clone the Repository

```sh
git clone https://github.com/AbHIsHEK4011/project.git
cd project
```

### Configuration

1. Create a `.env` file in the root directory and add your environment variables:

    ```env
    DJANGO_SETTINGS_MODULE=price_alerts.settings
    DATABASE_URL=postgres://postgres:qwerty@db:5432/price_alert_db
    ```

2. Update your `docker-compose.yml` if necessary to match your local setup.

### Build and Run

1. Build the Docker containers:

    ```sh
    docker-compose build
    ```

2. Start the Docker containers:

    ```sh
    docker-compose up
    ```

3. Apply migrations:

    ```sh
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser (optional):

    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

### API Endpoints

- **User Registration**:
    - **URL**: `/api/register/`
    - **Method**: `POST`
    - **Request Body**: `{ "username": "newuser", "password": "password123", "email": "newuser@example.com" }`
  
- **Token Obtain Pair**:
    - **URL**: `/api/token/`
    - **Method**: `POST`
    - **Request Body**: `{ "username": "newuser", "password": "password123" }`

- **List User Alerts**:
    - **URL**: `/api/alerts/`
    - **Method**: `GET`
    - **Headers**: `Authorization: Bearer <access_token>`

- **Create Alert**:
    - **URL**: `/api/alerts/`
    - **Method**: `POST`
    - **Request Body**: `{ "cryptocurrency": "BTC", "target_price": 30000.0 }`

- **Retrieve Single Alert**:
    - **URL**: `/api/alerts/{id}/`
    - **Method**: `GET`
    - **Headers**: `Authorization: Bearer <access_token>`

- **Delete Alert**:
    - **URL**: `/api/alerts/{id}/`
    - **Method**: `DELETE`
    - **Headers**: `Authorization: Bearer <access_token>`
![image](https://github.com/user-attachments/assets/c133d3f4-c84b-4b04-aa9e-8a30173a5257)

