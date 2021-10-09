from ipaddress import ip_network
import uuid

from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import V4Network, Ipv4Address, Domain, Host


class V4NetworkSerializer(serializers.ModelSerializer):

    hosts = []

    class Meta:
        model = V4Network
        fields = '__all__'

    def validate(self, data):
        network = data.get('network_address')
        prefix = data.get('prefix')

        try:
            hosts = ip_network(f'{network}/{prefix}').hosts()

            if Ipv4Address.objects.filter(ipv4_address__in=hosts).exists():
                raise ValidationError(
                    'アドレス範囲の重複が発生しています'
                )

        except TypeError:
            raise ValidationError(
                'ネットワークとプレフィックスの組み合わせが無効です'
            )
        except ValueError:
            raise ValidationError(
                '無効なネットワークアドレスです'
            )

        return data

    def create(self, validated_data):
        network = validated_data.get('network_address')
        prefix = validated_data.get('prefix')
        network_instance = super().create(validated_data)
        add_hosts = []

        self.get_hosts(network, prefix)

        for host in self.hosts:
            add_hosts.append(Ipv4Address(
                id=uuid.uuid4(),
                ipv4_address=host,
                fore_network_id=network_instance.id
            ))

        Ipv4Address.objects.bulk_create(add_hosts)

        return network_instance

    def get_hosts(self, network, prefix):

        self.hosts = [host.__str__() for host in ip_network(f'{network}/{prefix}').hosts()]


# ToDO: IPv4アドレスを逆参照してアドレス一覧を引っ張ってきてフィールドに格納する処理を書く
class V4NetworkDetailSerializer(serializers.ModelSerializer):

    ipv4_address_list = serializers.SerializerMethodField()

    class Meta:
        model = V4Network
        fields = [
            'id',
            'network_name',
            'network_address',
            'prefix',
            'description',
            'created_at',
            'ipv4_address_list',
        ]
        extra_kwargs = {
            'network_address': {
                'read_only': True
            },
            'prefix': {
                'read_only': True
            },
        }

    def get_ipv4_address_list(self, obj):
        try:
            filter_object = Ipv4AddressSerializer(
                Ipv4Address.objects.all().filter(fore_network_id=obj.id),
                many=True
            ).data
        except:
            filter_object = []
        return filter_object


class Ipv4AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ipv4Address
        fields = '__all__'
        extra_kwargs = {
            'ipv4_address': {
                'read_only': True
            },
            'fore_network': {
                'read_only': True
            },
        }


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = '__all__'
