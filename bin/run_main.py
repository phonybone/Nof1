import unittest, sys, os, argparse
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(root_dir, 'lib'))

from nof1_args import Nof1Args
from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline
from Pipeline.host import Host
from Pipeline.exceptions import *


def main(args):
    host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
    host=Host(host_conf)

    try:
        p=Nof1Pipeline(host, args.working_dir, 
                       args.data_basename, 
                       args.ref_index, 
                       args.variants_fn,
                       output_dir=args.output_dir, 
                       dry_run=args.dry_run,
                       echo=not args.no_echo, 
                       skip_if_current=args.skip)

        if args.cmd:
            cmd=p.find_command(args.cmd)
            if not cmd: raise UnknownCommandException(p, args.cmd)
            return cmd.run_cmd()
        else:
            return p.run()

    except PipelineFailed, e:
        print 'Failed: %s' % e.cmd.name
        print '  see %s for details' % e.cmd.get_stderr()
        return 1

    except PipelineException, e:
        print e
        return 1

    return 0
            

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'run the Nof1 pipeline', 'run_main')
    sys.exit(main(args.args))

