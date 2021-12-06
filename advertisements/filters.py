from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    favorite = filters.CharFilter(method='favorites_filter')

    class Meta:
        model = Advertisement
        fields = ['status', 'creator']

    def favorites_filter(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(favorite=self.request.user)
        return queryset

