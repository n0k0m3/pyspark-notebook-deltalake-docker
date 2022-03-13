# PySpark Notebook with DeltaLake for production

This repo tries to replicate databricks runtime, plus feature-rich jupyter/docker-stacks.

## Base image: rapidsai/rapidsai:22.02-cuda11.5-runtime-ubuntu20.04-py3.8
## Additional packages:
- (Almost) Everything in the [`jupyter/all-spark-notebook`](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook) and (eventually) [`jupyter/r-notebook`](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-r-notebook) images, and their ancestor images. ([Inheritance tree](http://interactive.blockdiag.com/?compression=deflate&src=eJyFzTEPgjAQhuHdX9Gws5sQjGzujsaYKxzmQrlr2msMGv-71K0srO_3XGud9NNA8DSfgzESCFlBSdi0xkvQAKTNugw4QnL6GIU10hvX-Zh7Z24OLLq2SjaxpvP10lX35vCf6pOxELFmUbQiUz4oQhYzMc3gCrRt2cWe_FKosmSjyFHC6OS1AwdQWCtyj7sfh523_BI9hKlQ25YdOFdv5fcH0kiEMA))
- `delta-lake` and `delta-spark`

## Planning:
- All additional packages from `jupyter/r-notebook`.
- All additional packages that are on top of Databricks runtime dependencies tree ([10.3 ML GPU runtime](https://docs.databricks.com/release-notes/runtime/10.3ml.html#python-libraries-on-gpu-clusters))
- `xgboost` and Spark distribution of `xgboost` ([Waiting for this PR](https://github.com/dmlc/xgboost/pull/7709))
- `hyperopt`

# Starting Docker

## Generate environment variables
Check `.env.template` for environment variables template, or modify and copy these lines
```sh
echo "JUPYTER_PATH=<path-to-notebook-directory>" > .env
echo "NB_UID=`id -u`" >> .env
echo "NB_GID=`id -g`" >> .env
```
Get `path-to-notebook-directory` using `pwd` in the notebook directory

## Docker Compose
```sh
docker-compose up -d
```