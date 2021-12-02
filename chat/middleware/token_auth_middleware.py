from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
'''
- Channels asenkron şekilde çalışmaktadır. Django ORM veya bir çok yapı şuan asenkron şekilde çalışmayı desteklememektedir. Bu yüzden Channels içinde
yapılacak veritabanı işlemleri gibi işlemler farklı bir fonksiyona alınıp üzerine "@database_sync_to_async" dekoratörü eklenmelidir. Bu oluşturulan yeni
fonksiyon çağrılırken "await" kullanılmalıdır. Bu kural consumer'lar içinde de geçerlidir.

- Custom auth middleware'ün genel yapısı aşağıdaki gibidir. Burada kilit nokta __call__ methodunun içidir. __call__ methodunun içinden bahsedecek olursak;
        - scope['headers'] ile kurulan bağlantıdaki headers alanını alıyoruz ve içinde "authorization" olup olmadığını kontrol ediyoruz.
        - Eğer "authorization" alanı varsa karşığında denk gelen token'ı alıyouz yoksa direk token'a None veriyoruz.
        - scope['headers'] incelemesi bittikten sonra token'ı kontrol için özel yazdığımız fonksiyone gönderiyoruz.
        - Aldığımız token'a karşılık gelen bir veri varsa bunu geri döndürüyoruz yoksa auth sınıfından "AnonymousUser()" objesini geri döndürüyoruz.
        - Burada bulduğumuz user, consumer içinde self.scope["user"] ile erişebiliriz. Eğer user bulunamamış ise self.scope["user"] objesine "AnonymousUser()" 
        atanıyor yukarıda belirttiğimiz gibi.
'''

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token = [x[1].decode() for x in scope['headers'] if x[0].decode() == "authorization"]
            if len(token) > 0:
                token = token[0].split(' ')[1]
            else:
                token = None
        except ValueError:
            token = None
        scope['user'] = AnonymousUser() if token is None else await get_user(token)
        return await super().__call__(scope, receive, send)
