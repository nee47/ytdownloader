import sys, re, json
import threading
from pathlib import Path
from download_url import EasyDownloader
import time
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import *


class DownloaderBackend(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.downloader = EasyDownloader()
        self._progress = 0
        self._running = False
        self.user_config = {}
        print(self.getConfig())    
    signalGetPath = Signal(bool)

    @Slot(str)
    def setOutputPath(self, targetPath):
        self.signalGetPath.emit(True)
        path = targetPath[8:]
        self.downloader.set_output_path(path)

    signalDownloadFinished = Signal(bool)
    signalCurrentProgress = Signal(dict)
    signalCurrentProgressAudio = Signal(dict)
    # def _downloadLogic2(self, resolution, url, currentProgressF):
    #     self.downloader.set_res(resolution)
    #     self.downloader.download(url, currentProgressF)
    #     self.signalDownloadFinished.emit(True)

    def _downloadLogic(self, url, currentProgressF, only_audio=False, resolution=None):
        if resolution:
            self.downloader.set_res(resolution)
        
        def f(i):
            self.progress = i

        self.downloader.download(url, f, currentProgressF, only_audio)
        self.progress = 0
        self.running = False

    def validate_url(self, url):
        result = re.search(r"youtu.?be(.com)?/\w+", url)
        return bool(result)

    def _get_progress(self):
        return self._progress

    def _set_progress(self, current_progress):
        self._progress = current_progress
        self.on_progress.emit()

    def _get_running(self):
        return self._running

    def _set_running(self, run):
        self._running = run
        self.on_running.emit()

    def getConfig(self):
        config_file = "config.json"

        with open(config_file, 'r') as file:
            config_data = json.load(file)
            return config_data
            


    signalErrorOcurred = Signal(str)
    @Slot(str, bool, dict)
    def download(self, url, only_audio, opts):
        if(self.validate_url(url)):    
            if not self._running:
                self.running = True
            task = None
            if only_audio:
                task = threading.Thread(target=self._downloadLogic, args=(url, self.signalCurrentProgressAudio.emit, True))      
            else:
                task = threading.Thread(target=self._downloadLogic, args=(url, self.signalCurrentProgress.emit, only_audio, opts.get('res'))) 
            task.start()
        else:
            self.signalErrorOcurred.emit("invalid youtube link ")
    

    @Slot()
    def update(self):    
        d = threading.Thread(target=self.downloader.update_ytdlp)
        d.start()

    on_progress = Signal()
    on_running = Signal()
    progress = Property(float, _get_progress, _set_progress, notify=on_progress)
    running = Property(bool, _get_running, _set_running, notify=on_running)


class LanguageManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        
        self.choosen_lang = "en"
        
        with open('language.json', 'r') as archivo:
            self.datos = json.load(archivo)

        self.current_raw_lang = self.datos[self.choosen_lang]
        #self.deault_language = self.datos[self.choosen_lang]
        print(self.current_raw_lang)

    def _get_lang(self):
        return self.current_raw_lang
    
    def _set_lang(self, lang):
        self.current_raw_lang = self.datos[lang]
        self.on_language_change.emit()

    @Slot(str)
    def update_language(self, lang):    
        self.current_lang = lang

    on_language_change = Signal()
    current_lang = Property(dict, _get_lang, _set_lang, notify=on_language_change)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    thebackend = DownloaderBackend()
    language_manager= LanguageManager()
    engine.rootContext().setContextProperty("backend", thebackend)
    engine.rootContext().setContextProperty("language_mana", language_manager)
    qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
