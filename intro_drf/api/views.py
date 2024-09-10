from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Institutions, Reports, Metadata
from .serializers import InstitutionsSerializer, ReportsSerializer, MetadataSerializer
from rest_framework.permissions import IsAuthenticated
import urllib.parse
import logging


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CachedListView(ListAPIView):
    cache_timeout = 60

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        result = cache.get(cache_key)
        
        if not result:
            logger.info('Cache miss. Querying the database.')
            queryset = self.filter_queryset(self.get_queryset())

            serializer = self.get_serializer(queryset, many=True)
            result = serializer.data

            cache.set(cache_key, result, self.cache_timeout)
            logger.info('Data cached successfully.')
        else:
            logger.info('Cache hit. Retrieving data from cache.')

        return Response(result)

    def get_cache_key(self):
        view_name = self.__class__.__name__
        params = self.request.query_params.dict()
        # Sort the parameters to ensure consistent ordering
        sorted_params = sorted(params.items())
        # Encode parameters to make the cache key URL-safe
        encoded_params = urllib.parse.urlencode(sorted_params)
        return f"{view_name}:{encoded_params}"


class InstitutionsView(CachedListView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        symbol = self.request.query_params.get('symbol', None)
        institution_name = self.request.query_params.get('name', None)

        query = Q()

        if symbol:
            symbol_list = symbol.split(',')
            symbol_query = Q()
            for sym in symbol_list:
                symbol_query |= Q(symbol__icontains=sym)
            query &= symbol_query

        if institution_name:
            institution_name_list = institution_name.split(',')
            institution_name_query = Q()
            for name in institution_name_list:
                institution_name_query |= (
                    Q(top_sellers__icontains=name) | 
                    Q(top_buyers__icontains=name)
                )
            query &= institution_name_query

        if query:
            queryset = queryset.filter(query)

        return queryset


class ReportsView(CachedListView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        sub_sector = self.request.query_params.get('sub_sector', None)

        if sub_sector:
            sub_sector_list = sub_sector.split(',')

            query = Q()
            for subsector in sub_sector_list:
                query |= Q(sub_sector__icontains=subsector)

            queryset = queryset.filter(query)

        return queryset


class MetadataView(CachedListView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.query_params.get('sector', None)
        sub_sector = self.request.query_params.get('sub_sector', None)

        query = Q()

        if sector:
            sector_list = sector.split(',')
            sector_query = Q()
            for sec in sector_list:
                sector_query |= Q(sector__icontains=sec)
            query &= sector_query

        if sub_sector:
            sub_sector_list = sub_sector.split(',')
            sub_sector_query = Q()
            for subsector in sub_sector_list:
                sub_sector_query |= Q(sub_sector__icontains=subsector)
            query &= sub_sector_query

        if query:
            queryset = queryset.filter(query)

        return queryset
