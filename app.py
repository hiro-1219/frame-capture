import re
import tkinter as tk

import cv2
from PIL import Image, ImageTk

from utils.capture import CaptureVideoLoader


class Application(tk.Frame):
    def __init__(self, config, master = None):
        super().__init__(master)
        self.config = config
        self.master.title(config["title"])
        self.master.bind("<KeyPress>", self.__input_key)
        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.time = tk.IntVar()
        slide = tk.Scale(
            self.master,
            variable=self.time,
            command=self.__scroll_capture,
            orient=tk.HORIZONTAL,
            length=800,
            from_=0,
            to=399,
            resolution=1,
            tickinterval=50,
        )
        button_capture = tk.Button(self.master, text="capture", command=self.__save_video_capture)
        button_next = tk.Button(self.master, text="next", command=self.__next_video_capture)
        button_back = tk.Button(self.master, text="back", command=self.__back_video_capture)
        self.text = tk.StringVar(self.master)
        self.text.set("")
        save_text_box = tk.Label(self.master, textvariable=self.text)

        self.canvas.pack()
        slide.pack()
        button_capture.pack(side=tk.TOP)
        button_next.pack(side=tk.RIGHT)
        button_back.pack(side=tk.LEFT)
        save_text_box.pack(side=tk.RIGHT)
        self.draw_iamge = None

        self.__initialize(config)
    
    def __get_now_video_captures(self, now_video_counter: int):
        path = self.video_path_list[now_video_counter]
        video_name = re.search(r'\/([^\/]+)$', path).group(1)

        self.text.set(video_name)
        return self.loader.load_capture_video(path)
    
    def __close_now_video_frames(self):
        self.now_video_capture.close_all_frame()
    
    def __back_video_capture(self):
        self.text.set("")
        self.__close_now_video_frames()
        if not (self.now_video_counter - 1 < 0):
            self.now_video_counter -= 1
        self.now_video_capture = self.__get_now_video_captures(self.now_video_counter)
        frame = self.now_video_capture.get_pos_frame(int(self.time.get()))
        self.__show_now_capture(frame)

    def __next_video_capture(self):
        self.text.set("")
        self.__close_now_video_frames()
        if not (self.now_video_counter + 1 >= len(self.video_path_list)):
            self.now_video_counter += 1
        self.now_video_capture = self.__get_now_video_captures(self.now_video_counter)
        frame = self.now_video_capture.get_pos_frame(int(self.time.get()))
        self.__show_now_capture(frame)
    
    def __save_video_capture(self):
        save_path = self.now_video_capture.save_capture(int(self.time.get()), self.config["ext"])
        self.text.set("save to {}".format(save_path))

    def __scroll_capture(self, event=None):
        frame = self.now_video_capture.get_pos_frame(int(self.time.get()))
        self.__show_now_capture(frame)

    def __show_now_capture(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.draw_image = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(320, 240, image=self.draw_image)

    def __input_key(self, event):
        key_name = event.keysym
        if key_name == "Right":
            if self.time.get() + 1 <= 399:
                self.time.set(int(self.time.get()) + 1)
        if key_name == "Up":
            if self.time.get() + 10 <= 399:
                self.time.set(int(self.time.get()) + 10)
        if key_name == "Left":
            if self.time.get() - 1 >= 0:
                self.time.set(int(self.time.get()) - 1)
        if key_name == "Down":
            if self.time.get() - 10 >= 0:
                self.time.set(int(self.time.get()) - 10)
        if key_name == "s":
            self.__save_video_capture()
        if key_name == "a":
            self.__back_video_capture()
        if key_name == "d":
            self.__next_video_capture()
        frame = self.now_video_capture.get_pos_frame(int(self.time.get()))
        self.__show_now_capture(frame)
    
    def __initialize(self, config):
        self.now_video_counter = 0
        self.loader = CaptureVideoLoader(config["data_base_path"], config["save_base_path"], config["video_type"])
        self.video_path_list = self.loader.get_video_path_list()
        self.now_video_capture = self.__get_now_video_captures(self.now_video_counter)
        frame = self.now_video_capture.get_pos_frame(0)
        self.__show_now_capture(frame)


if __name__ == "__main__":
    config = {
        "title": "frame-capture",
        "ext": "png",
        "data_base_path": "./data/",
        "save_base_path": "./capture/",
        "video_type": ["video/mp4", "video/x-msvideo"]
    }
    root = tk.Tk()
    app = Application(config, master=root)
    app.mainloop()