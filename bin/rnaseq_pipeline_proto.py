import sys, os, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Knowngene


def main(args):
    '''
    a mock-up of the rnaseq-counting pipeline, to be ported to SWF
    '''
    print args

    '''
    maybe we should create all the commands ahead of time to insure that we can,
    and can therefore error out ahead of time.
    '''


    try:
        pid=run_bowtie(args.data_basename, args.bt_index)
    except Exception, e:
        print 'caught %s' % e
        sys.exit(pid)

    #    (pid, status)=waitpid(pid, 0)
    #    print '%d: status=%s' % (pid, status)

    '''
    pid=run_rnaseq_count(args.data_basename, args.ucsc2ll)
    (pid, status)=waitpid(pid, 0)
    print '%d: status=%s' % (pid, status)
    '''

    def run_bowtie(data_basename, ref_index):
        '''
        run bowtie; this will need refactoring
        '''
        params['bt2_exe']='/local/bin/bowtie2'
        params['index']=ref_index
        params['threads']='-p 16'
        params['input']='-1 %s._1.fastq -2 %s._2.fastq' % (data_basename, data_basename)
        params['output']='-S %s.bt2.sam' % data_basename
        cmd='%(bt2_exe)s %(index)s %(threads)s %(input)s %(output)s' % params
        print cmd
        
        pid=os.fork()
        if pid==0:              # child process: exec and don't return
            v=[]
            v.append(params['index'])
            v.append(params['threads'])
            v.append(params['input'])
            v.append(params['output'])
#            os.execv(params['bt2_exe'], v) # doesn't normally return
            raise Exception('"%s" failed' % cmd) 

        return pid

    def run_rnaseq_count(data_basename, ucsc2ll):
        cmd='time  py bin/rnaseq_count.py  --in_fn data/test_rnaseq/rawdata/1047-COPD.100K.bt2.sam '
        params['exe']='python'
        params['script']='bin/rnaseq_count.py'
        params['ucsc2ll']=ucsc2ll
        params['input']='--in_fn %s.bt2.sam' % data_basename
        params['output']='--out_fn %s.gene_count' % data_basename


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'a mock-up of the rnaseq-counting pipeline, to be ported to SWF', 'rnaseq_pipeline_proto')
    main(args.args)

