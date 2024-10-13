from setuptools import setup, find_packages

setup(
    name="smig_trader",
    version="0.1.0",
    description="A trading package for interacting with Alpaca APIs",
    author="Mitch Murphy",
    author_email="mitch.murphy@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "alpaca-py",
        "httpx",
        "prophet",
        "autots",
        "darts",
        "pyql",
        "pandas",
        "finta",
        "matplotlib",
        "mplfinance",
        "backtesting",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
