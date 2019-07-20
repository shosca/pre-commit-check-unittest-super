import os

from setuptools import setup


readme = os.path.join(os.path.dirname(__file__), "README.rst")

setup(
    name="pre-commit-check-unittest-super",
    version="0.1.0",
    description="Checks for super calls in unittest setup/teardown]",
    long_description=open(readme).read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
    author="Serkan Hosca",
    author_email="serkan@hosca.com",
    url="https://github.com/shosca/pre-commit-check-unittest-super",
    license="MIT",
    py_modules=("check_unittest_super", "tests"),
    zip_safe=False,
    install_requires=[],
    entry_points={"console_scripts": ["check-unittest-super = check_unittest_super:main"]},
)
