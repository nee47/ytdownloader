from tkinter.filedialog import*
import tkinter
from tkinter import*
import os

class EasyDownloader():

	def __init__(self):
			self.ytdlp = "yt-dlp"
			self.res = None
			self.target_path = None
			self.ffmpeg_path = ""
			self.ext = ""
			self.url = None

	def setRes(self, res):
		if res== "720p":
			self.res = '-S "res:'+"720"+'"'
		if res== "1080p":
			self.res = '-S "res:'+"1080"+'"'
		if res== "2k":
			self.res = '-S "res:'+"1440"+'"'

	def setTargetPath(self, path):
		self.target_path = "-P "+ path

	def setEnconderPath(self, path):
		self.ffmpeg_path = "--ffmpeg-location "+path

	def setExtension(self, ext):
		self.ext = "--remux-video "+ext

	def setUrl(self, url):
		self.url = url

	def download(self):

		if not self.url or not self.target_path:
			print("ERROR, NO LINK")
			return
		
		ffmpeg = r"\ffmpeg\bin"
		f = f'"{os.getcwd()}{ffmpeg}"'
		print(f)
		self.setEnconderPath(f)	
		self.setExtension("mp4")

		container = [self.ytdlp, self.res, self.target_path, self.ffmpeg_path, self.ext, self.url]
		command = ' '.join(container)
		tmp = "tmp.cmd"
		
		with open(tmp, "w") as f:
			f.write(command)
		
		os.system(tmp)
		os.remove(tmp)

if __name__ == '__main__':

	tkinter.Tk().withdraw()
	url = tkinter.simpledialog.askstring(title="downloader", prompt="--------enter your url pls-------")
	d = EasyDownloader()
	d.download(url)
