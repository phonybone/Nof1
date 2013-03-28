from factory import factory

class DrugcardBuilderFactory(factory):
    aliases={'rdf':'drugcard_builder_rdf.DrugcardBuilderRdf',
             'django':'drugcard_builder_django.DrugcardBuilderDjango',
             }
    def __init__(self):
        pass
