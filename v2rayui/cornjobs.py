from v2rayui.models import User, InviteCode, Node


def organize_vmess_users():
    try:
        users = User.objects.filter().order_by("-date_joined")
    except User.DoesNotExist:
        users = []
