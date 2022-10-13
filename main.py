# This Python file uses the following encoding: utf-8
import sys
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

    signalGetUrlPath = Signal(bool)

    @Slot(str)
    def getUrl(self, urlPath):
        self.signalGetUrlPath.emit(True)
        self.downloader.setUrl(urlPath)
        
    signalDownload = Signal(bool)
    def _downloadLogic(self, index):
        self.downloader.setRes(index)
        self.downloader.download()
        self.signalDownload.emit(True)

    @Slot(str)
    def download(self, index):
        d = threading.Thread(target=self._downloadLogic, args=(index,))
        d.start()
        
        

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
