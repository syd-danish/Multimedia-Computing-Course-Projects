import sys
import cv2
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QSlider, QLineEdit
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal Video Player")
        self.video_path = None
        self.cap = None
        self.timer = QTimer()
        self.frame_rate = 30
        self.playback_speed = 1.0
        self.paused = True
        self.current_frame = 0

        # UI Components
        self.label = QLabel()
        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.seek_input = QLineEdit()
        self.seek_btn = QPushButton("Seek")
        self.speed_slider = QSlider(Qt.Horizontal)

        self.init_ui()
        self.timer.timeout.connect(self.next_frame)

    def init_ui(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.label.setFixedSize(640, 480)
        vbox.addWidget(self.label)

        self.play_btn.clicked.connect(self.play_video)
        self.pause_btn.clicked.connect(self.pause_video)
        self.seek_btn.clicked.connect(self.seek_video)

        self.speed_slider.setMinimum(5)
        self.speed_slider.setMaximum(15)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickInterval(5)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(self.update_speed)

        hbox.addWidget(self.play_btn)
        hbox.addWidget(self.pause_btn)
        hbox.addWidget(QLabel("Seek (hh:mm:ss):"))
        hbox.addWidget(self.seek_input)
        hbox.addWidget(self.seek_btn)
        hbox.addWidget(QLabel("Speed:"))
        hbox.addWidget(self.speed_slider)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Load video on startup
        self.load_video()

    def load_video(self):
        file_dialog = QFileDialog()
        self.video_path, _ = file_dialog.getOpenFileName(self, "Open Video File", "", "MP4 Files (*.mp4)")
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
            self.timer.setInterval(int(1000 / self.frame_rate))

    def play_video(self):
        if self.cap:
            self.paused = False
            self.timer.start()

    def pause_video(self):
        self.paused = True
        self.timer.stop()

    def update_speed(self):
        value = self.speed_slider.value()
        self.playback_speed = value / 10.0
        self.timer.setInterval(int(1000 / (self.frame_rate * self.playback_speed)))

    def seek_video(self):
        timestamp = self.seek_input.text()
        try:
            h, m, s = map(int, timestamp.split(":"))
            frame_number = int((h * 3600 + m * 60 + s) * self.frame_rate)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        except Exception as e:
            print("Invalid timestamp format. Use hh:mm:ss")

    def next_frame(self):
        if not self.cap or self.paused:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            return

        self.current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        timestamp = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        time_str = time.strftime('%H:%M:%S', time.gmtime(timestamp))

        # Overlay timestamp
        cv2.putText(frame, time_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(rgb_frame, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
