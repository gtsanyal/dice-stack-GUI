import importlib
import os
from pynput import keyboard
import time


class PluginInterface:
    def process(self, input: int) -> int:
        return input


class HostController:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = [] # Array where plugins are stored
        self.load_plugins()

        self.proceed = True
        self.mode_selector = 0

        self.processor = PluginInterface() #holds current implementation of fundction which provides data to print

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=True)             #HIS COMMMENT suppress - eat up keys
        self.listener.start()

    def load_plugins(self): #Change. Dont search for plug ins. Instead we should assime that list of plugins is already defined
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                print(f"Registering plugin: {module_name}")
                self.plugins.append(self.plugin_dir + '.' + module_name)

    def start(self):
        count = 0
        while self.proceed:
            count = self.processor.process(count)
            print(f"{count}", end=" ", flush=True)
            time.sleep(0.35)

    def on_press(self, key: (keyboard.Key |
                             keyboard.KeyCode |
                             None), injected):
        # An example of processing pressing
        # try:
        #     print('\nAlphanumeric key {} pressed; it was {}'.format(
        #         key.char, 'faked' if injected else 'not faked'))
        # except AttributeError: # for special keys (without key.char)
        #     print('special key {} pressed'.format(key))
        pass

    def on_release(self, key: (keyboard.Key |
                               keyboard.KeyCode |
                               None), injected):
        if key == keyboard.Key.esc:
            print("\nCONTROL: Exit")
            self.proceed = False
            return False
        try:
            if key.char == "w":
                self.on_activate_w()
            elif key.char == "s":
                self.on_activate_s()
        except AttributeError:
            pass

    def on_activate_w(self):
        # Next plugin
        print('\nCONTROL: w is activated')
        if self.mode_selector < len(self.plugins) - 1:
            self.mode_selector += 1
            self.processor = \
                importlib.import_module(self.plugins[self.mode_selector], ".") \
                         .ExamplePlugin() 

    def on_activate_s(self):
        # Previous plugin
        print('\nCONTROL: s is activated')
        if self.mode_selector > 0:
            self.mode_selector -= 1
            self.processor = \
                importlib.import_module(self.plugins[self.mode_selector], ".") \
                         .ExamplePlugin()


if __name__ == "__main__":
    host = HostController()
    host.start()
