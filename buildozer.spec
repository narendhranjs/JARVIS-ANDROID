[app]
# --- Basic Info ---
title = JARVIS Titan
package.name = jarvis_titan
package.domain = org.narendhran
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 4.0

# --- The Tools (Requirements) ---
# Added pyjnius for system control and requests for Gemini AI
requirements = python3, kivy==2.3.0, kivymd, requests, pyjnius, urllib3, charset-normalizer, idna, certifi

# --- The Permissions (The Keys to the Phone) ---
# RECORD_AUDIO: For Voice Commands
# ACCESS_WIFI_STATE: For the WiFi Scanner (NetHunter Mode)
# ACCESS_FINE_LOCATION: Required by Android to see WiFi names
android.permissions = INTERNET, RECORD_AUDIO, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, NEARBY_WIFI_DEVICES

# --- Android Hardware Settings --- [cite: 1.4, 3.1
