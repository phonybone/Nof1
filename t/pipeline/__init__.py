import os, sys
import logging, logging.config

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'lib'))


from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline
from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')
output_dir=os.path.join(root_dir, 'outputs')

log=logging.getLogger('Nof1Pipeline')
