import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QComboBox, QGroupBox, 
                             QStackedWidget, QDateEdit, QDialog, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QIcon 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# TEMALAR
LIGHT_THEME = """
    QMainWindow, QWidget { background-color: #f5f6fa; color: #2f3640; font-family: 'Segoe UI', sans-serif; }
    QGroupBox { font-weight: bold; border: 1px solid #dcdde1; border-radius: 8px; margin-top: 10px; background-color: #ffffff; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #2f3640; }
    QPushButton { background-color: #3498db; color: white; border-radius: 5px; padding: 8px 15px; font-weight: bold; }
    QPushButton:hover { background-color: #2980b9; }
    QLineEdit, QDateEdit, QComboBox { padding: 8px; border: 1px solid #dcdde1; border-radius: 5px; background-color: #ffffff; color: #2f3640; }
    QTableWidget { gridline-color: #dcdde1; background-color: #ffffff; alternate-background-color: #f1f2f6; border: 1px solid #dcdde1; border-radius: 5px; }
    QHeaderView::section { background-color: #3498db; color: white; padding: 5px; border: none; }
    QFrame#LoginCard { background-color: #ffffff; border-radius: 15px; border: 1px solid #dcdde1; }
"""

DARK_THEME = """
    QMainWindow, QWidget { background-color: #2f3640; color: #f5f6fa; font-family: 'Segoe UI', sans-serif; }
    QGroupBox { font-weight: bold; border: 1px solid #718093; border-radius: 8px; margin-top: 10px; background-color: #353b48; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #f5f6fa; }
    QPushButton { background-color: #8c7ae6; color: white; border-radius: 5px; padding: 8px 15px; font-weight: bold; }
    QPushButton:hover { background-color: #9c88ff; }
    QLineEdit, QDateEdit, QComboBox { padding: 8px; border: 1px solid #718093; border-radius: 5px; background-color: #2f3640; color: #f5f6fa; }
    QTableWidget { gridline-color: #718093; background-color: #353b48; alternate-background-color: #2f3640; border: 1px solid #718093; color: #f5f6fa; }
    QHeaderView::section { background-color: #8c7ae6; color: white; padding: 5px; border: none; }
    QFrame#LoginCard { background-color: #353b48; border-radius: 15px; border: 1px solid #718093; }
"""

# BACKEND
class AracYonetici:
    def __init__(self, dosya_adi='araclar.json'):
        self.dosya_adi = dosya_adi
        self.veriler = self.veri_yukle()

    def veri_yukle(self):
        if not os.path.exists(self.dosya_adi):
            return {"araclar": [], "toplam_gelir": 0, "gecmis_islemler": []}
        try:
            with open(self.dosya_adi, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"araclar": [], "toplam_gelir": 0, "gecmis_islemler": []}

    def kaydet(self):
        with open(self.dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=4)

    def arac_ekle(self, plaka, marka, model, ucret):
        yeni_arac = {
            "plaka": plaka, "marka": marka, "model": model,
            "ucret": float(ucret), "durum": "Müsait",
            "kiralayan": "", "baslangic": "", "bitis": ""
        }
        self.veriler["araclar"].append(yeni_arac)
        self.kaydet()

    def arac_sil(self, index):
        del self.veriler["araclar"][index]
        self.kaydet()

    def arac_guncelle(self, index, plaka, marka, model, ucret):
        arac = self.veriler["araclar"][index]
        arac["plaka"] = plaka
        arac["marka"] = marka
        arac["model"] = model
        arac["ucret"] = float(ucret)
        self.kaydet()

    def kiralama_yap(self, index, musteri, gun_sayisi, toplam_tutar, baslangic, bitis):
        arac = self.veriler["araclar"][index]
        arac["durum"] = "Kirada"
        arac["kiralayan"] = musteri
        arac["baslangic"] = baslangic
        arac["bitis"] = bitis
        
        self.veriler["toplam_gelir"] += toplam_tutar
        
        self.veriler["gecmis_islemler"].append({
            "plaka": arac["plaka"], 
            "tutar": toplam_tutar,
            "gun": gun_sayisi, 
            "tarih": datetime.now().strftime("%Y-%m-%d"), 
            "musteri": musteri
        })
        self.kaydet()

    def iade_al(self, index):
        arac = self.veriler["araclar"][index]
        arac["durum"] = "Müsait"
        arac["kiralayan"] = ""; arac["baslangic"] = ""; arac["bitis"] = ""
        self.kaydet()

# DÜZENLEME
class EditDialog(QDialog):
    def __init__(self, parent, arac_bilgisi):
        super().__init__(parent)
        self.setWindowTitle("Araç Düzenle")
        self.setFixedWidth(300)
        self.layout = QFormLayout(self)
        self.layout.setSpacing(15)

        self.ent_plaka = QLineEdit(arac_bilgisi["plaka"])
        self.ent_marka = QLineEdit(arac_bilgisi["marka"])
        self.ent_model = QLineEdit(arac_bilgisi["model"])
        self.ent_ucret = QLineEdit(str(arac_bilgisi["ucret"]))

        self.layout.addRow("Plaka:", self.ent_plaka)
        self.layout.addRow("Marka:", self.ent_marka)
        self.layout.addRow("Model:", self.ent_model)
        self.layout.addRow("Günlük Ücret:", self.ent_ucret)

        btn_save = QPushButton("Kaydet")
        btn_save.clicked.connect(self.accept)
        self.layout.addRow(btn_save)

    def get_data(self):
        return (self.ent_plaka.text(), self.ent_marka.text(), 
                self.ent_model.text(), self.ent_ucret.text())

#FRONTEND

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

class DashboardPage(QWidget):
    def __init__(self, switch_callback, veri_yoneticisi, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.db = veri_yoneticisi
        self.toggle_theme_callback = toggle_theme_callback
        self.current_rows_indices = []
        self.init_ui()

    def init_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main)

        top_bar = QHBoxLayout()
        self.lbl_welcome = QLabel("Yönetim Paneli")
        self.lbl_welcome.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.btn_report = QPushButton("📊 Detaylı Analiz")
        self.btn_report.clicked.connect(lambda: self.switch_callback(3))

        btn_theme = QPushButton("🌓 Tema")
        btn_theme.clicked.connect(self.toggle_theme_callback)

        btn_logout = QPushButton("Çıkış")
        btn_logout.setStyleSheet("background-color: #e74c3c; color: white;")
        btn_logout.clicked.connect(lambda: self.switch_callback(0))
        
        top_bar.addWidget(self.lbl_welcome)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_report)
        top_bar.addWidget(btn_theme)
        top_bar.addWidget(btn_logout)
        main.addLayout(top_bar)

        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Plaka, Marka veya Model Ara...")
        self.search_input.textChanged.connect(self.tabloyu_guncelle)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tümü", "Müsait", "Kirada"])
        self.filter_combo.currentTextChanged.connect(self.tabloyu_guncelle)
        
        filter_layout.addWidget(self.search_input, 70)
        filter_layout.addWidget(self.filter_combo, 30)
        main.addLayout(filter_layout)

        content = QHBoxLayout()
        
        self.left_panel = QGroupBox("Araç Ekleme Paneli")
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        self.left_panel.setLayout(left_layout)
        
        form = QFormLayout()
        form.setVerticalSpacing(15)
        self.ent_plaka = QLineEdit()
        self.ent_marka = QLineEdit()
        self.ent_model = QLineEdit()
        self.ent_ucret = QLineEdit()
        self.ent_ucret.setPlaceholderText("0.0")
        
        form.addRow("Plaka:", self.ent_plaka)
        form.addRow("Marka:", self.ent_marka)
        form.addRow("Model:", self.ent_model)
        form.addRow("Ücret (TL):", self.ent_ucret)
        left_layout.addLayout(form)
        
        btn_add = QPushButton("Listeye Ekle")
        btn_add.setStyleSheet("background-color: #27ae60; color: white;")
        btn_add.clicked.connect(self.arac_ekle)
        left_layout.addWidget(btn_add)
        left_layout.addStretch()
        content.addWidget(self.left_panel, 30)

        right_panel = QGroupBox("Araç Filosu")
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Plaka", "Marka", "Model", "Ücret", "Durum", "Kiralayan"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        right_layout.addWidget(self.table)
        
        btn_box = QHBoxLayout()
        self.btn_kirala = QPushButton("Kirala")
        self.btn_kirala.clicked.connect(self.kiralamaya_git)
        
        self.btn_iade = QPushButton("İade Al")
        self.btn_iade.clicked.connect(self.iade_et)

        self.btn_edit = QPushButton("Düzenle")
        self.btn_edit.clicked.connect(self.duzenle)

        self.btn_sil = QPushButton("Sil")
        self.btn_sil.setStyleSheet("background-color: #c0392b; color: white;")
        self.btn_sil.clicked.connect(self.sil)

        btn_box.addWidget(self.btn_kirala)
        btn_box.addWidget(self.btn_iade)
        btn_box.addWidget(self.btn_edit)
        btn_box.addWidget(self.btn_sil)
        right_layout.addLayout(btn_box)
        
        content.addWidget(right_panel, 70)
        main.addLayout(content)

    def tabloyu_guncelle(self):
        self.table.setRowCount(0)
        durum_filtre = self.filter_combo.currentText()
        arama_metni = self.search_input.text().lower()
        self.current_rows_indices = [] 
        
        for i, arac in enumerate(self.db.veriler["araclar"]):
            if durum_filtre == "Müsait" and arac["durum"] != "Müsait": continue
            if durum_filtre == "Kirada" and arac["durum"] != "Kirada": continue
            
            if arama_metni and (arama_metni not in arac["plaka"].lower() and 
                                arama_metni not in arac["marka"].lower() and 
                                arama_metni not in arac["model"].lower()):
                continue

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(arac["plaka"]))
            self.table.setItem(row, 1, QTableWidgetItem(arac["marka"]))
            self.table.setItem(row, 2, QTableWidgetItem(arac["model"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"{arac['ucret']} TL"))
            
            durum_item = QTableWidgetItem(arac["durum"])
            if arac["durum"] == "Müsait":
                durum_item.setForeground(QColor("#27ae60"))
            else:
                durum_item.setForeground(QColor("#c0392b"))
            durum_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            
            self.table.setItem(row, 4, durum_item)
            self.table.setItem(row, 5, QTableWidgetItem(arac["kiralayan"]))
            self.current_rows_indices.append(i)

    def arac_ekle(self):
        try:
            p, m, md = self.ent_plaka.text(), self.ent_marka.text(), self.ent_model.text()
            u = float(self.ent_ucret.text())
            if not p or not m: raise ValueError
            self.db.arac_ekle(p, m, md, u)
            QMessageBox.information(self, "Başarılı", "Araç sisteme eklendi.")
            self.tabloyu_guncelle()
            self.ent_plaka.clear(); self.ent_marka.clear(); self.ent_model.clear(); self.ent_ucret.clear()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları kontrol ediniz.")

    def duzenle(self):
        selected = self.table.currentRow()
        if selected == -1: return
        real_index = self.current_rows_indices[selected]
        arac = self.db.veriler["araclar"][real_index]
        dialog = EditDialog(self, arac)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                self.db.arac_guncelle(real_index, *data)
                QMessageBox.information(self, "Başarılı", "Güncellendi")
                self.tabloyu_guncelle()
            except: pass

    def kiralamaya_git(self):
        selected = self.table.currentRow()
        if selected == -1: return
        real_index = self.current_rows_indices[selected]
        arac = self.db.veriler["araclar"][real_index]
        if arac["durum"] != "Müsait":
            QMessageBox.warning(self, "Hata", "Araç zaten kirada!")
            return
        self.switch_callback(2, vehicle_index=real_index)

    def iade_et(self):
        selected = self.table.currentRow()
        if selected == -1: return
        real_index = self.current_rows_indices[selected]
        self.db.iade_al(real_index)
        QMessageBox.information(self, "Başarılı", "Araç iade alındı.")
        self.tabloyu_guncelle()

    def sil(self):
        selected = self.table.currentRow()
        if selected == -1: return
        if QMessageBox.question(self, "Onay", "Silmek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.arac_sil(self.current_rows_indices[selected])
            self.tabloyu_guncelle()

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

class ReportPage(QWidget):
    def __init__(self, switch_callback, veri_yoneticisi):
        super().__init__()
        self.switch_callback = switch_callback
        self.db = veri_yoneticisi
        self.is_dark_mode = False 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        
        self.lbl_title = QLabel("Finansal Analiz ve Doluluk Oranı")
        self.lbl_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_title)

        graph_layout = QHBoxLayout()
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)
        layout.addLayout(graph_layout)
        
        self.lbl_stats = QLabel()
        self.lbl_stats.setAlignment(Qt.AlignCenter)
        self.lbl_stats.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.lbl_stats)

        lbl_history = QLabel("📋 Detaylı Kiralama Geçmişi")
        lbl_history.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(lbl_history)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Tarih", "Plaka", "Müşteri", "Süre (Gün)", "Tutar"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.history_table)

        btn_back = QPushButton("Geri Dön")
        btn_back.clicked.connect(lambda: self.switch_callback(1))
        layout.addWidget(btn_back)

    def set_graph_theme(self, is_dark):
        self.is_dark_mode = is_dark
        if is_dark:
            self.figure.patch.set_facecolor('#2f3640')
            plt.rcParams['text.color'] = 'white'
        else:
            self.figure.patch.set_facecolor('#f5f6fa')
            plt.rcParams['text.color'] = 'black'
        self.guncelle()

    def guncelle(self):
        self.figure.clear()
        araclar = self.db.veriler["araclar"]
        toplam = len(araclar)
        kirada = sum(1 for x in araclar if x["durum"] == "Kirada")
        musait = toplam - kirada
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("none") 
        if toplam > 0:
            ax.pie([musait, kirada], labels=['Müsait', 'Kirada'], autopct='%1.1f%%', 
                   colors=['#27ae60', '#c0392b'], textprops=dict(color="white" if self.is_dark_mode else "black"))
        self.canvas.draw()
        self.lbl_stats.setText(f"Toplam Gelir: {self.db.veriler['toplam_gelir']} TL")

        gecmis = self.db.veriler["gecmis_islemler"]
        self.history_table.setRowCount(0)
        
        for islem in reversed(gecmis):
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(islem.get("tarih", "-")))
            self.history_table.setItem(row, 1, QTableWidgetItem(islem.get("plaka", "-")))
            self.history_table.setItem(row, 2, QTableWidgetItem(islem.get("musteri", "-")))
            
            gun_val = islem.get("gun", "-") 
            self.history_table.setItem(row, 3, QTableWidgetItem(str(gun_val)))
            
            self.history_table.setItem(row, 4, QTableWidgetItem(f"{islem.get('tutar', 0)} TL"))

# ANA PENCERE
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = AracYonetici()
        self.is_dark = False 
        
        self.setWindowTitle("Araç Kiralama Otomasyonu v2.3")
        self.setGeometry(100, 100, 1200, 850)
        
        self.setWindowIcon(QIcon('logo.png')) 
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.page_login = LoginPage(self.switch_page, self.toggle_theme)
        self.page_dashboard = DashboardPage(self.switch_page, self.db, self.toggle_theme)
        self.page_rental = RentalPage(self.switch_page, self.db)
        self.page_report = ReportPage(self.switch_page, self.db)
        
        self.stack.addWidget(self.page_login)     
        self.stack.addWidget(self.page_dashboard) 
        self.stack.addWidget(self.page_rental)    
        self.stack.addWidget(self.page_report)    

        self.apply_theme()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)
        self.page_report.set_graph_theme(self.is_dark)

    def switch_page(self, index, vehicle_index=None):
        self.stack.setCurrentIndex(index)
        if index == 1: 
            self.page_dashboard.tabloyu_guncelle()
        if index == 2 and vehicle_index is not None: 
            self.page_rental.prepare(vehicle_index)
        if index == 3: 
            self.page_report.guncelle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        import ctypes
        myappid = 'company.product.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except: pass
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())