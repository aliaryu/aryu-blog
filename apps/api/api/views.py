from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIRootView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "login": reverse("rest_framework:login", request=request),
            "user-register": reverse("users:user-register", request=request),
            "token-obtain-pair": reverse("token-obtain-pair", request=request),
            "token-refresh": reverse("token-refresh", request=request),
            "token-blacklist": reverse("token-blacklist", request=request),
            "user-list": reverse("users:user-list", request=request),
            "post-list": reverse("blog:post-list", request=request),
            "schema": reverse("schema", request=request),
            "schema-swagger-ui": reverse("swagger-ui", request=request),
            "schema-redoc": reverse("redoc", request=request),
        })
