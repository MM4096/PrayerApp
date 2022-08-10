import os.path
from kivy.clock import Clock
from kivy.app import App
from kivy.graphics import Color
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import exists
from kivy.config import Config
from kivy.graphics import *

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
        self.PrayerBox = BoxLayout()
        self.rectangle = None
        Clock.schedule_once(self.DrawLayout)
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            for i in range(6):
                localPrayers.append(data.readline())
        print(localPrayers)
        Clock.schedule_once(self.AddButtons(ButtonText=localPrayers))

    def DrawLayout(self, *args):
        MainBox = BoxLayout(orientation="vertical")
        TitleLabel = Label(text="Personal Prayer List",
                           size_hint_y=0.3,
                           font_size=dp(32),
                           color=(1, 1, 1))
        self.PrayerBox = BoxLayout(orientation="vertical")

        with self.canvas:
            Color(rgb=(0.25, 0.45, 0.62))

            self.rectangle = Rectangle(pos=self.center, size=(self.width / 2, self.height / 2))
            self.bind(pos=self.UpdateRectangle, size=self.UpdateRectangle)
        MainBox.add_widget(TitleLabel)
        MainBox.add_widget(self.PrayerBox)
        self.add_widget(MainBox)

    def UpdateRectangle(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

    def AddButtons(self, *args, ButtonText):
        for i in range(6):
            self.PrayerBox.add_widget(Button(text=ButtonText[i],
                                             color=(0, 0, 0),
                                             background_normal="",
                                             background_color=(1, 1, 1),
                                             size_hint=(0.8, 1),
                                             pos_hint={"x": 0.1}))
            self.PrayerBox.add_widget(Label(size_hint_y=0.2))


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
