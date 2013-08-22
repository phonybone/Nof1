import argparse, ConfigParser, os
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Nof1Args(object):
    def __init__(self, conf_fn, desc, name=None):
        self.conf_fn=conf_fn
        self.desc=desc
        conf=self._load_config()
        self.conf=conf

        parser=argparse.ArgumentParser(description=self.desc)
        parser.add_argument('--root_dir', dest='root_dir', 
                            default=root_dir,
                            help='name of root directory')
        parser.add_argument('--fuse', dest='fuse', default=-1, type=int,
                            help='internal fuse for debugging')
        parser.add_argument('--in_fn', help='input file')
        parser.add_argument('--out_fn', help='output file', nargs='?')
        parser.add_argument('--collection_name', help='collection name', 
                            default=self.conf_val(name, 'collection'))
        parser.add_argument('--db_name', help='database name',
                            default=conf.get('DEFAULT', 'db_name'))
        parser.add_argument('-v', action='store_true', help='verbose')
        parser.add_argument('-d', action='store_true', help='debugging flag')
        parser.add_argument('--log', default='INFO', help='log level')
        self.parser=parser

        try:
            getattr(self, name)(parser) # get the function named 'name' and call it with parser as arg
        except Exception, e:
            print 'caught "%s" on attempt to call %s' % (e, name)

        self.args=parser.parse_args()

    def conf_val(self, section, key):
        sec=section if section else 'DEFAULT'
        try:
            return self.conf.get(sec, key)
        except ConfigParser.NoSectionError:
            try:
                return self.conf.get('DEFAULT', key)
            except ConfigParser.NoOptionError:
                return None

    def _load_config(self):
        conf=ConfigParser.ConfigParser()
        conf.read(self.conf_fn)
        return conf


    def rebuild_ttd(self, parser):
        parser.add_argument('--burn-lines', dest='burn_lines', default=10, type=int)
        parser.add_argument('--builder', default='django')
        parser.add_argument('--clear_table', action='store_true')
        parser.add_argument('--uniprot_gene_fn', default=self.conf_val('rebuild_ttd', 'uniprot_gene_fn'))

    def rebuild_db(self, parser): # db=drugbank, not database
        parser.add_argument('--builder', default='django')
        parser.add_argument('--clear_table', action='store_true')
        parser.add_argument('--uniprot_gene_fn', default=self.conf_val('rebuild_ttd', 'uniprot_gene_fn'))

    def query(self, parser):
        print 'query called'
        parser.add_argument('--collection', default='Drugcard')
        parser.add_argument('query', nargs='+')

    def gene2targets(self, parser):
        parser.add_argument('gene')
        parser.add_argument('--collection', default='graph')

    def path2targets(self, parser):
        parser.add_argument('path')
        parser.add_argument('--collection', default='graph')

    def overlap(self, parser):
        parser.add_argument('--uniprot_gene_fn', default=self.conf_val('rebuild_ttd', 'uniprot_gene_fn'))
        parser.add_argument('--gene2syn_fn', default=self.conf_val('rebuild_ttd', 'gene2syn_fn'))
        parser.add_argument('--samgenes_fn', default=self.conf_val('overlap', 'samgenes_fn'))
        parser.add_argument('--tripnegs_fn', default=self.conf_val('overlap', 'tripneggenes_fn'))
        
    def gene_report(self, parser):
        parser.add_argument('--tripnegs_fn', default=self.conf_val('overlap', 'tripneggenes_fn'))
        parser.add_argument('--gene2syn_fn', default=self.conf_val('rebuild_ttd', 'gene2syn_fn'))
        
    def oncotator(self, parser):
        parser.add_argument('--base_url', default=self.conf_val('oncotator', 'base_url'))

    def load_variations(self, parser):
        parser.add_argument('src')
        parser.add_argument('gene')
        parser.add_argument('--clear_table', action='store_true')

    def extract_trip_neg_details(self, parser):
        parser.add_argument('--auto_fn', help='auto-excepted variants filename')
        parser.add_argument('--poly_fn', help='poly-excepted variants filename')

    def rnaseq_count(self, parser):
        ucsc2ll=os.path.join(root_dir, 'data/ucsc/ucsc_kg2ll')
#        parser.add_argument('--ucsc2ll', default=ucsc2ll)
        parser.add_argument('--output_id_type', default='gene_ensembl') # must be babel-compliant

    def rnaseq_pipeline_proto(self, parser):
        parser.add_argument('--data_basename', default='data/rawdata/1047-COPD.10K')
        parser.add_argument('--bt2_index_dir', default=os.path.join(root_dir, 'data/bt2_indexes'))
        parser.add_argument('--bt2_index', default='hg19')
        parser.add_argument('--ucsc2ll', default='data/ucsc/ucsc_kg2ll')

    def kg_babel_overlap(self, parser):
        parser.add_argument('--kg', default=os.path.join(root_dir, 'data/ucsc/knownGene.txt'))
        parser.add_argument('--babel', default=os.path.join(root_dir, 'data/ucsc/ucsc_kg2entrez2sym.tsv'))

    def filter_vep(self, parser):
        pass

    def combine_rnaseq_vep(self, parser):
        parser.add_argument('gene_counts_fn')
        parser.add_argument('auto_fn')
        parser.add_argument('polyphen_sift_fn')

    def find_regions(self, parser):
        parser.add_argument('--delimiter', default='\t')

if __name__=='__main__':
    args=Nof1Args('nof1.conf', 'testing Nof1')
    print args.args


