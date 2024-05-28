import subprocess
import os

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.video_file_name = 'videoonly.mp4'
        self.file_name = 'output.mp4'
        self.ffmpeg_process = None
        self.frame_rate = 60
        
    def on_modified(self, event):
        if event.is_directory:
            return
        src_path = event.src_path
        if(src_path.endswith("0000.bmp") and self.ffmpeg_process == None):
            ffmpeg_command = [
                'ffmpeg',
                '-y',
                '-loglevel','quiet',
                '-r', str(self.frame_rate),
                "-colorspace","bt709",
                '-i', 'pipe:0',
                '-preset', 'fast',
                '-crf', '21',
                # '-c:v', 'h264_nvenc',
                '-pix_fmt', 'yuv420p',
                
                self.video_file_name
            ]
            self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
        if(src_path.endswith(".aac")):
            if(self.ffmpeg_process!= None):
                self.ffmpeg_process.stdin.close()
                self.ffmpeg_process.wait()

            ffmpeg_command = [
                'ffmpeg',
                '-y',
                '-i', self.video_file_name,
                '-i', event.src_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                
                self.file_name
            ]
            print("merging...")
            subprocess.Popen(ffmpeg_command)

        try:
            if src_path.endswith(".bmp"):
                with open(event.src_path, 'rb') as video_file:
                    self.ffmpeg_process.stdin.write(video_file.read())
                    print(f"read: {event.src_path}")
                os.remove(event.src_path)
        except:
            return
def main():

    folder_to_watch = "./"  # Change this to the directory you want to watch
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()
    try:
        print(f"Watching directory: {folder_to_watch}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if(event_handler.ffmpeg_process!=None):
            event_handler.ffmpeg_process.stdin.close()
    observer.join()

main()