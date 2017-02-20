from setuptools import setup
from thdriver.version import SHORT_VERSION
setup(
    name="thdriver",
    version=SHORT_VERSION,
url="https://github.com/thgcode/thdriver",
description="A socket abstraction library and a main loop for servers",
    author="Thiago Seus",
    author_email="thiago.seus@yahoo.com.br",
    packages = ["thdriver"])
