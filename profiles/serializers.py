from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    """Used to provide super user with access to all profiles"""
    ## is_superuser = serializers.ReadOnlyField(source='owner.is_superuser')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner ## or request.user.is_superuser
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(owner=user, followed=obj.owner).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count' ## 'is_superuser'
        ]