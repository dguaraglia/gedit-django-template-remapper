import gedit
import gtksourceview2

class TabWatch:
    """ Monitor the tabs in gedit to find out when new tabs get opened """

    def __init__(self, window):
        self.geditwindow = window
        self.geditwindow.connect("tab_added", self.__tab_added)
        self.language_manager = gtksourceview2.LanguageManager()
        

    def __tab_added(self, window, tab):
        """ This event handler gets called every time a new tab is added """
        document = tab.get_document()

        # attach handlers for events that might change the filetype
        document.connect("saved", self.__document_updated)
        if document.is_untitled:
            document.connect("loaded", self.__document_updated)

    def __document_updated(self, document, *args):
        language = document.get_language()
        if language and (language.get_id() == 'html'):
            document.set_language(self.language_manager.get_language('tpl'))

class RemapDjangoTemplatesPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._watchers = {}

    def activate(self, window):
        # add a tab watcher for this window
        self._watchers[window] = TabWatch(window)

    def deactivate(self, window):
        del self._watchers[window]

    def update_ui(self, window):
        pass
