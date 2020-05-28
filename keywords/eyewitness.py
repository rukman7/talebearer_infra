#! /usr/bin/env python

from talebearer_infra.interfaces.shell_manager import shellController
from talebearer_infra.support_libraries import logger
from talebearer_infra.support_libraries.debug_decorators import DebugMetaClass
import os
import sys

class eyewitness(metaclass=DebugMetaClass):
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    ROBOT_LIBRARY_VERSION = '0.1'

    def __init__(self, outputdir, github_dir):
        self.session = shellController()
        self.outputdir = outputdir
        self.github_dir = github_dir

    def generateScreenshotsOfSubdomains(self, tool_dir, subdomain_file='subdomains.txt'):
        subdomains_path = os.path.join(self.outputdir, subdomain_file)
        logger.debug('subdomains path = {}'.format(subdomains_path))
        if os.path.exists(subdomains_path):
            tool = os.path.join(self.github_dir, tool_dir, 'Python/EyeWitness.py')
            output_dest = os.path.join(self.outputdir, 'EyeWitness')
            cmd = 'python3 {0} -f {1} --web -d {2} --no-prompt'.format(tool, subdomains_path, output_dest)
            logger.debug('command={}'.format(cmd))
            self.session.run_command(cmd)
        else:
            raise ValueError('subdomain file does not exist')
