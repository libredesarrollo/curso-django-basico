from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from listelement.models import Element, Type
from listelement.serializer import ElementSerializer,ElementSerializerSimple

from rest_framework.views import APIView
from rest_framework import mixins, generics

from rest_framework.pagination import PageNumberPagination

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# Create your views here.

class ProductPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'enlaces': {
                'siguiente': self.get_next_link(),
                'previo': self.get_previous_link()
            },
            'cantidad': self.page.paginator.count,
            'resultados': data
        })

def manualJson(request):

    data = {
        'id': 123,
        'name': 'Pepe'
    }

    data = Element.objects.all()
    response = {'elements': list(data.values('id','title', 'description'))}

    return JsonResponse(response)

class ProductList(generics.ListCreateAPIView):
    type = Type.objects.get(pk=1) #tipo products
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple
    pagination_class = ProductPagination
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated, DjangoModelPermissions]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    type = Type.objects.get(pk=1) #tipo products
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple

"""class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    type = Type.objects.get(pk=1) #tipo products
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    type = Type.objects.get(pk=1) #tipo products
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple

    def get(self, request, pk):
        return self.retrieve(request,pk)

    def put(self, request, pk):
        return self.update(request,pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
"""

"""
class ProductList(APIView):

    def get(self, request):
        type = Type.objects.get(pk=1) #tipo products
        products = Element.objects.filter(type=type)

        serializers = ElementSerializer(products, many=True)
        return Response(serializers.data)  

    def post(self, request):
        serializer = ElementSerializerSimple(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):

    def get_object(self,pk):
        type = Type.objects.get(pk=1) #tipo products
        product = Element.objects.get(type=type,pk=pk)
        return product

    def get(self, request, pk):
        product = self.get_object(pk)
        serializers = ElementSerializer(product)
        return Response(serializers.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ElementSerializerSimple(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        type = Type.objects.get(pk=1) #tipo products
        products = Element.objects.filter(type=type)

        serializers = ElementSerializer(products, many=True)
        return Response(serializers.data)
    if request.method == 'POST':
        print(request.data)
        serializer = ElementSerializerSimple(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def product_detail(request,pk):
    type = Type.objects.get(pk=1) #tipo products
    product = Element.objects.get(type=type,pk=pk)

    if request.method == 'GET':
        serializers = ElementSerializer(product)
        return Response(serializers.data)
    elif request.method == 'PUT':
        print(request.data)
        serializer = ElementSerializerSimple(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)