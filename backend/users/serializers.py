from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer, UserSerializer as DjoserUserSerializer
from .models import User


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'role')
        ref_name = 'CoreUserCreateSerializer'  # Уникальное имя для Swagger


class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        ref_name = 'CoreUserSerializer'  # Уникальное имя для Swagger