from setuptools import setup

setup(
    name='suffix-trees for covering similarity',
    packages=['STree4CS'],
    version='0.1',
    description='Suffix trees, generalized suffix trees for list of int and for covering similarity evaluation',
    author='Pierre-Francois Marteau',
    author_email='pierre-francois.marteau@univ-ubs.fr',
    url='https://github.com/pfmarteau/STree4CS',
    long_description=open('README.rst').read(),
    package_data={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
