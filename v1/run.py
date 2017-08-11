import os
import threading

def run():
	os.chdir('C:\\Users\\Ibrahim Algadi\\Desktop\\I3M\\i3m PROJECTS\\Pharmacy\\v1\\Pharmacy')
	os.system('python main.py')


thread = threading.Thread(target=run, args=())
thread.run()

