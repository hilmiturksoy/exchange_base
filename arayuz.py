from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QTextEdit, QComboBox
)
import sys
from currency_base import Usd_Currency, Euro_Currency, Try_Opening_Cash, Usd_Opening_Cash


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Döviz & Kasa Yönetimi")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tabs.addTab(self.alis_satis_tab(), "💱 Alış / Satış")
        self.tabs.addTab(self.kasa_tab(), "💰 Kasa Açılışı")
        self.tabs.addTab(self.rapor_tab(), "📊 Raporlar")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def alis_satis_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.rate_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.person_input = QLineEdit()
        self.firm_input = QLineEdit()
        self.doviz_turu = QComboBox()
        self.doviz_turu.addItems(["USD", "EUR"])
        self.transaction_type = QComboBox()
        self.transaction_type.addItems(["Alış", "Satış"])

        self.output = QTextEdit()

        btn = QPushButton("İşlem Kaydet")
        btn.clicked.connect(self.alis_satis_kaydet)

        layout.addWidget(QLabel("Kur"))
        layout.addWidget(self.rate_input)
        layout.addWidget(QLabel("Miktar"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Kişi"))
        layout.addWidget(self.person_input)
        layout.addWidget(QLabel("Firma"))
        layout.addWidget(self.firm_input)
        layout.addWidget(QLabel("Döviz Türü"))
        layout.addWidget(self.doviz_turu)
        layout.addWidget(QLabel("İşlem Türü"))
        layout.addWidget(self.transaction_type)
        layout.addWidget(btn)
        layout.addWidget(QLabel("Sonuç"))
        layout.addWidget(self.output)

        tab.setLayout(layout)
        return tab

    def alis_satis_kaydet(self):
        rate = float(self.rate_input.text())
        amount = float(self.amount_input.text())
        person = self.person_input.text()
        firm = self.firm_input.text()
        doviz = self.doviz_turu.currentText()
        islem = self.transaction_type.currentText()

        if doviz == "USD":
            obj = Usd_Currency(rate, amount, firm, person)
        else:
            obj = Euro_Currency(rate, amount, firm, person)

        if islem == "Alış":
            result = obj.oran_alis()
        else:
            result = obj.oran_satis()

        self.output.setText(result)

    def kasa_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.b200 = QLineEdit()
        self.b100 = QLineEdit()
        self.b50 = QLineEdit()
        self.b20 = QLineEdit()
        self.b10 = QLineEdit()
        self.b5 = QLineEdit()

        btn = QPushButton("TRY Açılış Kaydet")
        btn.clicked.connect(self.try_kasa_kaydet)
        self.kasa_output = QTextEdit()

        for label, box in [("200 TL", self.b200), ("100 TL", self.b100), ("50 TL", self.b50),
                           ("20 TL", self.b20), ("10 TL", self.b10), ("5 TL", self.b5)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(box)

        layout.addWidget(btn)
        layout.addWidget(self.kasa_output)

        tab.setLayout(layout)
        return tab

    def try_kasa_kaydet(self):
        b200 = int(self.b200.text() or 0)
        b100 = int(self.b100.text() or 0)
        b50 = int(self.b50.text() or 0)
        b20 = int(self.b20.text() or 0)
        b10 = int(self.b10.text() or 0)
        b5 = int(self.b5.text() or 0)

        kasa = Try_Opening_Cash(b200, b100, b50, b20, b10, b5, 0, 0, 0, 0, 0)
        kasa.open_balance()
        self.kasa_output.setText(kasa.gunluk_bakiye_listesi())

    def rapor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.rapor_box = QTextEdit()
        btn = QPushButton("📋 Kasa & İşlem Raporu")
        btn.clicked.connect(self.rapor_goster)

        layout.addWidget(btn)
        layout.addWidget(self.rapor_box)
        tab.setLayout(layout)
        return tab

    def rapor_goster(self):
        rapor = Usd_Currency.total_amount()
        self.rapor_box.setText(rapor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = MainApp()
    pencere.show()
    sys.exit(app.exec_())
