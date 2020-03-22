from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
