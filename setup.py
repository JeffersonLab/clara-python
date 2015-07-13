#!/usr/bin/env python
'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)


setup(name='pClara',
      version='1.0',
      description='pClara',
      author='Vardan Gyurgyan',
      author_email='vardan@jlab.org',
      url='https://claraweb.jlab.org',
      test_suite="tests",
      tests_require=['pytest', 'xmsg>=2.0'],
      dependency_links=['git+https://git.earthdata.nasa.gov/scm/naiads/xmsg-python.git@v2.0#egg=xmsg-2.0'],
      cmdclass={'test': PyTest},
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                      "tests", "examples", "examples.*"]),
      package_dir={"pClara": "clara"},
      install_requires=['pyzmq>=14.5.0', 'protobuf>=2.6', 'enum34>=1.0.4']
      )

