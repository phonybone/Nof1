import sys, os, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args

def main(args):
    '''
    a mock-up of the rnaseq-counting pipeline, to be ported to SWF
    '''
    print args
    print
    '''
    maybe we should create all the commands ahead of time to insure that we can,
    and can therefore error out ahead of time.
    '''

    '''
    pid=run_bowtie2(args.data_basename, args.bt2_index)
    (pid, status)=os.waitpid(pid, 0)
    print 'bowtie2(%d): status=%s' % (pid, status)
    if status!=0:
        print 'status=%d: bailing!' % status
        sys.exit(status)
    '''

    pid=run_rnaseq_count(args.data_basename, args.ucsc2ll)
    (pid, status)=os.waitpid(pid, 0)
    print '%d: status=%s' % (pid, status)
    if status!=0:
        print 'status=%d: bailing!' % status
        sys.exit(status)
    sys.exit(0)

def run_bowtie2(data_basename, ref_index, bt2_index_dir):
    '''
    run bowtie; this will need refactoring
    '''
    bowtie2_index_dir=bt2_index_dir
    params={}
    params['bt2_exe']='/local/bin/bowtie2'
    params['index']=os.path.join(bowtie2_index_dir, ref_index)
    params['threads']='16'
    params['input1']='%s_1.fastq' % data_basename
    params['input2']='%s_2.fastq' % data_basename
    params['output']='%s.bt2.sam' % data_basename
    e={'bt2_indexes':bowtie2_index_dir}

    cmd='%(bt2_exe)s %(index)s -p %(threads)s -1 %(input1)s -2 %(input2)s -S %(output)s' % params
    print cmd
    print e
    
    pid=os.fork()
    if pid==0:              # child process: exec and don't return
        v=[]
        v.append(params['bt2_exe'])
        v.append(params['index'])
        v.append('-p')
        v.append(params['threads'])
        v.append('-1')
        v.append(params['input1'])
        v.append('-2')
        v.append(params['input2'])
        v.append('-S')
        v.append(params['output'])

        os.execve(params['bt2_exe'], v, e) # doesn't normally return
        raise Exception('"%s" failed' % cmd) 
        
    return pid

def run_rnaseq_count(data_basename, ucsc2ll):
    cmd='time  py bin/rnaseq_count.py  --in_fn data/test_rnaseq/rawdata/1047-COPD.100K.bt2.sam '
    params={}
    params['exe']='/users/vcassen/vpython2.7/bin/python'
    params['script']='bin/rnaseq_count.py'
    params['ucsc2ll']=ucsc2ll
    params['input']='%s.bt2.sam' % data_basename
    
    pid=os.fork()
    if pid==0:              # child process: exec and don't return
        v=[]
        v.append(params['exe'])
        v.append(params['script'])
        v.append('--ucsc')
        v.append(params['ucsc2ll'])
        v.append('--in_fn')
        v.append(params['input'])
        os.execv(params['exe'], v) # doesn't normally return
        raise Exception('"%s" failed' % cmd) 
        
    return pid


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'a mock-up of the rnaseq-counting pipeline, to be ported to SWF', 'rnaseq_pipeline_proto')
    main(args.args)

