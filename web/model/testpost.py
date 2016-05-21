from django.db import models
from django.contrib.auth.models import User


class TestPost(models.Model):
    user_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=64)
    status=models.CharField(default='new submit',max_length=64)
    create_time=models.DateTimeField(auto_now=True)
    update_time=models.DateTimeField(auto_now=True)
    exec_log=models.TextField(max_length=4096,default=None)
    ext=models.TextField(max_length=1024,default=None)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.name)
