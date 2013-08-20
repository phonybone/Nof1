import os, sys

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
    def __init__(self, name, pipeline):
        self.name=name
        self.pipeline=pipeline

    def run(self):
        if self.pipeline.dry_run or self.pipeline.host.get('dry_run').lower()=='true':
            print '# %s' % self.name
            print self.cmd_string()
            print
            (self.pid, self.status)=(-1,-1)
            return
        
        print self.cmd_string()

        os.chdir(self.pipeline.working_dir) # fixme: make pipeline.run() do this?

        # put in something about checking for readability of all input files...

        pid=os.fork()
        if pid==0:
            os.execve(self.get_cmd(), self.get_args(), self.get_environ()) # this should never return
#            raise Exception('%s failed' % '\n'.join(cmd))
            raise CmdFailed(self)

        (self.pid, self.status)=os.waitpid(pid, 0)

        # could put something here about provenance
        # could also put something here about capturing stdout and stderr 



    def cmd_string(self):
        stuff=[self.get_cmd()]
        stuff.extend(self.get_args())
        return ' '.join(stuff)

    def get_environ(self):
        return {}


        
