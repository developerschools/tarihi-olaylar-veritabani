from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QTextBrowser
import sqlite3

class Olay:
    def __init__(self, ad, tarih, aciklama):
        self.ad = ad
        self.tarih = tarih
        self.aciklama = aciklama
        self.shahsiyetler = []
        self.donemler = []

    def __str__(self):
        return f"{self.ad} - {self.tarih}"

    def shahsiyet_ekle(self, shahsiyet):
        self.shahsiyetler.append(shahsiyet)

    def donem_ekle(self, donem):
        self.donemler.append(donem)

class Shahsiyet:
    def __init__(self, ad, donemler):
        self.ad = ad
        self.donemler = donemler

class Donem:
    def __init__(self, ad, baslangic, bitis):
        self.ad = ad
        self.baslangic = baslangic
        self.bitis = bitis

class TarihciArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarihçi - Tarihi Olaylar Veritabanı")
        self.init_ui()
        self.create_db()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label_arama = QLabel("Olay Ara:")
        self.input_arama = QLineEdit()

        self.label_olay_ad = QLabel("Olay Adı:")
        self.input_olay_ad = QLineEdit()

        self.label_olay_tarih = QLabel("Olay Tarihi:")
        self.input_olay_tarih = QLineEdit()

        self.label_olay_aciklama = QLabel("Olay Açıklaması:")
        self.input_olay_aciklama = QTextEdit()

        self.button_olay_ekle = QPushButton("Olay Ekle")
        self.button_olay_ekle.clicked.connect(self.olay_ekle)

        self.button_arama = QPushButton("Ara")
        self.button_arama.clicked.connect(self.olay_ara)

        self.liste_olaylar = QListWidget()
        self.liste_olaylar.itemClicked.connect(self.olay_secildi)

        self.label_olay_detay = QLabel("Olay Detayı:")
        self.text_olay_detay = QTextBrowser()

        self.label_shahsiyet_ad = QLabel("Şahsiyet Adı:")
        self.input_shahsiyet_ad = QLineEdit()

        self.label_shahsiyet_donemler = QLabel("Şahsiyetin Yaşadığı Dönemler (Virgülle Ayırın):")
        self.input_shahsiyet_donemler = QLineEdit()

        self.label_donem_ad = QLabel("Dönem Adı:")
        self.input_donem_ad = QLineEdit()

        self.label_donem_baslangic = QLabel("Dönemin Başlangıç Tarihi:")
        self.input_donem_baslangic = QLineEdit()

        self.label_donem_bitis = QLabel("Dönemin Bitiş Tarihi:")
        self.input_donem_bitis = QLineEdit()

        self.button_shahsiyet_ekle = QPushButton("Şahsiyet Ekle")
        self.button_shahsiyet_ekle.clicked.connect(self.shahsiyet_ekle)

        self.button_donem_ekle = QPushButton("Dönem Ekle")
        self.button_donem_ekle.clicked.connect(self.donem_ekle)

        arama_layout = QHBoxLayout()
        arama_layout.addWidget(self.label_arama)
        arama_layout.addWidget(self.input_arama)
        arama_layout.addWidget(self.button_arama)

        self.layout.addLayout(arama_layout)
        self.layout.addWidget(self.label_olay_ad)
        self.layout.addWidget(self.input_olay_ad)
        self.layout.addWidget(self.label_olay_tarih)
        self.layout.addWidget(self.input_olay_tarih)
        self.layout.addWidget(self.label_olay_aciklama)
        self.layout.addWidget(self.input_olay_aciklama)
        self.layout.addWidget(self.button_olay_ekle)
        self.layout.addWidget(self.liste_olaylar)
        self.layout.addWidget(self.label_olay_detay)
        self.layout.addWidget(self.text_olay_detay)
        self.layout.addWidget(self.label_shahsiyet_ad)
        self.layout.addWidget(self.input_shahsiyet_ad)
        self.layout.addWidget(self.label_shahsiyet_donemler)
        self.layout.addWidget(self.input_shahsiyet_donemler)
        self.layout.addWidget(self.button_shahsiyet_ekle)
        self.layout.addWidget(self.label_donem_ad)
        self.layout.addWidget(self.input_donem_ad)
        self.layout.addWidget(self.label_donem_baslangic)
        self.layout.addWidget(self.input_donem_baslangic)
        self.layout.addWidget(self.label_donem_bitis)
        self.layout.addWidget(self.input_donem_bitis)
        self.layout.addWidget(self.button_donem_ekle)

        self.setLayout(self.layout)

        self.olaylar = []
        self.conn = sqlite3.connect('tarih.db')
        self.cur = self.conn.cursor()

    def create_db(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Olaylar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ad TEXT,
                            tarih TEXT,
                            aciklama TEXT)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Shahsiyetler (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            olay_id INTEGER,
                            ad TEXT,
                            FOREIGN KEY(olay_id) REFERENCES Olaylar(id))''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Donemler (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            olay_id INTEGER,
                            ad TEXT,
                            baslangic TEXT,
                            bitis TEXT,
                            FOREIGN KEY(olay_id) REFERENCES Olaylar(id))''')

    def olay_ekle(self):
        olay_ad = self.input_olay_ad.text()
        olay_tarih = self.input_olay_tarih.text()
        olay_aciklama = self.input_olay_aciklama.toPlainText()

        if not olay_ad or not olay_tarih or not olay_aciklama:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        self.cur.execute("INSERT INTO Olaylar (ad, tarih, aciklama) VALUES (?, ?, ?)", (olay_ad, olay_tarih, olay_aciklama))
        self.conn.commit()

        olay = Olay(olay_ad, olay_tarih, olay_aciklama)
        self.olaylar.append(olay)
        self.liste_olaylar.addItem(str(olay))
        QMessageBox.information(self, "Bilgi", "Olay başarıyla eklendi!")

    def shahsiyet_ekle(self):
        if not self.liste_olaylar.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir olay seçin!")
            return

        secili_olay = self.liste_olaylar.currentItem().text()
        for olay in self.olaylar:
            if str(olay) == secili_olay:
                ad = self.input_shahsiyet_ad.text()
                if not ad:
                    QMessageBox.warning(self, "Uyarı", "Lütfen bir şahsiyet adı girin!")
                    return
                donemler = self.input_shahsiyet_donemler.text().split(',')
                shahsiyet = Shahsiyet(ad, donemler)
                olay.shahsiyet_ekle(shahsiyet)
                QMessageBox.information(self, "Bilgi", "Şahsiyet başarıyla eklendi!")
                return

    def donem_ekle(self):
        ad = self.input_donem_ad.text()
        baslangic = self.input_donem_baslangic.text()
        bitis = self.input_donem_bitis.text()

        if not ad or not baslangic or not bitis:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        donem = Donem(ad, baslangic, bitis)
        QMessageBox.information(self, "Bilgi", "Dönem başarıyla eklendi!")

    def olay_secildi(self, item):
        olay_ad = item.text()
        for olay in self.olaylar:
            if str(olay) == olay_ad:
                self.text_olay_detay.setText(f"Olay Adı: {olay.ad}\nOlay Tarihi: {olay.tarih}\nOlay Açıklaması:\n{olay.aciklama}")
                if olay.shahsiyetler:
                    shahsiyet_str = "\n".join([shahsiyet.ad for shahsiyet in olay.shahsiyetler])
                    self.text_olay_detay.append(f"\nOlaya Katılan Şahsiyetler:\n{shahsiyet_str}")
                if olay.donemler:
                    donem_str = "\n".join([donem.ad for donem in olay.donemler])
                    self.text_olay_detay.append(f"\nOlayın Geçtiği Dönemler:\n{donem_str}")
                return

    def olay_ara(self):
        aranan_metin = self.input_arama.text().lower()
        self.liste_olaylar.clear()
        for olay in self.olaylar:
            if aranan_metin in olay.ad.lower() or aranan_metin in olay.tarih.lower() or aranan_metin in olay.aciklama.lower():
                self.liste_olaylar.addItem(str(olay))

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TarihciArayuzu()
    window.show()
    sys.exit(app.exec_())
