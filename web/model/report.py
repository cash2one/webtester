from django.db import models
from web.model.case import Case


class Report(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    store_path = models.CharField(max_length=1024)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.case.name)
