import subprocess

MAMBA_PREFIX = """RUN source activate rapids && \\
    gpuci_mamba_retry install --quiet --yes \\
    -c numba \\
    -c conda-forge \\
    -c pytorch \\
    -c defaults \\"""


def run(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=True)


# Fancy header
def header(text: str, dockerfile_text: str = None) -> str:
    dockerfile_text = "#" * 50 + "\n"
    dockerfile_text += f"#####{text : ^40}#####" + "\n"
    dockerfile_text += "#" * 50 + "\n"
    return dockerfile_text


# Modify mamba/conda
def modify_mamba(mamba_part: list) -> str:
    mamba_part = (
        "\n".join(
            [x for x in mamba_part if "fix-permissions" not in x and "NB_USER" not in x]
        )
        .replace("RUN mamba install --quiet --yes \\", MAMBA_PREFIX)
        .replace("RUN mamba install --quiet --yes", MAMBA_PREFIX + "\n   ")
        .replace("mamba clean --all -f -y && \\", "gpuci_mamba_retry clean --all -f -y")
        .strip()
    )
    return mamba_part
