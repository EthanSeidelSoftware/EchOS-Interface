from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SafeZoneScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)

        label = Label(
            text="🛡️ You are safe here.\nTake a deep breath.",
            font_size=36,
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))  # Wrap text

        calm_btn = Button(text="🎵 Enter Calm Mode", font_size=24, size_hint=(1, None), height=60)
        calm_btn.bind(on_press=self.go_to_calm)

        back_btn = Button(text="← Back", font_size=24, size_hint=(1, None), height=60)
        back_btn.bind(on_press=self.go_home)

        layout.add_widget(label)
        layout.add_widget(calm_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_to_calm(self, *args):
        self.manager.current = 'calm'

    def go_home(self, *args):
        self.manager.current = 'home'
