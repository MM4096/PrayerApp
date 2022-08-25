import os.path
from os.path import exists
from kivy import app
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import *
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

# for desktop users, right-clicking doesn't generate a red dot
Config.set("input", 'mouse', "mouse,multitouch_on_demand")

"""Python naming conventions: Capital in front of every word (also because errors with screen manager and camel case 
naming) Creates window manager"""


# screens
class WindowManager(ScreenManager):
    pass


class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)


class MyPrayers(Screen):

    def __init__(self, **kwargs):
        self.PrayerIndex = 0
        super(MyPrayers, self).__init__(**kwargs)
        # creating the variables here first
        self.PrayerBox = BoxLayout()
        self.rectangle = None
        # draws layout
        Clock.schedule_once(self.DrawLayout)
        # Reads 6 lines at a time, to get your prayer
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
            localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))

    def DrawLayout(self, *args):
        # BoxLayout
        MainBox = BoxLayout(orientation="vertical")
        # Adds the title
        TitleLabel = Label(text="Personal Prayer List",
                           size_hint_y=0.3,
                           font_size=dp(32),
                           color=(1, 1, 1))
        # BoxLayout for the prayers
        self.PrayerBox = BoxLayout(orientation="vertical")
        # adding widgets
        MainBox.add_widget(TitleLabel)
        MainBox.add_widget(self.PrayerBox)
        self.add_widget(MainBox)

    def AddButtons(self, *ButtonText):
        StartingIndex = self.PrayerIndex
        # see if first index exists
        if StartingIndex < len(ButtonText[0]):
            for i in range(5):
                # see if value exists
                try:
                    # Creates the styled buttons
                    self.PrayerBox.add_widget(Button(text=str(ButtonText[0][i + StartingIndex]),
                                                     color=(0, 0, 0),
                                                     background_normal="",
                                                     background_color=(1, 1, 1),
                                                     size_hint=(0.8, 1),
                                                     pos_hint={"x": 0.1}))
                    # margin between buttons
                    self.PrayerBox.add_widget(Label(size_hint_y=0.2))
                    # generate empty label same size as button
                except IndexError:
                    self.PrayerBox.add_widget(Label(size_hint_y=1.2))
            # even bigger margin for the buttons to go
            self.PrayerBox.add_widget(Label(size_hint_y=0.2))

    def LoadMore(self):
        self.PrayerBox.clear_widgets()
        self.PrayerIndex += 5
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))

    def reset(self):
        localPrayers = []
        self.PrayerIndex = 0
        self.PrayerBox.clear_widgets()
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))


class CreatePage(Screen):
    title = StringProperty("")
    content = StringProperty("")

    def submit(self, widget):
        # gets data
        self.title = self.ids.title.text
        self.content = self.ids.body.text
        # replaces \n with tag <newline>
        self.content = self.content.replace("\n", "<newline>")
        # finding "illegal" characters
        if "\\" or "~" or "<newline>" in self.title:
            self.ids.TitleError.text = "Error: You cannot use words/characters: \\ ~ <newline> in your title or content"
        elif "\\" or "~" or "<newline>" in self.content:
            self.ids.TitleError.text = "Error: You cannot use words/characters: \\ ~ <newline> in your title or content"
        elif self.title == "":
            self.ids.TitleError.text = "Error: You must enter a title"
        else:
            # making the prayer in the way it is saved
            writeStr = self.title + "~" + self.content
            with open("data/LocalPrayers.txt", 'r+') as file:
                # reads file
                data = file.read()
                # places writing at start
                file.seek(0, 0)
                # writes
                file.write(writeStr + "\n" + data)


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
