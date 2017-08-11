import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy import Config
Config.set('graphics', 'multisamples', '0')

class PharmacyApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    PharmacyApp().run()