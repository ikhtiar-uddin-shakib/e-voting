from rest_framework.pagination import PageNumberPagination


class ElectionPagination(PageNumberPagination):
    page_size = 3
class PositionPagination(PageNumberPagination):
    page_size = 3
class VotePagination(PageNumberPagination):
    page_size = 3
class VoterPagination(PageNumberPagination):
    page_size = 3
class CandidatePagination(PageNumberPagination):
    page_size = 3
