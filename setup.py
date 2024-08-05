from setuptools import setup, find_packages

# from pkg_resources import parse_requirements

# with open("requirements.txt", encoding="utf-8") as fp:
#     install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name="mcpi3",
    version="1.1.0",
    author="NONG DaJun",
    author_email="ndj8886@163.com",
    description="A library connect to Minecraft Pi3 Mod",
    long_description="A library connect to Minecraft Pi3 Mod",
    license="",
    url="https://github.com/nongdajun/mcpi3-python",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    packages=["mcpi3"]
)
