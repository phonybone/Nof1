from __future__ import unicode_literals
from django.db import models

class Drug(models.Model):
    id=models.CharField(max_length=12, primary_key=True)
    name=models.CharField(max_length=30)
    primary_acc=models.CharField(max_length=30)
    approval=models.CharField(max_length=30)
    condition=models.CharField(max_length=50)
    src=models.CharField(max_length=3)

    approvals=['Approved', 'Approved by FDA as orphan drug', 'Approved Orphan drug', 'Launched']

    def __unicode__(self):
        return 'drug %s (%s, %s, %s)' % (self.name, self.id, self.primary_acc, self.src)
               

class DrugSynonym(models.Model):
    drug=models.ForeignKey(Drug)
    synonym=models.CharField(max_length=20)

    def __unicode__(self):
        return '%s -> %s' % (self.drug, self.synonym)

class DrugPathway(models.Model):
    name = models.CharField(max_length=50)
    drug = models.ForeignKey(Drug)

    def __unicode__(self):
        return 'pathway %s (%s)' % (self.name, self.drug)


class Target(models.Model):
    id=models.CharField(max_length=12, primary_key=True)
    name=models.CharField(max_length=30)
    drugs=models.ManyToManyField(Drug)
    reaction=models.CharField(max_length=255)
    uniprot_id=models.CharField(max_length=20)
    gene_sym=models.CharField(max_length=12)
    src=models.CharField(max_length=3)

    def __unicode__(self):
        return 'target: %s (id=%s, %s)' % (self.name, self.id, self.src)

class TargetSynonym(models.Model):
    target=models.ForeignKey(Target)
    synonym=models.CharField(max_length=20)

    def __unicode__(self):
        return self.synonym

class TargetPathway(models.Model):
    name = models.CharField(max_length=50)
    target = models.ForeignKey(Target)

    def __unicode__(self):
        return 'pathway %s (%s)' % (self.name, self.target)

class OncotatorGene(models.Model):
    name = models.CharField(max_length=10)
    full_name=models.CharField(max_length=255)
    chr = models.CharField(max_length=2)
    location = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)


class UniprotProtein(models.Model):
    id=models.CharField(max_length=12, primary_key=True)
    gene = models.ForeignKey(OncotatorGene)
    

class Variation(models.Model):
    dnaVariation=models.CharField(max_length=16)
    protVariation=models.CharField(max_length=16)
    assay=models.CharField(max_length=32)
    gene=models.CharField(max_length=8)
    source=models.CharField(max_length=8)

    def __unicode__(self):
        return '-'.join([self.dnaVariation, self.protVariation, self.assay, self.gene, self.source])

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Knowngene(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    chrom = models.CharField(max_length=255, db_index=True)
    strand = models.CharField(max_length=1)
    txstart = models.IntegerField(db_column='txStart', db_index=True) # Field name made lowercase. This field type is a guess.
    txend = models.IntegerField(db_column='txEnd', db_index=True) # Field name made lowercase. This field type is a guess.
    cdsstart = models.IntegerField(db_column='cdsStart') # Field name made lowercase. This field type is a guess.
    cdsend = models.IntegerField(db_column='cdsEnd') # Field name made lowercase. This field type is a guess.
    exoncount = models.IntegerField(db_column='exonCount') # Field name made lowercase. This field type is a guess.
    exonstarts = models.TextField(db_column='exonStarts') # Field name made lowercase. This field type is a guess.
    exonends = models.TextField(db_column='exonEnds') # Field name made lowercase. This field type is a guess.
    proteinid = models.CharField(max_length=40, db_column='proteinID') # Field name made lowercase.
    alignid = models.CharField(max_length=255, db_column='alignID') # Field name made lowercase.
    class Meta:
        db_table = 'knownGene'

    def unicode(self):
        return self.name
