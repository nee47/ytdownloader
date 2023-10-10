import os
import subprocess
import re

class EasyDownloader():

	def __init__(self):
			self.ytdlp = "yt-dlp --newline "
			self.res = None
			self.target_path = None
			self.ffmpeg_path = ""
			self.ext = ""
			self.url = None

	def setRes(self, res):
		r = int(res[:-1]) if res != "2k" else 2048
		self. res = f'-S "res:{r}"' 

	def setTargetPath(self, path):
		self.target_path = f"-P {path}"

	def setEnconderPath(self, enconderPath):
		self.ffmpeg_path = f"--ffmpeg-location {enconderPath}"

	def setExtension(self, ext):
		self.ext = f"--remux-video {ext}"

	def setUrl(self, url):
		self.url = url

	def download(self, url, currentProgressF):

		if not url or not self.target_path:
			print("ERROR, NO LINK")
			return
		
		ffmpeg = r"\ffmpeg\bin"
		f = f'"{os.getcwd()}{ffmpeg}"'
		print(f)
		self.setEnconderPath(f)	
		self.setExtension("mp4")

		container = [self.ytdlp, self.res, self.target_path, self.ffmpeg_path, self.ext, url]
		command = ' '.join(container)
		
		process = subprocess.Popen(command, 
						stdout=subprocess.PIPE, 
						stderr=subprocess.STDOUT,
						creationflags=subprocess.CREATE_NO_WINDOW,
						text=True)
		previous = 0
		while process.poll() is None:
			line = process.stdout.readline()
			print(line)
			x = re.search(r"\[download\]\s+(\d{1,3}.\d+%)", line)
			if x:
				current = x.groups()[0][:-1]
				current_numb = round(float(current))
				if(current_numb != previous):
					currentProgressF(current_numb)
					previous = current_numb

		process.stdout.close()
	
	def update_ytdlp(self):
		lines = []
		command = self.ytdlp+" -U"
		process = subprocess.Popen(command, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.STDOUT,
				text=True)
		while process.poll() is None:
			line = process.stdout.readline()
			if line != '' :
				lines.append(line)
		
		return lines