import os

from setuptools import setup, find_packages

from loadsheddingstatus.__init__ import __version__


def _package_files(directory: str, suffix: str) -> list:
    """
        Get all of the file paths in the directory specified by suffix.

        :param directory:
        :return:
    """

    paths = []

    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(suffix):
                paths.append(os.path.join('..', path, filename))

    return paths


# here - where we are.
here = os.path.abspath(os.path.dirname(__file__))

# read the package requirements for install_requires
with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    requirements = f.readlines()

# setup!
setup(
    name='eskom-loadshedding-status',
    description='Eskom Load Shedding Status Notification Bot',
    license='MIT',

    author='Leon Jacobs',
    author_email='leonja511@gmail.com',

    url='https://github.com/leonjza/eskom-loadshedding-status',
    download_url='https://github.com/leonjza/eskom-loadshedding-status/archive/' + __version__ + '.tar.gz',

    keywords=['eskom', 'loadshedding', 'status', 'bot'],
    version=__version__,

    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'loadsheddingstatus=loadsheddingstatus.cli:cli',
        ],
    },
)
