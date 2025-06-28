from kivy.config import Config
Config.set('kivy', 'video', 'ffpyplayer')

from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class CalmModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Use a FloatLayout to overlay the back button on top of the video
        layout = FloatLayout()

        self.video = Video(
            source="assets/breathing_loop.mp4",
            state='stop',
            options={'eos': 'loop'},
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        layout.add_widget(self.video)

        # Small back button in top-left corner
        back_button = Button(
            text="← Back",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'x': 0, 'top': 1},
            font_size=18,
            on_press=self.go_home
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

        self.sound = None

    def on_enter(self):
        if not self.sound:
            self.sound = SoundLoader.load("assets/calm_music.mp3")
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        self.video.state = 'play'

    def on_leave(self):
        if self.sound:
            self.sound.stop()
        self.video.state = 'stop'

    def go_home(self, *args):
        self.manager.current = 'home'
