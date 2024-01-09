from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.core.window import Window
import os
import datetime

Window.size = (350, 600)

class TimerWindow(Screen):

    # Starting image
    start_img = 'Fruits/fresita.png'

    # Colors used
    GREEN = "#5D9C59"
    DEEP_PINK = "#EE1289"
    PINK_RGB = (1, 0.8196078431372549, 0.8549019607843137)
    PURPLE = "#9336B4"

    # Size for buttons
    x_size = NumericProperty(1)
    y_size = NumericProperty(None)


class MainWindow(Screen):
    pass


class Aideefresa(MDApp):

    dogs_list = [img for img in os.listdir('Dogs')]
    fruits_list = [img for img in os.listdir('Fruits')]
    cats_list = [img for img in os.listdir('Cats')]
    DEEP_PINK_RGB = (0.9333333333333333, 0.07058823529411765, 0.5372549019607843, 1)
    PINK_RGB = (1, 0.8196078431372549, 0.8549019607843137, 1)

    def build(self):

        sm = ScreenManager(transition=FadeTransition(duration=0.10))
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(TimerWindow(name='timer'))
        self.theme_cls.primary_palette = "Purple"

        self.cats_index = 0
        self.fruits_index = 0
        self.dogs_index = 0
        self.reps = 0
        self.reset = 0


        # get_screen('timer') didn't work in this function
        # because it has to be called after the app is built
        # if not, NoneType has no attribute "get_screen"...

        return sm

    def customize_time(self):

        work_time = self.root.get_screen('main').ids.user_work_time_input.text
        break_time = self.root.get_screen('main').ids.user_break_time_input.text

        if work_time == "" or break_time == "":
            self.root.current = 'main'

        else:
            self.root.current = 'timer'

            self.initial_time = float(work_time) * 60
            self.time = float(work_time) * 60
            self.short_break = float(break_time) * 60

            self.root.get_screen('timer').ids.timer_label.text = self.format_timer()

    def dogs_update(self):
        self.animals_index += 1

        if self.animals_index == len(self.dogs_list):
            self.animals_index = 0

        self.root.get_screen('timer').ids.center_img.source = f"Dogs/{self.dogs_list[self.animals_index]}"

    def fruits_update(self):
        self.fruits_index += 1

        if self.fruits_index == len(self.fruits_list):
            self.fruits_index = 0

        self.root.get_screen('timer').ids.center_img.source = f"Fruits/{self.fruits_list[self.fruits_index]}"

    def cats_update(self):
        self.bisito_index += 1

        if self.bisito_index == len(self.cats_list):
            self.bisito_index = 0

        self.root.get_screen('timer').ids.center_img.source = f"Cats/{self.cats_list[self.bisito_index]}"

    def change_button(self):

        if self.root.get_screen('timer').ids.fruits_button.text == "Button 3":
            self.root.get_screen('timer').ids.fruits_button.text = "3rd Button"

        else:
            self.root.get_screen('timer').ids.fruits_button.text = "Button 3"

    def start_clock(self):
        Clock.schedule_interval(self.update_label, 1)
        self.root.get_screen('timer').ids.start_button.disabled = True

    def reset_clock(self):

        # goes back to main screen if the "reset" button is pressed twice
        self.reset += 1

        if self.reset == 2:
            self.root.current = 'main'
            self.root.transition.direction = "right"
            self.reset = 0

        self.time = self.initial_time

        # TODO
        self.root.get_screen('timer').ids.timer_label.text = self.format_timer()
        self.root.get_screen('timer').ids.left_label.text = "Work label 1"
        self.root.get_screen('timer').ids.right_label.text = "Work label 2"

        for widget in self.root.walk():
            for widget_name in widget.ids:
                if "label" in widget_name:
                    widget.ids[widget_name].color = TimerWindow.GREEN
                elif "button" in widget_name:
                    widget.ids[widget_name].md_bg_color = TimerWindow.DEEP_PINK

        # Enable the start button
        self.root.get_screen('timer').ids.start_button.disabled = False
        Clock.unschedule(self.update_label)

    def update_label(self, instance):

        # Number of seconds is being reduced by 1 every second
        # Clock is updating this specific function
        # That is the reason why our time is decreasing here

        self.time -= 1

        # Every second, the label is also updated
        # TODO
        self.root.get_screen('timer').ids.timer_label.text = self.format_timer()

        # This series of if statements checks whether it's time for a work or a break session
        # This is done by using a global variable "self.reps"
        # Which keeps tracks of the rounds completed and depending on how many rounds
        # The timer will start from the respective time
        if self.time == 0 and self.reps % 2 != 0:
            self.time = self.initial_time
            self.root.get_screen('timer').ids.left_label.text = "Work label 1"
            self.root.get_screen('timer').ids.right_label.text = "Work label 2"

            for widget in self.root.walk():
                for widget_name in widget.ids:
                    # Getting value through the key, in this case "widget_name"
                    # And changing labels color
                    if "label" in widget_name:
                        widget.ids[widget_name].color = TimerWindow.GREEN

                        # Changing buttons color
                    elif "button" in widget_name:
                        widget.ids[widget_name].md_bg_color = TimerWindow.DEEP_PINK

            self.reps += 1

        elif self.time == 0 and self.reps % 2 == 0:
            self.time = self.short_break
            self.root.get_screen('timer').ids.left_label.text = "Break label 1"
            self.root.get_screen('timer').ids.right_label.text = "Break label 2"

            for widget in self.root.walk():

                # widget.ids is dictionary
                for widget_name in widget.ids:
                    if "label" in widget_name:
                        # Getting value through the key, in this case "widget_name"
                        # And changing labels color
                        widget.ids[widget_name].color = TimerWindow.PURPLE

                        # Changing buttons color
                    elif "button" in widget_name:
                        widget.ids[widget_name].md_bg_color = TimerWindow.PURPLE

            self.reps += 1

    def format_timer(self):

        # Format the timer seconds to the "00:00" format
        formatted_time = datetime.timedelta(seconds=self.time)

        # Return the formatted time
        return str(formatted_time)


if __name__ == "__main__":
    Aideefresa().run()
