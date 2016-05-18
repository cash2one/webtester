from django.db import models
from django.contrib.auth.models import User


class TestPost(models.Model):
    user_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=64)
    ext=models.TextField(max_length=1024)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.name)
