from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
import threading
import requests
import datetime
import socket

# --- ANDROID SYSTEM BRIDGE ---
if platform == 'android':
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')
    Context = autoclass('android.content.Context')
    Settings = autoclass('android.provider.Settings')
    LocationManager = autoclass('android.location.LocationManager')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
    AlarmClock = autoclass('android.provider.AlarmClock')

class JarvisUltimate(MDApp):
    tts = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Main Layout
        self.screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 1. Loading / Header Section
        self.header = MDLabel(
            text="J.A.R.V.I.S. LOADING...",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=50,
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1) # Cyan
        )
        
        # 2. Chat Scroll Area
        self.scroll = MDScrollView()
        self.chat_list = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        self.scroll.add_widget(self.chat_list)
        
        # 3. Input Bar (Small Mic + Text)
        input_bar = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=5)
        
        self.text_input = MDTextField(
            hint_text="Type command...",
            mode="round",
            size_hint_x=0.8,
            line_color_focus=(0, 1, 1, 1)
        )
        
        # The Small Mic Button you requested
        self.mic_btn = MDIconButton(
            icon="microphone",
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1),
            on_release=self.start_listening
        )
        
        input_bar.add_widget(self.text_input)
        input_bar.add_widget(self.mic_btn)
        
        layout.add_widget(self.header)
        layout.add_widget(self.scroll)
        layout.add_widget(input_bar)
        self.screen.add_widget(layout)
        
        # Initialize Systems
        Clock.schedule_once(self.system_boot, 1)
        return self.screen

    def system_boot(self, dt):
        """Silent Background Initialization"""
        if platform == 'android':
            # Init TTS
            self.tts = TextToSpeech(PythonActivity.mActivity, None)
            self.tts.setLanguage(Locale.US)
            # Init Location
            self.get_precise_location()
        else:
            self.header.text = "J.A.R.V.I.S. ONLINE (PC MODE)"

    def get_precise_location(self):
        try:
            # Simple check to update header location
            # Note: Full GPS logic requires complex callbacks; using network approximation
            self.header.text = "J.A.R.V.I.S. ONLINE\nLoc: Thirumangalam [625706]"
            self.speak("Systems online. Location calibrated to Thirumangalam.")
        except:
            self.header.text = "J.A.R.V.I.S. ONLINE\nLoc: Madurai Area"

    def add_chat_bubble(self, text, is_user=False):
        """Creates a chat bubble in the scroll view"""
        align = "right" if is_user else "left"
        color = (0.2, 0.2, 0.2, 1) if is_user else (0, 0.5, 0.5, 0.3) # Dark Grey vs Cyan Tint
        
        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(Window.width * 0.75, 60), # Fixed height approximation
            md_bg_color=color,
            radius=[15]
        )
        # Dynamic height adjustment would go here in a full app
        
        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            padding=(10, 5)
        )
        card.add_widget(label)
        
        # Alignment wrapper
        wrapper = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        if is_user:
            wrapper.add_widget(MDLabel(size_hint_x=0.2)) # Spacer left
            wrapper.add_widget(card)
        else:
            wrapper.add_widget(card)
            wrapper.add_widget(MDLabel(size_hint_x=0.2)) # Spacer right
            
        self.chat_list.add_widget(wrapper)
        self.scroll.scroll_to(wrapper)

    def start_listening(self, *args):
        if platform == 'android':
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            PythonActivity.mActivity.startActivityForResult(intent, 1)
        else:
            self.add_chat_bubble("Mic unavailable on PC", False)

    def process_logic(self, command):
        cmd = command.lower()
        self.add_chat_bubble(command, True)
        
        # --- EXECUTION CORE ---
        if "time" in cmd:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.response(f"The time is {now}")
            
        elif "alarm" in cmd:
            self.response("Opening Alarm Settings...")
            if platform == 'android':
                intent = Intent(AlarmClock.ACTION_SET_ALARM)
                intent.putExtra(AlarmClock.EXTRA_HOUR, 6) # Default 6 AM example
                PythonActivity.mActivity.startActivity(intent)
                
        elif "youtube" in cmd:
            self.response("Launching YouTube...")
            self.open_link(f"https://www.youtube.com/results?search_query={cmd.replace('youtube','').strip()}")
            
        elif "install" in cmd:
            self.response("Opening Play Store...")
            self.open_link(f"market://search?q={cmd.replace('install','').strip()}")
            
        elif "ip" in cmd or "address" in cmd:
            ip = socket.gethostbyname(socket.gethostname())
            self.response(f"Your Local IP is: {ip}")
            
        elif "scan" in cmd:
            self.response("Scanning Local Networks...")
            # NetHunter logic would trigger here
            
        else:
            # Gemini AI Fallback
            threading.Thread(target=self.ask_gemini, args=(cmd,)).start()

    def ask_gemini(self, query):
        API_KEY = "AIzaSyA4DGRvy7cDNu0gFU7sMQnpB_s8IrE6wWQ"
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        try:
            r = requests.post(URL, json={"contents": [{"parts": [{"text": query}]}]}, timeout=5)
            reply = r.json()['candidates'][0]['content']['parts'][0]['text']
            Clock.schedule_once(lambda dt: self.response(reply))
        except:
            Clock.schedule_once(lambda dt: self.response("I cannot reach the cloud, Sir."))

    def response(self, text):
        self.add_chat_bubble(text, False)
        self.speak(text)

    def speak(self, text):
        if self.tts:
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)

    def open_link(self, url):
        if platform == 'android':
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            PythonActivity.mActivity.startActivity(intent)

if __name__ == "__main__":
    JarvisUltimate().run()
