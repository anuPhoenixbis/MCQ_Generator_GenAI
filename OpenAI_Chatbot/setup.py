from setuptools import setup, find_packages

setup(
    name="MCQ Generator",
    version="0.1",
    author="Anubhav Biswas",
    author_email="anubhavbiswas25@gmail.com",
    description="A tool to generate multiple choice questions from text using deepseek-r1 model.",
    install_requires=["openai", "langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages(), # Uses find_packages() to include all Python packages in your project directory.
)
#setup.py allows others (or you) to install your project and its dependencies easily with pip install . or similar commands.