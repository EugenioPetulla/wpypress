from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wpypress",
    version="0.1.2",
    author="Eugenio Petullà",
    author_email="eugenio@codeat.it",
    description="A versatile Python library for seamless interaction with the WordPress REST API, including built-in SEO features and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EugenioPetulla/wpypress",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.25.1",
    ],
)
