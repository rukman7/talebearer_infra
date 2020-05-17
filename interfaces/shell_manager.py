from talebearer_infra.support_libraries.debug_decorators import DebugMetaClass
from talebearer_infra.support_libraries import logger
import subprocess
import json

class shellController(metaclass=DebugMetaClass):
    def __init__(self):
        pass

    def run_command(self, command, ignore_errors=False):
        process = subprocess.Popen(command.split(" "), stdout =
            subprocess.PIPE, stderr = subprocess.PIPE)
        output, error = process.communicate()
        logger.info('output = {}, error = {}'.format(output.decode('utf-8'), error.decode('utf-8')))
        if not ignore_errors:
            if len(error.decode('utf-8')) > 0:
                raise

