import sys, re
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
        
    signalGetPath = Signal(bool)

    @Slot(str)
    def getFolderPath(self, targetPath):
        self.signalGetPath.emit(True)
        path = targetPath[8:]
        self.downloader.set_output_path(path)
     
    signalDownloadFinished = Signal(bool)
    signalCurrentProgress = Signal(int, str)
    def _downloadLogic2(self, resolution, url, currentProgressF):
        self.downloader.set_res(resolution)
        self.downloader.download(url, currentProgressF)
        self.signalDownloadFinished.emit(True)

    def _downloadLogic(self, resolution, url, currentProgressF):
        self.downloader.set_res(resolution)
        for i in range(100):
            self.progress = i
            time.sleep(0.04)
        self.running = False
        #self.downloader.download(url, currentProgressF)
        #self.signalDownloadFinished.emit(True)
        

    def validate_url(self, url):
        result = re.search(r"youtu.?be(.com)?/\w+", url)
        return True if result else False

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

    signalErrorOcurred = Signal(str)
    @Slot(str, str)
    def download(self, resolution, url):
        if(self.validate_url(url)):    
            if not self._running:
                self.running = True
            
            d = threading.Thread(target=self._downloadLogic, args=(resolution, url, self.signalCurrentProgress.emit))
            d.start()
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

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    thebackend = DownloaderBackend()
    engine.rootContext().setContextProperty("backend", thebackend)
    qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
