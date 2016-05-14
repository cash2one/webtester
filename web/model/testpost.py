from django.db import models
from django.contrib.auth.models import User


class TestPost(models.Model):
    user_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=512)
    browsers = models.CharField(max_length=128)
    browser_high_width = models.CharField(max_length=128)
    browser_window_position = models.CharField(max_length=128)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.name)
