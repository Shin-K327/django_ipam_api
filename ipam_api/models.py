import uuid
from django.db import models
from django.core.validators import RegexValidator, validate_ipv4_address, MinValueValidator, MaxValueValidator


class Domain(models.Model):
    class Meta:
        db_table = 'domain'
        verbose_name = verbose_name_plural = 'ドメイン'
        ordering = ['domain_name']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    domain_name = models.CharField(
        verbose_name='ドメイン名',
        unique=True,
        max_length=63,
        validators=[RegexValidator(
            r'^[a-z0-9][a-z0-9\-]+$',
            message='ドメイン名は小文字英字、数字、ハイフンのみが使用できます'
        )],
        error_messages={
            'unique': '重複するドメイン名が存在します'
        }
    )
    created_at = models.DateField(verbose_name='登録日', auto_now_add=True)
    description = models.TextField(verbose_name='説明', max_length=300, null=True, blank=True)

    def __str__(self):
        return self.domain_name


class Host(models.Model):
    class Meta:
        db_table = 'host'
        verbose_name = verbose_name_plural = 'ホスト'
        ordering = ['host_name']

    HOST_USE_TYPE = [
        ('APL', (
            ('L2S', 'L2 Switch'),
            ('L3S', 'L3 Switch'),
            ('RTR', 'Router'),
        ),
         ),
        ('SVR', (
            ('WEB', 'Web Server'),
            ('MGR', 'Manage Server'),
            ('DNS', 'DNS Server'),
        ),
         ),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    host_verbose = models.CharField(verbose_name='詳細名', max_length=64)
    host_name = models.CharField(
        verbose_name='ホストネーム',
        unique=True,
        max_length=15,
        validators=[RegexValidator(
            r'^[a-z][a-z0-9\_]+$',
            message='ホストネームは小文字の英字と数字で先頭が英字から始まる必要があります'
        )],
        error_messages={
            'unique': '重複するホストネームが存在します'
        }
    )
    fore_domain = models.ForeignKey(Domain, on_delete=models.PROTECT, null=True)
    use_type = models.CharField(choices=HOST_USE_TYPE, max_length=3)
    description = models.TextField(verbose_name='説明', max_length=300, null=True, blank=True)
    created_at = models.DateField(verbose_name='登録日', auto_now_add=True)

    def __str__(self):
        return self.host_name


class Instance(models.Model):
    class Meta:
        db_table = 'instance'
        verbose_name = verbose_name_plural = 'インスタンス'

    host_model = models.OneToOneField(Host, on_delete=models.CASCADE)


class V4Network(models.Model):
    class Meta:
        db_table = 'v4network'
        verbose_name = verbose_name_plural = 'ネットワーク'
        ordering = ['created_at']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    network_name = models.CharField(verbose_name='ネットワーク名', max_length=64)
    network_address = models.CharField(
        verbose_name='ネットワークアドレス',
        unique=True,
        max_length=15,
        # TODO: エラー発生時のメッセージを"IPアドレス"ではなく"ネットワーク"に修正する
        validators=[validate_ipv4_address],
        error_messages={
            'unique': 'ネットワークアドレスの重複は許可されていません'
        },
    )
    prefix = models.PositiveSmallIntegerField(
        verbose_name='プレフィックス',
        validators=[
            MinValueValidator(limit_value=8),
            MaxValueValidator(limit_value=31)
        ],
    )
    description = models.TextField(verbose_name='説明', max_length=300, null=True, blank=True)
    created_at = models.DateField(verbose_name='登録日', auto_now_add=True)

    def __str__(self):
        return f'{self.network_address}/{self.prefix}'


class Ipv4Address(models.Model):
    class Meta:
        db_table = 'ipv4address'
        verbose_name = verbose_name_plural = 'IPv4アドレス'
        ordering = ['ipv4_address']

    class AddressUseTypeChoices(models.IntegerChoices):
        service = 1, 'service'
        manage = 2, 'manage'
        storage = 3, 'storage'
        ha = 4, 'HA'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    ipv4_address = models.CharField(
        verbose_name='IPv4アドレス',
        unique=True,
        max_length=15,
        validators=[validate_ipv4_address],
        editable=False,
    )
    fore_network = models.ForeignKey(V4Network, on_delete=models.CASCADE)
    use_type = models.IntegerField(choices=AddressUseTypeChoices.choices, null=True)
    fore_host = models.ForeignKey(Host, on_delete=models.PROTECT, null=True)
    update_at = models.DateField(verbose_name='変更日', auto_now_add=True)

    def __str__(self):
        return self.ipv4_address
