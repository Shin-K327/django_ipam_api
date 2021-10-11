from django.urls import path

from .views import *

# define view methods bind pattern
network_list_cr = NetworkAndIpv4CreateAPIView.as_view()
network_detail_ud = NetworkRetrieveUDAPIView.as_view()
ipv4_list_ro = Ipv4ListReadAPIView.as_view({
    'get': 'list',
})
ipv4_detail_u = Ipv4DetailUDAPIView.as_view()
domain_list_cr = DomainListCreateAPIView.as_view()
domain_detail_ud = DomainRetrieveUDAPIView.as_view()
host_list_cr = HostListCreateAPIView.as_view()
host_detail_ud = HostDetailUDAPIView.as_view()


urlpatterns = [
    path('network/', network_list_cr),
    path('network/<pk>', network_detail_ud),
    path('ip/', ipv4_list_ro),
    path('ip/<pk>', ipv4_detail_u),
    path('domain/', domain_list_cr),
    path('domain/<pk>', domain_detail_ud),
    path('host/', host_list_cr),
    path('host/<pk>', host_detail_ud),
]
