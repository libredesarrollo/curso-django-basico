from rest_framework import serializers

from .models import Element, Category, Type
from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_count(self, obj):
        print(obj)

        return Comment.objects.filter(element_id = obj.element_id).count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True) #serializers.StringRelatedField(many=True)
    class Meta:
        model = Element
        fields = '__all__'

class ElementSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'