with open("src/Dockerfile.header", "r") as f:
    dockerfile = f.read() + "\n"

docker_stacks_order = [
    "base-notebook",
    "minimal-notebook",
    "scipy-notebook",
    "pyspark-notebook",
    "all-spark-notebook",
]

for stack in docker_stacks_order:
    with open(f"src_docker-stacks/Dockerfile.{stack}", "r") as f:
        dockerfile += f.read() + "\n"

with open("src_additional/Dockerfile.delta-lake", "r") as f:
    dockerfile += f.read() + "\n"

with open("src/Dockerfile.footer", "r") as f:
    dockerfile += f.read() + "\n"

with open(".build/Dockerfile", "w") as f:
    f.write(dockerfile)