#!/usr/bin/env python
__author__ = 'bluzky'

# from distutils.core import setup
#
# setup(name='Domor',
#       version='1.0',
#       description='A simple pomodoro application for Linux user',
#       author='Dung , Nguyen Tien',
#       author_email='bluesky.1289@gmail.com',
#       url='http://www.kebano.net',
#       packages=['domor'],
#       install_requires=[
#           "pyglet",
#       ],
#       scripts=['domor/domor_indicator.py']
#       )

from setuptools import setup, find_packages
from glob import glob

setup(name='Domor',
      version='1.0',
      description='A simple pomodoro application for Linux user',
      author='Dung , Nguyen Tien',
      author_email='bluesky.1289@gmail.com',
      url='http://www.kebano.net',
      packages=find_packages(),
      install_requires=[
          "pyglet",
      ],
      package_data={"domor":['ui/*']},
      include_package_data=True,
      data_files=[('share/domor/img', glob("img/*")), ('share/domor/sound', glob('sound/*')), ('share/domor/ui', glob('ui/*'))],
      #scripts=['script/domor-indicator.py'],
      # other arguments here...
      entry_points={
          # 'console_scripts': [
          #     'foo = my_package.some_module:main_func',
          #     'bar = other_module:some_func',
          # ],
          'console_scripts': [
              'domor = domor.domor_indicator:start_app',
          ]
      },
      zip_safe= False,
      
      )
