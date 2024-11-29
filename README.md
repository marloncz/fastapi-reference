# Fastapi-Reference



## Overview

## ⚙️ Installation

A convenient `make` command is provided to install the project.
It will create a virtual environment with the correct python version and install all packages with `poetry`.
In addition, all development tools are installed with `brew` on macOS if they are not already installed.

```bash
make install
```

## 🚧 Usage

The project can be run from the main entry point `src/main.py` with the following command.

```bash
python src/fastapi_reference/main.py
```

## SQLite Database

For showcasing purposes, a SQLite database is created locally and initialized with mock data. The database is stored in the `database` directory with the filename `sql_database.db`.

The database can be initialized with the function `init_local_sql` within `/src/fastapi_reference/sql.py`. The notebook `notebooks/01_local_sql_setup.ipynb` can also be used to initialize the database.

### Mock Data Generation
Mock data is generated using random values and inserted into the database. Below is an example schema of the `products` table:

| id   | product_id | product_name          | product_category | product_description                       | valid_from | valid_to   | price   | stock | user_name | user_email       |
|------|------------|-----------------------|------------------|-------------------------------------------|------------|------------|---------|-------|-----------|------------------|
| 1    | "00001"    | "Durable Phone V7.2" | "Category F"     | "Est tempora quisquam velit neque..."    | 2015-11-30 | 2024-02-18 | 342.99  | 32    | "admin"   | "admin@mail.com" |
| 2    | "00002"    | "Eco Headset V3.0"   | "Category B"     | "Numquam neque sit eius porro..."        | 2018-08-06 | 2020-12-27 | 119.66  | 58    | "admin"   | "admin@mail.com" |
| 3    | "00003"    | "Reliable Table V1.9" | "Category A"    | "Magnam aliquam labore voluptat..."      | 2018-03-19 | 2024-07-03 | 488.46  | 7     | "admin"   | "admin@mail.com" |
| ...  | ...        | ...                   | ...              | ...                                       | ...        | ...        | ...     | ...   | ...       | ...              |
| 998  | "00998"    | "Premium Watch V5.1" | "Category F"     | "Ut consectetur magnam adipisci..."      | 2016-05-31 | 2021-12-23 | 250.41  | 20    | "admin"   | "admin@mail.com" |
| 999  | "00999"    | "Fancy Laptop V7.0"  | "Category B"     | "Non neque non etincidunt."              | 2015-07-08 | 2023-09-11 | 146.43  | 5     | "admin"   | "admin@mail.com" |
| 1000 | "01000"    | "Durable Watch V1.7" | "Category F"     | "Numquam ut tempora porro quiqu..."      | 2019-10-31 | 2021-02-07 | 358.81  | 87    | "admin"   | "admin@mail.com" |


**Features**
- Mock data includes 1000 rows of randomly generated products.
- Automatically clears and repopulates the database upon initialization.
- The `generate_mock_data` function utilizes [Polars](https://docs.pola.rs/api/python/stable/reference/index.html) and randomization to create realistic entries.

## FastAPI Service Docker Instructions

### Building and Running the Docker Container

The Docker container for the FastAPI service can be built and started using the provided `docker/fastapi_reference/Dockerfile`.

#### Steps to Build and Start the Container

1. **Build and Start the Container**  

    Use the following command to build the image and start the container:

   ```bash
   make docker-up
   ```

2. **Service Information**

    Once the container is up and running, the FastAPI service will be accessible on port **8000**.

3. **Accessing the API**

    You can interact with the API at the following base URL:
    ```bash
   http://127.0.0.1:8000
   ```

   Example to check the health of the service:
    - Using `curl`
        ```bash
        curl http://127.0.0.1:8000/health
        ```
    - Using Python:
        ```bash
        import requests
        base_url = "http://127.0.0.1:8000"
        response = requests.get(base_url + "/health")
        print(response.json())
        ```

4. **Development Notes**

    - Ensure Docker is installed and running on your system before executing the make docker-up command.
    - To view running containers, use:
        ```bash
        docker ps
        ```
    - To view logs for the running container, use:
        ```bash
        docker logs <container_name_or_id>
        ```
    - To rebuild the container from scratch:
        ```bash
        docker compose down && make docker-up
        ```

## Commit Conventions

```bash
commit -m "<type>(<scope>): <description>

[body]

[footer(s)]
"
```

Example:

```bash
commit -m "feat(model): adding new model for training a forecasting model"
```

```bash
commit -m "build: update pandas to version 2.0"
```

Type of commit:
- **fix**: Bugfixes
- **feat**: New features
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **docs**: Documentation-only changes
- **test**: Addition or correction of tests
- **build**: Changes of build components or external dependencies, like pip, docker ...
- **perf**: Code changes that improve the performance or general execution time
- **ci**: Changes to CI-configuration files and scripts
- **style**: Code style changes

Optional commit:
- **scope**: Context of the change
- **body**: Concise description of the change.
- **footer**: Consequences, which arise from the change
