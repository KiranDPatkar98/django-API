from rest_framework import serializers
from .models import Todo
import re
from django.utils.text import slugify


class TodoSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        # fields = '__all__'
        fields = ['todo_title', 'slug', 'todo_description', 'is_done', 'uid']
        # exclude = ['created_at']

    def get_slug(self, obj):
        return slugify(obj.todo_title)

# if you want to validate only one specific field you can do like this
    # def validate_todo_title(self, data):
        # validation logiv

    def validate(self, validated_data):
        if validated_data.get('todo_title'):
            todo_title = validated_data['todo_title']
            regex = re.compile("[@_!#$%^&*()<>?/|}{~:]")

            if len(todo_title) < 3:
                raise serializers.ValidationError(
                    'tpto_title should contain atleast 3 characters')

            if regex.search(todo_title) != None:
                raise serializers.ValidationError(
                    'todod_title cannot contain special characters ')
        return validated_data
