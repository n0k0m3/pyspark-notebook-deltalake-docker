# PySpark Notebook with DeltaLake for production

This repo tries to replicate databricks environment

## Base image: jupyter/pyspark-notebook
## Installed packages:
- gcc
- xgboost
- delta-lake

## Planning:
- delta-spark
- plotly

# Starting Docker

```
docker run -d \
    --name ds \
    -p 4040:4040 \
    -p 4041:4041 \
    -p 8888:8888 \
    -v $JUPYTER_PATH:/home/jovyan/ \
    -e JUPYTER_ENABLE_LAB=yes \
    -e GRANT_SUDO=yes \
    --user root \
    -e RESTARTABLE=yes \
    n0k0m3/pyspark-notebook-datalake-docker
```
