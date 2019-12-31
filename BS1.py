"""
BS 1.0
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


def welcome():
    """
    Introducing welcome!
    """
    headline = f"Welcome to Battle System Manager v 0.9.2 (ALPHA)"
    message = f"{headline}\n" \
              f"{' ' * ((len(headline) // 2) + 7)}Made by Toonu\n" \
              f"{' ' * ((len(headline) // 2) + 1)}The Emperor of Iconia\n" \
              f"{' ' * ((len(headline) // 2) - 10)}With the help of Red, Litz and Sleepy"
    return message


class Interface(BoxLayout):
    years = [1975, 2020]
    welcome_message = welcome()
    years.append(f"Specify default battle year {years[0]} - {years[1]}:")


class BSApp(App):
    def align_text(self, label):  # makes the text half size of the box
        label.font_size = 0.5 * label.height

    def build(self):
        return Interface()


if __name__ == '__main__':
    BSApp().run()
