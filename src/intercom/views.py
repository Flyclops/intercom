from django.http import HttpResponse
from django.utils import timezone
from . import models
from . import utils


def entry_point(request):
    intercom = utils.Intercom(request.get_host())
    intercom.greet()
    # intercom.authenticate()

    response = HttpResponse(str(intercom), content_type='text/xml')
    return response

def authenticate(request):
    intercom = utils.Intercom(request.get_host())
    intercom.authenticate()
    
    response = HttpResponse(str(intercom), content_type='text/xml')
    return response

def authenticate_member(request):
    intercom = utils.Intercom(request.get_host())
    digits = request.REQUEST.get('Digits')

    if digits == '0':
        intercom.send_to_front_desk()

    else:
        try:
            member = models.Member.objects.get(code=digits, active=True)

            now = timezone.now()
            if member.is_allowed_access(now):
                intercom.notify_of_valid_code(member, digits)
                member.access()
            else:
                intercom.send_to_front_desk()

        except models.Member.DoesNotExist:
            intercom.notify_of_invalid_code(digits)

    response = HttpResponse(str(intercom), content_type='text/xml')
    return response
