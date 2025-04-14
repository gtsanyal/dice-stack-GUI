from host import PluginInterface

class ExamplePlugin(PluginInterface):
    def process(self, count: int) -> int:
        return count - 1
