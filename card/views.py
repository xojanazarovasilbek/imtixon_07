from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CardItemsSerializer, CardSerializer
from .models import Card,CardItem
from auto_user_.user_perm import IsUser
from qurilish.models import Product
# Create your views here.

class CardCreate(APIView):
    permission_classes = [IsUser]
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response({'data':serializer.data, "status":status.HTTP_201_CREATED if created else status.HTTP_200_OK})



class AddToCard(APIView):
    permission_classes = [IsUser, ]
    def post(self, request):
        product_id = request.data['product_id']
        amount = int(request.data['amount'])

        if not Product.objects.filter(id=product_id).exists():
            data = {
                'error':"siz mavjud bolmagan tavardi tanladiz",
                'status':status.HTTP_400_BAD_REQUEST   
            }
            return Response(data)

        if amount <= 0 or amount > 100:
            data = {
                'error':"siz xato malumot kiritdingiz",
                'status':status.HTTP_400_BAD_REQUEST   
            }
            return Response(data)

        card, _ = Card.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)


        if not CardItem.objects.filter(card=card, product=product).exists():
            product = CardItem.objects.create(
               card = card,
               product = product,
               amount = amount 
            )
        else:
            product = CardItem.objects.get(card=card, product=product)
            product.amount += amount

        product.save()

        serializer = CardItemsSerializer(product)
        data = {
            'data':serializer.data,
            'status':status.HTTP_201_CREATED    
        }
        return Response(data)
    
class CardItemUpdate(APIView):
    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)

        product = CardItem.objects.get(card__user=request.user, id=pk)
        if count:
            product.amount = int(count)
            product.save()


        elif mtd:
            if mtd == '+':
                product.amount +=1
            elif mtd == '-':
                if product.amount == 1:
                    product.delete()
                else:
                    product.amount -= 1
            product.save()
        else:
            return Response({'error':'Error','status':status.HTTP_400_BAD_REQUEST})
        
        serializer = CardItemsSerializer(product)
        data = {
            'data': serializer.data,
            'status': status.HTTP_200_OK,
            'msg':"o'zgartirildi"
        }
        return Response(data)


