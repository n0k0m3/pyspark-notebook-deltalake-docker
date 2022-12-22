# Environment scraping guide

## Suggestion

- Get minimal conda environment from RAPIDS-AI Container
- Do a set difference using `pip freeze` between RAPIDS-AI and Databricks for missing packages

## RAPIDS-AI Container

Install `conda-tree`
```sh
conda install -c conda-forge conda-tree 'networkx>=2.5'
```

Generate minimal package
```sh
conda-tree leaves --export
```

## Databricks

Getting python package list from [Databricks Runtime Release Notes](https://docs.databricks.com/release-notes/runtime/12.0ml.html) by copy the table to a text file, then use these regex substitution to clean up

| Find             | Replace                     |
| ---------------- | --------------------------- |
| `\s+`            | nothing                     |
| `[\s\n]+(\d)`    | (note space preceding)` $1` |
| `[\s\n]+([a-z])` | `\n$1`                      |

**Notes:**
- `pipdeptree` output won't have `xgboost` installed, needs to be installed manually
- GPU runtime has these NVIDIA library installed (need to check if RAPIDS-AI already has these):
  - CUDA
  - cuDNN
  - NCCL
  - TensorRT
- Differences between CPU and GPU ML runtime:

    | ML CPU              | ML GPU             |
    | ------------------- | ------------------ |
    | `prometheus-client` |                    |
    | `tensorflow-cpu`    | `tensorflow`       |
    | `torch` CPU         | `torch` CUDA       |
    | `torchvision` CPU   | `torchvision` CUDA |



To get the minimal packages, use `pipdeptree` in a databrick cluster notebook, excluding Databricks-exclusive libraries and default Python packages

```
pipdeptree --exclude pip,pipdeptree,setuptools,wheel,databricks-feature-store,databricks-automl-runtime --warn silence | grep -E '^\w+'
```
