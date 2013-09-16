import sys, os, csv

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
import pyBabel.SmartClient as babel

'''
Combine the results of the RnaseqBranch and VEPBranch parts of the Nof1Pipeline
by taking the union of the two outputs of the VEPBranch, and then taking the 
intersection of those genes with those from the RnaseqBranch.  

The RnaseqBranch leaves its results as a .genes.out file, which contains ensembl
gene ids and their counts.

The VEPBranch leaves its results as two files: variants that were automatically
selected as interestings (.auto), and variants that passed the VEP filter (.poly).

This script converts all outputs to hugo (gene symbol) ids.
'''

def main(args):
    if args.v: print args

    babel_client=babel.SmartClient()
    babel_client.load(['gene_ensembl','gene_symbol'])

    # make a set of (expressed) gene symbols from the rnaseq_branch; (convert from ensembl->hugo) (rnaseq)
    # make a set of auto-selected genes from beginning of VEP (already in hugo) (auto)
    # make a set of polyphen/SIFT genes from end of VEP (convert from ensembl->hugo) (poly_sift)
    rnaseq=get_rnaseq(args, babel_client)
    auto=get_auto(args, babel_client)
    polyphen_sift=get_polyphen_sift(args, babel_client)
    
    # return intersection(union(auto, poly_sift), rnaseq)
    genes=(auto | polyphen_sift) & rnaseq # set ops, wheeee!
    with open(args.out_fn, 'w') as f:
        for g in genes:
            print g
    if args.v: 
        print '%s written' % args.out_fn
        print 'returning 0'
    return 0



def get_rnaseq(args, babel_client):
    rnaseq=set()
    with open(args.gene_counts_fn) as f:
        reader=csv.reader(f, delimiter=':')
        for row in reader:
            rnaseq.add(row[0])
    return rnaseq

def get_auto(args, babel_client):
    auto=set()
    with open(args.auto_fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for row in reader:
            hugo=row[0]
            auto.add(hugo)
    return auto

def get_polyphen_sift(args, babel_client):
    ps=set()
    with open(args.polyphen_sift_fn) as f:
        reader=csv.reader(f, delimiter=':')
        for row in reader:
            ensembl=row[4]
            hugo=babel_client.gene_ensembl2gene_symbol(ensembl)
            ps.add(hugo)
    return ps


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'combine the results of the RnaseqCount branch and the VEP branch', 'combine_rnaseq_vep')
    sys.exit(main(args.args))
