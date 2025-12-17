# gui/dashboard.py
import os
import shutil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QDialog,
                             QScrollArea, QGridLayout, QFrame, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt

# --- DÜZENLEME PENCERESİ CLASS ---
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

# --- DASHBOARD PAGE CLASS (Resimli & Grid Yapılı) ---
class DashboardPage(QWidget):
    def __init__(self, switch_callback, veri_yoneticisi, toggle_theme_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.db = veri_yoneticisi
        self.toggle_theme_callback = toggle_theme_callback
        self.secilen_resim_yolu = None # Yeni araç eklerken tutulacak geçici yol
        self.init_ui()

    def init_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main)

        # --- ÜST BAR ---
        top_bar = QHBoxLayout()
        self.lbl_welcome = QLabel("Yönetim Paneli - Galeri")
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

        # --- FİLTRELEME ALANI ---
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Plaka, Marka veya Model Ara...")
        self.search_input.textChanged.connect(self.kartlari_guncelle)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tümü", "Müsait", "Kirada"])
        self.filter_combo.currentTextChanged.connect(self.kartlari_guncelle)
        
        filter_layout.addWidget(self.search_input, 70)
        filter_layout.addWidget(self.filter_combo, 30)
        main.addLayout(filter_layout)

        content = QHBoxLayout()
        
        # --- SOL PANEL: ARAÇ EKLEME (Resim Seçmeli) ---
        self.left_panel = QGroupBox("Yeni Araç Ekle")
        self.left_panel.setFixedWidth(300) 
        left_layout = QVBoxLayout()
        self.left_panel.setLayout(left_layout)
        
        # Resim Önizleme Alanı
        self.img_preview = QLabel("Resim Yok")
        self.img_preview.setAlignment(Qt.AlignCenter)
        self.img_preview.setFixedSize(260, 150)
        self.img_preview.setStyleSheet("border: 2px dashed #bdc3c7; border-radius: 10px; color: gray;")
        left_layout.addWidget(self.img_preview, alignment=Qt.AlignCenter)

        btn_select_img = QPushButton("📸 Fotoğraf Seç")
        btn_select_img.clicked.connect(self.resim_sec)
        left_layout.addWidget(btn_select_img)

        form = QFormLayout()
        form.setVerticalSpacing(10)
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
        btn_add.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_add.clicked.connect(self.arac_ekle)
        left_layout.addWidget(btn_add)
        left_layout.addStretch()
        content.addWidget(self.left_panel)

        # --- SAĞ PANEL: ARAÇ FİLOSU (SCROLL AREA & GRID) ---
        right_group = QGroupBox("Araç Filosu")
        right_layout = QVBoxLayout()
        right_group.setLayout(right_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20) 
        self.scroll_content.setLayout(self.grid_layout)
        
        self.scroll.setWidget(self.scroll_content)
        right_layout.addWidget(self.scroll)
        
        content.addWidget(right_group)
        main.addLayout(content)

        self.kartlari_guncelle()

    def resim_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Araç Resmi Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        if dosya_yolu:
            self.secilen_resim_yolu = dosya_yolu
            pixmap = QPixmap(dosya_yolu)
            self.img_preview.setPixmap(pixmap.scaled(260, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.img_preview.setText("") 

    def kartlari_guncelle(self):
        # Grid temizleme
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)

        durum_filtre = self.filter_combo.currentText()
        arama_metni = self.search_input.text().lower()
        
        row = 0
        col = 0
        max_col = 3 # Yan yana 3 araç

        for i, arac in enumerate(self.db.veriler["araclar"]):
            # Filtreleme
            if durum_filtre == "Müsait" and arac["durum"] != "Müsait": continue
            if durum_filtre == "Kirada" and arac["durum"] != "Kirada": continue
            if arama_metni and (arama_metni not in arac["plaka"].lower() and 
                                arama_metni not in arac["marka"].lower() and 
                                arama_metni not in arac["model"].lower()):
                continue
            
            # --- KART TASARIMI ---
            card = QFrame()
            card.setObjectName("CarCard")
            card.setStyleSheet("""
                QFrame#CarCard { 
                    background-color: white; 
                    border: 1px solid #dcdde1; 
                    border-radius: 15px; 
                }
                QFrame#CarCard:hover {
                    border: 2px solid #3498db;
                }
            """)
            card.setFixedSize(260, 360) 
            
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(10, 10, 10, 10)
            card.setLayout(card_layout)

            # 1. Resim
            lbl_img = QLabel()
            lbl_img.setFixedSize(240, 160)
            lbl_img.setAlignment(Qt.AlignCenter)
            lbl_img.setStyleSheet("background-color: #ecf0f1; border-radius: 10px;")
            
            resim_path = arac.get("resim")
            # Otomatik resim eşleştirme (Eski veriler için)
            if not resim_path and i < 6:
                resim_path = f"assets/arac{i+1}.png"
            elif not resim_path:
                resim_path = "assets/default_car.png"
            
            pixmap = QPixmap(resim_path)
            if pixmap.isNull():
                lbl_img.setText("Resim Yok")
            else:
                lbl_img.setPixmap(pixmap.scaled(240, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            card_layout.addWidget(lbl_img)

            # 2. Bilgiler
            lbl_info = QLabel(f"{arac['marka']} {arac['model']}\n{arac['plaka']}")
            lbl_info.setFont(QFont("Segoe UI", 12, QFont.Bold))
            lbl_info.setAlignment(Qt.AlignCenter)
            lbl_info.setWordWrap(True)
            card_layout.addWidget(lbl_info)

            lbl_price = QLabel(f"{arac['ucret']} TL / Gün")
            lbl_price.setStyleSheet("color: #e67e22; font-weight: bold; font-size: 14px;")
            lbl_price.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(lbl_price)

            # Durum
            lbl_status = QLabel(arac["durum"])
            lbl_status.setAlignment(Qt.AlignCenter)
            if arac["durum"] == "Müsait":
                lbl_status.setStyleSheet("color: white; background-color: #27ae60; border-radius: 5px; padding: 2px;")
            else:
                lbl_status.setStyleSheet("color: white; background-color: #c0392b; border-radius: 5px; padding: 2px;")
                if arac["kiralayan"]:
                    lbl_status.setText(f"Kirada: {arac['kiralayan']}")
            card_layout.addWidget(lbl_status)

            # 3. Butonlar
            btn_layout = QHBoxLayout()
            
            btn_action = QPushButton("Kirala" if arac["durum"] == "Müsait" else "İade Al")
            btn_action.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
            if arac["durum"] == "Müsait":
                btn_action.clicked.connect(lambda checked, idx=i: self.switch_callback(2, vehicle_index=idx))
            else:
                btn_action.clicked.connect(lambda checked, idx=i: self.iade_et(idx))
            
            btn_edit = QPushButton("✏️")
            btn_edit.setFixedWidth(30)
            btn_edit.clicked.connect(lambda checked, idx=i: self.duzenle(idx))
            
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedWidth(30)
            btn_delete.setStyleSheet("background-color: #c0392b;")
            btn_delete.clicked.connect(lambda checked, idx=i: self.sil(idx))

            btn_layout.addWidget(btn_action)
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            card_layout.addLayout(btn_layout)

            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_col:
                col = 0
                row += 1

    def arac_ekle(self):
        try:
            p, m, md = self.ent_plaka.text(), self.ent_marka.text(), self.ent_model.text()
            u = float(self.ent_ucret.text())
            if not p or not m: raise ValueError
            
            # Resim Kopyalama ve Kaydetme
            final_path = "assets/default_car.png"
            if self.secilen_resim_yolu:
                if not os.path.exists("assets"): os.makedirs("assets")
                dosya_adi = os.path.basename(self.secilen_resim_yolu)
                final_path = f"assets/{dosya_adi}"
                try:
                    shutil.copy(self.secilen_resim_yolu, final_path)
                except: pass
            
            self.db.arac_ekle(p, m, md, u, final_path)
            QMessageBox.information(self, "Başarılı", "Araç resimli olarak eklendi.")
            
            self.ent_plaka.clear(); self.ent_marka.clear(); self.ent_model.clear(); self.ent_ucret.clear()
            self.img_preview.setText("Resim Yok")
            self.img_preview.setPixmap(QPixmap())
            self.secilen_resim_yolu = None
            
            self.kartlari_guncelle()
            
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen bilgileri kontrol ediniz.")

    def duzenle(self, index):
        arac = self.db.veriler["araclar"][index]
        dialog = EditDialog(self, arac)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                self.db.arac_guncelle(index, *data)
                QMessageBox.information(self, "Başarılı", "Güncellendi")
                self.kartlari_guncelle()
            except: pass

    def iade_et(self, index):
        self.db.iade_al(index)
        QMessageBox.information(self, "Başarılı", "Araç iade alındı.")
        self.kartlari_guncelle()

    def sil(self, index):
        if QMessageBox.question(self, "Onay", "Silmek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.arac_sil(index)
            self.kartlari_guncelle()