from setuptools import setup

setup(
    name='CACodeFramework',
    version='1.0.0',
    author='CACode',
    author_email='cacode@163.com',
    url='https://github.com/cctvadmin/CACodeFramework-python-ORM',
    description='CACode Framework For Python Flask,This framework corresponds to the ORM problem',
    packages=['CACodeFramework'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cacode=CACodeFramework.MainWork.__init__:__name__',
        ]
    }
)
