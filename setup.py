from setuptools import setup, find_packages

setup(
    name="chess_engine",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'numpy',
        'chess',
        'pytest',
        'cairosvg',
        'python-chess'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A chess engine implemented in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)