from collections import OrderedDict, namedtuple

from rest_framework.response import Response
from rest_framework import pagination

# TODO: implement pagination

class APILimitOffsetPagination(pagination.LimitOffsetPagination):

    paginate_by = 2
    max_limit = 2
    default_limit = 2

    def get_paginated_response(self, data):

        meta = OrderedDict([
            ('offset', self.offset),
            ('limit', self.limit),
            ('total_count', self.count),
            ('next', _strip_host(self.get_next_link())),
            ('previous', _strip_host(self.get_previous_link())),
        ])

        return Response(OrderedDict([('meta', meta), ('objects', data)]))


    def get_results(self, data):
        print("Ho ho ho!")
        return data['objects']
