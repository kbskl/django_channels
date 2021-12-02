import json
import websocket
import _thread


def on_message(ws, message):
    '''
    Kurulan bağlantı üzerine bir mesaj geldiği zaman bu fonksiyon çalışır.
    '''
    print(message)


def on_error(ws, error):
    '''
    Kurulan bağlantıda bir hata olduğu zaman bu fonksiyon çalışır.
    '''
    print(f"BAGLANTIDA BİR HATA OLDU. HATA:{error}")


def on_close(ws, close_status_code, close_msg):
    '''
    Kurulan bağlantı kapandığı zaman bu fonksiyon çalışır.
    '''
    print("BAGLANTI KAPANDI")


def on_open(ws):
    '''
    Bağlantı kurulduğu zaman bu fonksiyon çalışır.
    def run ve altında thread başlatma işlemi sadece mesaj gönderilmek için yazılmıştır.
    '''
    print("BAGLANTI KURULDU")

    def run(*args):
        while 1:
            message = input("Mesaj:")
            ws.send(json.dumps({
                "message": f"{message}"
            }))

    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    '''
    Authentication sağlamak için header oluşturup bunu websockete vermemiz gerekiyor.
    '''
    # ahmet@mail.com kullanıcısı
    header = "Authorization: Token b6805028ff98064001cb178722d0af391e567e2f"
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/20/",
                                header=[header],
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
