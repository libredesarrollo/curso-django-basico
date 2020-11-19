from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Element, Category, Type
from .serializer import ElementSerializer, CategorySerializer, TypeSerializer, CommentSerializer

from comment.models import Comment



class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Element.objects.all()
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        #queryset = Element.objects.get(url_clean=request.query_params['url_clean'])
        queryset = get_object_or_404(Element,url_clean=request.query_params['url_clean'])
        serializer = ElementSerializer(queryset, many=False)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        queryset = Element.objects.filter(category_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        queryset = get_object_or_404(Category,url_clean=request.query_params['url_clean'])
        serializer = CategorySerializer(queryset, many=False)
        return Response(serializer.data)

    '''def list(self, request):
        queryset = Category.objects.all()
        #print(queryset)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)'''

class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        queryset = Element.objects.filter(type_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Type.objects.all()
        serializer = TypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        queryset = get_object_or_404(Type,url_clean=request.query_params['url_clean'])
        serializer = TypeSerializer(queryset, many=False)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.exclude(element__isnull=True)
    serializer_class = CommentSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)