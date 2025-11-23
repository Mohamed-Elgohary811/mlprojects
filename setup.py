from setuptools import find_packages, setup # setuptools: A Python library that helps you package your project so it can become an installable package,
                                            #             allowing you to upload it to PyPI or install it using pip.
from typing import List # find_packages(): Automatically searches for all folders that contain an __init__.py file and considers them as Python packages.


HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    #This function will return the list of requirements
    
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name='mlproject',
    version='0.0.1',
    author='Mohaemed Elgohary',
    author_email='mohamedegohary4@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    )