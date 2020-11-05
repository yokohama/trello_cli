import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Trello-CLI",
    version="0.0.1",
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': ['trello=trello_cli:main'],
    },
    author="Yokohama",
    author_email="yuhei.yokohama@gmail.com",
    description="Trello card managment on CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
