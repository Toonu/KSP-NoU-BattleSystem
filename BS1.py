"""
BS 1.0
"""

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


def welcome():
    """
    Introducing welcome!
    """
    headline = f"Welcome to Battle System Manager v 0.9.2 (ALPHA)"
    message = f"{headline}\n" \
              f"{' ' * ((len(headline) // 2) + 6)}Made by Toonu\n" \
              f"{' ' * (len(headline) // 2)}The Emperor of Iconia\n" \
              f"{' ' * ((len(headline) // 2) - 11)}With the help of Red, Litz and Sleepy"
    return message


class BSApp(App):
    font_size = NumericProperty(20)
    welcome_message = welcome()
    years = [1975, 2020]
    years.append(f"Specify default battle year {years[0]} - {years[1]}:")

    def oob_battle_configuration(self, years_text_input, side_1, side_2, years):
        """

        @param years_text_input:
        @param side_1:
        @param side_2:
        @param years:
        """
        if self.user_input_ui(years_text_input, minimum=years[0], maximum=years[1]) and \
                self.user_input_ui(side_1, minimum=1, maximum=99) and self.user_input_ui(side_2, minimum=1, maximum=99):
            print("YES")
            # TODO GoTo next screen
        else:
            print("NO")

    def user_input_ui(self, fn, fn_res=None, minimum=0, maximum=1, string=False, check=""):
        """

        @param fn:
        @param fn_res:
        @param minimum:
        @param maximum:
        @param string:
        @param check:
        @return:
        """
        fn.font_size = 0.5 * fn.height
        from re import match
        try:
            if string and match(check, fn.text) is not None:
                if fn_res is not None:
                    fn_res.text = "Correct input!"
                return True
            elif minimum <= int(fn.text) <= maximum:
                if fn_res is not None:
                    fn_res.text = "Correct input!"
                return True
        except ValueError:
            if fn_res is not None:
                fn_res.text = "Invalid input!"
        else:
            if fn_res is not None:
                fn_res.text = "Invalid input!"
            return False

    def build(self):
        """

        @return:
        """
        root_widget = Interface()
        return root_widget


class Interface(BoxLayout):
    """

    """
    pass


class CalculatorApp(App):
    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        output_label = Label(size_hint_y=1)

        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=')

        button_grid = GridLayout(cols=4, size_hint_y=2)  # Size hint reserves twice space for this than for label above
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        clear_button = Button(text='clear',
                              size_hint_y=None,  # If height set and hint none, it always have this size no matter what
                              height=100)

        def print_button_text(instance):
            output_label.text += instance.text

        def resize_label_text(label, new_height):  # makes the text half size of the box
            label.font_size = 0.5 * label.height

        output_label.bind(height=resize_label_text)

        def evaluate_result(instance):  # calculates the result when = is pressed
            try:
                output_label.text = str(eval(output_label.text))
            except SyntaxError:
                output_label.text = 'Python syntax error!'

        button_grid.children[0].bind(on_press=evaluate_result)

        # Remember, button_grid.children[0] is the '=' button

        def clear_label(instance):  # clears the label
            output_label.text = ''

        clear_button.bind(on_press=clear_label)

        for button in button_grid.children[1:]:  # children property is for every widget,
            # has all widgets attached to it
            button.bind(on_press=print_button_text)  # Binds the function above to each button

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)

        return root_widget


if __name__ == "__main__":
    BSApp().run()
