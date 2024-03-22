# bmp2video
watch filesystem changes, write into ffmpeg, delete source immediately.

观察文件系统改动，把文件写入FFmpeg，然后立即删除源文件。

这个脚本试图为不支持FFmpeg的剪辑软件提供FFmpeg导出。

# 使用
确保系统上安装了FFmpeg

安装依赖项：
```
pip install watchdog
```

运行：
```
python bmp2video.py
```

导出bmp序列到脚本所在的文件夹。

在导出视频之后，导出aac音频到脚本所在的文件夹。脚本会合并输出。

文件路径中最好不要有中文，否则会产生一些错误，一部分图片会被忽略。

ffmpeg不能立即处理整个视频。请在任务管理器中将你的剪辑软件进程优先级设置为低，以免过快的产生图像。

任务管理器->详细信息->选中进程->右键->设置优先级->低