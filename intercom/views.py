from django.http import HttpResponse
from . import models
from . import utils


def entry_point(request):
    intercom = utils.Intercom(request.get_host())
    intercom.greet()
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
            member = models.Member.objects.get(code=digits)
            intercom.notify_of_valid_code(member, digits)
        except models.Member.DoesNotExist:
            intercom.notify_of_invalid_code(digits)
            intercom.authenticate()

    response = HttpResponse(str(intercom), content_type='text/xml')
    return response
