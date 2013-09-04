import os, sys
import logging, logging.config

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'lib'))


from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')
output_dir=os.path.join(root_dir, 'outputs')

logging.config.fileConfig(os.path.join(root_dir, 't', 'pipeline', 'logging.conf'))
log=logging.getLogger('Pipeline')
