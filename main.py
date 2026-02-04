from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window
from android.runnable import run_on_ui_thread
import threading
import requests

# --- ANDROID NATIVE BRIDGE ---
if platform == 'android':
    from jnius import autoclass, cast
    from android import activity
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')

class JarvisUltimate(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Main Screen Layout
        layout = MDFloatLayout()
        
        # 1. HEADER (Status & Location)
        self.status_label = MDLabel(
            text="[J.A.R.V.I.S. ONLINE]\nSYSTEMS NOMINAL",
            halign="center", pos_hint={"center_x": 0.5, "top": 0.95},
            size_hint=(1, 0.1), theme_text_color="Custom", text_color=(0, 1, 1, 1),
            font_style="H5"
        )
        
        # 2. CENTER CONSOLE (The "Face")
        self.progress = MDProgressBar(
            value=0, max=100, pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint_x=0.8, color=(0, 1, 1, 1)
        )
        
        # 3. APP GRID (Organized Icons)
        grid = MDGridLayout(cols=3, spacing=20, size_hint=(0.8, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.65})
        # Adding dummy icons for visuals (They can be linked to functions later)
        grid.add_widget(MDIconButton(icon="wifi", theme_text_color="Custom", text_color=(0,1,1,1))) # NetHunter
        grid.add_widget(MDIconButton(icon="youtube", theme_text_color="Custom", text_color=(1,0,0,1))) # YouTube
        grid.add_widget(MDIconButton(icon="google-play", theme_text_color="Custom", text_color=(0,1,0,1))) # Store
        
        # 4. MICROPHONE TRIGGER (Bottom Center - The "Arc Reactor")
        # This is the button you TAP to speak.
        self.mic_btn = MDFloatingActionButton(
            icon="microphone",
            pos_hint={"center_x": 0.5, "y": 0.05},
            md_bg_color=(0, 1, 1, 1), # Cyan Glow
            icon_color=(0, 0, 0, 1),
            on_release=self.activate_voice_listener
        )

        layout.add_widget(self.status_label)
        layout.add_widget(self.progress)
        layout.add_widget(grid)
        layout.add_widget(self.mic_btn)
        
        # Bind the Android Result Listener (THE MISSING LINK)
        if platform == 'android':
            activity.bind(on_activity_result=self.on_activity_result)
            
        Clock.schedule_once(self.silent_boot, 1)
        return layout

    def silent_boot(self, *args):
        # A purely visual boot sequence
        threading.Thread(target=self.boot_logic, daemon=True).start()

    def boot_logic(self):
        self.update_ui("Authenticating...", 20)
        import time; time.sleep(1)
        self.update_ui("Loading Modules...", 60)
        time.sleep(1)
        self.update_ui("READY FOR COMMAND", 100)

    # --- VOICE LOGIC ---
    def activate_voice_listener(self, instance):
        if platform != 'android': return
        try:
            # Standard Android Voice Intent
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak now, Sir...")
            PythonActivity.mActivity.startActivityForResult(intent, 100)
        except Exception as e:
            self.update_ui(f"Mic Error: {str(e)}", 0)

    # --- THE LISTENER (Catches what you said) ---
    def on_activity_result(self, request_code, result_code, intent):
        if request_code == 100 and result_code == -1: # RESULT_OK
            # Extract the text from the voice input
            matches = intent.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if matches and matches.size() > 0:
                command = matches.get(0)
                self.process_command(command)
            else:
                self.update_ui("Create voice input failed.", 0)

    # --- THE BRAIN (Decides what to do) ---
    def process_command(self, command):
        cmd = command.lower()
        self.update_ui(f"Processing: {cmd}", 50)
        
        if "youtube" in cmd:
            self.open_link(f"https://www.youtube.com/results?search_query={cmd.replace('youtube', '')}")
        elif "install" in cmd:
            self.open_link(f"market://search?q={cmd.replace('install', '')}")
        else:
            threading.Thread(target=self.ask_gemini, args=(cmd,), daemon=True).start()

    def open_link(self, url):
        if platform == 'android':
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            PythonActivity.mActivity.startActivity(intent)
            self.update_ui("Executing...", 100)

    def ask_gemini(self, query):
        API_KEY = "AIzaSyA4DGRvy7cDNu0gFU7sMQnpB_s8IrE6wWQ" # Keep your key safe!
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        try:
            r = requests.post(URL, json={"contents": [{"parts": [{"text": query}]}]}, timeout=5)
            if r.status_code == 200:
                reply = r.json()['candidates'][0]['content']['parts'][0]['text']
                self.update_ui(reply[:60] + "...", 100) # Short preview
            else:
                self.update_ui("Signal Lost.", 0)
        except:
            self.update_ui("Connection Failed.", 0)

    def update_ui(self, text, val):
        Clock.schedule_once(lambda dt: self._set_ui(text, val))

    def _set_ui(self, t, v):
        self.status_label.text = t
        self.progress.value = v

if __name__ == "__main__":
    JarvisUltimate().run()
