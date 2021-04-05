import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CACodeFramework",  # Replace with your own username
    version="1.1.0.04",
    author="CACode",
    author_email="cacode@163.com",
    description="CACode Framework For Python Flask,This framework corresponds to the ORM problem,You can see:https://github.com/cctvadmin/CACodeFramework-python-ORM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cctvadmin/CACodeFramework-python-ORM",
    project_urls={
        "Bug Tracker": "https://github.com/cctvadmin/CACodeFramework-python-ORM/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
