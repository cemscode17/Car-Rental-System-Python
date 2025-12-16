from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QDateEdit, 
                             QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt, QDate

class RentalPage(QWidget):
    def __init__(self, switch_callback, veri_yoneticisi):
        super().__init__()
        self.switch_callback = switch_callback
        self.db = veri_yoneticisi
        self.target_index = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        
        container = QGroupBox("Kiralama Sözleşmesi")
        container.setFixedSize(500, 450)
        con_layout = QVBoxLayout()
        container.setLayout(con_layout)

        self.lbl_info = QLabel()
        self.lbl_info.setStyleSheet("font-size: 14px; color: #2980b9; font-weight: bold; margin-bottom: 10px;")
        con_layout.addWidget(self.lbl_info)

        form = QFormLayout()
        form.setVerticalSpacing(15)
        self.ent_musteri = QLineEdit()
        self.date_start = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        self.date_end = QDateEdit(calendarPopup=True, date=QDate.currentDate().addDays(1))
        self.lbl_tutar = QLabel("0.0 TL")
        self.lbl_tutar.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")

        self.date_start.dateChanged.connect(self.hesapla)
        self.date_end.dateChanged.connect(self.hesapla)

        form.addRow("Müşteri Adı:", self.ent_musteri)
        form.addRow("Başlangıç:", self.date_start)
        form.addRow("Bitiş:", self.date_end)
        form.addRow("Toplam Tutar:", self.lbl_tutar)
        con_layout.addLayout(form)
        con_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("İptal")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white;")
        btn_cancel.clicked.connect(lambda: self.switch_callback(1))
        
        btn_save = QPushButton("Onayla")
        btn_save.setStyleSheet("background-color: #27ae60; color: white;")
        btn_save.clicked.connect(self.kaydet)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        con_layout.addLayout(btn_layout)

        layout.addWidget(container)

    def prepare(self, index):
        self.target_index = index
        arac = self.db.veriler["araclar"][index]
        self.lbl_info.setText(f"{arac['marka']} {arac['model']} - {arac['plaka']}")
        self.hesapla()

    def hesapla(self):
        if self.target_index is None: return
        d1 = self.date_start.date()
        d2 = self.date_end.date()
        days = d1.daysTo(d2)
        if days <= 0:
            self.lbl_tutar.setText("Geçersiz Tarih")
            return
        ucret = self.db.veriler["araclar"][self.target_index]["ucret"]
        self.lbl_tutar.setText(f"{days * ucret} TL ({days} Gün)")

    def kaydet(self):
        musteri = self.ent_musteri.text()
        if not musteri or "Geçersiz" in self.lbl_tutar.text():
            QMessageBox.warning(self, "Hata", "Bilgileri kontrol ediniz.")
            return
        
        d1 = self.date_start.date()
        d2 = self.date_end.date()
        days = d1.daysTo(d2)
        ucret = self.db.veriler["araclar"][self.target_index]["ucret"]
        
        self.db.kiralama_yap(self.target_index, musteri, days, days*ucret, 
                             d1.toString("yyyy-MM-dd"), d2.toString("yyyy-MM-dd"))
        QMessageBox.information(self, "Başarılı", "Kiralama yapıldı.")
        self.switch_callback(1)