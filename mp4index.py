import os
import shutil
import glob
from datetime import datetime
import json
import ffmpeg
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(prog="mp4index", description="mp4 list")
parser.add_argument("-i",  required=True, help="input folder")
parser.add_argument("-o", default="", help="output folder")
parser.add_argument("--ffmpeg", default="", help="ffmpeg bin directory")
parser.add_argument("--force", action='store_true', help="force rebuild")
args = parser.parse_args()

input_folder = args.i
output_folder = args.o
ffmpeg_path = args.ffmpeg
force_rebuild = args.force

output_default = 'index'
output_html = 'index.html'
prefix_str = r"const videoData = "
cover_time = 30
cover_width = 360
preview_width = 144

if not output_folder:
    output_folder = os.path.join(input_folder, output_default)

os.makedirs(output_folder, exist_ok=True)
if ffmpeg_path:
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']

jsonfile = os.path.join(output_folder, "video-data.js")

def get_media_created_date(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path))
    # try:
    #     probe = ffmpeg.probe(file_path)
    #     format_info = probe['format']
    #     creation_time = format_info.get('tags', {}).get('creation_time')
    #     return datetime.fromisoformat(creation_time)
    # except Exception as e:
    #     return datetime.fromtimestamp(os.path.getctime(file_path))

def get_media_info(file_path):
    try:
        default_title =  os.path.basename(os.path.splitext(file_path)[0])
        probe = ffmpeg.probe(file_path)
        format_info = probe['format']
        duration = float(format_info['duration'])
        title = format_info.get('tags', {}).get('title')
        return { 'title': title if title else default_title, 'duration': duration }
    except Exception as e:
        return { 'title': default_title, 'duration': 0 }


file_paths = glob.glob(os.path.join(input_folder, '*.mp4'))
sorted_files = sorted(file_paths, key=get_media_created_date, reverse=True)

jsdata = []

if os.path.exists(jsonfile) and not force_rebuild:
    with open(jsonfile, 'r') as file:
        rawdata = file.read()
    rawdata = rawdata.removeprefix(prefix_str)
    jsdata = json.loads(rawdata)

out_jsdata = []

for file_path in tqdm(sorted_files):

    exist_data = next((d for d in jsdata if d['filename'] == file_path), None)
    if exist_data is not None:
        out_jsdata.append(exist_data)
        continue

    fname = os.path.basename(os.path.splitext(file_path)[0])
    preview_folder = os.path.join(output_folder, fname)
    os.makedirs(preview_folder, exist_ok=True)
    thumbfile = os.path.join(output_folder, fname + ".png")
    ffmpeg.input(file_path, ss=cover_time).filter('scale', cover_width, -1).output(thumbfile, vframes=1).run(quiet=True, overwrite_output=True)
    info = get_media_info(file_path)
    title = info['title']
    duration = info['duration']
    count = 50
    slice = duration / count
    pimages = {}
    for i in range(count):
        iname = os.path.join(preview_folder, f'{i}.jpg')
        itime = round(i * slice)
        ffmpeg.input(file_path, ss = itime).filter('scale', preview_width, -1).output(iname, vframes=1).run(quiet=True, overwrite_output=True)
        pimages[f'{itime}'] = iname
    out_jsdata.append({ "title": title, "filename": file_path, "coverImage": thumbfile, "previewVideo": file_path, "previewImages": pimages })


with open(os.path.join(output_folder, "video-data.js"), 'w') as file:
    file.write(prefix_str + json.dumps(out_jsdata))

target_html = os.path.join(output_folder, output_html)

if not os.path.exists(target_html) or force_rebuild:
    shutil.copyfile(output_html, target_html)

print(f"{target_html} Done!")
