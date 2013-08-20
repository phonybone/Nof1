import unittest, sys, os, re
from cStringIO import StringIO
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
print 'root: %s' % root_dir
sys.path.append(os.path.join(root_dir, 'lib'))
for d in sys.path:
    if os.path.exists(os.path.join(d,'Pipeline','MainPipeline.py')):
        print 'found in %s' % d
import Pipeline
print 'Pipeline: %s' % dir(Pipeline)
print 'Pipeline.__file__: %s' % Pipeline.__file__

import Pipeline.Pipeline
print 'Pipeline.Pipeline.__file__: %s' % Pipeline.Pipeline.__file__

from Pipeline.run_vep import RunVep

