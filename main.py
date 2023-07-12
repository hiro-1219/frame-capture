import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master.title("frame-capture")
        self.master.bind("<KeyPress>", self.input_key)
        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.canvas.pack()
        self.time = tk.IntVar()
        slide = tk.Scale(
            self.master,
            variable=self.time,
            command=self.slider_scroll,
            orient=tk.HORIZONTAL,
            length=800,
            from_=0,
            to=399,
            resolution=1,
            tickinterval=50,
        )
        slide.pack()
        button_capture = tk.Button(self.master, text="capture", command=self.capture)
        button_capture.pack(side=tk.TOP)

        self.next_button = tk.Button(self.master, text=">", command=self.next_data)
        self.next_button.pack(side=tk.RIGHT)
        self.back_button = tk.Button(self.master, text="<", command=self.back_data)
        self.back_button.pack(side=tk.LEFT)
        
        self.text = tk.StringVar(self.master)
        self.text.set("")
        self.save_text_box = tk.Label(self.master, textvariable=self.text)
        self.save_text_box.pack(side=tk.RIGHT)

        self.data_path = os.listdir("./data/")
        self.data_path = [ os.path.join("./data", i) for i in self.data_path ]
        print(self.data_path)
        self.capture_base_path = "./capture/"
        self.now_video_counter = 0
        self.now_frame = get_all_frame(self.data_path[self.now_video_counter])
        self.draw_image = None
        self.get_now_image(0)

    def slider_scroll(self, event=None):
        now_frame_num = int(self.time.get())
        self.get_now_image(now_frame_num)
    
    def get_now_image(self, now_frame_num):
        image_rgb = cv2.cvtColor(self.now_frame[now_frame_num], cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.draw_image = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(320, 240, image=self.draw_image)

    def capture(self):
        self.save_capture()

    def save_capture(self):
        save_name = os.path.basename(self.data_path[self.now_video_counter])
        save_name = os.path.splitext(save_name)[0] + ".jpg"
        save_frame(self.data_path[self.now_video_counter], int(self.time.get()), os.path.join(self.capture_base_path, save_name))
        self.text.set("saved to " + os.path.join(self.capture_base_path, save_name))

    def next_data(self):
        self.next_data_image()

    def next_data_image(self):
        self.text.set("")
        if not (self.now_video_counter + 1 >= len(self.data_path)):
            self.now_video_counter += 1
        self.now_frame = get_all_frame(self.data_path[self.now_video_counter])
        self.get_now_image(0)

    def back_data(self):
        self.back_data_image()

    def back_data_image(self):
        self.text.set("")
        if not (self.now_video_counter - 1 < 0):
            self.now_video_counter -= 1
        self.now_frame = get_all_frame(self.data_path[self.now_video_counter])
        self.get_now_image(0)
    
    def input_key(self, event):
        key_name = event.keysym
        if key_name == "Right":
            if self.time.get() + 1 <= 399:
                self.time.set(int(self.time.get()) + 1)
        if key_name == "Up":
            if self.time.get() + 10 <= 399:
                self.time.set(int(self.time.get()) + 10)
        if key_name == "Left":
            if self.time.get() - 1>= 0:
                self.time.set(int(self.time.get()) - 1)
        if key_name == "Down":
            if self.time.get() - 10>= 0:
                self.time.set(int(self.time.get()) - 10)
        if key_name == "s":
            self.save_capture()
        if key_name == "a":
            self.back_data_image()
        if key_name == "d":
            self.next_data_image()
        now_frame_num = int(self.time.get())
        self.get_now_image(now_frame_num)


def save_frame(video_path, frame_num, result_path):
    cap = cv2.VideoCapture(video_path)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(result_path, frame)


def get_frame_num(video_path):
    cap = cv2.VideoCapture(video_path)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def get_all_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    digit = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    all_frame = []
    for _ in range(digit):
        ret, frame = cap.read()
        if ret:
            all_frame.append(frame)
    return all_frame


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()