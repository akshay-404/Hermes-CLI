from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.layout.containers import FloatContainer, Float
from prompt_toolkit.widgets import TextArea, Frame, Button, Dialog
from prompt_toolkit.key_binding import KeyBindings

class ChatUI:

    def __init__(self):

        self.username = None
        self.input_callback = None
        self.key_bindings = KeyBindings()

        self.chat_area = TextArea(
            text="",
            read_only=True,
            scrollbar=True,
            wrap_lines=True,
        )
        self.info_area = TextArea(
            height=1,
            read_only=True,
        )
        self.input_field = TextArea(
            height=1,
            prompt=lambda: f"{self.username} > " if self.username else "> ",
            multiline=False,
        )

        self.main_container = HSplit([
            Frame(self.chat_area, title="Hermes CLI"),
            Frame(self.info_area),
            Frame(self.input_field, title="Message"),
        ])

        self.floats = []
        self.root_container = FloatContainer(
            content=self.main_container,
            floats=self.floats,
        )

        @self.key_bindings.add("enter")
        def submit_message(event):
            if not event.app.layout.has_focus(self.input_field):
                return

            text = self.input_field.text
            if not text:
                return

            self.input_field.text = ""
            if self.input_callback:
                self.input_callback("default", text)

        @self.key_bindings.add("c-c")
        def _(event):
            event.app.exit()

        self.application = Application(
            layout=Layout(
                self.root_container,
                focused_element=self.input_field,
            ),
            key_bindings=self.key_bindings,
            full_screen=True,
            mouse_support=True
        )

        self.current_dialog = None

    def set_username(self, username=None):
        self.username = username
        self.application.invalidate()

    def set_input_callback(self, callback):
        self.input_callback = callback

    def print_system(self, message=""):
        current_text = self.chat_area.text
        new_text = (current_text + message + "\n")
        self.chat_area.buffer.set_document(
            Document(new_text),
            bypass_readonly=True,
        )
        self.chat_area.buffer.cursor_position = len(new_text)
        self.application.invalidate()

    def print_info(self, message):
        self.info_area.buffer.set_document(
            Document(message),
            bypass_readonly=True,
        )

    def print_message(self, username, message, timestamp, is_self=False):
        suffix = "*" if is_self else ""
        current_text = self.chat_area.text
        new_text = (
            current_text
            + f"[{timestamp}] {suffix} "
            + f"{username}: "
            + f"{message}\n"
        )
        self.chat_area.buffer.set_document(
            Document(new_text),
            bypass_readonly=True,
        )
        self.chat_area.buffer.cursor_position = len(new_text)

    def show_login(self):
        username_field = TextArea(
            height=1,
            prompt="Username: ",
            multiline=False,
        )
        password_field = TextArea(
            height=1,
            prompt="Password: ",
            multiline=False,
            password=True,
        )

        def login():
            username = username_field.text.strip()
            password = password_field.text

            if not username:
                self.print_system("[!] Username cannot be empty.")
                return
            if not password:
                self.print_system("[!] Password cannot be empty.")
                return

            if self.input_callback:
                self.input_callback(
                    "login",
                    {
                        "username": username,
                        "password": password,
                    },
                )

            self.close_dialog()

        def cancel():
            self.close_dialog()

        dialog = Dialog(title="Login", body=HSplit([
            username_field, password_field,
        ]),
            buttons=[Button(text="Login", handler=login,),
                     Button(text="Cancel", handler=cancel,),
                     ],
            width=40,
        )
        self.show_dialog(dialog, username_field,)

    def show_register(self):
        username_field = TextArea(
            height=1,
            prompt="Username: ",
            multiline=False,
        )
        password_field = TextArea(
            height=1,
            prompt="Password: ",
            multiline=False,
            password=True,
        )
        invite_field = TextArea(
            height=1,
            prompt="Invite code: ",
            multiline=False,
        )

        def register():
            username = username_field.text.strip()
            password = password_field.text
            invite_code = invite_field.text.strip()
            if not username:
                self.print_system("[!] Username cannot be empty.")
                return
            if not password:
                self.print_system("[!] Password cannot be empty.")
                return
            if not invite_code:
                self.print_system("[!] Invite code cannot be empty.")
                return

            if self.input_callback:
                self.input_callback(
                    "register",
                    {
                        "username": username,
                        "password": password,
                        "invite": invite_code,
                    },
                )
            self.close_dialog()

        def cancel():
            self.close_dialog()

        dialog = Dialog(
            title="Register",
            body=HSplit([
                username_field,
                password_field,
                invite_field,
            ]),
            buttons=[
                Button(text="Register", handler=register,),
                Button(text="Cancel", handler=cancel,),
                     ],
            width=40,
        )
        self.show_dialog(dialog, username_field,)

    def show_dialog(self, dialog, focus_element,):
        self.current_dialog = dialog
        self.floats.append(
            Float(
                content=dialog,
            )
        )
        self.application.invalidate()
        self.application.layout.focus(focus_element)

    def close_dialog(self):
        self.floats.clear()
        self.current_dialog = None
        self.application.invalidate()
        self.application.layout.focus(self.input_field)

    def run(self):
        self.application.run()

    def stop(self):
        self.application.exit()
