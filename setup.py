from setuptools import setup, find_packages

VERSION="1.0.0"
DESCRIPTION="Python binding for OpenHaptics"
LONG_DESCRIPTION="Basic functions to mimic the OpenHaptics library on C++. Written into a more Python friendly language"

setup(
    name="pyOpenHaptics",
    version=VERSION,
    author="Mikel De Iturrate Reyzabal",
    author_email="mikelitubiomed@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["haptics", "3dsystems"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)