# How to start Apache Airflow container in the docker from this project 

1. clone this project fron GitHub
    ```bash
    git clone https://github.com/Chuan-Tung-Cheng/carbon_emission.git
    ```
2. enter this project's root directory and run the following commandline
    ```bash
    cd carbon_emission
    docker network create airflow-network
    docker run -d \
    --name airflow-server \
    --network airflow-network \
    --restart unless-stopped \
    -p 8080:8080 \
    -v $PWD/airflow/dags:/opt/airflow/dags \
    -v $PWD/airflow/tasks:/opt/airflow/tasks \
    -v $PWD/airflow/utils:/opt/airflow/utils \
    -v $PWD/logs:/opt/airflow/logs \
    -v $PWD/data:/opt/airflow/data \
    -v $PWD/src:/opt/airflow/src \
    -e PYTHONPATH=/opt/airflow \
    -e AIRFLOW_ENV=production \
    airflow-server:v2 \
    airflow standalone
    ```
3. create your own account for manipulating Airflow GUI
    ```bash
    airflow users create \
    --username airflow \
    --firstname airflow \
    --password airflow \
    --lastname airflow \
    --role Admin \
    --email your_email@example.com
   ```
