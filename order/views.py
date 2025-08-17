from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer
from qurilish.models import Product
from card.models import Card, CardItem   


class CreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            card = request.user.card
        except Card.DoesNotExist:
            return Response(
                {"xatolik": "Savatchangiz topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )


        if not card.items.exists():
            return Response(
                {"xatolik": "Savatchangiz bo‘sh"},
                status=status.HTTP_400_BAD_REQUEST
            )


        order = Order.objects.create(user=request.user)

        for card_item in card.items.all():
            OrderItem.objects.create(
                order=order,
                product=card_item.product,
                amount=card_item.amount
            )


        card.items.all().delete()


        serializer = OrderSerializer(order)
        return Response(
            {
                "xabar": "Zakazingiz qabul qilindi ",
                "order": serializer.data
            },
            status=status.HTTP_201_CREATED
        )