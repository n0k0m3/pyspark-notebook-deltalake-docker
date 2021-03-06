from utils import run, header, modify_mamba
import os
import shutil
import re

# Checkout base-notebook
def checkout_base_notebook():
    base_notebook_dockerfile_part = header("From: jupyter/base-notebook")
    with open("docker-stacks/base-notebook/Dockerfile", "r") as f:
        base_notebook_dockerfile = f.read()

    base_notebook_dockerfile_part += (
        re.findall(
            r"(# Fix: https://github.com/hadolint/hadolint/wiki/DL4006[\w\W]+)\# Configure environment",
            base_notebook_dockerfile,
        )[0].strip()
        + "\n"
    )
    with open("src_docker-stacks/Dockerfile.base-notebook", "w") as f:
        f.write(base_notebook_dockerfile_part)


# Checkout miminal-notebook
def checkout_minimal_notebook():
    minimal_notebook_dockerfile_part = header("From: jupyter/minimal-notebook")
    with open("docker-stacks/minimal-notebook/Dockerfile", "r") as f:
        minimal_notebook_dockerfile = f.read()

    minimal_notebook_dockerfile_part += (
        re.findall(
            r"USER root([\w\W]+)\# Switch back to jovyan", minimal_notebook_dockerfile
        )[0].strip()
        + "\n"
    )
    with open("src_docker-stacks/Dockerfile.minimal-notebook", "w") as f:
        f.write(minimal_notebook_dockerfile_part)


# Checkout scipy-notebook
def checkout_scipy_notebook():
    scipy_notebook_dockerfile_part = header("From: jupyter/scipy-notebook")
    with open("docker-stacks/scipy-notebook/Dockerfile", "r") as f:
        scipy_notebook_dockerfile = f.read()

    apt_part = (
        re.findall(
            r"USER root([\w\W]+)USER \${NB_UID}\n\n# Install Python 3 packages",
            scipy_notebook_dockerfile,
        )[0].strip()
        + "\n"
    )

    mamba_part = (
        re.findall(
            r"USER \${NB_UID}([\w\W]+)# Install facets", scipy_notebook_dockerfile
        )[0]
        .strip()
        .split("\n")
    )
    mamba_part = modify_mamba(mamba_part)

    scipy_notebook_dockerfile_part += apt_part + "\n" + mamba_part + "\n"
    with open("src_docker-stacks/Dockerfile.scipy-notebook", "w") as f:
        f.write(scipy_notebook_dockerfile_part)


def checkout_pyspark_notebook():
    pyspark_notebook_dockerfile_part = header("From: jupyter/pyspark-notebook")
    with open("docker-stacks/pyspark-notebook/Dockerfile", "r") as f:
        pyspark_notebook_dockerfile = f.read()

    spark_part = (
        re.findall(
            r"(\# Spark dependencies[\w\W]+)USER \${NB_UID}",
            pyspark_notebook_dockerfile,
        )[0]
        .replace('RUN fix-permissions "/etc/ipython/"', "")
        .strip()
        + "\n"
    )
    mamba_part = (
        re.findall(
            r"USER \${NB_UID}([\w\W]+)WORKDIR \"\${HOME}\"", pyspark_notebook_dockerfile
        )[0]
        .strip()
        .split("\n")
    )

    mamba_part = modify_mamba(mamba_part)

    pyspark_notebook_dockerfile_part += spark_part + "\n" + mamba_part + "\n"
    with open("src_docker-stacks/Dockerfile.pyspark-notebook", "w") as f:
        f.write(pyspark_notebook_dockerfile_part)

    shutil.copyfile(
        "docker-stacks/pyspark-notebook/ipython_kernel_config.py",
        ".build/ipython_kernel_config.py",
    )


def checkout_all_spark_notebook():
    all_spark_notebook_dockerfile_part = header("From: jupyter/all-spark-notebook")
    with open("docker-stacks/all-spark-notebook/Dockerfile", "r") as f:
        all_spark_notebook_dockerfile = f.read()

    apt_part = (
        modify_mamba(
            re.findall(
                r"USER root([\w\W]+)USER \${NB_UID}", all_spark_notebook_dockerfile
            )[0]
            .strip()
            .split("\n")
        )
        + "\n"
    )
    mamba_part = (
        re.findall(r"USER \${NB_UID}([\w\W]+)", all_spark_notebook_dockerfile)[0]
        .strip()
        .split("\n")
    )
    mamba_part = modify_mamba(mamba_part).replace(
        "install --sys-prefix && \\", "install --sys-prefix"
    )
    mamba_part = mamba_part.split("\n")
    mamba_part[-2] += " && \\"
    mamba_part = "\n".join(mamba_part)

    all_spark_notebook_dockerfile_part += apt_part + "\n" + mamba_part + "\n"
    with open("src_docker-stacks/Dockerfile.all-spark-notebook", "w") as f:
        f.write(all_spark_notebook_dockerfile_part)


def checkout_r_notebook():
    r_notebook_dockerfile_part = header("From: jupyter/r-notebook")
    with open("docker-stacks/r-notebook/Dockerfile", "r") as f:
        r_notebook_dockerfile = f.read()

    apt_part = (
        re.findall(r"USER root([\w\W]+)USER \${NB_UID}", r_notebook_dockerfile)[
            0
        ].strip()
        + "\n"
    )
    mamba_part = (
        re.findall(r"USER \${NB_UID}([\w\W]+)", r_notebook_dockerfile)[0]
        .strip()
        .split("\n")
    )
    mamba_part = modify_mamba(mamba_part).replace(
        "install --sys-prefix && \\", "install --sys-prefix"
    )

    r_notebook_dockerfile_part += apt_part + "\n" + mamba_part + "\n"
    with open("src_docker-stacks/Dockerfile.r-notebook", "w") as f:
        f.write(r_notebook_dockerfile_part)


def main():
    # Check if docker-stacks is cloned
    if os.path.exists("docker-stacks"):
        print("docker-stacks directory already exists")
    else:
        # Clone docker-stacks
        run("git clone https://github.com/jupyter/docker-stacks.git")

    checkout_base_notebook()
    checkout_minimal_notebook()
    checkout_scipy_notebook()
    checkout_pyspark_notebook()
    checkout_all_spark_notebook()


if __name__ == "__main__":
    main()
