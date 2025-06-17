from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import pyttsx3
from kivy.uix.textinput import TextInput

class CommunicateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)

        self.sentence = ""

        main_layout = BoxLayout(orientation='horizontal', spacing=20, padding=20)

        # LEFT SIDE: Quick Phrases
        phrases = ["I want", "I'm hungry", "I'm sad", "I need help", "Yes", "No"]
        phrase_layout = GridLayout(cols=1, spacing=10, size_hint=(0.3, 1))
        for phrase in phrases:
            btn = Button(text=phrase, font_size=28)
            btn.bind(on_press=self.add_to_sentence)
            phrase_layout.add_widget(btn)

        # RIGHT SIDE: Sentence + Bottom Buttons
        right_layout = BoxLayout(orientation='vertical', spacing=20)

        self.sentence_input = TextInput(
            text="",
            font_size=36,
            size_hint=(1, 0.8),
            multiline=True,
            readonly=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1)
        )
        right_layout.add_widget(self.sentence_input)

        # Bottom button row: Speak + Back
        bottom_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=20)
        speak_btn = Button(text="🔊 Speak", font_size=24, background_color=(0.2, 0.7, 0.4, 1))
        speak_btn.bind(on_press=self.speak_sentence)
        back_btn = Button(text="← Back", font_size=24, background_color=(0.6, 0.6, 0.6, 1))
        back_btn.bind(on_press=self.go_home)

        bottom_buttons.add_widget(speak_btn)
        bottom_buttons.add_widget(back_btn)
        right_layout.add_widget(bottom_buttons)

        # Combine layouts
        main_layout.add_widget(phrase_layout)
        main_layout.add_widget(right_layout)
        self.add_widget(main_layout)

    def update_text_size(self, *args):
        self.sentence_label.text_size = self.sentence_label.size

    def add_to_sentence(self, instance):
        self.sentence_input.text += instance.text + " "

    def speak_sentence(self, *args):
        text = self.sentence_input.text.strip()
        if text:
            self.tts.say(text)
            self.tts.runAndWait()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # Check for Ctrl+Alt+D
        if 'ctrl' in modifiers and 'alt' in modifiers and codepoint.lower() == 'd':
            filepath = os.path.join(os.getcwd(), 'LongTTSTest.txt')
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.sentence_input.text += "\n" + f.read()
            else:
                print("LongTTSTest.txt not found.")


    def go_home(self, *args):
        self.manager.current = 'home'
