import os.path

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import exists

from kivy.uix.widget import Widget

"""Python naming conventions: Capital in front of every word (also because errors with screen manager and camel case 
naming) Creates window manager"""

# loads kv file
kv = Builder.load_file('main.kv')


# screens
class MainPage(Screen):
    pass


class MyPrayers(Screen):
    # code to see how many buttons it should generate

    # checking if file doesn't exist, creates it
    if not exists("data/LocalPrayers.txt"):
        if not exists("data/"):
            os.makedirs("data/")
        with open("data/LocalPrayers.txt", "x") as f:
            pass

    # reads how many lines are in the file
    count = 0
    with open("data/LocalPrayers.txt", "r") as data:
        for count, line in enumerate(data):
            pass

    def __init__(self, **kwargs):
        super(MyPrayers, self).__init__(**kwargs)
        label = Button(text="hello world!")
        for i in range(self.count + 1):
            self.ids.FillIn.add_widget(label)


# app class
class PrayerApp(App):
    def build(self):
        return kv


# run app
if __name__ == '__main__':
    PrayerApp().run()
