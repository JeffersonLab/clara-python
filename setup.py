#!/usr/bin/env python
# coding=utf-8

import os
import clara
from distutils.core import setup, Command
from setuptools.command.test import test as TestCommand
from setuptools import find_packages


class ClaraTest(TestCommand):

    test_args = []
    test_suite = True

    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)


class ClaraClean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./.cache ./.eggs ./build ./dist')
        os.system('rm -vrf ./*.tgz ./*.egg-info')
        os.system('find . -name "*.pyc" -exec rm -vrf {} \;')
        os.system('find . -name "__pycache__" -exec rm -rf {} \;')

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as license_file:
    LICENSE = license_file.read()

if __name__ == "__main__":
    setup(name='clara',
          version=clara.__version__,
          description='Clara Framework for python',
          author='Ricardo Oyarzun',
          author_email='oyarzun@jlab.org',
          url='https://claraweb.jlab.org',
          license=LICENSE,
          long_description=README,
          install_requires=['xmsg>=2.4.7'],
          test_suite="tests",
          tests_require=['pytest', 'xmsg'],
          cmdclass={
              'test': ClaraTest,
              'clean': ClaraClean,
          },
          packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                          "tests", "examples", "examples.*"]),
          package_dir={"clara": "clara"},
          scripts=['clara/scripts/unix/p_dpe']
          )
