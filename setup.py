import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="melon",
    version="0.0.2",
    author="evoneutron",
    author_email="evoneutron@gmail.com",
    description="Library for data interpretation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/evoneutron/melon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click==7.0", "tqdm==4.29.0"],
    entry_points={
        "console_scripts": [
            "melon=scripts.cli:cli"
        ]
    }
)
