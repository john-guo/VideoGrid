# VideoGrid

**VideoGrid** 是一个轻量级、响应式的网页应用，能够动态生成视频列表，支持悬停预览、进度控制和弹窗视频播放。轻松浏览、预览和交互您的视频文件，呈现在简洁的网格界面中。

---

## 中文说明

### 项目简介

这个项目生成了一个简单的网页版视频列表，用户可以通过点击预览视频。页面包括鼠标悬停时的视频预览、进度条、以及声音控制功能，提升了用户的视频浏览体验。

### 文件结构

- **index.html**: 主要的HTML页面，包含了视频列表的结构和样式定义。
- **mp4index.py**: 用于生成包含视频数据的JavaScript文件 (video-data.js)，该文件被 `index.html` 引用来动态生成视频列表。

### 使用步骤

1. 确保你的项目目录下有 `index.html` 和 `mp4index.py` 文件。
2. 使用 Python 脚本生成视频数据文件：
   ```bash
   python3 mp4index.py -i <input_folder> -o <output_folder> --ffmpeg <ffmpeg_directory> --force

- -i: 必须指定输入文件夹，包含所有 .mp4 视频文件。
- -o: 输出文件夹，用于保存生成的封面和预览图片，默认为 input_folder/index。
- --ffmpeg: 指定 ffmpeg 可执行文件的路径（PATH查找路径包含的话可以不用这个选项，否则必须指定）。
- --force: 如果指定此选项，会强制重新生成视频数据。

3. 使用浏览器打开 index.html，即可查看视频列表页面。
  
### 功能

- **视频封面预览**: 鼠标悬停在视频上时会播放视频预览。
- **进度条控制**: 可以通过拖动进度条来调整视频播放进度。
- **视频播放弹窗**: 点击视频后，会弹出视频播放窗口进行播放。
- **静音开关**: 支持视频预览时的静音/取消静音功能。
  
## English Instructions

### Project Overview

VideoGrid is a lightweight, responsive web app that dynamically generates a video list where users can preview and play videos. It includes features such as hover-based video preview, progress bars, and sound control for an enhanced user experience.

### File Structure

- **index.html: The main HTML page that contains the structure and styles for the video list.
- **mp4index.py: A Python script that generates the video data file (video-data.js) used by index.html to dynamically display the video list.

### How to Use

1. Make sure you have the index.html and mp4index.py files in your project directory.
2. Use the Python script to generate the video data file:
   ```bash
   python3 mp4index.py -i <input_folder> -o <output_folder> --ffmpeg <ffmpeg_directory> --force

- -i: The input folder containing all .mp4 video files (required).
- -o: The output folder where the generated video covers and preview images will be stored. Defaults to input_folder/index.
- --ffmpeg: The path to the ffmpeg binary (optional if the ffmpeg has already been included in PATH).
- --force: Forces a rebuild of the video data if specified.

3. Open index.html in a web browser to view the video list.

### Features

- **Video Cover Preview**: Videos will preview when you hover over the video thumbnails.
- **Progress Bar Control**: Drag the progress bar to adjust the video playback time.
- **Popup Video Player**: Clicking a video opens a modal to play it.
- **Mute Toggle**: The video preview can be muted or unmuted with a toggle switch.
