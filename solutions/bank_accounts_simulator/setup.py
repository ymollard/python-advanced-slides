from setuptools import setup, find_packages

setup(name='accounts-correction',
      version='1.0',
      description='Simulator of bank accounts transactions',
      license='GPL3',
      author='Bob Dupont',
      author_email='bob@example.com',
      url='https://advanced.python.training.aubrune.eu',
      description='This is the correction of the test package that we created during our training.'
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib'] # Dependencies to install
)

