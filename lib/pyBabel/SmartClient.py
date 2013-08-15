import os, types, cPickle
import pyBabel.Client as babel

class SmartClient(babel.Client):
    def __init__(self):
        super(SmartClient,self).__init__()
        self.tables={}


    def load(self, id_types):
        table=self._get_cache(id_types)
        maps=self._table2maps(id_types, table)
        self.tables.update(maps)
        self._make_funcs(id_types)
        return self

    def _cache_dir(self):
        cd=os.path.join(os.environ['HOME'], '.babel')
        if not os.path.exists(cd):
            os.makedirs(cd)
        return cd

    def _get_id_key(self, id_types):
        return '-'.join(id_types)

    def _get_cache_path(self, id_types):
        return os.path.join(self._cache_dir(), '%s.pkl' % self._get_id_key(id_types))

    def _get_cache(self, id_types):
        '''
        id_types: first entry is input type
        remaining entries are output types

        returns the table associated with the id_types (lol)

        could write something clever to see if id_types[1:] matches any superset
        already in cache...
        '''
        id_key=self._get_id_key(id_types)
        try:
            return self.tables[id_key]
        except KeyError:
            pass

        cp=self._get_cache_path(id_types)
        if os.path.exists(cp):
            with open(cp) as f:
                table=cPickle.load(f)
        else:
            print 'fetching from babel...'
            table=self.translateAll(input_type=id_types[0],
                                    output_types=id_types[1:])
            with open(cp, 'wb') as f:
                cPickle.dump(table, f)

        self.tables[id_key]=table
        return table
            

    def _table2maps(self, id_types, table):
        ''' take a list of lists, as returned by babel, and return '''
        in_type=id_types[0]

        # init maps:
        maps={}
        for out_type in id_types[1:]:
            key='%s2%s' % (in_type, out_type)
            maps[key]={}

        for line in table:
            in_val=line[0]
            # line[0] is input value, line[i>0] is output value:
            for out_type,out_val in zip(id_types[1:], line[1:]):
                key='%s2%s' % (in_type, out_type)
                maps[key][in_val]=out_val

        return maps

    def _make_funcs(self, id_types):
        in_type=id_types[0]
        for out_type in id_types[1:]:
            func_name='%s2%s' % (in_type, out_type)
            func=lambda self, in_val, : self.tables[func_name][in_val]
            setattr(self, func_name, types.MethodType(func, self))
