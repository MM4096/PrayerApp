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

# for viewing prayers (index)
viewPrayersIndex = 0

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
        self.prayerIndex = 0
        super(MyPrayers, self).__init__(**kwargs)
        # creating the variables here first
        self.prayerBox = BoxLayout()
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
        # separation of title with content
        for i in range(len(localPrayers)):
            localPrayers[i] = localPrayers[i].split("~")
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))

    def DrawLayout(self, *args):
        # BoxLayout
        mainBox = BoxLayout(orientation="vertical")
        # Adds the title
        titleLabel = Label(text="Personal Prayer List",
                           size_hint_y=0.3,
                           font_size=dp(32),
                           color=(1, 1, 1))
        # BoxLayout for the prayers
        self.prayerBox = BoxLayout(orientation="vertical")
        # adding widgets
        mainBox.add_widget(titleLabel)
        mainBox.add_widget(self.prayerBox)
        self.add_widget(mainBox)

    def AddButtons(self, *buttonText):
        startingIndex = self.prayerIndex
        # see if first index exists
        if startingIndex < len(buttonText[0]):
            for i in range(5):
                # see if value exists
                try:
                    button = Button(text=str(buttonText[0][i + startingIndex][0]),
                                    color=(0, 0, 0),
                                    background_normal="",
                                    background_color=(1, 1, 1),
                                    size_hint=(0.8, 1),
                                    pos_hint={"x": 0.1})
                    if i == 0:
                        button.bind(on_press=(lambda dt: self.ViewPrayer(0 + startingIndex)))
                    elif i == 1:
                        button.bind(on_press=(lambda dt: self.ViewPrayer(1 + startingIndex)))
                    elif i == 2:
                        button.bind(on_press=(lambda dt: self.ViewPrayer(2 + startingIndex)))
                    elif i == 3:
                        button.bind(on_press=(lambda dt: self.ViewPrayer(3 + startingIndex)))
                    elif i == 4:
                        button.bind(on_press=(lambda dt: self.ViewPrayer(4 + startingIndex)))
                    # Creates the styled buttons
                    # buttonText[0][...][0] selects title
                    self.prayerBox.add_widget(button)
                    # margin between buttons
                    self.prayerBox.add_widget(Label(size_hint_y=0.2))
                    # generate empty label same size as button
                except IndexError:
                    self.prayerBox.add_widget(Label(size_hint_y=1.2))
            # even bigger margin for the buttons to go
            self.prayerBox.add_widget(Label(size_hint_y=0.2))

    def ViewPrayer(self, index):
        global viewPrayersIndex
        viewPrayersIndex = index
        self.parent.current = "view"

    def LoadMore(self):
        self.prayerBox.clear_widgets()
        self.prayerIndex += 5
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        for i in range(len(localPrayers)):
            localPrayers[i] = localPrayers[i].split("~")
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))

    def Reset(self):
        localPrayers = []
        self.prayerIndex = 0
        self.prayerBox.clear_widgets()
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        for i in range(len(localPrayers)):
            localPrayers[i] = localPrayers[i].split("~")
        # add the buttons: lambda dt removes the callback
        Clock.schedule_once(lambda dt: self.AddButtons(localPrayers))


class CreatePage(Screen):
    title = StringProperty("")
    content = StringProperty("")

    def Submit(self, widget):
        # gets data
        self.title = self.ids.title.text
        self.content = self.ids.body.text
        # replaces \n with tag <newline>
        self.content = self.content.replace("\n", "<newline>")
        # finding "illegal" characters
        if "~" in self.title or "<newline>" in self.title:
            self.ids.titleError.text = "Error: You cannot use words/characters: \\ ~ <newline> in your title or content"
        elif "~" in self.content or "<newline>" in self.content:
            self.ids.titleError.text = "Error: You cannot use words/characters: \\ ~ <newline> in your title or content"
        elif self.title == "":
            self.ids.titleError.text = "Error: You must enter a title"
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
            # clears inputs
            self.ids.title.text = ""
            self.ids.body.text = ""
            self.ids.titleError.text = ""
            # redirects to the prayer list
            self.parent.current = "MyPrayers"


class ViewPage(Screen):

    def LoadItems(self):
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        for i in range(len(localPrayers)):
            localPrayers[i] = localPrayers[i].split("~")
        self.ids.prayerTitle.text = localPrayers[viewPrayersIndex][0]
        try:
            self.ids.prayerBody.text = localPrayers[viewPrayersIndex][1]
        except IndexError:
            self.ids.prayerBody.text = ""

    def Delete(self):
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        localPrayers.pop()
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        localPrayers.pop(viewPrayersIndex)
        with open("data/LocalPrayers.txt", "w") as file:
            file.write("\n".join(localPrayers))
        self.parent.current = "MyPrayers"



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
