from Pipeline import Pipeline
from .run_bowtie2 import RunBowtie2
from .run_rnaseq_count import RunRnaseqCount
from .exceptions import *

class RnaseqBranch(Pipeline):
    '''
    this represents the Rnaseq branch of the Nof1 Pipeline.
    Not sure if we're still using it or not; definitely not finished as of 8/8/13.
    '''

    def __init__(self, 
                 host,          # host to run on
                 working_dir,   # directory to cd to; pathnames can be rel to this
                 data_basename, 
                 ref_index,
                 dry_run=False,
                 output_dir=None):
        super(RnaseqBranch, self).__init__('RnaseqBranch', host, working_dir, dry_run, output_dir)
        self.data_basename=data_basename
        self.ref_index=ref_index
        self.host=host
        self.working_dir=working_dir

        self.bt2=RunBowtie2(self, data_basename, ref_index)
        self.rc=RunRnaseqCount(self, data_basename)
        

    def run(self):
        try:
            retcode=self.bt2.run()
            print 'retcode is %s' % retcode
            if retcode != 0:
                raise CmdFailed(self.bt2)
            retcode=self.rc.run()
            print 'retcode is %s' % retcode
            if retcode != 0:
                raise CmdFailed(self.rc)
        except CmdFailed, e:
            print "this failed (retcode=%d):\n%s" % (e.run_cmd.retcode, e.run_cmd.cmd_string())
            print "see %s for details" % e.run_cmd._get_stderr()
            raise PipelineFailed(self, e)

    def outputs(self):
        return self.rc.outputs()
