import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon

from core.database import AracYonetici
from core.styles import LIGHT_THEME, DARK_THEME
from gui.login import LoginPage
from gui.dashboard import DashboardPage
from gui.rental import RentalPage
from gui.report import ReportPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = AracYonetici()
        self.is_dark = False 
        
        self.setWindowTitle("Araç Kiralama Otomasyonu")
        self.setGeometry(100, 100, 1200, 850)

        self.setWindowIcon(QIcon('assets/logo.png')) 
        
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
            self.page_dashboard.kartlari_guncelle() 
        if index == 2 and vehicle_index is not None: 
            self.page_rental.prepare(vehicle_index)
        if index == 3: 
            self.page_report.guncelle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
 
    try:
        import ctypes
        myappid = 'company.product.rentcar.modular'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except: pass
    
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())