# Consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import User, OrderHistory
from channels.db import database_sync_to_async

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.raspberry_pi_group_name = "raspberry_pi"
        await self.channel_layer.group_add(
            self.raspberry_pi_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.raspberry_pi_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
    async def raspberry_pi_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def confirm_order(self, text_data_json):
        if "status" not in text_data_json or "userid" not in text_data_json or "orderid" not in text_data_json:
            return

        userid = text_data_json['userid']
        orderid = text_data_json['orderid']

        try:
            user = User.objects.get(id=userid)
            orderhistory = OrderHistory.objects.get(id=orderid, user=user)
        except (User.DoesNotExist, OrderHistory.DoesNotExist):
            return

        if text_data_json['status'] == "success":
            self.process_order(user, orderhistory, text_data_json)
        elif text_data_json['status'] == "error":
            orderhistory.status = OrderHistory.Status.ORDER_ERROR
            orderhistory.save()

    def process_order(self, user, orderhistory, text_data_json):
        for letter in letters:
            attr_value = getattr(orderhistory, letter)
            if attr_value:
                user_attr_value = getattr(user, letter)
                if user_attr_value >= attr_value:
                    setattr(user, letter, user_attr_value - attr_value)
                else:
                    orderhistory.status = None
                    orderhistory.error = f"You don't have enough '{letter}' to complete the order"
                    orderhistory.is_error = True
                    break

        user.save()
        orderhistory.save()
        print("Order confirmed and updated")
