import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="novation-launchpad",
    version="1.0.0",
    author="Eduardo Avelar",
    author_email="eavelardev@gmail.com",
    description="A Python library for launchpad mini, mk2 and pro devices with examples.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eavelardev/novation-launchpad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = ["python-rtmidi"]
)
