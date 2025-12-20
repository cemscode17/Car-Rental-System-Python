import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter # <-- QPainter ve QPixmap eklendi

class LoginPage(QWidget):
    def __init__(self, switch_callback, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.toggle_theme_callback = toggle_theme_callback
        
        self.setObjectName("LoginPage")
        # Dosya yolunu oluştur
        base_dir = os.getcwd()
        image_path = os.path.join(base_dir, "assets", "background.jpg")      
        # Resmi Python belleğine yükle
        self.background_image = QPixmap(image_path)

        if self.background_image.isNull():
            print(f"HATA: Resim bulunamadı veya yüklenemedi: {image_path}")
        else:
            print("BAŞARILI: Arkaplan resmi yüklendi.")

        self.init_ui()

    # Bu fonksiyon pencere her yenilendiğinde çalışır ve resmi arkaplana çizer.
    def paintEvent(self, event):
        if not self.background_image.isNull():
            painter = QPainter(self)
            # Resmi pencere boyutuna (self.rect) göre ölçekleyip çiz
            painter.drawPixmap(self.rect(), self.background_image)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        btn_theme = QPushButton("🌓 Tema")
        btn_theme.setFixedWidth(80)
        btn_theme.setStyleSheet("background-color: #3498db; color: white; border: none; padding: 5px; border-radius: 5px;")
        btn_theme.clicked.connect(self.toggle_theme_callback)
        top_bar.addWidget(btn_theme)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(400, 350)
        
        # Login kutusunun arkaplanını hafif şeffaf beyaz yapıyoruz ki resim üzerinde okunsun
        self.card.setStyleSheet("""
            #LoginCard {
                background-color: rgba(255, 255, 255, 240); 
                border-radius: 15px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        self.card.setLayout(card_layout)

        title = QLabel("Yönetici Girişi")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; background: transparent;") 
        card_layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Kullanıcı Adı")
        self.user_input.setText("admin") 
        self.user_input.setStyleSheet("background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        
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
        info.setStyleSheet("font-size: 10px; color: gray; background: transparent;")
        card_layout.addWidget(info)

        main_layout.addWidget(self.card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

    def check_login(self):
        u, p = self.user_input.text(), self.pass_input.text()
        if u == "admin" and p == "1234":
            self.switch_callback(1) 
        else:
            QMessageBox.warning(self, "Hata", "Hatalı Giriş Bilgileri")