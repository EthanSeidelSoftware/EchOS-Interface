from kivy.config import Config
Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'fullscreen', '1')  # <-- fullscreen ON

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os

from calm_mode import CalmModeScreen
from EchOSComunitcator import CommunicateScreen
from EchOSPlanner import DailyPlannerScreen
from SafeZone import SafeZoneScreen
from EchOSShell import LimitedShellScreen
from kivy.core.window import Window
from kivy.base import EventLoop


# ... rest of your code unchanged ...
# Window.fullscreen = True  # or 'auto', 'fake', 'borderless'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        layout.add_widget(Button(text="🗣️ Communicate", font_size=32, on_press=self.goto_communicate))
        layout.add_widget(Button(text="🎵 Calm Mode", font_size=32, on_press=self.goto_calm))
        layout.add_widget(Button(text="📅 Daily Planner", font_size=32, on_press=self.goto_planner))
        layout.add_widget(Button(text="🔒 Safe Zone", font_size=32, on_press=self.goto_safezone))
        
        # Add Power Off button at the bottom
        power_button = Button(text="⏻ Power Off", font_size=28, size_hint=(1, None), height=60)
        power_button.bind(on_press=self.show_power_menu)
        layout.add_widget(power_button)

        self.add_widget(layout)

    def goto_calm(self, *args):
        self.manager.current = 'calm'

    def goto_communicate(self, *args):
        self.manager.current = 'communicate'

    def goto_planner(self, *args):
        self.manager.current = 'planner'

    def goto_safezone(self, *args):
        self.manager.current = 'safezone'

    def show_power_menu(self, *args):
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)

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
        # Placeholder for actual shutdown/reboot commands
        if action == 'shutdown':
            print("Shutting down...")
            os.system("sudo shutdown -h now")
        elif action == 'reboot':
            print("Rebooting...")
            os.system("sudo reboot")
class EchOSApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CalmModeScreen(name='calm'))
        self.sm.add_widget(CommunicateScreen(name='communicate'))
        self.sm.add_widget(DailyPlannerScreen(name='planner'))
        self.sm.add_widget(SafeZoneScreen(name='safezone'))
        self.sm.add_widget(LimitedShellScreen(name='shell'))
        return self.sm

    def on_start(self):
        Window.bind(on_key_down=self.handle_keys)

    def handle_keys(self, window, key, scancode, codepoint, modifiers):
        if 'ctrl' in modifiers and 'alt' in modifiers and codepoint == 't':
            self.sm.current = 'shell'

if __name__ == "__main__":
    EchOSApp().run()
