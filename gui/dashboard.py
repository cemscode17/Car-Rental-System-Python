from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, 
                             QComboBox, QGroupBox, QDialog)
from PyQt5.QtGui import QFont, QColor

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