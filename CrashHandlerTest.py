import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import time

class ApplicationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.title = Label(
            text="📱 Applications",
            font_size=36,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=60
        )
        self.title.bind(size=self.title.setter('text_size'))

        self.layout.add_widget(self.title)

        # Scrollable container for apps
        self.app_scroll = ScrollView(size_hint=(1, 1))
        self.app_list_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.app_list_layout.bind(minimum_height=self.app_list_layout.setter('height'))
        self.app_scroll.add_widget(self.app_list_layout)

        self.layout.add_widget(self.app_scroll)

        # Back button
        back_btn = Button(text="← Back", font_size=24, size_hint=(1, None), height=60)
        back_btn.bind(on_press=self.go_home)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

        self.refresh_app_list()
        time.sleep(10)


    def refresh_app_list(self):
        self.app_list_layout.clear_widgets()

        app_folder = os.path.join(os.getcwd(), "applications")
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)

        app_files = [f for f in os.listdir(app_folder) if f.endswith('.appimage')]

        if app_files:
            for app in app_files:
                btn = Button(
                    text=app,
                    font_size=20,
                    size_hint=(1, None),
                    height=50
                )
                # Placeholder: you could bind btn to launch the app
                self.app_list_layout.add_widget(btn)
        else:
            no_apps = Label(
                text="🚫 No applications installed",
                font_size=24,
                halign='center',
                valign='middle',
                size_hint=(1, None),
                height=100
            )
            no_apps.bind(size=no_apps.setter('text_size'))
            self.app_list_layout.add_widget(no_apps)

    def on_enter(self):
        self.refresh_app_list()

    def go_home(self, *args):
        self.manager.current = 'home'
        print(0/0)