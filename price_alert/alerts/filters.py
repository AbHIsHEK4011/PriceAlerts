# alerts/filters.py

import django_filters
from .models import Alert

class AlertFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = Alert
        fields = ['status']
