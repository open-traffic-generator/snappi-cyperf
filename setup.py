"""
To build distribution: python setup.py sdist bdist_wheel --universal
"""

import os
import setuptools

pkg_name = "snappi_cyperf"
version = "0.0.3"

# read long description from readme.md
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, "readme.md")) as fd:
    long_description = fd.read()
print(setuptools.find_packages())
setuptools.setup(
    name=pkg_name,
    version=version,
    description="The Snappi Cyperf Open Traffic Generator Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/open-traffic-generator/snappi-cyperf",
    author="dipendughosh",
    author_email="dipendu.ghosh@keysight.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="snappi cyperf testing open traffic generator automation",
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=2.7, <4",
    install_requires=["requests"],
    extras_require={
        "testing": [
            "pytest",
            "mock",
            "dpkt==1.9.4",
        ]
    },
)
