import os

class RunCmd(object):
    def __init__(self, dir):
        self.dir=dir

    def run(self):
        os.chdir(dir)
        pid=os.fork()
        if pid==0:
            os.execve(self.cmd, self.get_args(), self.get_environ()) # this should never return
            raise Exception('%s failed' % '\n'.join(cmd))

        (pid, status)=os.waitpid(pid, 0)
        return (pid, status)

    def cmd_string(self):
        stuff=[self.get_cmd()]
        stuff.extend(self.get_args())
        return ' '.join(stuff)
