#!/usr/bin/env python
#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
import os

from distutils.core import setup, Command
from distutils.command.clean import clean
from distutils.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import find_packages


class claraTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)


class claraClean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


class claraInstall(install):

    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

if __name__ == "__main__":
    setup(name='clara-python',
          version='2.0',
          description='Clara Framework for python',
          author='Ricardo Oyarzun',
          author_email='royarzun@gmail.com',
          url='https://claraweb.jlab.org',
          test_suite="tests",
          tests_require=['pytest', 'xmsg>=2.3'],
          dependency_links=['git+ssh://git@git.earthdata.nasa.gov:7999/naiads/xmsg-python.git@v2.3#egg=xmsg-2.3'],
          cmdclass={
              'test': claraTest,
              'clean': claraClean,
          },
          packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                          "tests", "examples", "examples.*"]),
          package_dir={"pClara": "clara"},
          install_requires=['xmsg>=2.3', 'simplejson>=3.8.0'],
          scripts=['bin/unix/p_dpe']
          )
