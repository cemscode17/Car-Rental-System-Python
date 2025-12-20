import os  # <-- Dosya yolunu bulmak için gerekli
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class LoginPage(QWidget):
    def __init__(self, switch_callback, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.toggle_theme_callback = toggle_theme_callback

        self.setObjectName("LoginPage")

        base_dir = os.getcwd()
        image_path = os.path.join(base_dir, "assets", "background.jpg")
        image_path = image_path.replace("\\", "/")

        self.setStyleSheet(f"""
            #LoginPage {{
                background-image: url({image_path}); 
                background-position: center;
                background-repeat: no-repeat;
                /* Resmi pencereye sığdır ve orantılı uzat */
                border-image: url({image_path}) 0 0 0 0 stretch stretch;
            }}
        """)
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # Üst Bar (Tema Butonu)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        btn_theme = QPushButton("🌓 Tema")
        btn_theme.setFixedWidth(80)
        btn_theme.setStyleSheet("background-color: #3498db; color: white; border: none; padding: 5px; border-radius: 5px;")
        btn_theme.clicked.connect(self.toggle_theme_callback)
        top_bar.addWidget(btn_theme)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        # --- ORTA KART (Login Kutusu) ---
        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(400, 350)
        
        # Gölge Efekti (Kartın resimden ayrılması için)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        self.card.setLayout(card_layout)

        title = QLabel("Yönetici Girişi")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        card_layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Kullanıcı Adı")
        self.user_input.setText("admin") 
        self.user_input.setStyleSheet("background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        
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
        
        info = QLabel("Varsayılan: admin / 1234")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 10px; color: gray;")
        card_layout.addWidget(info)

        main_layout.addWidget(self.card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

    def check_login(self):
        u, p = self.user_input.text(), self.pass_input.text()
        if u == "admin" and p == "1234":
            self.switch_callback(1) 
        else:
            QMessageBox.warning(self, "Hata", "Hatalı Giriş Bilgileri")