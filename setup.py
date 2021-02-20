from setuptools import setup, find_packages

setup(
    name='redmine2wikijs',
    version='0.1.1',
    description='Migrate a redmine project to gitlab',
    long_description=README,
    author='Julian Cervino',
    author_email='jcerigl@gmail.com',
    license='GPL',
    url='https://github.com/juliancervino/redmine-wikijs-migrator',
    packages=find_packages(),
    install_requires=['pyyaml', 'requests', 'GitPython', 'pypandoc'],
    entry_points={
        'console_scripts': [
            'redmine2wikijs = redmine2wikijs.commands:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)