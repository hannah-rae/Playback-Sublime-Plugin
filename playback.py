import sublime, sublime_plugin
import time
import threading

class Buffers(object):
	def __init__(self):
		self.buffers = []

	def __add__(self, text):
		temp_time = time.time()
		self.buffers.append((text, temp_time - self.prev_time))
		self.prev_time = temp_time

	def empty_buffer(self):
		self.buffers = []
		assert len(self.buffers) == 0

	def setTime(self):
		self.prev_time = time.time()

class Recorder(object):
	def __init__(self):
		self.record = False

	def startRecording(self):
		print "started Recording"
		self.record = True

	def stopRecording(self):
		print "stopped "
		self.record = False

	def getRecording(self):
		return self.record

buffers = Buffers()
recording = Recorder()

class StartRecordingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		buffers.setTime()
		recording.startRecording()

class StopRecordingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		recording.stopRecording()

class PlayInNewWindowCommand(sublime_plugin.TextCommand):
	def play_it_back(self):
		for text, _time in buffers.buffers:
			time.sleep(_time)
			def display_text():
				screen = sublime.Region(0, self.new_view.size())
				self.new_view.replace(self.edit, screen, text)
			sublime.set_timeout(display_text, 0)	
		buffers.empty_buffer()

	def run(self, edit):
		recording.stopRecording()
		window = self.view.window()
		self.new_view = window.new_file()
		self.new_view.set_name("Playback")
		self.edit = edit
		t = threading.Thread(target=self.play_it_back)
		t.start()

class MyEventListener(sublime_plugin.EventListener):
	def on_modified(self, view):
		if recording.getRecording():
			buffers + view.substr(sublime.Region(0, view.size()))
			
