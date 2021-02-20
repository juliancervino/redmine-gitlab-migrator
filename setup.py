from setuptools import setup, find_packages

setup(
    name='redmine-wikijs-migrator',
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
            'redmine2wikijs = redmine-wikijs-migrator.commands:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)