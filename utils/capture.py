from typing import List, Dict, Any
import magic
from tqdm import tqdm
import cv2
import os


class CaptureVideo:
    def __init__(self, video_path: str, save_base_path: str) -> None:
        super(CaptureVideo, self).__init__()
        self.video_path = video_path
        self.save_base_path = save_base_path
        self.cv2_cap = cv2.VideoCapture(video_path)
        self.all_frame = []
        
    def save_capture(self, save_frame_pos: int, save_ext: str) -> str:
        video_name = os.path.basename(self.video_path)
        video_name = os.path.splitext(video_name)[0] + "." + save_ext
        save_path = os.path.join(self.save_base_path, video_name)
        os.makedirs(self.save_base_path, exist_ok=True)
        self.cv2_cap.set(cv2.CAP_PROP_POS_FRAMES, save_frame_pos)
        ret, frame = self.cv2_cap.read()
        if ret:
            cv2.imwrite(save_path, frame)
        return save_path
    
    def get_pos_frame(self, frame_pos: int) -> List[Any]:
        return self.all_frame[frame_pos]

    def get_all_frame(self) -> None:
        frame_size = self.get_frame_size()
        cap = self.cv2_cap
        self.all_frame = []
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for _ in tqdm(range(frame_size)):
            ret, frame = cap.read()
            if ret:
                self.all_frame.append(frame)
        
    def get_frame_size(self) -> int:
        return int(self.cv2_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    def close_all_frame(self) -> None:
        self.all_frame = []


class CaptureVideoLoader:
    def __init__(self, video_base_path: str, save_base_path: str) -> None:
        super(CaptureVideoLoader, self).__init__()
        self.save_base_path = save_base_path
        self.video_path_list = self.__get_video_path_list(video_base_path)
        self.cap = self.__create_cap_list(self.video_path_list)

    def load_capture_video(self, video_path: str) -> CaptureVideo:
        capture_video = self.cap[video_path]
        capture_video.get_all_frame()
        return capture_video

    def get_video_path_list(self) -> List[str]:
        return self.video_path_list

    def __create_cap_list(self, video_path_list: List[str]) -> Dict[str, CaptureVideo]:
        cap_dict = dict()
        for path in video_path_list:
            cap_dict[path] = CaptureVideo(path, self.save_base_path)
        return cap_dict

    def __get_video_path_list(self, base_path: str) -> List[str]:
        f = magic.Magic(mime=True, uncompress=True)
        path_list = os.listdir(base_path)
        path_list = [ os.path.join(base_path, path) for path in path_list ]
        video_path_list = []
        for path in path_list:
            if f.from_file(path) in ["video/mp4", "video/x-msvideo"]:
                video_path_list.append(path)
        return video_path_list

