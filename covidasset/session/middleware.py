from django.contrib.auth import logout
from django.contrib import messages
import datetime

from django.conf import settings

class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        print("Middle Ware called")
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            
            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                (current_datetime - request.session['last_activity']).seconds > \
                settings.SESSION_IDLE_TIMEOUT:
                print("Session is valid")
                logout(request)
                messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
                print(request.session)
        return None
