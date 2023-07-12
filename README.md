# Framce-Capture
動画から画像をキャプチャするアプリケーション

## Requirements
python package
- opencv-python
- opencv-contrib-python

(Ubuntu22.04 apt package)
- libgl1-mesa-dev libglib2.0-0
- python3 python3-pip python3-tk python3-pil.imagetk

## Usage
```
$ python3 main.oy
```

## keybinding
- カーソルキー
    - 右 : フレームを1進める
    - 左 : フレームを1戻す
    - 上 : フレームを10進める
    - 下 : フレームを10戻す
- a : 前の動画に戻す
- d : 次の動画に進む
- s : キャプチャを保存する