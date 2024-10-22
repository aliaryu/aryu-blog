from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIRootView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "login": reverse("rest_framework:login", request=request),
            "user-list": reverse("user-list", request=request),

        })
