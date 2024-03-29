import os
import subprocess
import re
import yt_dlp

class EasyDownloader():

	def __init__(self):
			self.opts = {'res': '', 'output_path': '', 'ffmpeg_path':'', 'ext':''}
			self.url = None

	def set_res(self, res):
		r = int(res[:-1]) if res != "2k" else 2048
		self.opts['res'] = f'res:{r}'

	def set_output_path(self, path):
		self.opts['output_path'] = path

	def set_ffmpeg_path(self, path):
		self.opts['ffmpeg_path'] = path

	def set_extension(self, ext):
		self.ext = ext

	def set_url(self, url):
		self.url = url
	
	def download(self, url, progress, currentProgressF=None, only_audio=False):
		if not url:
			print("ERROR, NO LINK")
			return
		
		ffmpeg = r"\ffmpeg\bin"
		f = fr"{os.getcwd()}{ffmpeg}"
		self.opts['ffmpeg_path'] = f
		self.opts['ext'] = "mp4"

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

				di = {'elapsed': round(d['elapsed'], 1)}

				if d.get('eta'):
					#text += f"{round(d['eta'])}s"
					di['eta'] = round(d['eta'])

				if d.get('speed'):
					speed_Mbps = round(d['speed'] * 0.000001)
					di['speed'] = speed_Mbps

				if d.get('total_bytes'):
						prog = d['downloaded_bytes']/d['total_bytes'] * 100
						di['current_progress'] = prog 
						progress(prog) 

				currentProgressF(di)

		ydl_opts = {
			'logger': MyLogger(),
			'progress_hooks': [my_hook],
			'ffmpeg_location': self.opts.get('ffmpeg_path'),
			'format_sort': [self.opts.get('res')],
			'paths': {'home': self.opts['output_path']},
			'postprocessors': [{'key': 'FFmpegVideoRemuxer', 'preferedformat': self.opts['ext']}]
		}

		ydl_audio_opts = {
			'logger': MyLogger(),
			'progress_hooks': [my_hook],
			'ffmpeg_location': self.opts.get('ffmpeg_path'),
			'final_ext': 'mp3',
			'format': 'bestaudio/best',
			'paths': {'home': self.opts['output_path']},
			'postprocessors': [{'key': 'FFmpegExtractAudio',
                     'nopostoverwrites': False,
                     'preferredcodec': 'mp3',
                     'preferredquality': '5'}]
		}

		chosen_opts = ydl_audio_opts if only_audio else ydl_opts

		with yt_dlp.YoutubeDL(chosen_opts) as ydl:
			ydl.download(url)
		
	# Needs rework, using ytdlp module now
	def update_ytdlp(self):
		# lines = []
		# command = self.ytdlp+" -U"
		# process = subprocess.Popen(command, 
		# 		stdout=subprocess.PIPE, 
		# 		stderr=subprocess.STDOUT,
		# 		text=True)
		# while process.poll() is None:
		# 	line = process.stdout.readline()
		# 	if line != '' :
		# 		lines.append(line)
		
		# return lines
		pass