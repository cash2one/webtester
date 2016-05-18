from django.db import models
from case import Case


class Action(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    xpath = models.CharField(max_length=128)
    action_type = models.CharField(max_length=16)
    input=models.CharField(max_length=1024)
    wait_time = models.IntegerField(default=0)
    ext=models.TextField(max_length=1024)

    def __unicode__(self):
        return "%d:%s:%s:%s" % (id, self.case.name, self.xpath, self.action_type)
