import argparse, ConfigParser

class Nof1Args(object):
    def __init__(self, conf_fn, desc, name=None):
        self.conf_fn=conf_fn
        self.desc=desc
        conf=self._load_config()

        parser=argparse.ArgumentParser(description=self.desc)
        parser.add_argument('--root_dir', dest='root_dir', 
                            default=conf.get('DEFAULT', 'root_dir'),
                            help='name of root directory')
        parser.add_argument('--fuse', dest='fuse', default=-1, type=int,
                            help='internal fuse for debugging')
        parser.add_argument('--in_fn', help='input file')
        parser.add_argument('--collection_name', help='collection name', 
                            default=self.conf_val(conf, name, 'collection'))
        parser.add_argument('--db_name', help='database name',
                            default=conf.get('DEFAULT', 'db_name'))

        try:
            getattr(self, name)(parser)
        except Exception, e:
            pass
#            print 'caught "%s" on attempt to call %s' % (e, name)

        self.args=parser.parse_args()

    def conf_val(self, conf, section, key):
        sec=section if section else 'DEFAULT'
        try:
            return conf.get(sec, key)
        except ConfigParser.NoSectionError:
            try:
                return conf.get('DEFAULT', key)
            except ConfigParser.NoOptionError:
                return None

    def _load_config(self):
        conf=ConfigParser.ConfigParser()
        conf.read(self.conf_fn)
        return conf


    def rebuild_ttd(self, parser):
        parser.add_argument('--burn-lines', dest='burn_lines', default=10, type=int)


    def rebuild_db(self, parser): # db=drugbank, not database
        parser.add_argument('--builder', default='drugcard_builder_rdf.DrugcardBuilderRdf')

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


if __name__=='__main__':
    args=Nof1Args('nof1.conf', 'testing Nof1')
    print args.args


