from rest_framework.pagination import PageNumberPagination

class MaxResults(PageNumberPagination):
    permission_classes = []
    """
    BoardsPagination is used to override default pagination settings for boards.
    Included:
    max_results - url query paramteters to adjust return amounts of board results 
    page - default pagination query parameters
    """
    page_size = 20
    page_size_query_param = 'max_results'
    max_page_size = 100
