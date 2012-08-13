import json
import hashlib
import hmac
import time
import base64
from django.conf import settings
from django.contrib import auth

class FacebookMiddleware:
    def process_request(self, request):
        # if this is a fist load in a Facebook iframe, then the request came as
        # a POST with a signed_request
        if u'signed_request' in request.POST:
            # ideally we should change the POST to a GET here since Facebook
            # always initiates the first canvas page load with a POST request
            # that should be a GET, unfortunately that's not possible in Django
            signed_request = request.REQUEST['signed_request']
            try:
                sig, payload = signed_request.split(u'.', 1)
                sig = self.base64_url_decode(sig)
                data = json.loads(self.base64_url_decode(payload))

                expected_sig = hmac.new(settings.FACEBOOK_APP_SECRET, msg=payload, digestmod=hashlib.sha256).digest()

                # allow the signed_request to function for upto 1 day
                if sig == expected_sig and data[u'issued_at'] > (time.time() - 86400):
                    user_id = data.get(u'user_id')
                    access_token = data.get(u'oauth_token')

                    if user_id:
                        user = auth.authenticate(user_id=user_id, access_token=access_token)
                        request.user = user
                        auth.login(request, user)
                        return None
                
            except ValueError:
                pass
            
            auth.logout(request)
            
        request.user = auth.get_user(request)
        return None
    
    def process_response(self, request, response):
        if settings.FACEBOOK_APP_TYPE == 'canvas':
            # set P3P header so that authentication for canvas apps could work in IE
            response[u'P3P'] = u'CP=HONK'
            return response
        else:
            return response
    
    def base64_url_decode(self, data):
        data = data.encode(u'ascii')
        data += '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data)

    def base64_url_encode(self, data):
        return base64.urlsafe_b64encode(data).rstrip('=')
            