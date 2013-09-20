import csv
from lazy import lazy

class Reporter(object):
    def __init__(self, host, genes):
        self.genes=set([x.upper() for x in list(genes)])
        self.BRCAness_list_fn=host.get('reporter.brcaness_list')
        self.core_fn=host.get('reporter.core_data')
        self.pathway_genes=('PTEN', 'TSC1', 'NF2')

        self.stats={'n_pathway':2,
                    'n_pathway_matches':0,
                    'n_core_matches':0,
                    'n_BRCAness_matches':0,
                }

    def report(self):
        return '%s\n%s\n%s\n' % (self.core_report(), 
                                 self.BRCAness_report(),
                                 self.pathway_report())

    @lazy
    def BRCAness_set(self):
        brcaness=set()
        with open(self.BRCAness_list_fn) as f:
            for line in f:
                brcaness.add(line.strip())
        self.stats['n_BRCAness']=len(brcaness)
        return brcaness

    @lazy
    def core_data(self):
        ''' return a dict of the core_data.csv file '''
        core={}
        with open(self.core_fn) as f:
            reader=csv.reader(f, delimiter=',')
            for row in reader:
                if row[0].startswith('#'): continue
                try:
                    (symbol, variant, annot, pmid)=row
                except ValueError:
                    continue
                core[symbol]={'variant':variant,
                              'annot':annot,
                              'pmid':pmid}

        self.stats['n_core']=len(core)
        return core

    def BRCAness_report(self):
        report=sorted(list(self.genes & self.BRCAness_set))
        self.stats['n_BRCAness_matches']=len(report)
        report.insert(0, '# BRCAness:')
        return '\n'.join(report)

    def core_report(self):
        report=[]
        for gene in self.genes:
            try:
                record=self.core_data[gene]
                report.append('\t'.join([gene, record['pmid'], record['annot']]))
            except KeyError:
                continue
        self.stats['n_core_matches']=len(report)
        report.insert(0, '# Core')
        return '\n'.join(report)

    def pathway_report(self):
        report=['# Pathway']
        if 'PTEN' in self.genes:
            report.append("The tumor harbors a deleterious mutation in the PTEN/PI3K pathway and thus may be sensitive to P13K, mTOR inhibitors")
            self.stats['n_pathway_matches']+=1

        if 'TSC1' in self.genes or 'NF2' in self.genes:
            report.append("The tumor harbors a deleterious mutation in TSC1 (or NF2) and thus may be sensitive to mTORC1 inhibitors like Everolimus")
            self.stats['n_pathway_matches']+=1

        return '\n'.join(report)

            
