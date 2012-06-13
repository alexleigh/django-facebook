import cgi
import urllib

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def login(request, template_name='facebook/login.html'):
    redirect_to = request.REQUEST.get('next', '')
    
    # if this is a POST request, it may have come from the client side authentication code
    if request.method == "POST":
        access_token = request.REQUEST.get('access_token', '')
        if access_token:
            user = auth.authenticate(access_token=access_token)
            request.user = user
            auth.login(request, user)
    
    # the user may have already been logged in by our Facebook middleware layer
    if request.user.is_authenticated():
        # Light security check: make sure redirect_to isn't garbage.
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        return HttpResponseRedirect(redirect_to)
        
    # this is for the client-side Facebook authentication workflow
    if settings.FACEBOOK_AUTH_TYPE == 'client':
        return render_to_response(template_name, context_instance=RequestContext(request))
    
    # this is for the server-side Facebook authentication workflow
    else:
        request.session['next'] = redirect_to
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'scope': settings.FACEBOOK_SCOPE,
            'redirect_uri': request.build_absolute_uri('/facebook/callback/'),
        }
        return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def callback(request):
    redirect_to = request.session.get('next', settings.LOGIN_REDIRECT_URL)
    
    code = request.GET.get('code')
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': request.build_absolute_uri('/facebook/callback/'),
        'code': code,
    }

    target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
    response = cgi.parse_qs(target)
    try:
        access_token = response['access_token'][-1]
        user = auth.authenticate(access_token=access_token)
        auth.login(request, user)
        # Light security check: make sure redirect_to isn't garbage.
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        
    except KeyError:
        redirect_to = settings.LOGIN_URL

    return HttpResponseRedirect(redirect_to)

def logout(request):
    access_token = ''
    if request.user.is_authenticated():
        access_token = request.user.facebookprofile.access_token
        auth.logout(request)
        args = {
            'access_token': access_token,
            'next': request.build_absolute_uri('/'),
        }
        return HttpResponseRedirect('https://www.facebook.com/logout.php?' + urllib.urlencode(args))
    
    else:
        auth.logout(request)
        return HttpResponseRedirect('/')
