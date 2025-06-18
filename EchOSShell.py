from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
import subprocess

class TerminalOutput(Label):
    text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "assets/DejaVuSansMono.ttf"
        self.font_size = 14
        self.markup = True
        self.halign = 'left'
        self.valign = 'top'
        self.text_size = (Window.width, None)  # Wrap only vertically
        self.size_hint_y = None
        self.bind(texture_size=self.update_size)

    def update_size(self, *args):
        self.height = self.texture_size[1]

class LimitedShellScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.terminal_text = "[b]EchOS Terminal[/b]\n$ "
        self.current_input = ""

        self.output = TerminalOutput(text=self.terminal_text)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        scroll.add_widget(self.output)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(scroll)
        self.add_widget(layout)

        Window.bind(on_key_down=self.on_key_down)

        self.allowed_cmds = ["ls", "df", "uptime", "whoami", "uname -a", "free -h", "date", "clear"]

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 8:  # Backspace
            self.current_input = self.current_input[:-1]
        elif key in (13, 271):  # Enter
            self.process_command(self.current_input.strip())
            self.current_input = ""
        elif codepoint and codepoint.isprintable():
            self.current_input += codepoint

        # Update display
        self.output.text = self.terminal_text + self.current_input
        return True

    def process_command(self, cmd):
        if not cmd.strip():
            self.terminal_text += "$ "
            self.output.text = self.terminal_text
            return

        blocked_cmds = ["sudo", "rm", "python", "python3", "reboot", "shutdown", "poweroff"]
        base_cmd = cmd.split()[0]

        if base_cmd in blocked_cmds:
            self.terminal_text += f"{cmd}\nCommand '{base_cmd}' is not allowed.\n$ "
        elif cmd == "clear":
            self.terminal_text = "[b]EchOS Terminal[/b]\n$ "
        else:
            try:
                result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
                self.terminal_text += f"{cmd}\n{result}$ "
            except subprocess.CalledProcessError as e:
                self.terminal_text += f"{cmd}\n{e.output}$ "
            except Exception as e:
                self.terminal_text += f"{cmd}\nError: {str(e)}\n$ "

        self.output.text = self.terminal_text


