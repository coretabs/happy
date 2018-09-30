from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 100

class PostsPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000

class CommentsPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000