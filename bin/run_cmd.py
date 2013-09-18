import sys, os, importlib, inspect, re
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(os.path.join(root_dir, 'lib'))

from nof1_args import Nof1Args
from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host

def main(args):
    if args.v: print args

    pl=get_pipeline(args)
    cls=get_cmd_class(args)

    needed=inspect.getargspec(cls.__init__)[0]
    cls_args={'pipeline': pl}
    
    pl_args=get_pipeline_args(args, needed)
    cls_args.update(pl_args)

    cmd=cls(**cls_args)
    print '# %s' % cmd.cmd_string()
    cmd.run()

    return 0


def get_pipeline(args):
    host=Host()
    p=Pipeline('mock', host, args.working_dir,
               dry_run=args.dry_run, output_dir=args.output_dir, echo=not args.no_echo, 
               skip_if_current=args.skip)
    return p

def get_cmd_class(args):
    mod_name='Nof1Pipeline.run_%s' % args.cmd_name
    cls_name='Run%s' % uscore2cc(args.cmd_name)
    print 'looking for %s.%s' % (mod_name, cls_name)
    mod=importlib.import_module(mod_name)
    cls=getattr(mod, cls_name)
    print 'found %s' % args.cmd_name
    return cls

def get_pipeline_args(args, arg_names):
    '''
    
    '''
    if not args.pipeline_args:
        args.pipeline_args=os.path.join(root_dir, 'inputs', '%s.args' % args.cmd_name)

    if os.path.exists(args.pipeline_args):
        import ConfigParser
        conf=ConfigParser.ConfigParser()
        conf.read(args.pipeline_args)
        d=dict(conf._sections['args'])
        print 'config\'d args: %s' % d
    else:
        d=vars(args)
                
    final_args={}
    for name in list(arg_names):
        print 'name is %s' % name
        try: 
            final_args[name]=d[name]
            print 'fa[%s]=%s' % (name, final_args[name])
        except KeyError: 
            print 'arg %s not found' % name
        except Exception, e:
            print 'caught %s: %s' % (type(e), e)
    return final_args


        

def cc2_(name):
    ''' 
    convert 'CamelCase' to 'camel_case'
    credit: http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case 
    '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def uscore2cc(name):
    '''
    convert 'camel_case' to 'CamelCase'
    credit: http://stackoverflow.com/questions/4303492/how-can-i-simplify-this-conversion-from-underscore-to-camelcase-in-python
    '''
    def camelcase(): 
#        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in name.split("_"))

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'show or run a pipeline command', 'run_cmd')
    sys.exit(main(args.args))
