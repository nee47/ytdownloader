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
		r = int(res[:-1])
		self. res = f'-S "res:{r},codec:vp9"' 

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

