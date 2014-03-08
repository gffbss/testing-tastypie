from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):
    # user is many to media
    file_name = models.FileField(upload_to="static/media", null=True, blank=True)
    name = models.CharField(max_length=100)
    upload_date = models.DateField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name




