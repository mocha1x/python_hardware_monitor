from setuptools import setup, find_packages

setup(
    name="python_hardware_monitor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["psutil"],
    author="mocha1x",
    keywords=['python', 'hardware', 'monitor', 'CPU', 'GPU', 'RAM', 'usage'],
    description="A lightweight GPU/CPU monitoring logger compatible with Windows, Linux, and macOS.",
    scripts=['py-hwmonitor/main.py']
)