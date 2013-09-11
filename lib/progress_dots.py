import sys

class ProgressDots(object):
    def __init__(self, pings_per_dot, dot_char='.', new_line='\n', dots_per_line=50, msg=None):
        self.pings_per_dot=pings_per_dot
        self.dot_char=dot_char
        self.new_line=new_line
        self.counter=0
        self.dots_per_line=dots_per_line
        self.msg=msg
        self.n_dots=0

    def ping(self):
        self.counter+=1
        if self.counter % self.pings_per_dot == 0:
            sys.stdout.write('.')
            self.n_dots+=1
            if self.n_dots % self.dots_per_line == 0:
                msg=self.msg if self.msg else ''
                sys.stdout.write(' %-15d%s\n' % self.counter, msg)
                self.n_dots=0
            sys.stdout.flush()
