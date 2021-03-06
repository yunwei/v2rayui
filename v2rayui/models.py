from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings
import uuid


class User(AbstractUser):
    """
    用户信息
    """
    user_id = models.UUIDField(verbose_name="用户UUID", primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    level = models.PositiveIntegerField(verbose_name="用户等级", default=settings.DEFAULT_LEVEL, validators=[MinValueValidator(0), MaxValueValidator(64)])
    alter_id = models.IntegerField("额外ID数", default=8)
    is_free = models.BooleanField(verbose_name="是否免费用户", default=False)
    expire_at = models.DateTimeField(verbose_name="账号过期时间", default=timezone.now, null=True)
    inviter_name = models.CharField(verbose_name="邀请人用户名", max_length=150, null=True)
    invite_code_num = models.PositiveIntegerField(verbose_name="可生成的邀请码数量", default=settings.INVITE_CODE_NUM)
    total_traffic = models.BigIntegerField("每月总流量(GB)", default=settings.DEFAULT_TRAFFIC)

    class Meta(AbstractUser.Meta):
        verbose_name_plural = "用户"


class UserTraffic(models.Model):
    """
    用户流量
    """
    recore_id = models.AutoField(verbose_name="流量记录ID", primary_key=True)
    user_id = models.UUIDField(verbose_name="用户UUID")
    year_month = models.CharField(verbose_name="年月记录", max_length=64, db_index=True)
    upload_traffic = models.BigIntegerField("上传流量", default=0)
    download_traffic = models.BigIntegerField("下载流量", default=0)

    class Meta:
        verbose_name_plural = "用户流量"


class InviteCode(models.Model):
    """
    邀请码
    """
    code = models.CharField(verbose_name="邀请码", primary_key=True, unique=True, max_length=64)
    mark = models.CharField(verbose_name="邀请码备注", max_length=150)
    username = models.CharField(verbose_name="邀请人用户名", db_index=True, max_length=150)
    new_username = models.CharField(verbose_name="新注册的用户名", max_length=150, default='')
    is_used = models.BooleanField(verbose_name="是否已使用", default=False)
    is_free = models.BooleanField(verbose_name="是否是免费账号", default=False)
    user_level = models.PositiveIntegerField(verbose_name="新用户等级", default=settings.DEFAULT_LEVEL,
                                             validators=[MinValueValidator(0), MaxValueValidator(64)])
    user_expired_at = models.DateTimeField(verbose_name="新账号过期时间")
    created_at = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    expired_at = models.DateTimeField(verbose_name="过期时间", db_index=True, default=timezone.now)

    class Meta:
        verbose_name_plural = "邀请码"


class Node(models.Model):
    node_id = models.UUIDField(verbose_name="节点UUID", primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    api_key = models.CharField("节点通信的Key", max_length=128, db_index=True)
    name = models.CharField("节点名称", max_length=32)
    server = models.CharField("服务器地址", max_length=128)
    port = models.IntegerField("端口", default=443)
    protocol = models.CharField("协议", default="ws", max_length=32, choices=[('ws', 'ws'), ('http', 'http')])
    path = models.CharField("ws或http2路径", max_length=128)
    comment = models.CharField("节点说明", max_length=512)
    country = models.CharField("国家", max_length=8)
    total_traffic = models.BigIntegerField("总流量", default=0)
    enable = models.BooleanField("是否开启", default=True)
    created_at = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        verbose_name_plural = "服务器节点"


class NodeTraffic(models.Model):
    """
    节点流量
    """
    recore_id = models.AutoField(verbose_name="流量记录ID", primary_key=True)
    node_id = models.UUIDField(verbose_name="节点UUID")
    year_month = models.CharField(verbose_name="年月记录", max_length=64, db_index=True)
    upload_traffic = models.BigIntegerField("上传流量", default=0)
    download_traffic = models.BigIntegerField("下载流量", default=0)

    class Meta:
        verbose_name_plural = "节点流量"
