from django.db import models
from testpost import TestPost


class Case(models.Model):
    test_post = models.ForeignKey(TestPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    repeat_time = models.IntegerField(default=1)
    check_wait_time = models.IntegerField(default=1)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.name)
