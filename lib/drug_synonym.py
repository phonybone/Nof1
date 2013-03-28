from django.db import models

class DrugSynonym(models.Model):
    drug=modles.ForeignKey(Drug)
    synonym=Model.CharField(max_length=20)
