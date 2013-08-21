import os, sys, subprocess, tempfile
from datetime import datetime
from lazy import lazy

class RunCmd(object):
    '''
    Abstract class to launch a shell command, then wait for it to finish (a lot like 
    os.system()).  
    Subclasses must define:
    get_cmd()
    get_args()

    And may override:
    get_envion()
    '''

    @lazy
    def _ts(self):
        return datetime.now()

    _ts_format='%Y%b%d.%H.%m.%S'

    def __init__(self, name, pipeline):
        self.name=name
        self.pipeline=pipeline

    def run(self):
        if self.pipeline.dry_run or self.pipeline.dry_run:
            print '# %s' % self.name
            print self.cmd_string()
            print
            (self.pid, self.status)=(-1,-1)
            return
        
        os.chdir(self.pipeline.working_dir) 

        # fixme: make pipeline.run() do this?
        #   or keep this, so that individual cmds can set their own working_dir?

        # put in something about checking for readability of all input files...

        new_stdout=open(self._get_stdout(), 'w')
        new_stderr=open(self._get_stderr(), 'w')

        cmd=[self.get_cmd()]
        cmd.extend(self.get_args())
        retcode=subprocess.call(cmd, env=self.get_environ(),
                                stdout=new_stdout, stderr=new_stderr,
                                )
        new_stdout.close()      # don't know if these are necessary or not...
        new_stderr.close()      # ...but they don't seem to hurt

        self.retcode=retcode
        return retcode



        # could put something here about provenance
        # could also put something here about capturing stdout and stderr 

    def __get_output_fn(self, fn_type):
        return os.path.join(self.pipeline.output_dir,
                            '%s.%s.%s' % (self.name, self._ts.strftime(self._ts_format), fn_type))

    def _get_stdout(self):
        ''' return the name of the file to which to redirect stdout '''
        return self.__get_output_fn('stdout')
                            
    def _get_stderr(self):
        ''' return the name of the file to which to redirect stderr '''
        return self.__get_output_fn('stderr')

    def cmd_string(self):
        stuff=[self.get_cmd()]
        stuff.extend(self.get_args())
        return ' '.join(stuff)

    def get_environ(self):
        return {}


        
