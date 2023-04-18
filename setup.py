from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "pyyaml",
    "python-daemon",
]

dev_requirements = [
    "black",
    "flake8",
    "isort",
]


setup(
    name="taskmaster",
    version="0.1.0",
    author="judumay, mabouce",
    author_email="judumay@student.42.fr, mabouce@student.42.fr",
    description="A simple and customizable process manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChokMania/TaskMaster",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["taskmaster = taskmaster.main:main"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
)
