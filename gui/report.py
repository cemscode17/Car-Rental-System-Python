from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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

        self.history_table.setColumnCount(7) 

        self.history_table.setHorizontalHeaderLabels(["Tarih", "Plaka", "Marka", "Model", "Müşteri", "Süre (Gün)", "Tutar"])
        
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
            self.history_table.setItem(row, 2, QTableWidgetItem(islem.get("marka", "-"))) 
            self.history_table.setItem(row, 3, QTableWidgetItem(islem.get("model", "-"))) 
            self.history_table.setItem(row, 4, QTableWidgetItem(islem.get("musteri", "-")))
            
            gun_val = islem.get("gun", "-") 
            self.history_table.setItem(row, 5, QTableWidgetItem(str(gun_val)))
            
            self.history_table.setItem(row, 6, QTableWidgetItem(f"{islem.get('tutar', 0)} TL"))