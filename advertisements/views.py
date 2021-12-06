from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.filter()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend,]
    filter_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            Q(is_draft=False) | Q(is_draft=True, creator=request.user.id)
        )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            Q(is_draft=False) | Q(is_draft=True, creator=request.user.id)
        )
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def set_favorite(self, request, pk=None):
        adv = Advertisement.objects.get(id=pk)
        if adv.creator == request.user:
            return Response({'favorite': 'You cannot add your advertisement to favorite'})
        if request.user in adv.favorite.all():
            return Response({'favorite': 'Advertisement already has added to favorite'})
        adv.favorite.add(request.user)
        return Response({'favorite': 'Advertisement successfully mark as favorite'})

    @action(detail=True, methods=['patch'])
    def unset_favorite(self, request, pk=None):
        adv = Advertisement.objects.get(id=pk)
        if request.user not in adv.favorite.all():
            return Response({'favorite': 'Advertisement didnt found in your favorites'})
        adv.favorite.remove(request.user)
        return Response({'favorite': 'Advertisement successfully unmark as favorite'})

    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly(), IsOwner()]
