from setuptools import setup


DESCRIPTION = """\
A package to simplify the creation and manipulation of recursive data \
structures."""


setup(
    name='recursive-abc',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Samuel Deslauriers-Gauthier',
    author_email='sam.deslauriers@gmail.com',
    url='https://github.com/sdeslauriers/recur',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='recursive data structure tree graph',
    packages=['recur'])
