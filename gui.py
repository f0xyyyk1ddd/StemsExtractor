import sys
import os
import shutil
import threading
import logging
from pathlib import Path
import static_ffmpeg
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QRadioButton, QButtonGroup, 
                             QProgressBar, QMessageBox, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QPixmap

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("GUI")

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

class StemsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_path = None
        self.is_processing = False
        self.signals = WorkerSignals()
        self.signals.update_status.connect(self.update_status_label)
        self.signals.finished.connect(self.on_success)
        self.signals.error.connect(self.on_error)

    def initUI(self):
        self.setWindowTitle('Stems Extractor Pro')
        self.setGeometry(300, 300, 600, 550)
        
        # Determine path to logo (works in dev and frozen modes)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        logo_path = os.path.join(base_path, "logo.png")
        self.setWindowIcon(QIcon(logo_path))

        # Professional Dark Theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', '.AppleSystemUIFont', 'Helvetica Neue', sans-serif;
                font-size: 14px;
            }
            QFrame {
                border: none;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                color: #e0e0e0;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #505050;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QPushButton:disabled {
                background-color: #252525;
                color: #555555;
                border-color: #2d2d2d;
            }
            QLabel {
                color: #cccccc;
            }
            QProgressBar {
                background-color: #2d2d2d;
                border: none;
                border-radius: 4px;
                height: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 4px;
            }
            QRadioButton {
                spacing: 8px;
                color: #dddddd;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #555;
            }
            QRadioButton::indicator:checked {
                background-color: #007acc;
                border-color: #007acc;
            }
            .card {
                background-color: #252526;
                border-radius: 8px;
                border: 1px solid #333;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Content Wrapper with Padding
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 40, 40, 30)

        # Header Section (Logo + Title)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label)

        # Title Text Stack
        title_stack = QVBoxLayout()
        title_stack.setSpacing(2)
        
        app_title = QLabel("Stems Extractor Pro")
        app_title.setStyleSheet("font-size: 26px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;")
        title_stack.addWidget(app_title)
        
        subtitle = QLabel("AI-Powered Music Separation")
        subtitle.setStyleSheet("font-size: 13px; color: #888888; font-weight: 400;")
        title_stack.addWidget(subtitle)
        
        header_layout.addLayout(title_stack)
        content_layout.addLayout(header_layout)
        
        content_layout.addSpacing(10)

        # Main Card
        card_frame = QFrame()
        card_frame.setProperty("class", "card")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)

        # File Selection Area
        file_area = QVBoxLayout()
        file_area.setSpacing(10)
        
        self.file_btn = QPushButton("📂  Выберите аудиофайл")
        self.file_btn.setCursor(Qt.PointingHandCursor)
        self.file_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: 1px dashed #555;
                font-size: 15px;
                padding: 20px;
                text-align: center;
            }
            QPushButton:hover {
                border-color: #007acc;
                background-color: #333;
            }
        """)
        self.file_btn.clicked.connect(self.select_file)
        file_area.addWidget(self.file_btn)

        self.file_label = QLabel("Файл не выбран")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("color: #666; font-style: italic; font-size: 13px;")
        file_area.addWidget(self.file_label)
        
        card_layout.addLayout(file_area)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #333; max-height: 1px;")
        card_layout.addWidget(line)

        # Stems Options
        stems_layout = QVBoxLayout()
        stems_label = QLabel("Режим разделения")
        stems_label.setStyleSheet("font-weight: 600; color: #ddd; margin-bottom: 5px;")
        stems_layout.addWidget(stems_label)

        self.stems_group = QButtonGroup(self)
        
        radio_style = "font-size: 14px;"
        
        self.radio2 = QRadioButton("2 Stems (Вокал + Инструментал)")
        self.radio2.setChecked(True)
        self.stems_group.addButton(self.radio2, 2)
        stems_layout.addWidget(self.radio2)

        self.radio4 = QRadioButton("4 Stems (Вокал, Ударные, Бас, Другое)")
        self.stems_group.addButton(self.radio4, 4)
        stems_layout.addWidget(self.radio4)

        self.radio5 = QRadioButton("5 Stems (+ Пианино)")
        self.stems_group.addButton(self.radio5, 5)
        stems_layout.addWidget(self.radio5)
        
        card_layout.addLayout(stems_layout)
        
        content_layout.addWidget(card_frame)

        # Action Area
        action_layout = QVBoxLayout()
        
        self.process_btn = QPushButton("НАЧАТЬ ОБРАБОТКУ")
        self.process_btn.setCursor(Qt.PointingHandCursor)
        self.process_btn.clicked.connect(self.start_processing)
        self.process_btn.setEnabled(False)
        self.process_btn.setFixedHeight(50)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #005a9c;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #555;
            }
        """)
        action_layout.addWidget(self.process_btn)

        # Progress Bar & Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888; font-size: 13px; margin-top: 5px;")
        action_layout.addWidget(self.status_label)

        self.progressbar = QProgressBar()
        self.progressbar.setRange(0, 0)
        self.progressbar.hide()
        self.progressbar.setFixedHeight(4)
        action_layout.addWidget(self.progressbar)
        
        content_layout.addLayout(action_layout)

        # Open Output Folder Button
        self.open_folder_btn = QPushButton("Открыть папку с результатами")
        self.open_folder_btn.setCursor(Qt.PointingHandCursor)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #444;
                color: #aaa;
                font-size: 13px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
                border-color: #666;
                color: #fff;
            }
        """)
        content_layout.addWidget(self.open_folder_btn)

        content_layout.addStretch()

        # Footer
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(4)
        
        footer_tagline = QLabel("FOR DJ'S BY DJ'S")
        footer_tagline.setAlignment(Qt.AlignCenter)
        footer_tagline.setStyleSheet("color: #555; font-size: 11px; font-weight: 800; letter-spacing: 1px;")
        footer_layout.addWidget(footer_tagline)

        dev_label = QLabel("Developed by SCVDL & f0xyyy133")
        dev_label.setAlignment(Qt.AlignCenter)
        dev_label.setStyleSheet("color: #444; font-size: 11px;")
        footer_layout.addWidget(dev_label)
        
        content_layout.addLayout(footer_layout)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)

    def open_output_folder(self):
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        try:
            os.system(f"open '{output_dir.resolve()}'")
        except:
            pass

    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "", "Audio Files (*.mp3 *.wav *.flac *.m4a *.aiff)")
        if filename:
            self.input_path = Path(filename)
            self.file_label.setText(f"Выбран: {self.input_path.name}")
            self.file_label.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
            self.process_btn.setEnabled(True)

    def start_processing(self):
        if self.is_processing:
            return

        self.is_processing = True
        self.process_btn.setEnabled(False)
        self.process_btn.setText("Обработка...")
        self.file_btn.setEnabled(False)
        self.progressbar.show()
        self.status_label.setText("Инициализация AI и моделей...")
        self.status_label.setStyleSheet("color: #3498db;")

        thread = threading.Thread(target=self.run_separation, daemon=True)
        thread.start()

    def run_separation(self):
        try:
            # Check FFmpeg
            static_ffmpeg.add_paths()
            if not shutil.which("ffmpeg"):
                raise Exception("FFmpeg не найден. Установка повреждена.")

            stems = self.stems_group.checkedId()
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)

            self.signals.update_status.emit("Загрузка моделей (может занять время)...")

            # Lazy import
            import os
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            from spleeter.separator import Separator

            self.signals.update_status.emit(f"Разделение на {stems} дорожек...")
            separator = Separator(f"spleeter:{stems}stems")
            
            separator.separate_to_file(str(self.input_path), str(output_dir))
            
            result_path = output_dir / self.input_path.stem
            self.signals.finished.emit(str(result_path))

        except Exception as e:
            self.signals.error.emit(str(e))

    def update_status_label(self, text):
        self.status_label.setText(text)

    def on_success(self, result_path):
        self.is_processing = False
        self.progressbar.hide()
        self.status_label.setText("Готово! Файлы сохранены.")
        self.status_label.setStyleSheet("color: #2ecc71;")
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Начать разделение")
        self.file_btn.setEnabled(True)

        reply = QMessageBox.question(self, 'Успех', f"Разделение завершено!\nОткрыть папку с результатом?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            try:
                os.system(f"open '{result_path}'")
            except:
                pass

    def on_error(self, error_msg):
        self.is_processing = False
        self.progressbar.hide()
        self.status_label.setText("Ошибка обработки")
        self.status_label.setStyleSheet("color: #e74c3c;")
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Начать разделение")
        self.file_btn.setEnabled(True)
        QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{error_msg}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StemsApp()
    ex.show()
    sys.exit(app.exec_())
