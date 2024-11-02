from django.shortcuts import redirect
from rest_framework.reverse import reverse


def redirect_to_api(request):
    return redirect(reverse("api-root", request=request))
