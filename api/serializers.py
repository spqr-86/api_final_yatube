from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import User, Post, Comment, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )
    following = serializers.SlugRelatedField(
        many=False,
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        fields = '__all__'
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        if (self.context['request'].method == 'POST' and
                data['following'] == data['user']):
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя")
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group
