from setuptools import setup, find_packages

from src.newline_tools import (
    __program__,
    __version__,
    __description__,
    __author__,
    __email__,
    __url__,
)


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=__program__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=__url__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tqdm',
        'profusion',
    ],
    entry_points={
        'console_scripts': [
            'newline=newline_tools.__main__:main',
        ],
    },
)