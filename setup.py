import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """ Custom clean command to tidy up the project root. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


class PrepublishCommand(setuptools.Command):
    """  Custom prepublish command. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('python setup.py clean')
        os.system('python setup.py sdist bdist_wheel')


setuptools.setup(
    cmdclass={
        'clean': CleanCommand,
        'prepublish': PrepublishCommand,
    },
    name='db-tqdm',
    version='1.1.4',
    url='https://github.com/jmgomezsoriano/db-tqdm',
    license='lGPLv3',
    author='José Manuel Gómez Soriano',
    author_email='jmgomez.soriano@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='A database tqdm process monitor with web user interface.',
    packages=setuptools.find_packages(exclude=['test']),
    package_dir={'dbtqdm': 'dbtqdm'},
    include_package_data=True,
    package_data={
        'dbtqdm': ['dbtqdm/templates/*'],
        'static': ['dbtqdm/static/*', 'dbtqdm/static/js/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "tqdm>=4.60,<5.0",
        "mysmallutils>=0.2.6,<2.0"
    ],
    entry_points={
        'console_scripts': [
            'dbtqdm=dbtqdm.server:main'
        ]
    }
)
