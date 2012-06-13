from django.conf import settings

def facebook_settings(request):
    return {
        'XML_NAMESPACES' : 'xmlns:og="http://ogp.me/ns#" xmlns:fb="http://ogp.me/ns/fb#"',
        'FACEBOOK_APP_NAME' : settings.FACEBOOK_APP_NAME,
        'FACEBOOK_APP_ID' : settings.FACEBOOK_APP_ID,
        'FACEBOOK_APP_TYPE' : settings.FACEBOOK_APP_TYPE,
        'FACEBOOK_SCOPE' : settings.FACEBOOK_SCOPE,
    }
    
    