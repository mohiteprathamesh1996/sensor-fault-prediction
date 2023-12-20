from setuptools import find_packages, setup


def get_requirements():
    """
    This function will return a list of requirements
    """
    
    with open("requirements.txt") as f:
        lines = f.read()
        
    list_packages = lines.split()

setup(
    name = "sensor",
    version = "0.0.1",
    author = "Prathamesh Mohite",
    author_email = "prathamesh.mohite96@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)