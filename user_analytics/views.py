from django.views.generic import View
from django.http import HttpResponse
from tracking import register_event

class VerifyView(View):
    '''
    View called by javascript to verify that cookies are enabled along with javascript
    '''

    def post(self, request, *args, **kwargs):

        tracking_id = self.request.COOKIES.get('yb_user', None)
        register_event(tracking_id, event_name='VERIFY_COOKIE', request=self.request)
        response = HttpResponse('Verified')
        response.delete_cookie('yb_verify')

        return response

class RegisterEventView(View):
    '''
    View called by javascript to verify that cookies are enabled along with javascript
    '''

    def post(self, request, *args, **kwargs):

        event_name = self.request.POST.get('event_name', None)
        raw_event_data = self.request.POST.get('event_data', None)

        event_data = None

        if raw_event_data is not None:
            #truncate at 1024 character to avoid malicious content
            event_data = (raw_event_data[:1024] + '..') if len(raw_event_data) > 1024 else raw_event_data
        else:
            event_data = raw_event_data

        tracking_id = self.request.COOKIES.get('yb_user', None)
        register_event(tracking_id=tracking_id, event_name=event_name, request=self.request, event_data=event_data)
        response = HttpResponse('OK')

        return response