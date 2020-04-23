from setuptools import setup, find_packages

setup(name='vizzero',
      version='0.0.1',
      url='',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=['numpy', 'scipy', 'websockets', 'pyside2', 'vispy==0.6.0', 'pyserial', 'brainflow', 'rx', 'pandas'],
      zip_safe=False)