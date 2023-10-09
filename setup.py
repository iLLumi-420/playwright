from setuptools import setup, find_packages

setup(
    name="practice",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.68.0", 
        "uvicorn==0.15.0", 
        "pytest-playwright" 
    ],
    author="Sandeep",
    author_email="email@example.com",
    description="A brief description ",
    url="https://github.com/your_username/your_project_name",
)




