from rest_framework import pagination


class CoinPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'size'
    max_page_size = 100
