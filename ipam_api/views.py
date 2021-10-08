from rest_framework import status, views, generics, viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import V4Network, Ipv4Address, Domain, Host
from .serializers import V4NetworkSerializer,\
    V4NetworkDetailSerializer, \
    Ipv4AddressSerializer,\
    HostSerializer,\
    DomainSerializer


# Create your views here.
class NetworkAndIpv4CreateAPIView(generics.ListAPIView):
    serializer_class = V4NetworkSerializer
    queryset = V4Network.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = V4NetworkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        print(instance)

        return Response(serializer.data, status.HTTP_201_CREATED)


class NetworkRetrieveUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = V4NetworkDetailSerializer
    queryset = V4Network.objects.all()


# TODO: フィルタークラスはまとめてfilters.pyに移し参照する形にする
class Ipv4Filter(filters.FilterSet):

    ipv4_address = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ipv4Address
        fields = ['ipv4_address', 'use_type']


class Ipv4ListReadAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = Ipv4AddressSerializer
    queryset = Ipv4Address.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = Ipv4Filter


class Ipv4DetailUDAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = Ipv4AddressSerializer
    queryset = Ipv4Address.objects.all()


class DomainFilter(filters.FilterSet):

    domain_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Domain
        fields = ['domain_name']


class DomainListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DomainFilter


class DomainRetrieveUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()


class HostFilter(filters.FilterSet):

    host_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Host
        fields = ['host_name', 'fore_domain']


class HostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HostSerializer
    queryset = Host.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = HostFilter


class HostDetailUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HostSerializer
    queryset = Host.objects.all()
