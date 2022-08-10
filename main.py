import os.path
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import exists
from kivy.config import Config

from kivy.uix.widget import Widget

Config.set("input", 'mouse', "mouse,multitouch_on_demand")

"""Python naming conventions: Capital in front of every word (also because errors with screen manager and camel case 
naming) Creates window manager"""


# screens
class MainPage(Screen):
    pass

class MyPrayers(Screen):

    def __init__(self, **kwargs):
        super(MyPrayers, self).__init__(**kwargs)
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            for i in range(6):
                localPrayers.append(data.readline())
        print(localPrayers)

        Clock.schedule_once(self.AddButtons(ButtonText=localPrayers, start=0))

    def AddButtons(self, *args, ButtonText, start):
        for i in range(6):
            print(i)
            self.ids.FillIn.add_widget.add_widget(Button(text=ButtonText[i],
                                                         color=(0, 0, 0),
                                                         background_normal="",
                                                         background_color=(1, 1, 1),
                                                         size_hint=(0.8, 1),
                                                         pos_hint={"x": 0.1}))
            self.ids.FillIn.add_widget(Label(size_hint_y=0.2))


# app class
class PrayerApp(App):
    def build(self):
        # loads kv file
        kv = Builder.load_file('main.kv')
        return kv


# run app
if __name__ == '__main__':
    # code to see how many buttons it should generate

    # checking if file doesn't exist, creates it
    if not exists("data/LocalPrayers.txt"):
        if not exists("data/"):
            os.makedirs("data/")
        with open("data/LocalPrayers.txt", "x") as f:
            pass
    PrayerApp().run()
