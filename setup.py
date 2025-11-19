from setuptools import setup, find_packages

setup(
    name="python_hardware_monitor",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "py-hardware-monitor = py-hwmonitor.main:main",
        ]
    },
    author="mocha1x",
    description="A lightweight GPU/CPU monitoring logger compatible with Windows, Linux, and macOS.",
)