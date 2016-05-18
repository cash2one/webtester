from django.db import models
from web.model.case import Case


class Check(models.Model):
    case = models.ForeignKey(Case, models.CASCADE)
    check_type = models.CharField(max_length=12)
    check_data = models.CharField(max_length=1024)
    check_result=models.IntegerField(default=0)
    ext=models.TextField(max_length=1024)

    def __unicode__(self):
        return "%d:%s:%s" % (self.id, self.case.name, self.check_type)
