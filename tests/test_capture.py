import unittest
from utils.capture import CaptureVideo, CaptureVideoLoader
import numpy as np

class TestCapture(unittest.TestCase):
    def setUp(self) -> None:
        super(TestCapture, self).__init__()
        self.video_base_path = "./data/"
        self.save_base_path = "./capture/"

    def test_load_capture(self):
        loader = CaptureVideoLoader(self.video_base_path, self.save_base_path)
        video_path = loader.get_video_path_list()
        print(video_path)
        cap = loader.load_capture_video(video_path[0])
        pos_frame = cap.get_pos_frame(0)
        cap.save_capture(0, "jpg")
        self.assertEqual(type(pos_frame), np.ndarray)
        self.assertEqual(cap.get_frame_size(), 400)
        