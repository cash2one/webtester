from django.db import models
from .case import Case


class Action(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    xpath = models.CharField(max_length=1024)
    action_type = models.CharField(max_length=16)
    input=models.CharField(max_length=4096)
    wait_time = models.IntegerField(default=0)
    create_time=models.DateTimeField(auto_now=True)
    update_time=models.DateTimeField(auto_now=True)
    ext=models.TextField(max_length=1024)

    def __unicode__(self):
        return "%d:%s:%s:%s" % (id, self.case.name, self.xpath, self.action_type)
