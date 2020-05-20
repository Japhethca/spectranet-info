from distutils.core import setup

setup(
    name="Spectranet Account Details Logger",
    description="A cli tool or library for displaying spectranet account details",
    version="0.1",
    author="Chidiebre Anyigor",
    author_email="chidiebere.anyigor@gmail.com",
    py_modules=["spectranet"],
    keywords="spectranet data bundle",
    install_requires=["requests", "lxml", "simple-chalk", "terminaltables"],
)
