import sys, os, re, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Variation
from dump_obj import dump

def main(args):
    print args
#    fix_leading_blank_dna_variation(args)
#    fix_protein_abbrvs(args)
    count_dups(args)

def fix_leading_blank_dna_variation(args):
    fuse=args.fuse

    for var in Variation.objects.all():
        var.dnaVariation=var.dnaVariation.strip()
        print var.dnaVariation
        var.save()
        
        fuse -= 1
        if fuse==0:
            break


def fix_protein_abbrvs(args):
    '''
    Ram wanted to change all the Leu's -> L, but it won't work because of Lys, Gln & Glu, Thr & Tyr, etc
    '''
    d={}
    for var in Variation.objects.all():
        prot_var=var.protVariation
        mg=re.search(r'^p\.([a-zA-Z]{3})\d+([a-zA-Z]{3})$', prot_var)
        if mg:
            p1=mg.group(1)
            p2=mg.group(2)
            print '%s: %s->%s, %s->%s' % (prot_var, p1[0], p1, p2[0], p2)
            for p in [p1,p2]:
                if p[0] not in d:
                    d[p[0]]=p
                else:
                    if d[p[0]] != p:
                        print 'ralph! %s: d[%s]=%s, p=%s' % (prot_var, p[0], d[p[0]], p)
                    else:
                        pass    # p already in d

        else:
            print 'barf: %s' % prot_var
    for k,v in d.items():
        print '%s -> %s' % (k,v)


def count_dups(args):
    ''' list all the dup entries in data_variation '''
    d={}
    for var in Variation.objects.all():
        k=str(var)
        try:
            d[k]+=1
        except KeyError:
            d[k]=1
    for k,v in d.items():
        if v==1: continue
        print '%s: %d' % (k,v)


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'fix mistakes entered in to the  variations db', 'fix_variations')
    main(args.args)

