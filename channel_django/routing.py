from django.urls import path

from chat.consumers.chat_consumer import ChatConsumer

'''
- Websocket için olan route'ları burada belirtiyoruz.

- Aşağıdaki örnekteki gibi path içinde değişken tanımlayabiliyoruz.

- Path kısmının başındaki ws sadece bu path'in websocket olduğunu belli etmek için yazılmıştır, zorunlu değildir.

- Buradaki bir önemli nokta ise tanımadığımız consumerın yapısına göre(consumer kısmında detaylandırılacaktır) .as_asgi() eklenmesidir. 
'''
websocket_urlPattern = [
    path('ws/chat/<str:id>/', ChatConsumer.as_asgi()),
]
