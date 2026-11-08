from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HelloApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.message = Label(text="Hello, welcome to Kivy!")
        button = Button(text="Click Me")
        button.bind(on_press=self.change_message)
        layout.add_widget(self.message)
        layout.add_widget(button)
        return layout

    def change_message(self, instance):
        self.message.text = "Button clicked!"


if __name__ == "__main__":
    HelloApp().run()
