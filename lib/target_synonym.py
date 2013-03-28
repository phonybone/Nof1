from django.db import models

class TargetSynonym(models.Model):
    target=modles.ForeignKey(Target)
    synonym=Model.CharField(max_length=20)
