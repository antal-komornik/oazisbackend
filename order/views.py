from django.shortcuts import render
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # Értesítés küldése WebSocketen keresztül a konyhának
        async_to_sync(channel_layer.group_send)(
            f'kitchen',
            {
                'type': 'new_order',
                'order_id': order.id
            }
        )
