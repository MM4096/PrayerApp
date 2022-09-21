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


# screens
class WindowManager(ScreenManager):
    pass


class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)


class MyPrayers(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def LoadItems(self):
        localPrayers = []
        with open("data/LocalPrayers.txt", "r") as data:
            localPrayers.append(data.readline())
            while not localPrayers[len(localPrayers) - 1] == "":
                localPrayers.append(data.readline())
        # removes \n or \r\n from the end of each line
        localPrayers = [x.rstrip() for x in localPrayers]
        localPrayers.pop()
        # separation of title with content
        for i in range(len(localPrayers)):
            localPrayers[i] = localPrayers[i].split("~")
            button = Button(text=localPrayers[i][0],
                            size_hint=(1, None),
                            height=dp(100),
                            color=(0, 0, 0),
                            background_normal="",
                            background_color=(1, 1, 1),
                            pos_hint={"x": 0.1})
            button.bind(on_release=(lambda dt, i=i: self.ViewPrayer(i)))
            self.ids.prayerBox.add_widget(button)
            self.ids.prayerBox.add_widget(Label(size_hint_y=None, height=dp(20)))

    def ViewPrayer(self, index):
        global viewPrayersIndex
        viewPrayersIndex = index
        print(viewPrayersIndex)
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
