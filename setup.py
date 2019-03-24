from setuptools import find_packages, setup

setup(
    name="auto-water",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "tinydb",
        "markdown2",
        "adafruit-mcp3008",
        "Adafruit_GPIO",
        "gpiozero"
    ]
)
