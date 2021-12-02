import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channel_django.routing import websocket_urlPattern
from chat.middleware.token_auth_middleware import TokenAuthMiddleware
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel_django.settings')
'''
- websocket yerine farklı protokoller kullanılacaksa routing'i buradan yapılmalıdır.

- websocket veya başka bir protokol için oluşturulan route'lar buraya verilir. Önerilen yapıda route'lar başka bir alanda oluşturulmalıdır.
o yüzden bizde route'ları başka bir yerde oluştıurup "websocket_urlPattern" parametresi ile websocket'e verdik.

- Channel üzerinde kullanılacak middleware'ler burada tanımlanır. Sadece Authentication için değil güvenlik için olan
middleware'larda burada tanımlanmaktadır. Aşağıda görünen AuthMiddlewareStack, Channels'ın default olarak kullandığı
session-based authentication'ı destekleyen bir middleware'dür. TokenAuthMiddleware ise bizim yazdığımız restframework yapısındaki
token-based authentication'ı destekleyen custom middleware'dür.
'''

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": AuthMiddlewareStack(URLRouter(websocket_urlPattern)),
    "websocket": TokenAuthMiddleware(URLRouter(websocket_urlPattern)),
})
