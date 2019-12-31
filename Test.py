from kivy.uix.screenmanager import ScreenManager, Screen

# Create the manager
sm = ScreenManager()

# Add few screens
for i in range(4):
    screen = Screen(name='Title %d' % i)
    sm.add_widget(screen)

# By default, the first screen added into the ScreenManager will be
# displayed. You can then change to another screen.

# Let's display the screen named 'Title 2'
# A transition will automatically be used.
sm.current = 'Title 2'


class BSXApp(App):
    def build(self):
        self.root = ScreenManager()

        self.welcomesc = Screen(name="welcomesc")
        self.welcome_message = welcome()
        # noinspection PyListCreation
        self.years = [1975, 2020]
        self.years.append(f"Specify default battle year {self.years[0]} - {self.years[1]}:")

        welcome_box = BoxLayout(orientation='vertical', size_hint_y=5)

        maim_img = Image(source="IS.ico", size_hint_y=3)

        lower_welcome_box = BoxLayout(orientation="horizontal", size_hint_y=2)

        air_img = Image(source="Air.png", size_hint_y=1)
        welcome_text = Label(size_hint_y=1, halign="center", valign="center", text=self.welcome_message)
        navy_img = Image(source="Navy.png", size_hint_y=1)

        welcome_box.add_widget(maim_img)
        welcome_box.add_widget(lower_welcome_box)
        lower_welcome_box.add_widget(air_img)
        lower_welcome_box.add_widget(welcome_text)
        lower_welcome_box.add_widget(navy_img)

        oob_bs_grid = GridLayout(height=50, size_hint_y=None, cols=4)

        blank_years = Widget(size_hint_x=1)
        oob_bs_years = Label(text=self.years[2], halign="right", valign="center", size_hint_x=2)
        oob_bs_years_in = TextInput(multiline=False, halign="center", size_hint_x=2)
        repeater_years = Label(size_hint_x=1)

        oob_bs_grid.add_widget(blank_years)
        oob_bs_grid.add_widget(oob_bs_years)
        oob_bs_grid.add_widget(oob_bs_years_in)
        oob_bs_grid.add_widget(repeater_years)

        oob_bs_grid_sidea = GridLayout(height=50, size_hint_y=None, cols=4)

        blank_sidea = Widget(size_hint_x=1)
        oob_bs_sidea = Label(text="Side 1 # of units:", halign="right", valign="center", size_hint_x=3)
        oob_bs_sidea_in = TextInput(multiline=False, halign="center", size_hint_x=1)
        repeater_sidea = Label(size_hint_x=1)

        oob_bs_grid_sidea.add_widget(blank_sidea)
        oob_bs_grid_sidea.add_widget(oob_bs_sidea)
        oob_bs_grid_sidea.add_widget(oob_bs_sidea_in)
        oob_bs_grid_sidea.add_widget(repeater_sidea)

        oob_bs_grid_sideb = GridLayout(height=50, size_hint_y=None, cols=4)

        blank_sideb = Widget(size_hint_x=1)
        oob_bs_sideb = Label(text="Side 2 # of units:", halign="right", valign="center", size_hint_x=3)
        oob_bs_sideb_in = TextInput(multiline=False, halign="center", size_hint_x=1)
        repeater_sideb = Label(size_hint_x=1)

        oob_bs_grid_sideb.add_widget(blank_sideb)
        oob_bs_grid_sideb.add_widget(oob_bs_sideb)
        oob_bs_grid_sideb.add_widget(oob_bs_sideb_in)
        oob_bs_grid_sideb.add_widget(repeater_sideb)

        oob_bs_button_grid = GridLayout(height=50, size_hint_y=None, cols=3)

        blank_bs_button = Label(size_hint_x=1)
        oob_bs_button = Button(text="Finish", halign="right", valign="center", size_hint_x=4)
        repeater_bs_button = Label(size_hint_x=1)

        oob_bs_button_grid.add_widget(blank_bs_button)
        oob_bs_button_grid.add_widget(oob_bs_button)
        oob_bs_button_grid.add_widget(repeater_bs_button)

        self.welcomesc.add_widget(welcome_box)
        self.welcomesc.add_widget(oob_bs_grid)
        self.welcomesc.add_widget(oob_bs_grid_sidea)
        self.welcomesc.add_widget(oob_bs_grid_sideb)
        self.welcomesc.add_widget(oob_bs_button_grid)

        self.root.add_widget(self.welcomesc)
        return self.root


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
