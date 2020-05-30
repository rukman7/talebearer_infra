#! /usr/bin/env python

from talebearer_infra.interfaces.shell_manager import shellController
from talebearer_infra.support_libraries import logger
from talebearer_infra.support_libraries.debug_decorators import DebugMetaClass
import os

class subdomainTakeover(metaclass=DebugMetaClass):
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    ROBOT_LIBRARY_VERSION = '0.1'

    def __init__(self, outputdir, github_dir=None):
        self.session = shellController()
        self.outputdir = outputdir
        self.github_dir = github_dir

    def __populate_cmd(self, cmd, args, kwargs, args_list, kwargs_list):
        for arg in args:
            if arg in args_list:
                cmd += ' -'+arg
        for k, v in kwargs.items():
            if k in kwargs_list:
                cmd +=' -'+k+' '+v
        return cmd

    def subover(self, *args, **kwargs):
        '''
        args & kwargs: command line arguments the tool supports.
        '''
        args_list = ['a','v','https']
        kwargs_list = ['l','t','timeout']
        mandatory_things = ['l','output_file']
        
        try:
             os.chdir(os.path.join(os.environ['HOME'], 'go-workspace/bin'))
        except Exception as e:
            logger.error('unable to change current working directory')

        logger.info('current working directory={}'.format(os.getcwd()))

        cmd = 'SubOver'
        for entry in mandatory_things:
            if entry not in kwargs:
                raise ValueError('mandatory parameter [{}] not provided'.format(entry))

        cmd = self.__populate_cmd(cmd, args, kwargs, args_list, kwargs_list)

        if not os.path.exists(kwargs['l']):
            raise ValueError('provided subdomains file not found.')

        logger.info('command={}'.format(cmd))
        output = self.session.run_command(cmd, ignore_errors=True, ret=True)
        #this tools doen't doesn't provide option to get result in a text file
        output_file = os.path.join(self.outputdir, kwargs['output_file'])
        with open(output_file, 'w') as infile:
            if output:
                infile.write(output)
        if 'v' not in args and len(output) > 200:
            raise ValueError('found vulnerable subdomains...')

    def subjack(self, *args, **kwargs):
        '''
        args & kwargs: list of command line arguments the tool supports.
        '''
        args_list = ['ssl','a','m','c']
        kwargs_list = ['w','t','timeout','o']
        if 'w' not in kwargs:
            raise ValueError('path of file containing list of subdomains should be provided.')
        logger.info('{}'.format(kwargs['w']))
        if not os.path.exists(kwargs['w']):
            raise ValueError('provided subdomains file not found.')
        cmd = 'subjack'
        cmd = self.__populate_cmd(cmd, args, kwargs, args_list, kwargs_list)
        logger.info('command={}'.format(cmd))
        self.session.run_command(cmd, ignore_errors=True)

