import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="dictmodel",
    version="0.1.0",
    author="yairv.dar",
    author_email="yairv.dar@gmail.com",
    description="Unified access to (almost) any file type local or s3",
    license="BSD",
    platforms=['any'],
    keywords="struct model json yaml jsonmodel dictmodel",
    url="http://pypy/dictmodel",
    packages=find_packages(),
    # exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # package_data={'cfg': [os.path.join('cfg', '*.yml')]},
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
