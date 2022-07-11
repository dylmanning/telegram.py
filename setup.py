from setuptools import setup

requirements = [r.strip() for r in open("requirements.txt").readlines()]

setup(
    name="telegram",
    version="1.0",
    packages=["telegram"],
    package_dir={
        "telegram": "./telegram",
    },
    install_requires=requirements,
)
