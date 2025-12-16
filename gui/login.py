from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class LoginPage(QWidget):
    def __init__(self, switch_callback, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.toggle_theme_callback = toggle_theme_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        btn_theme = QPushButton("🌓 Tema")
        btn_theme.setFixedWidth(80)
        btn_theme.clicked.connect(self.toggle_theme_callback)
        top_bar.addWidget(btn_theme)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(400, 350)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
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
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)
        
        card_layout.addWidget(self.user_input)
        card_layout.addWidget(self.pass_input)

        btn_login = QPushButton("Sisteme Giriş")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setMinimumHeight(40)
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