# This Python file uses the following encoding: utf-8
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
        self.downloader.setTargetPath(path)
     
    signalDownload = Signal(bool)
    signalCurrentProgress = Signal(int)
    def _downloadLogic(self, resolution, url, currentProgressF):
        self.downloader.setRes(resolution)
        self.downloader.download(url, currentProgressF)
        self.signalDownload.emit(True)

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

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    thebackend = DownloaderBackend()
    engine.rootContext().setContextProperty("backend", thebackend)
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
