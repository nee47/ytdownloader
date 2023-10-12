import os
import subprocess
import re
import yt_dlp

class EasyDownloader():

	def __init__(self):
			self.ytdlp = "yt-dlp --newline "
			self.opts = {'res': '', 'output_path': '', 'ffmpeg_path':'', 'ext':''}
			self.res = None
			self.target_path = None
			self.ffmpeg_path = ""
			self.ext = ""
			self.url = None

	def set_res(self, res):
		r = int(res[:-1]) if res != "2k" else 2048
		self.opts['res'] = f'res:{r}'
		#self.res = f'res:{r}'

	def set_output_path(self, path):
		#self.target_path = path
		self.opts['output_path'] = path

	def set_ffmpeg_path(self, path):
		#self.ffmpeg_path = enconderPath
		self.opts['ffmpeg_path'] = path

	def set_extension(self, ext):
		self.ext = ext

	def set_url(self, url):
		self.url = url
	
	def download(self, url, currentProgressF=None):
		
		if not url or not self.target_path:
			print("ERROR, NO LINK")
			return
		
		ffmpeg = r"\ffmpeg\bin"
		f = fr"{os.getcwd()}{ffmpeg}"
		self.setEnconderPath(f)	
		self.setExtension("mp4")

		class MyLogger:
			def debug(self, msg):
				# For compatibility with youtube-dl, both debug and info are passed into debug
				# You can distinguish them by the prefix '[debug] '
				if msg.startswith('[debug] '):
					pass
				else:
					#self.info(msg)
					pass


			def info(self, msg):
				print(msg)

			def warning(self, msg):
				print(msg)

			def error(self, msg):
				print(msg)

		def my_hook(d):
			if d['status'] == 'finished':
				print('Done downloading, now post-processing ...')
			elif d['status'] == 'downloading':
				if d.get('speed') and d.get("eta") and d.get('elapsed'):
					speed_Mbps = round(d['speed'] * 0.000001)
					speed = f"elapsed time: {round(d['elapsed'])}s    estimated time: {round(d['eta'])}s   speed: {speed_Mbps} Mb/s"
					currentProgressF(d['downloaded_bytes']/d['total_bytes'] * 100, speed)

		ydl_opts = {
			'logger': MyLogger(),
			'progress_hooks': [my_hook],
			'ffmpeg_location': self.ffmpeg_path,
			'format_sort': [self.res],
			'paths': {'home': self.target_path},
			'postprocessors': [{'key': 'FFmpegVideoRemuxer', 'preferedformat': self.ext}]
		}

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download(url)
		
	# Needs rework, using ytdlp module now
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