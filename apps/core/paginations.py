from rest_framework import pagination


class SmallResultPagination(pagination.PageNumberPagination):
    page_size = 5
