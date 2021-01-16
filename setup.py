from setuptools import setup

setup(
        name='StreetNoParser',
        version='1.0',
        packages=['StreetNoParser'],
        install_requires=[
            'tabulate~=0.8.7'
        ],
        url='https://github.com/Cediddi/StreetNoParser',
        license='GPLv3',
        author='Umut Karcı',
        author_email='cediddi@gmail.com',
        description='A simple street name and house no parser.',
        entry_points={
            'console_scripts': [
                'StreetNoParser=StreetNoParser.__main__:main',
            ],
        },
)
