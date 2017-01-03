from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='lspython',
      version='0.1',
      description='An implementation of the "ls" command in Python',
      long_description=readme,
      url='https://github.com/connormason/lspython',
      author="Connor Mason",
      author_email='connor@conmason.com',
      license="MIT",
      packages=find_packages(),
      install_requires=[
          'prettytable',
      ],
      entry_points = {
          'console_scripts': [
              'lspython=lspython.lspython:lspython'
          ],
      },
      zip_safe=False)