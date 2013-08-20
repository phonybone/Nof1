class PipelineException(Exception):
    pass

class NotImplementedException(PipelineException):
    pass

class AbstractMethodNotImplemented(NotImplementedException):
    pass

class MissingArgs(PipelineException):
    pass

class PipelineFailed(PipelineException):
    def __init__(self, pipeline, exp):
        self.pipeline=pipeline
        self.exp=exp

class CmdFailed(PipelineException):
    def __init__(self, run_cmd):
        self.run_cmd=run_cmd
