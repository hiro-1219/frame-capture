from typing import Dict, Any
from utils.capture import CaptureVideo, CaptureVideoLoader
import tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, config: Dict[Any], master = None):
        super().__init__(master)
        self.master.title(config["title"])
        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.time = tk.IntVar()
        slide = tk.Scale(
            self.master,
            variable=self.time,
            orient=tk.HORIZONTAL,
            length=800,
            from_=0,
            to=399,
            resolution=1,
            tickinterval=50,
        )
        button_capture = tk.Button(self.master, text="capture")
        button_next = tk.Button(self.master, text="next")
        button_back = tk.Button(self.master, text="back")

        self.now_video_counter = 0
        self.loader = CaptureVideoLoader(config["data_base_path"], config["save_base_path"])
        self.video_path_list = self.loader.get_video_path_list()
        self.now_video_capture = self.__get_now_video_capture(self.now_video_capture)
        
    
    def __get_now_video_capture(self, now_video_counter: int):
        return self.loader.load_capture_video(self.video_path_list[now_video_counter])




