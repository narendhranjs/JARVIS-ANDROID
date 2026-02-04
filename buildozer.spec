[app]
title = JARVIS Ultimate
package.name = jarvis_ultimate
package.domain = org.narendhran
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.0

# THE TOOLKIT
requirements = python3, kivy==2.3.0, kivymd, requests, pyjnius, urllib3, charset-normalizer, idna, certifi

# THE PERMISSIONS (Crucial for 100% function)
android.permissions = INTERNET, RECORD_AUDIO, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, SET_ALARM, WAKE_LOCK

# ANDROID CONFIG
orientation = portrait
fullscreen = 0  # 0 allows seeing the status bar (time/battery)
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
