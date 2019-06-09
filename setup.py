#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='emojinounce',
    version='0.1.0',
    description='A Slack emoji announcer',
    author='Jay Kline',
    author_email='jay@slushpupie.com',
    url='https://github.com/slushpupie/emojinounce',
    packages=find_packages(),
    install_requires=[
      'slackclient',
      'slackeventsapi'
    ],
    extras_require={
      'dev': [
        'flake8'
      ]
    }
)
