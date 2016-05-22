from django.db import models
from testpost import TestPost


class Case(models.Model):
    test_post = models.ForeignKey(TestPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    repeat_time = models.IntegerField(default=1)
    check_wait_time = models.IntegerField(default=1)
    browsers = models.CharField(max_length=128)
    browser_window_size = models.CharField(max_length=128)
    screen_resolution = models.CharField(max_length=128)
    browser_scroll_position = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    ext = models.TextField(max_length=1024)

    def __unicode__(self):
        return "%d:%s" % (self.id, self.name)
