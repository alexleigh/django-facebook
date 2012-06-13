import urllib
import json

from django.contrib.auth.models import User
from facebook.models import FacebookProfile
from facebook.utils import url_safe_encode

class FacebookBackend:
    def authenticate(self, user_id=None, access_token=None):
        data = None
        if user_id is None:
            data = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
            data = json.load(data)
            user_id = data[u'id']
            
        try:
            # try to find the user
            fb_user = FacebookProfile.objects.get(facebook_id=user_id)
            user = fb_user.user

            # update access_token
            fb_user.access_token = access_token
            fb_user.save()

        except FacebookProfile.DoesNotExist:
            # user does not exist yet, get some more data and create a new user
            if data is None:
                data = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
                data = json.load(data)
                user_id = data[u'id']
            
            # use Facebook username if possible, but not all Facebook users
            # have usernames. In that case we still ensure the usernames are
            # unique
            username = ""
            email = ""
            if 'username' in data:
                username = data['username']
                if 'email' in data:
                    email = data['email']
                else:
                    email = data['username'] + "@facebook.com"
            elif 'email' in data:
                username = data['email'].split('@')[0] + url_safe_encode(long(user_id))
                email = data['email']
            else:
                username = "fbuid" + url_safe_encode(long(user_id))
                email = username + '@facebook.com'
            
            user = User.objects.create_user(username, email)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            # Create the FacebookProfile
            fb_user = FacebookProfile(user=user, facebook_id=user_id, access_token=access_token)
            fb_user.save()

        return user

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    supports_object_permissions = False
    supports_anonymous_user = False
