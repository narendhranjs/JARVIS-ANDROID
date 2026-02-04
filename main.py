from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivy.utils import platform
from kivy.clock import Clock
import requests
import threading

# --- ANDROID SYSTEM BRIDGE ---
if platform == 'android':
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')
    Context = autoclass('android.content.Context')

class JarvisTitan(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        screen = MDScreen()

        # Personalized Status [Memory: Madurai Location]
        self.status = MDLabel(
            text="[J.A.R.V.I.S. TITAN ONLINE]\nLocation: Madurai | Unit: fun-da-mentals",
            halign="center", pos_hint={"center_y": 0.7},
            theme_text_color="Custom", text_color=(0, 1, 1, 1)
        )

        self.progress = MDProgressBar(
            value=0, max=100, pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint_x=0.8
        )

        screen.add_widget(self.status)
        screen.add_widget(self.progress)

        # Silent Initialization Sequence
        Clock.schedule_once(self.run_startup, 2)
        return screen

    def run_startup(self, *args):
        threading.Thread(target=self.initialize_systems, daemon=True).start()

    def initialize_systems(self):
        # 1. AI Sync (33%)
        self.update_ui("AI Core Syncing...", 33)
        # 2. Network Check (66%)
        self.update_ui("NetHunter Scanner Warming Up...", 66)
        # 3. Finalize (100%)
        self.update_ui("ALL SYSTEMS READY, SIR.", 100)
        Clock.schedule_once(lambda dt: self.start_voice_listener(), 1)

    # --- VOICE COMMAND SYSTEM ---
    def start_voice_listener(self):
        if platform != 'android': return
        try:
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Command me, Sir.")
            PythonActivity.mActivity.startActivityForResult(intent, 1)
        except: self.update_ui("Mic Failure.", 0)

    # --- COMMAND PARSER (YouTube, Store, Gemini) ---
    def process_voice_result(self, command):
        cmd = command.lower()
        
        if "youtube" in cmd:
            query = cmd.replace("youtube", "").strip()
            self.open_link(f"https://www.youtube.com/results?search_query={query}")
            
        elif "install" in cmd or "play store" in cmd:
            app = cmd.replace("install", "").replace("play store", "").strip()
            self.open_link(f"market://search?q={app}")
            
        elif "scan wifi" in cmd:
            self.run_nethunter_scan()
            
        else: # Standard Gemini AI logic
            self.ask_gemini(cmd)

    def open_link(self, url):
        activity = PythonActivity.mActivity
        intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        activity.startActivity(intent)

    def ask_gemini(self, query):
        API_KEY = "AIzaSyA4DGRvy7cDNu0gFU7sMQnpB_s8IrE6wWQ"
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        try:
            r = requests.post(URL, json={"contents": [{"parts": [{"text": query}]}]})
            reply = r.json()['candidates'][0]['content']['parts'][0]['text']
            self.update_ui(reply[:100], 100)
        except: self.update_ui("Uplink failed.", 0)

    def update_ui(self, text, val):
        Clock.schedule_once(lambda dt: self._set_ui(text, val))

    def _set_ui(self, t, v):
        self.status.text = t
        self.progress.value = v

if __name__ == "__main__":
    JarvisTitan().run()
