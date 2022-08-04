from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


# Python naming conventions: Capital in front of every word
# Creates window manager
class WindowManager(ScreenManager):
    pass

# screens
class MainPage(Screen):
    pass


class SecondPage(Screen):
    pass


# loads kv file
kv = Builder.load_file('main.kv')


# app class
class PrayerApp(App):
    def build(self):
        return kv


# run app
if __name__ == '__main__':
    PrayerApp().run()
