import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nuclaer-sync-chain",
    version="0.0.0",
    author="Dylan Brophy",
    author_email="dylanbrophy@gmail.com",
    description="Blockchain for data storage and management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NuclearManD/SyncChain",
    packages=setuptools.find_packages(),
    install_requires=[
          'ecdsa', 'pysha3'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
