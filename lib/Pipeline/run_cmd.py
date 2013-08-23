import os, sys, subprocess, tempfile, logging
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

    log=logging.getLogger('Pipeline')

    def run(self):
        self.log.info('running %s' % self.name)
        if self.pipeline.dry_run or self.pipeline.echo:
            print '# %s' % self.name
            print self.cmd_string()
            print
            if self.pipeline.dry_run:
                (self.pid, self.status)=(-1,-1)
                self.log.info('dry_run is True: bye!')
                return 0            # success!
        
        os.chdir(self.pipeline.working_dir) 
        self.log.info("chdir\'d to %s" % self.pipeline.working_dir)
        self.log.info(self.cmd_string())

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
        self.log.info('retcode=%d' % retcode)
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
        env={'HOME':os.environ['HOME']}
        return env

        
