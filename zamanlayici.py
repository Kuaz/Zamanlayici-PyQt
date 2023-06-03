import sys
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QTimeEdit, QWidget, QTabWidget


class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zamanlayici")
        self.setGeometry(200, 200, 380, 500)

        self.timer_running = False
        self.countdown_active = False
        self.elapsed_time = 0
        self.current_lap = 0
        self.lap_times = []

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 10, 280, 230)

        self.timer_tab = QWidget()
        self.countdown_tab = QWidget()

        self.tab_widget.addTab(self.timer_tab, "Kronometre")
        self.tab_widget.addTab(self.countdown_tab, "Zamanlayıcı")

        self.init_timer_tab()
        self.init_countdown_tab()

        self.setCentralWidget(self.tab_widget)

    def init_timer_tab(self):
        self.time_label = QLabel(self.timer_tab)
        self.time_label.setGeometry(50, 40, 200, 50)

        self.lap_label = QLabel(self.timer_tab)
        self.lap_label.setGeometry(50, 100, 200, 100)

        self.start_button = QPushButton("Başlat", self.timer_tab)
        self.start_button.setGeometry(50, 250, 75, 30)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Durdur", self.timer_tab)
        self.stop_button.setGeometry(150, 250, 75, 30)
        self.stop_button.clicked.connect(self.stop_timer)

        self.lap_button = QPushButton("Tur Atla", self.timer_tab)
        self.lap_button.setGeometry(250, 250, 75, 30)
        self.lap_button.clicked.connect(self.lap)

    def init_countdown_tab(self):
        self.countdown_edit = QTimeEdit(self.countdown_tab)
        self.countdown_edit.setGeometry(50, 50, 120, 30)
        self.countdown_edit.setDisplayFormat("mm:ss")
        self.countdown_edit.setTime(QTime(0, 0))

        self.start_countdown_button = QPushButton("Başlat", self.countdown_tab)
        self.start_countdown_button.setGeometry(50, 250, 75, 30)
        self.start_countdown_button.clicked.connect(self.start_countdown)

        self.stop_countdown_button = QPushButton("Durdur", self.countdown_tab)
        self.stop_countdown_button.setGeometry(150, 250, 75, 30)
        self.stop_countdown_button.clicked.connect(self.stop_countdown)

        self.reset_countdown_button = QPushButton("Sıfırla", self.countdown_tab)
        self.reset_countdown_button.setGeometry(250, 250, 75, 30)
        self.reset_countdown_button.clicked.connect(self.reset_countdown)

        self.countdown_label = QLabel(self.countdown_tab)
        self.countdown_label.setGeometry(50, 150, 200, 50)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(10)  # Her 10 milisaniyede bir güncelleme yap

    def start_countdown(self):
        if not self.countdown_active:
            self.countdown_active = True
            self.countdown_time = self.countdown_edit.time()
            self.countdown_timer = QTimer(self)
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)  # Her saniyede bir güncelleme yap

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.timer.stop()

    def stop_countdown(self):
        if self.countdown_active:
            self.countdown_active = False
            self.countdown_timer.stop()

    def lap(self):
        if self.timer_running:
            self.current_lap += 1
            lap_time = "{:.3f}".format(self.elapsed_time)  # Tur süresini üç basamaklı hale getirin
            self.lap_times.append(lap_time)
            self.update_lap_label()

    def update_lap_label(self):
        lap_text = ""
        for i, lap_time in enumerate(self.lap_times):
            lap_text += f"{i + 1}. tur: {lap_time} saniye\n"
        self.lap_label.setText(lap_text.strip())

    def update_timer(self):
        self.elapsed_time += 0.01  # Her güncellemede 0.01 saniye ekleyin
        self.time_label.setText(f"Geçen süre: {self.elapsed_time:.3f} saniye")  # Üç ondalık basamakla görüntüleyin

    def update_countdown(self):
        self.countdown_time = self.countdown_time.addSecs(-1)
        if self.countdown_time <= QTime(0, 0):
            self.countdown_timer.stop()
            self.countdown_active = False
            self.countdown_label.setText("Süre Bitti!")
        else:
            self.countdown_label.setText(f"Kalan süre: {self.countdown_time.toString('mm:ss')}")

    def reset_countdown(self):
        self.countdown_timer.stop()
        self.countdown_active = False
        self.countdown_edit.setTime(QTime(0, 0))
        self.countdown_label.setText("Kalan süre: 00:00")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())

