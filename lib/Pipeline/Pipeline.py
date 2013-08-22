import os, tempfile, logging
from .exceptions import *

class Pipeline(object):
    log=logging.getLogger(__name__)

    def __init__(self, name, host, working_dir, logger, dry_run=False, output_dir=None):
        self.name=name
        self.host=host
        self.working_dir=working_dir
        self.logger=logger
        self.output_dir=output_dir or working_dir
        self.dry_run=dry_run

    def __repr__(self):
        return 'Pipeline %s: working_dir=%s' % (
            self.name, 
            self.working_dir)

    def run(self):
        raise AbstractMethodNotImplementedException('Pipeline.Pipeline.run')

    def _run_cmd(self, cmd):
            retcode=cmd.run()
            if retcode != 0:
                self.log.debug('%s failed (retcode=%s), throwing exception' % (cmd.name, retcode))
                raise CmdFailed(cmd)
        
    def _run_cmds(self, *cmds):
        try:
            for cmd in cmds:
                self.log.debug('about to run %s' % cmd.name)
                self._run_cmd(cmd)
                self.log.debug('%s returned' % cmd.name)
        except CmdFailed, e:
            try: retcode=e.run_cmd.retcode
            except: retcode=None
            self.log.info("this failed (retcode=%s):\n%s" % (retcode, e.run_cmd.cmd_string()))
            self.log.info("see %s for details" % e.run_cmd._get_stderr())
            raise PipelineFailed(self, e)


    def _create_output_dir(self):
        try:
            with tempfile.TemporaryFile(dir=self.output_dir) as tmp:
                tmp.write('testing')
        except OSError, e:
            os.mkdir(self.output_dir) # fixme: could still fail...

