import sys, re
import threading
from pathlib import Path
from download_url import EasyDownloader

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import *


class DownloaderBackend(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.downloader = EasyDownloader()
        
    signalGetPath = Signal(bool)

    @Slot(str)
    def getFolderPath(self, targetPath):
        self.signalGetPath.emit(True)
        path = targetPath[8:]
        self.downloader.set_output_path(path)
     
    signalDownloadFinished = Signal(bool)
    signalCurrentProgress = Signal(int, str)
    def _downloadLogic(self, resolution, url, currentProgressF):
        self.downloader.set_res(resolution)
        self.downloader.download(url, currentProgressF)
        self.signalDownloadFinished.emit(True)

    def validate_url(self, url):
        result = re.search(r"youtu.?be(.com)?/\w+", url)
        return True if result else False


    signalErrorOcurred = Signal(str)
    @Slot(str, str)
    def download(self, resolution, url):
        if(self.validate_url(url)):    
            d = threading.Thread(target=self._downloadLogic, args=(resolution, url, self.signalCurrentProgress.emit))
            d.start()
        else:
            self.signalErrorOcurred.emit("invalid youtube link ")
    
    @Slot()
    def update(self):    
        d = threading.Thread(target=self.downloader.update_ytdlp)
        d.start()
        

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
