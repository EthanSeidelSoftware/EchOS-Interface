from kivy.config import Config
import os
Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

Config.set('graphics', 'fullscreen', '1')  # <-- fullscreen ON

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp

from calm_mode import CalmModeScreen
from EchOSComunitcator import CommunicateScreen
from EchOSPlanner import DailyPlannerScreen
from SafeZone import ApplicationsScreen
from EchOSShell import LimitedShellScreen
from kivy.core.window import Window
from kivy.base import EventLoop
import sys
from kivy.clock import Clock
import traceback
from kivy.core.text import LabelBase

def global_exception_handler(exctype, value, tb):
    error_text = ''.join(traceback.format_exception(exctype, value, tb))
    print(f"[UNCAUGHT ERROR]\n{error_text}")

    # Show a crash screen using Kivy's Clock to avoid thread issues
    def show_crash_screen(dt):
        app = App.get_running_app()
        crash_screen = AppCrashScreen(app_name="App", name="crash")
        app.sm.add_widget(crash_screen)
        app.sm.current = "crash"

    Clock.schedule_once(show_crash_screen, 0)

sys.excepthook = global_exception_handler


# Now use it with font_name="EmojiFont"


# ... rest of your code unchanged ...
# Window.fullscreen = True  # or 'auto', 'fake', 'borderless'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        # 🌄 Background wallpaper
        wallpaper = Image(
            source="assets/flowers.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        root.add_widget(wallpaper)

        # 🧩 Foreground layout
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(30),
            padding=dp(60),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        button_style = {
            "font_size": 32,
            "size_hint": (1, None),
            "height": dp(80),
            "background_color": (1, 1, 1, 0.8),  # semi-transparent white
            "color": (0, 0, 0, 1)  # black text
        }

        layout.add_widget(Button(text="Communicate", on_press=self.goto_communicate, **button_style))
        layout.add_widget(Button(text="Calm Mode", on_press=self.goto_calm, **button_style))
        layout.add_widget(Button(text="Daily Planner", on_press=self.goto_planner, **button_style))
        layout.add_widget(Button(text="Applications", on_press=self.goto_safezone, **button_style))

        # Power button
        power_button = Button(
            text="Power Off",
            font_size=26,
            size_hint=(1, None),
            height=dp(60),
            background_color=(1, 0.4, 0.4, 0.85),
            color=(1, 1, 1, 1),
            on_press=self.show_power_menu
        )
        layout.add_widget(power_button)

        root.add_widget(layout)
        self.add_widget(root)


    def goto_calm(self, *args):
        self.manager.current = 'calm'

    def goto_communicate(self, *args):
        self.manager.current = 'communicate'

    def goto_planner(self, *args):
        self.manager.current = 'planner'

    def goto_safezone(self, *args):
        self.manager.current = 'safezone'

    def show_power_menu(self, *args):
        content = BoxLayout(orientation='vertical', spacing=30, padding=20)

        btn_shutdown = Button(text="Shut down", font_size=24, size_hint_y=None, height=50)
        btn_reboot = Button(text="Reboot", font_size=24, size_hint_y=None, height=50)
        btn_cancel = Button(text="Cancel", font_size=24, size_hint_y=None, height=50)

        content.add_widget(btn_shutdown)
        content.add_widget(btn_reboot)
        content.add_widget(btn_cancel)

        popup = Popup(title='Power Options', content=content,
                      size_hint=(.6, .4), auto_dismiss=False)

        btn_shutdown.bind(on_press=lambda *a: self.power_action('shutdown', popup))
        btn_reboot.bind(on_press=lambda *a: self.power_action('reboot', popup))
        btn_cancel.bind(on_press=popup.dismiss)

        popup.open()

    def power_action(self, action, popup):
        popup.dismiss()

        if action == 'shutdown':
            print("Shutting down...")
            os.system("sudo shutdown -h now")
        elif action == 'reboot':
            print("Rebooting...")
            os.system("sudo reboot")

class AppCrashScreen(Screen):
    def __init__(self, app_name="An app", **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        label = Label(text=f"❌ {app_name} has quit unexpectedly.", font_size=32, font_name="assets/NotoEmoji-Regular.ttf")
        back = Button(text="← Back to Home", font_size=24, size_hint=(1, None), height=60)
        back.bind(on_press=self.go_home)
        layout.add_widget(label)
        layout.add_widget(back)
        self.add_widget(layout)

    def go_home(self, *args):
        self.manager.current = 'home'

class EchOSApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))

        # Try to load each app screen safely
        screens_to_load = [
            ('calm', CalmModeScreen),
            ('communicate', CommunicateScreen),
            ('planner', DailyPlannerScreen),
            ('safezone', ApplicationsScreen),
            ('shell', LimitedShellScreen),
        ]

        for name, screen_cls in screens_to_load:
            try:
                self.sm.add_widget(screen_cls(name=name))
            except Exception as e:
                print(f"[ERROR] Failed to load {name}: {e}")
                self.sm.add_widget(AppCrashScreen(app_name=name.capitalize(), name=name))

        return self.sm

    def on_start(self):
        Window.bind(on_key_down=self.handle_keys)

    def handle_keys(self, window, key, scancode, codepoint, modifiers):
        if 'ctrl' in modifiers and 'alt' in modifiers and codepoint == 't':
            self.sm.current = 'shell'

if __name__ == "__main__":
    sys.excepthook = global_exception_handler
    EchOSApp().run()
