from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(name='check_workspace',
      version='0.1',
      description='utilities for plotting in ROOT',
      url='https://github.com/xju2/check_workspace',
      long_description=readme,
      author='Xiangyang Ju',
      author_email='xiangyang.ju@gmail.com',
      license=license,
      packages=['check_workspace'],
      zip_safe=False
     )
