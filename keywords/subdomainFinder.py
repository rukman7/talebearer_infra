#! /usr/bin/env python

from talebearer_infra.interfaces.shell_manager import shellController
from talebearer_infra.support_libraries import logger
from talebearer_infra.support_libraries.debug_decorators import DebugMetaClass
from io import StringIO
import shutil
import os
import json

class subdomainFinder(metaclass=DebugMetaClass):
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    ROBOT_LIBRARY_VERSION = '0.1'

    def __init__(self, outputdir, github_dir):
        self.session = shellController()
        self.outputdir = outputdir
        self.github_dir = github_dir

    def createTempDir(self, dir_name='tempSubdomains'):
        path = '{0}/{1}'.format(self.outputdir, dir_name)
        try:
            os.mkdir(path, 0o755)
        except FileExistsError as e:
            logger.info('file already exists')
            pass
    
    def sublister(self, domain, tool_dir, dir_name='tempSubdomains'):
        cmd = 'python {0}/{1}/sublist3r.py -d {2} -o {3}/{4}/sublists.txt'.format(self.github_dir,tool_dir,\
                domain, self.outputdir, dir_name)
        logger.debug("command is {}".format(cmd))
        self.session.run_command(cmd)

    def amass(self, domain, dir_name='tempSubdomains'):
        cmd = 'amass enum -d {0} -o {1}/{2}/amass_scan.txt'.format(domain,self.outputdir, dir_name)
        logger.debug('command is {}'.format(cmd))
        self.session.run_command(cmd, ignore_errors=True)

    def subbrute(self, domain, tool_dir, dir_name='tempSubdomains'):
        current_dir = os.getcwd()
        os.chdir('{0}/{1}'.format(self.github_dir, tool_dir))
        cmd = 'python {0}/{1}/subbrute.py {2} -o {3}/{4}/subbrute_scan.txt'.format(self.github_dir, tool_dir, domain,\
                self.outputdir, dir_name)
        logger.debug('command is {}'.format(cmd))
        self.session.run_command(cmd, ignore_errors=True)
        of.chdir(current_dir)

    def knockpy(self, domain, tool_dir, dir_name='tempSubdomains'):
        cmd = 'python {0}/{1}/knockpy/knockpy.py -j {2}'.format(self.github_dir, tool_dir, domain)
        logger.debug('command is {}'.format(cmd))
        self.session.run_command(cmd, ignore_errors=True)
        #knockpy saves results in csv or json format. have to extract the subdomains from the result into a txt file
        files = os.listdir()
        for document in files:
            logger.info('{}'.format(domain.split('.')[0]))
            if domain.split('.')[0] in document:
                logger.info(document)
                json_data = {}
                with open(document, 'r') as json_file:
                    json_data = json.load(json_file)
                try:
                    json_data = json_data['found']['subdomain']
                    if json_data:
                        txt_stream = StringIO()
                        for entry in json_data:
                            txt_stream.write(entry+'\n')
                        with open('{0}/{1}/knockpy.txt'.format(self.outputdir, dir_name), 'w') as infile:
                            infile.write(txt_stream.getvalue())
                        source = os.getcwd()+'/'+document
                        destination = '{0}/{1}/{2}'.format(self.outputdir, dir_name, document)
                        logger.info('source = {}'.format(source))
                        logger.info('destination = {}'.format(destination))
                        try:
                            shutil.move(source, destination)
                        except Exception as e:
                            logger.debug('{}'.format(e))
                            pass
                        txt_stream.close()
                except Exception as e:
                    logger.debug('{}'.format(e))
                    pass




    def gatherAllSubdomains(self, dir_name='tempSubdomains', fileName='subdomains'):
        txt_stream = StringIO()
        unique_subdomains = set()
        path = '{0}/{1}'.format(self.outputdir,dir_name)
        logger.debug('{}'.format(path))
        logger.debug('{}'.format(os.path.isdir(path)))
        if os.path.isdir(path):
            logger.info('{}'.format(os.listdir(path)))
            try:
                    for item in os.listdir(path):
                        if '.txt' in item:
                            with open(path+'/'+item, 'r') as infile:
                                data = infile.readlines()
                                count = 0
                                for line in data:
                                    if '<BR>' in line:
                                        tmp = line.split('<BR>')
                                        for athing in tmp:
                                            if '\n' in athing:
                                                unique_subdomains.add(athing)
                                            else:
                                                unique_subdomains.add(athing+'\n')
                                    else:
                                        unique_subdomains.add(line)
                                    count = count + 1
                                logger.info('Entries returned by {0} = {1}'.format(item, count))    
            except Exception as e:
                logger.error(str(e))
        for subdomain in unique_subdomains:
            txt_stream.write(subdomain)
        try:
            with open(self.outputdir+'/'+fileName+'.txt', 'w') as infile:
                infile.write(txt_stream.getvalue())
        except Exception as e:
            logger.error(str(e))
            logger.debug('exception caused by writing to file')


    def deleteTempDir(self, delete=True, dir_name='tempSubdomains'):
        path = '{0}/{1}'.format(self.outputdir, dir_name)
        if delete:
            try:
                shutil.rmtree(path)
            except Exception as e:
                logger.debug(str(e))
                pass

