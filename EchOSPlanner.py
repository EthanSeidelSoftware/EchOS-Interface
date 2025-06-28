from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class DailyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Input area
        self.task_input = TextInput(hint_text="Enter a task...", font_size=24, size_hint=(1, None), height=60)
        add_btn = Button(text="Add Task", font_size=24, size_hint=(1, None), height=60)
        add_btn.bind(on_press=self.add_task)

        input_row = BoxLayout(size_hint=(1, None), height=60)
        input_row.add_widget(self.task_input)
        input_row.add_widget(add_btn)
        layout.add_widget(input_row)

        # Scrollable task list
        self.task_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_layout.bind(minimum_height=self.task_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 0.4))
        scroll.add_widget(self.task_layout)
        layout.add_widget(scroll)

        # On-screen keyboard
        keyboard_rows = [
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L',';'],
            ['Z','X','C','V','B','N','M',',','.','?'],
            ['','','','','','Space','','','←','']
        ]
        keyboard_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.3))
        for row in keyboard_rows:
            row_layout = BoxLayout(spacing=5)
            for key in row:
                if key == '':
                    row_layout.add_widget(Button(disabled=True, background_color=(0, 0, 0, 0)))
                elif key == 'Space':
                    btn = Button(text='␣', font_size=20)
                    btn.bind(on_press=lambda i: self.add_character(' '))
                    row_layout.add_widget(btn)
                elif key == '←':
                    btn = Button(text='⌫', font_size=20)
                    btn.bind(on_press=self.backspace)
                    row_layout.add_widget(btn)
                else:
                    btn = Button(text=key, font_size=20)
                    btn.bind(on_press=lambda i, k=key: self.add_character(k))
                    row_layout.add_widget(btn)
            keyboard_layout.add_widget(row_layout)
        layout.add_widget(keyboard_layout)

        # Back button
        back_btn = Button(text="← Back", font_size=24, size_hint=(1, None), height=60)
        back_btn.bind(on_press=self.go_home)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def add_task(self, *args):
        task_text = self.task_input.text.strip()
        if task_text:
            task_btn = Button(text=task_text, font_size=20, size_hint_y=None, height=50)
            task_btn.bind(on_press=lambda btn: self.task_layout.remove_widget(btn))  # Quick delete
            self.task_layout.add_widget(task_btn)
            self.task_input.text = ""

    def add_character(self, char):
        self.task_input.text += char

    def backspace(self, *args):
        self.task_input.text = self.task_input.text[:-1]

    def go_home(self, *args):
        self.manager.current = 'home'
