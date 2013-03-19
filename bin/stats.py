import os, sys
rootdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(os.path.join(rootdir, 'lib'))

from dao_mongo import dao_mongo
from histo import Histogram
from drugcard import Drugcard

def main(args):
    print args
    
    dc_dao=dao_mongo(cls=Drugcard, db='nof1')
    drug_histo=Histogram()
    pw_histo=Histogram()
    gene_histo=Histogram()
   
    for dc in dc_dao.iter({'_cls':'drugcard.Drugcard'}):
#        print 'dc %s' % dc.id
        if not dc.Drug_Type:
            continue
        if not ('Approved' in dc.Drug_Type or 'Biotech' in dc.Drug_Type):
            continue

        try:
            drug_histo.add(dc.Generic_Name[0])
        except IndexError:
            print "no Generic_Name for %s" % dc.id

        for pw in dc.Pathways:
            pw_histo.add(pw)

            for target in dc.targets:
                try:
                    for pw in target.Pathway:
                        pw_histo.add(pw)
                except AttributeError, e:
                    print "no Pathway for pw id=%s" % target.ID

                try:
                    for gene in target.Gene_Name:
                        gene_histo.add(gene)
                except AttributeError, e:
                    print "no Gene_Name for pw id=%s" % target.ID


#    print pw_histo
    print '%d distinct generic names' % len(drug_histo)
    print '%d distinct pathways' % len(pw_histo)
    print '%d distinct genes' % len(gene_histo)

    # count distinct pathways (Drug_Target_n_Pathway)
    # count distinct genes (Drug_Target_n_GeneName)
    # count distinct Generic_Name
    

if __name__=='__main__':
    from nof1_args import Nof1Args
    conf_fn=os.path.join(rootdir, 'nof1.conf')
    args=Nof1Args(conf_fn, 'script to compile stats about Nof1 dbs')
    main(args.args)
