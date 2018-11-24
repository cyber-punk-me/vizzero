from setuptools import setup, find_packages

setup(name='openbci-node-python-vis',
      version='0.0.1',
      description='Node to Python the right way',
      url='',
      author='AJ Keller',
      author_email='pushtheworldllc@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy', 'pyzmq', 'vispy'],
      zip_safe=False)