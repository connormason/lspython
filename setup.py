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
              'git_checkout_radar=radarcltools.command_line:git_checkout_radar',
              'git_branch_radar=radarcltools.command_line:git_branch_radar',
              'create_phab_branch=radarcltools.command_line:create_phab_branch',
              'edit_radar=radarcltools.command_line:edit_radar',
              'get_assigned_radars=radarcltools.command_line:get_assigned_radars',
              'setup_background_refresh=radarcltools.command_line:setup_background_refresh',
          ],
      },
      zip_safe=False)