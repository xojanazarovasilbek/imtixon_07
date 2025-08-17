from rest_framework import generics,status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Comments
from .serializers import ProductSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from auto_user_.user_perm import IsUser

class ProductApiView(APIView):
    def get(self, request, pk=None):
        search = request.GET.get('search')
        product = Product.objects.all()

        if search:
            product = product.filter(nomi__icontains=search)
        paginator = PageNumberPagination()
        paginated_qs = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(paginated_qs, many=True)


        data = {
            'product':serializer.data,
            'count':product.count(),
            'status':status.HTTP_200_OK
        }
        return paginator.get_paginated_response(data)
    permission_classes = [permissions.IsAuthenticated, IsUser, ]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApi(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ozgartirildi ', 'data': serializer.data})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Qisman ozgartirildi ', 'data': serializer.data})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'message': 'Ochirildi '}, status=status.HTTP_204_NO_CONTENT)



class CommentApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:  
            comments = Comments.objects.all()
        else:  
            comments = Comments.objects.filter(user=request.user)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            return Response({'error': 'Comment topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return Response({'msg': "Comment o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': "Siz bu komentni o'chira olmaysiz"}, status=status.HTTP_403_FORBIDDEN)













# class ListCreateApi(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['category', 'price']
#     search_fields = ['name', 'desc']
#     ordering_fields = ['price', 'name']
#     ordering = ['price']

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
