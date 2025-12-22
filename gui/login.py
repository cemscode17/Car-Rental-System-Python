import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter

class LoginPage(QWidget):
    def __init__(self, switch_callback, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.toggle_theme_callback = toggle_theme_callback
        
        self.setObjectName("LoginPage")
        base_dir = os.getcwd()
        image_path = os.path.join(base_dir, "assets", "background.jpg")
        self.background_image = QPixmap(image_path)
        
        if self.background_image.isNull():
            print(f"HATA: Resim bulunamadı: {image_path}")

        self.init_ui()

    def paintEvent(self, event):
        if not self.background_image.isNull():
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.background_image)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        btn_theme = QPushButton("🌓 Tema")
        btn_theme.setFixedWidth(80)
        btn_theme.setStyleSheet("background-color: #3498db; color: white; border: none; padding: 5px; border-radius: 5px; font-weight: bold;")
        btn_theme.clicked.connect(self.toggle_theme_callback)
        top_bar.addWidget(btn_theme)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(400, 350)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        self.card.setLayout(card_layout)

        self.lbl_title = QLabel("Yönetici Girişi")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        card_layout.addWidget(self.lbl_title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Kullanıcı Adı")
        self.user_input.setText("admin") 
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)
        
        card_layout.addWidget(self.user_input)
        card_layout.addWidget(self.pass_input)

        btn_login = QPushButton("Sisteme Giriş")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setMinimumHeight(45)
        btn_login.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        btn_login.clicked.connect(self.check_login)
        card_layout.addWidget(btn_login)

        self.lbl_info = QLabel("Varsayılan: admin / 1234")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 10px; color: gray; background: transparent;")
        card_layout.addWidget(self.lbl_info)

        main_layout.addWidget(self.card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.set_theme_mode(False)

    def set_theme_mode(self, is_dark):
        if is_dark:
            card_bg = "rgba(30, 30, 30, 240)" 
            text_color = "white"
            input_bg = "#2f3640"
            input_text = "white"
            input_border = "1px solid #57606f"
            placeholder_color = "#a4b0be"
        else:
            card_bg = "rgba(255, 255, 255, 240)"
            text_color = "#2c3e50"
            input_bg = "white"
            input_text = "black"
            input_border = "1px solid #bdc3c7"
            placeholder_color = "gray"

        self.card.setStyleSheet(f"#LoginCard {{ background-color: {card_bg}; border-radius: 15px; }}")

        self.lbl_title.setStyleSheet(f"color: {text_color}; background: transparent;")

        input_style = f"""
            QLineEdit {{ 
                background-color: {input_bg}; 
                color: {input_text}; 
                padding: 10px; 
                border-radius: 5px; 
                border: {input_border};
            }}
        """
        self.user_input.setStyleSheet(input_style)
        self.pass_input.setStyleSheet(input_style)

        self.lbl_info.setStyleSheet(f"font-size: 10px; color: {text_color}; background: transparent;")

    def check_login(self):
        u, p = self.user_input.text(), self.pass_input.text()
        if u == "admin" and p == "1234":
            self.switch_callback(1) 
        else:
            QMessageBox.warning(self, "Hata", "Hatalı Giriş Bilgileri")