from setuptools import find_packages, setup

extras_require = {
    "dev": ["pre-commit", "black", "isort"],
    "test": [],
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Feedly2Instapaper",
    version="0.1.4",
    data_files=[".env-example"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    url="https://github.com/Barabazs/Feedly2Instapaper",
    license="MIT",
    author="Barabazs",
    author_email="",
    description='Feedly2Instapaper adds your "Saved for later" entries to Instapaper and removes those entries in Feedly.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "instapaper==0.4",
        "feedly-client==0.25",
        "python-dotenv==0.21.0",
    ],
    extras_require=extras_require,
)
