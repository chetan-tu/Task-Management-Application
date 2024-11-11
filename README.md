# Task Management Application

A RESTful API allowing users to create, view, update, and delete tasks with ease. This application is designed to provide simple and efficient task management functionality

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation and Configuration](#installation-and-configuration)
5. [Usage Instructions](#usage-instructions)
6. [Testing](#testing)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Docker Instructions](#docker-instructions)
9. [Implementation Choices](#implementation-choices)
10. [Challenges & Solutions](#challenges--solutions)
11. [Potential improvements](#potential-improvements)

---

## Project Overview

## Project Overview

The Task Management Application provides a RESTful API to manage tasks. Users can perform the following operations:

- **Create tasks**: Add new tasks with titles, descriptions, and statuses.
- **Retrieve tasks**: View all tasks or retrieve a specific task by its ID.
- **Update tasks**: Modify task details such as title, description, or status.
- **Delete tasks**: Remove tasks by their ID.

The application includes a PostgreSQL database for data storage, environment-based configuration files for managing settings.

## Features

- **CRUD Operations**: Create, read, update, and delete tasks.
- **RESTful API Endpoints**:
  - `GET /tasks`: Retrieve all tasks.
  - `POST /tasks`: Create a new task.
  - `GET /tasks/{id}`: Retrieve a specific task by ID.
  - `PUT /tasks/{id}`: Update an existing task.
  - `DELETE /tasks/{id}`: Delete a task by ID.

- **PostgreSQL Integration**: Uses PostgreSQL for data persistence and efficient task management.
- **Environment-Based Configuration**: Separate `.env` files for development and `.env.test` testing and add it <u>under `apps`and `tests` folders in the project respectively.</u>

### Example `.env` file

  ```plaintext
        DATABASE_HOST=localhost
        DATABASE_NAME=celonistask
        DATABASE_USER=postgres
        DATABASE_PASSWORD=<your_password>
  ```

### Example `.env.test` file
 ```plaintext
        DATABASE_HOST=localhost
        DATABASE_NAME=celonistask_test
        DATABASE_USER=postgres
        DATABASE_PASSWORD=<your_password>
        DATABASE_PORT=5432
  ```

- **Data Model**:
  - **ID**: Unique identifier for each task.
  - **Title**: Short description of the task.
  - **Description**: Detailed explanation of the task.
  - **Status**: State of the task (e.g., Open, In Progress, Closed).
  - **CreatedAt**: Timestamp of creation.
  - **UpdatedAt**: Timestamp of last update.

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (for production and testing)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Installation and Configuration

1. **Clone the Repository**:
   - Ensure Git is Installed: Make sure Git is installed on your system. You can check this by running:
     ```bash
      git --version
     ```
 
   - Clone the project repository to your local machine:
     ```bash
     git clone https://github.com/chetan-tu/Task-Management-Application.git
     cd Task-Management-Application
     ```

2. **Install Dependencies**:
   - Ensure you have Python installed. Then, install the required packages:
     ```bash
     python -m pip install -r requirements.txt
     ```

3. **Set Up PostgreSQL Database**:

    Before running the application, ensure that PostgreSQL is installed and running on your system.

   **Install PostgreSQL**:
   - Follow the installation instructions for your operating system from the [official PostgreSQL website](https://www.postgresql.org/download/).

   **Create Databases**:
   - Use the PostgreSQL command line or a database client to create the databases specified in your `.env` and `.env.test` files.
     - Example commands -

    ```bash
     CREATE DATABASE celonistask;
     CREATE DATABASE celonistask_test;
    ```

   - Ensure PostgreSQL is running and accessible.

## Usage Instructions

1. **Run the Application**:
    - Open a terminal or command prompt in the root directory of the project.
   - Ensure your PostgreSQL database is running and configured as per the `.env` file and add it <u>under `apps` folder in the project.</u>
   - Start the FastAPI server:
     ```bash
     python -m uvicorn apps.main:app --reload
     ```
   - The application will be accessible at `http://127.0.0.1:8000`.

   - If you prefer to run the application with Docker, refer to the [Docker Instructions](#running-the-application-with-docker) section for instructions.


- Once the application is running, open your browser and navigate to `http://127.0.0.1:8000/docs`.
- This will open the **Swagger UI**, which provides an interactive interface to test each endpoint.
  
Alternatively, you can use tools like `curl` or **Postman** to interact with the API:

As an example- 

- **Get all tasks**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/tasks"
  ```

## Testing

To ensure the application is functioning correctly, you can run unit and end-to-end tests.

1. **Set Up the Test Environment**:
   - Make sure a separate test database is configured in the `.env.test` file and add it <u>under `tests` folder in the project.</u>
      - Example `.env.test` file:
         ```plaintext
            DATABASE_HOST=localhost
            DATABASE_NAME=celonistask_test
            DATABASE_USER=postgres
            DATABASE_PASSWORD=<your_password>
            DATABASE_PORT=5432
        ```

2. **Create the Test Database**:
   - Use the PostgreSQL command line or a database client to create the test database (IF NOT ALREADY DONE):
     ```sql
     CREATE DATABASE celonistask_test;
     ```

3. **Run Tests**:
   - Use the following command to run all tests:
     ```bash
     python -m pytest
     ```
   - This will execute all tests in the project and use the configuration from `.env.test`.

4. **Types of Tests**:
   - **Unit Tests**: Focus on testing individual functions for reading ,creating, updating, deleting and validating tasks.
   - **End-to-End Tests**: Simulate user actions by creating, updating, and deleting tasks through API calls to ensure all endpoints work as expected.

## CI/CD Pipeline

1. **Add and Push All Files**:
   - Ensure all necessary files are added to the commit, including the `.github/workflows/ci.yml` file for the CI/CD pipeline configuration.
   - Run the following commands:
     ```bash
     git add .
     git commit -m "chore: add project files and CI/CD pipeline configuration"
     git push origin main
     ```

2. **Automatic Testing**:
   - Once pushed, GitHub Actions will automatically run tests on each push to the main branch.

## Docker Instructions

Before proceeding, make sure **Docker is installed and running** on your system. You can download Docker from [the official Docker website](https://www.docker.com/get-started) if needed.

1. **Build the Docker Image**:
   - In the project root, build the Docker image with the following command:
     ```bash
     docker build -t my-fastapi-app .
     ```

2. **Run the Docker Container**:
   - Start the container with this command:
     ```bash
     docker run -d -p 8000:8000 -e DATABASE_HOST=host.docker.internal my-fastapi-app
     ```
   - Explanation of options:
     - `-e DATABASE_HOST=host.docker.internal`: Sets the `DATABASE_HOST` environment variable to allow the container to connect to a database on the host machine. This setting **overrides the `DATABASE_HOST` value specified in the `.env` file**.


3. **Access the Application**:
   - After the container is running, open your browser and navigate to `http://localhost:8000` to access the application.
   - API documentation is available at `http://localhost:8000/docs`.

## Implementation choices
<u>FastAPI</u>

<u>Justification</u>: FastAPI is a high-performance, modern framework ideal for building RESTful APIs. It offers asynchronous capabilities, automatic interactive documentation, and is known for its speed, making it well-suited for this task management application:

1.Asynchronous Support: FastAPI handles multiple requests efficiently, making it scalable and responsive.

2.Automatic Documentation: FastAPI automatically generates Swagger and Redoc documentation, which streamlines testing and collaboration.

3.Performance: FastAPI, when run with Uvicorn, is one of the fastest Python setups, ensuring the application can handle requests quickly and reliably.

4.Data Validation: Built-in data validation with Pydantic provides robust checks on data, enhancing data consistency.

Additionally, I chose FastAPI due to my familiarity with it, which enabled a more efficient development process.

<u>PostgreSQL</u>

<u>Justification</u>: PostgreSQL is a reliable, robust, and feature-rich database management system. It’s particularly well-suited for applications that require complex data handling and scalability:

1.Reliability: PostgreSQL ensures data integrity with ACID compliance, which is crucial for managing tasks.

2.Rich Data Types: Support for data types like JSON and arrays makes PostgreSQL flexible for various data needs.


## Challenges & Solutions

1.Challenge: Running the Application in Docker with Local Database Connectivity

When attempting to run the application in Docker, I encountered a problem connecting to the local PostgreSQL database. Docker containers are isolated environments, and by default, they cannot directly access services on the host machine.
Solution:

<u>Solution:</u>

To resolve this,after some research, I used the -e flag to override the DATABASE_HOST environment variable, setting it to host.docker.internal in the Docker run command:
```bash
docker run -d -p 8000:8000 -e DATABASE_HOST=host.docker.internal my-fastapi-app
```

2.Challenge: Managing Path Issues with Dependencies in Command Line

Some dependencies, like uvicorn and pytest, were not initially accessible through the command line due to missing PATH configurations, making it challenging to run commands smoothly.

<u>Solution:</u>

To ensure compatibility regardless of PATH configuration, I standardized commands using python -m (e.g., python -m uvicorn) in the README instructions. This approach guarantees that the application can be run consistently, even if packages are not directly in the PATH.

## Potential Improvements

<u>Current Handling of Synchronous Database Calls</u>
<u>Using psycopg2</u>: The application currently uses psycopg2 for database interactions with PostgreSQL. psycopg2 is a popular and reliable library for PostgreSQL, but it operates synchronously, meaning each database query blocks the event loop until it completes.

<u>Why It Works for This Application</u>: For a smaller application with limited traffic, psycopg2 provides stable and efficient database handling, and the impact of blocking calls is minimal. This setup is sufficient for handling moderate request loads.

<u>Future scope</u>
<u>Async Database Integration with asyncpg</u>
As the application scales, synchronous calls via psycopg2 may become a bottleneck under high traffic due to their blocking nature.
Improvement: Transition to asyncpg, an async-compatible PostgreSQL library, to enable non-blocking database operations. This would allow FastAPI to maintain higher concurrency, fully leveraging its asynchronous capabilities, which is beneficial for handling more simultaneous requests.
