from setuptools import setup, find_packages

setup(name='my_math',
      version='1.0',
      description='Simulator of bank accounts transaction',
      license='GPL3',
      author='Bob Dupont',
      author_email='example@example.com',
      url='https://advanced.python.training.aubrune.eu',
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib'] # Dependencies to install
)

