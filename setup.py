from setuptools import setup, find_packages
import os

setup(
    name="tanginas-cli",  # Konsisten dengan entry_points
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",  # Menentukan versi minimum untuk kejelasan
        "astor>=0.8.1",
        "pygments>=2.0.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "tanginas-cli = tanginas_cli.code_assistant:main",  # Pastikan nama modul sesuai
        ],
    },
    author="Kiki Ginanjar",
    author_email="kiki.jtk10@gmail.com",
    description="An advanced code assistant with AI capabilities",
    long_description=(
        open("README.md", encoding="utf-8").read()
        if os.path.exists("README.md")
        else ""
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/kikiginanjar16/tanginas-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
