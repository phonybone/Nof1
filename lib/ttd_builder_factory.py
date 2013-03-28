from factory import factory

class TtdBuilderFactory(factory):
    aliases={'rdf':'ttd_builder_rdf.TtdBuilderRdf',
             'django':'ttd_builder_django.TtdBuilderDjango',
             'sqlite':'ttd_builder_sqlite.TtdBuilderSqlite'}
