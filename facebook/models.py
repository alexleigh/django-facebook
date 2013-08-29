import json, urllib

from django.db import models
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.CharField(max_length=30)
    access_token = models.CharField(max_length=245)
    
    def __unicode__(self):
        return self.facebook_id
    
    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)
