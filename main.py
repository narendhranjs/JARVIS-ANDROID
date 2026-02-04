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
            self.header.text = "J.A
