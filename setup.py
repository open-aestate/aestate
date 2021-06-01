import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

pa = setuptools.find_packages()
print(pa)
pa = ['aestate', 'aestate.cacode', 'aestate.exception', 'aestate.field', 'aestate.opera',
      'aestate.util', 'aestate.work', 'aestate.opera.DBPool']

setuptools.setup(
    name="aestate",
    version="1.0.1",
    author="CACode",
    author_email="cacode@163.com",
    description="Aestate framework for Python,You can see:https://gitee.com/cacode_cctvadmin/aestate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/cacode_cctvadmin/aestate",
    project_urls={
        "Bug Tracker": "https://gitee.com/cacode_cctvadmin/aestate/issues",
    },
    license=' Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=pa,
    python_requires=">=3.6",
    setup_requires=['aestate-json']
)
