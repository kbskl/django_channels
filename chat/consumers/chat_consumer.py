from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        '''
        - Websocket ile bağlantı ilk kurulmaya çalışıldığı zaman bu fonksiyon çalışır.
        - await self.accept() =>  ile bağlantı kabul edilir.
        - await self.channel_layer.group_add(
                      self.groupname,
                      self.channel_name,
                  ) => ile gelen isteğin sahibi bir gruba dahil edilir. O gruba gönderilen her mesaj burada gruba dahil edilen herkese gider.
                      Örneğimizdeki groupname, path kısmıda verilen id olarak belirtilmiştir. Buradaki amaç aynı path üzerinde olan insanların birbiri ile
                      gruba dahil olması yani konuşabilmesidir.
        - self.scope["user"] ise yazdığımız auth middleware üzerinde bulunan kullanıcıyı alıyoruz. Aldığımız kullanıcının "AnonymousUser()"
            olup olmadığını kontrol ediyoruz. Eğer token doğru değilse veya kullanıcı yoksa bağlantıyı kabul etmiyoruz. Kabul edilmeyen bağlantı belli bir süre
            sonra düşer. Burada daha farklı kontrollerde yapılabilir. Örnek verilecek olursak; ID kısmı veritabanında tutulan bir oda olabilir ve bu odaya
            erişim belli kullanıcılar için verilebilir. Gelen ID ile self.user erişimi kontrol edilir. Eğer erişimi varsa bağlantı kabul edilir yoksa edilmez.
            Buradaki bir önemli nokta middleware yazılırken de belirtildiği gibi veritabanı gibi işlemler için farklı bir yol izlenmesidir.
        '''
        try:
            self.user = self.scope["user"]
            self.groupname = self.scope['url_route']['kwargs']['id']
            print(self.user)
            print(self.groupname)
            if self.user != AnonymousUser():
                await self.accept()
                await self.channel_layer.group_add(
                    self.groupname,
                    self.channel_name,
                )
        except Exception as e:
            print(e)

    async def disconnect(self, code):
        '''
        - Bir bağlantı sonlandırılırken en son bu method çalışır.
        - Ayrıca bir gruba dahil ise gruptan çıkartılır.
        '''
        try:
            self.groupname = self.scope['url_route']['kwargs']['id']
            await self.channel_layer.group_discard(
                self.groupname,
                self.channel_name
            )
        except Exception as e:
            print(e)

    async def receive(self, text_data=None, bytes_data=None):
        '''
        - Websocket bağlantısı başarılıyla kurulmuş bir yapıda gönderilen her data receive fonksiyonuna gelir ve buradan tüm grup üyelerine dağılır.
        - await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'consumer_send_message_users',
                    'data_obj': data
              ) => kod ile type kısmına sınıfın içindeki gönderici fonksiyonu veririz ve altına gönderilecek datayı. Gönderilecek data'nın parametre
              ismini biz belirleyebiliriz fakat fonksiyonu belirttiğimiz yerin ismi "type" olmak zorundadır. group_send methodu ile tüm grup üyelerine
              gelen datayı aktarırız. type kısmında belirttiğimiz fonksiyon ismi diğer consumerlar içinde bulunmaması daha sağlıklıdır(ismin tekil olması)
              çünkü django içinde bazen belli bir gruba özel data göndermeniz gerekebiliyor.
              Bu durumda direk bu fonksiyon ismini verip o gruba ait herkese mesaj gönderebiliyoruz.
        - Gelen datalar burada kontrol edilip, istenmeyen içerik varsa data gönderilmeyebilir veya datanın kayıt altına alınması gerekiyorsa burada bu işlem
        yapılabilir.
        - Örnekte kullanmak amacıyla gelen gönderilen mesajın içine gönderen kişinin adı soyadı eklenmiştir.
        '''
        try:
            data = json.loads(text_data)
            data['gonderen_user'] = f"{self.user.first_name} {self.user.last_name}"
            group_name = self.scope['url_route']['kwargs']['id']
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'consumer_send_message_users',
                    'data_obj': data
                }
            )
        except Exception as e:
            print(e)

    async def consumer_send_message_users(self, event):
        data_obj = event['data_obj']
        await self.send(text_data=json.dumps(data_obj))
