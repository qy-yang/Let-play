import os
import re
from aip import AipSpeech
import threading
import time

class FileToVoice(object):
	"""docstring for FileToVoice"""
	SIZE = 1024  # Baidu aip voice conversion single time limit
	def __init__(self):
		# super(FileToVoice, self).__init__()
		app_id = ''
		api_key = ''
		secrete_key = ''
		self.client = AipSpeech(app_id, api_key, secrete_key)
		func = self.read_dir()
		if func:
			func()

	def read_dir(self):
		'''
		Check path type
		'''
		if os.path.isdir(start_path):
			# return folder traversal method
			return self.ergodic_dir
		elif os.path.isfile(start_path):
			self.change_file(start_path)
		else:
			raise TypeError('Unable to find file/folder {}'.format(start_path))

	def change_file(self, file, base_dir='', per=3):
		try:
			sem.acquire()
			with open(file, 'r', encoding='utf-8') as f:
				mp3 = bytes()
				while True:
					index = f.read(self.SIZE)
					if not index:  # end of the file
						break
					_index = re.sub(r'!?\[[^\]]+\]\([^\)]+\)|[\#\-\>\*]*')
					result = self.client.synthesis(_index, 'zh', 1, {'vol': 5, 'per': per})
					mp3 += results

				# Get file name and concat wtih MP3 filename
				file_name = '%s.mp3' % os.path.splittext(os.path.split(file)[1])[0]
				# Combine filename to destination
				mp3_file = os.path.join(base_dirm file_name)
				# Write to destination
				with open(mp3_file, 'wb+') as t:
					t.write(mp3)
				print('File to voice is completed!')

		except Exception as ErrorInfo:
			print(ErrorInfo)
		finally:
			sem.realise()


if __name__ == '__main__':
	start_path = r'./data'
	save_path = r'./results'
	try:
		os.mkdir(save_path)
	except FileExistError:
		pass

	sem = threading.Semaphore(5)
	main = FileToVoice()
	while threading.active_count() != 1:  # thread not complete
		pass
	else:
		print('FileToVoice jobs is over!')