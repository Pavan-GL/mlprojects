from setuptools import find_packages, setup
from typing import List

"""setup(
    name='mlproject',
    version='0.01',
    author='Pavan',
    author_email='pavanglsmg@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',          # Example dependency
        'pandas',         # Example dependency
        'scikit-learn',   # Example dependency
        # Add other dependencies as needed
    ],
)"""

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    This function return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


    pass


setup(
    name='mlproject',
    version='0.01',
    author='Pavan',
    author_email='pavanglsmg@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt')
)
