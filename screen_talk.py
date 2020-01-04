from random import choice, randint

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

screen_talk_kv = """
<ScreenOne>:
    # Set the name, of course.

    name: "screen_one"

    # Set text_input_x attributes for ScreenOne, where each
    # text_input_x refers to text_input_x which are id values.
 
    # These are to be used in ScreenTwo

    text_input_one: text_input_one
    text_input_two: text_input_two

    GridLayout:
        cols: 2
        rows: 2
        padding: "10px"

        # Create the TextInput widgets, and then assign ids

        TextInput:
            id: text_input_one

            # on_text is an event that fires off everytime the
            # text inside TextInput is changed e.g. when you
            # type or as long as it changes it general, in this
            # case, what we do is we refer to the ScreenOne
            # widget with root, then we refer to its screen_two
            # attribute, which can be seen later, then we refer
            # to the label_one attribute of screen_two, and
            # finally, the text attribute of label_one...

            # After all that traversal, we make the text attribute
            # be equals to args[1], which is a variable available
            # because of how on_text works.

            on_text: root.screen_two.label_one.text = args[1]

        TextInput
            id: text_input_two
            on_text: root.screen_two.label_two.text = args[1]

        Button:
            text: "Request random integer."

            # The on_press behavior just modifies text_input_x
            # by requesting a random integer through a method
            # defined in the ScreenOne class.

            on_press:
                text_input_one.text = root.request_random_int()
                text_input_two.text = root.request_random_int()

        Button:
            text: "Move on to next screen."

            # Just changes screens :D

            on_press:
                root.manager.current = "screen_two"


<ScreenTwo>:
    name: "screen_two"

    # Set label_x attributes for ScreenTwo where each
    # label_x refers to label_x which are id values.

    # These are used in ScreenOne

    label_one: label_one
    label_two: label_two

    GridLayout
        cols: 2
        rows: 2
        padding: "10px"

        Label:
            id: label_one

            # As discussed above, on_text is an event, in this case
            # we're accessing ScreenTwo.screen_one.text_input_one.text
            # and modifying it with the new value of this label.

            on_text: root.screen_one.text_input_one.text = args[1]

        Label:
            id: label_two
            on_text: root.screen_one.text_input_two.text = args[1]

        Button:
            text: "Return to previous screen."
            on_press:
                root.manager.current = "screen_one"

        Button:
            text: "Choose from foo, bar, and baz."
            on_press:

                # Modifies the text attributes of label_x by
                # calling a method in the root class.

                label_one.text = root.choose_foo_bar_baz()
                label_two.text = root.choose_foo_bar_baz()


ScreenManager:
    ScreenOne:
        id: screen_one
        screen_two: screen_two  # This is where we actually set the screen_two attribute.

    ScreenTwo:
        id: screen_two
        screen_one: screen_one  # Same as above.
"""


class ScreenOne(Screen):
    # As you can see, if you don't need to access any
    # widget properties in Python, you don't need to
    # declare them as one e.g.
    # screen_two = ObjectProperty(None)

    def request_random_int(self):
        return str(randint(100_000, 999_999))


class ScreenTwo(Screen):
    def choose_foo_bar_baz(self):
        return choice(("foo", "bar", "baz"))


class ScreenTalkApp(App):
    def build(self):
        # Manually load the kv file because 
        # we've overriden the build method.
        self.root = Builder.load_string(screen_talk_kv)


if __name__ == "__main__":
    ScreenTalkApp().run()
