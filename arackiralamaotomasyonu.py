import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5 import QtCore
from datetime import datetime
import sqlite3
from PyQt5 import QtWidgets
from xlsxwriter.workbook import Workbook
import pandas as pd

anaekran_butonlar = QFont("Centruy Gothic", 13)
label_girdi = QFont("Centruy Gothic", 12)
label_text = QFont("Centruy Gothic", 9)
labelgiris = QFont("Centruy Gothic", 11)
sonuclar = QFont("Centruy Gothic", 17)

baglanti = sqlite3.connect("veritabanı.db")
etiket = baglanti.cursor()

etiket.execute(
    "CREATE TABLE IF NOT EXISTS musteri(TC TEXT PRIMARY KEY NOT NULL,Isim TEXT NOT NULL,Soyisim TEXT NOT NULL,Dogumtrh TEXT NOT NULL, Ceptelefonu TEXT NOT NULL,Email TEXT NOT NULL,"
    "Adres TEXT NOT NULL, Ehliyetno TEXT NOT NULL, Ehliyetturu TEXT NOT NULL)")
etiket.execute(
    "CREATE TABLE IF NOT EXISTS araclar(Plaka TEXT PRIMARY KEY NOT NULL,Marka TEXT NOT NULL,MODEL TEXT NOT NULL,YIL TEXT NOT NULL,YAKIT TEXT NOT NULL,MOTOR_GUCU TEXT NOT NULL,"
    "SON_KM INT NOT NULL,VITES TEXT NOT NULL,SILINDIR TEXT NOT NULL,CEKIS TEXT NOT NULL,"
    "KASA_TIPI TEXT NOT NULL,KAPI_SAYISI INT NOT NULL,RENK TEXT NOT NULL,FREN_CESIDI TEXT NOT NULL)")
etiket.execute(
    "CREATE TABLE IF NOT EXISTS kira(MUSTERI_TC TEXT ,MUSTERI_ISIM TEXT,MUSTERI_SOYISIM TEXT ,ARAC_PLAKA TEXT ,"
    "ARAC_MARKA TEXT, ARAC_MODEL TEXT ,BASLAMA TEXT,BITIS TEXT,ODENECEK_TUTAR TEXT)")


class giris_pencere(QWidget):

    def anaekran(self):
        self.musteriekle = QPushButton("Müşteri Ekle", self)
        self.musteriekle.setFont(anaekran_butonlar)
        self.musteriekle.setGeometry(20, 20, 150, 70)
        self.musteriekle.setIcon(QtGui.QIcon("musteri2.ico"))
        self.musteriekle.setIconSize((QtCore.QSize(30, 30)))

        self.musterilistele = QPushButton("Müşteri Listele", self)
        self.musterilistele.setFont(anaekran_butonlar)
        self.musterilistele.setGeometry(190, 20, 150, 70)
        self.musterilistele.setIcon(QtGui.QIcon("user.ico"))
        self.musterilistele.setIconSize((QtCore.QSize(30, 30)))

        self.aracekle = QPushButton("Araç Ekle", self)
        self.aracekle.setFont(anaekran_butonlar)
        self.aracekle.setGeometry(360, 20, 150, 70)
        self.aracekle.setIcon(QtGui.QIcon("arabaekle.ico"))
        self.aracekle.setIconSize((QtCore.QSize(50, 50)))

        self.araclistele = QPushButton("Araç Listele", self)
        self.araclistele.setFont(anaekran_butonlar)
        self.araclistele.setGeometry(530, 20, 150, 70)
        self.araclistele.setIcon(QtGui.QIcon("arac_listele.ico"))
        self.araclistele.setIconSize((QtCore.QSize(35, 35)))

        self.arackirala = QPushButton("Araç Kirala", self)
        self.arackirala.setFont(anaekran_butonlar)
        self.arackirala.setGeometry(700, 20, 150, 70)
        self.arackirala.setIcon(QtGui.QIcon("kira_ekle.ico"))
        self.arackirala.setIconSize((QtCore.QSize(35, 35)))

        self.kiradakiaraclar = QPushButton("Kira Listesi", self)
        self.kiradakiaraclar.setFont(anaekran_butonlar)
        self.kiradakiaraclar.setGeometry(870, 20, 150, 70)
        self.kiradakiaraclar.setIcon(QtGui.QIcon("kirala.ico"))
        self.kiradakiaraclar.setIconSize((QtCore.QSize(35, 35)))

    def resim(self):
        image = QPixmap("resim.png")
        self.arkaplan = QLabel(self)
        self.arkaplan.setGeometry(90, 120, 1150, 400)
        self.arkaplan.setPixmap(image)

    def musteri_ekle_gec(self):
        self.gec = musteri_ekle()
        self.gec.show()

    def musteri_liste_gec(self):
        self.gec1 = musteri_listele()
        self.gec1.show()

    def arac_ekle_gec(self):
        self.gec2 = arac_ekle()
        self.gec2.show()

    def arac_listele_gec(self):
        self.gec3 = arac_listele()
        self.gec3.show()

    def kira_ekle_gec(self):
        self.gec4 = kira_ekle()
        QMessageBox.information(kira_ekle(), "Bilgilendirme", "LÜTFEN SEÇİMLERİ YAPMADAN KAYIT İŞLEMİ YAPMAYINIZ")
        self.gec4.show()

    def kira_listele_gec(self):
        self.gec5 = kira_listele()
        self.gec5.show()

    def __init__(self):
        super().__init__()
        self.widtth = 1050
        self.heigght = 550
        self.setMaximumSize(self.widtth, self.heigght)
        self.setMinimumSize(self.widtth, self.heigght)
        self.setGeometry(450, 250, 1050, 550)
        self.anaekran()
        self.resim()
        self.musteriekle.clicked.connect(self.musteri_ekle_gec)
        self.musterilistele.clicked.connect(self.musteri_liste_gec)
        self.aracekle.clicked.connect(self.arac_ekle_gec)
        self.araclistele.clicked.connect(self.arac_listele_gec)
        self.arackirala.clicked.connect(self.kira_ekle_gec)
        self.kiradakiaraclar.clicked.connect(self.kira_listele_gec)
        self.show()
class musteri_ekle(QWidget):

    def kullanici_alani(self):
        self.tc = QLabel("T.CNo : ", self)
        self.tc.move(80, 53)
        self.tc.setFont(label_girdi)
        self.tc_girdi = QLineEdit(self)
        self.tc_girdi.setFont(label_text)
        self.tc_girdi.setGeometry(160, 50, 220, 23)
        self.tc_girdi.setPlaceholderText("TC kimlik numaranız...")

        self.isim = QLabel("İsim : ", self)
        self.isim.move(99, 93)
        self.isim.setFont(label_girdi)
        self.isim_girdi = QLineEdit(self)
        self.isim_girdi.setFont(label_text)
        self.isim_girdi.setGeometry(160, 90, 220, 23)
        self.isim_girdi.setPlaceholderText("İsim giriniz...")

        self.soyisim = QLabel("Soyisim : ", self)
        self.soyisim.move(75, 133)
        self.soyisim.setFont(label_girdi)
        self.soyisim_girdi = QLineEdit(self)
        self.soyisim_girdi.setFont(label_text)
        self.soyisim_girdi.setGeometry(160, 130, 220, 23)
        self.soyisim_girdi.setPlaceholderText("Soyisim giriniz...")

        self.dgmtrhi = QLabel("Doğum Tarihi :", self)
        self.dgmtrhi.move(32, 173)
        self.dgmtrhi.setFont(label_girdi)
        self.dgmtrhi_girdi = QLineEdit(self)
        self.dgmtrhi_girdi.setFont(label_text)
        self.dgmtrhi_girdi.setGeometry(160, 170, 220, 23)
        self.dgmtrhi_girdi.setPlaceholderText("Soyisim giriniz...")

        self.telnumarasi = QLabel("Cep Telefonu :", self)
        self.telnumarasi.move(36, 213)
        self.telnumarasi.setFont(label_girdi)
        self.telnumarasi_girdi = QLineEdit(self)
        self.telnumarasi_girdi.setFont(label_text)
        self.telnumarasi_girdi.setGeometry(160, 210, 220, 23)
        self.telnumarasi_girdi.setPlaceholderText("Cep Telefonunuz...")

        self.email = QLabel("E-Mail :", self)
        self.email.move(500, 53)
        self.email.setFont(label_girdi)
        self.email_girdi = QLineEdit(self)
        self.email_girdi.setFont(label_text)
        self.email_girdi.setGeometry(577, 50, 220, 23)
        self.email_girdi.setPlaceholderText("E-mail adresiniz...")

        self.adres = QLabel("Adres :", self)
        self.adres.move(502, 93)
        self.adres.setFont(label_girdi)
        self.adres_girdi = QTextEdit(self)
        self.adres_girdi.setFont(label_text)
        self.adres_girdi.setGeometry(577, 90, 220, 63)

        self.ehliyet_no = QLabel("Ehliyet No :", self)
        self.ehliyet_no.move(470, 175)
        self.ehliyet_no.setFont(label_girdi)
        self.ehliyet_no_girdi = QLineEdit(self)
        self.ehliyet_no_girdi.setFont(label_text)
        self.ehliyet_no_girdi.setGeometry(577, 170, 220, 23)
        self.ehliyet_no_girdi.setPlaceholderText("Ehliyet no...")

        self.ehliyet_türü = QLabel("Ehliyet Türü :", self)
        self.ehliyet_türü.move(455, 215)
        self.ehliyet_türü.setFont(label_girdi)
        self.ehliyet_türü_sec = QComboBox(self)
        self.ehliyet_türü_sec.setFont(labelgiris)
        self.ehliyet_türü_sec.setGeometry(577, 213, 220, 23)
        self.ehliyet_türü_sec.addItems(
            ["M", "A1", "A2", "A", "B1", "B", "BE", "C1", "C1E", "C", "CE", "D1", "D1E", "D", "DE", "F", "G"])

        self.kayıt_et = QPushButton("Kaydet", self)
        self.kayıt_et.setFont(anaekran_butonlar)
        self.kayıt_et.setGeometry(90, 300, 190, 70)
        self.kayıt_et.setIcon(QtGui.QIcon("kayıtol.ico"))
        self.kayıt_et.setIconSize((QtCore.QSize(40, 40)))

        self.düzenle = QPushButton("Düzenle", self)
        self.düzenle.setFont(anaekran_butonlar)
        self.düzenle.setGeometry(320, 300, 190, 70)
        self.düzenle.setIcon(QtGui.QIcon("düzenle.ico"))
        self.düzenle.setIconSize((QtCore.QSize(40, 40)))

        self.sil = QPushButton("Sil", self)
        self.sil.setFont(anaekran_butonlar)
        self.sil.setGeometry(550, 300, 190, 70)
        self.sil.setIcon(QtGui.QIcon("sil.ico"))
        self.sil.setIconSize((QtCore.QSize(40, 40)))

    def kayitet(self):

        self.tcgirdi = self.tc_girdi.text()
        sec = self.tcgirdi
        fetch = etiket.execute("Select TC From musteri where TC = ?", (sec,))
        data = fetch.fetchall()
        self.isimgirdi = self.isim_girdi.text()
        self.soyisimgirdi = self.soyisim_girdi.text()
        self.dgmtrhigirdi = self.dgmtrhi_girdi.text()
        self.telnumarasigirdi = self.telnumarasi_girdi.text()
        self.emailgirdi = self.email_girdi.text()
        self.adresgirdi = self.adres_girdi.toPlainText()
        self.ehliyetno = self.ehliyet_no_girdi.text()
        self.ehliyet_türüsec = self.ehliyet_türü_sec.currentText()

        if len(self.tcgirdi) == 0 or len(self.isimgirdi) == 0 or len(self.soyisimgirdi) == 0 or len(
                self.dgmtrhigirdi) == 0 or len(self.telnumarasigirdi) == 0 or len(self.emailgirdi) == 0 or len(
            self.adresgirdi) == 0 or len(self.ehliyetno) == 0 or len(self.ehliyet_türüsec) == 0:
            QMessageBox.information(self, "Bilgilendirme", "Boş Bıraktığınız Alanlar Var!")

        elif len(data) != 0:
            QMessageBox.information(self, "Bilgi", "Müşteri Sistemde Mevcut Kayıt Edilemez...")
        else:
            etiket.execute("REPLACE INTO musteri VALUES (?,?,?,?,?,?,?,?,?)",
                           (self.tcgirdi, self.isimgirdi, self.soyisimgirdi, self.dgmtrhigirdi, self.telnumarasigirdi,
                            self.emailgirdi, self.adresgirdi, self.ehliyetno, self.ehliyet_türüsec))
            QMessageBox.information(self, "Bilgilendirme", "Kayıt Başarılı")
            baglanti.commit()

    def gec(self):
        self.gec2 = musteri_listele()
        self.gec2.show()

    def __init__(self):
        super().__init__()
        self.widtth = 850
        self.heigght = 450
        self.setMaximumSize(self.widtth, self.heigght)
        self.setMinimumSize(self.widtth, self.heigght)
        self.kullanici_alani()
        self.setGeometry(450, 200, 850, 450)
        self.setWindowTitle("Müşteri Ekle")
        self.kayıt_et.clicked.connect(self.kayitet)
        self.sil.clicked.connect(self.gec)
        self.düzenle.clicked.connect(self.gec)
        self.show()
class musteri_listele(QWidget):

    def listele(self):
        self.tc = QLabel("TC'den arayınız :", self)
        self.tc.setFont(label_girdi)
        self.tc.move(60, 180)
        self.tc_girdi = QLineEdit(self)
        self.tc_girdi.setGeometry(200, 177, 150, 23)
        self.tc_girdi.setPlaceholderText("TC'den arayınız...")
        self.tcden_bul = QPushButton("Bul", self)
        self.tcden_bul.setGeometry(370, 160, 150, 50)
        self.tcden_bul.setFont(anaekran_butonlar)
        self.tcden_bul.setIcon(QtGui.QIcon("ara.ico"))
        self.tcden_bul.setIconSize((QtCore.QSize(30, 30)))

        self.ehliyetnobul = QLabel("Ehliyet No'dan bul :", self)
        self.ehliyetnobul.move(40, 300)
        self.ehliyetnobul.setFont(label_girdi)
        self.ehliyetno_girdi = QLineEdit(self)
        self.ehliyetno_girdi.setGeometry(200, 297, 150, 23)
        self.ehliyetno_girdi.setPlaceholderText("TC'den arayınız...")
        self.ehliyetnodanbul = QPushButton("Bul", self)
        self.ehliyetnodanbul.setGeometry(370, 280, 150, 50)
        self.ehliyetnodanbul.setFont(anaekran_butonlar)
        self.ehliyetnodanbul.setIcon(QtGui.QIcon("ara.ico"))
        self.ehliyetnodanbul.setIconSize((QtCore.QSize(30, 30)))

        self.sonuclar = QLabel("Arama Sonuçları :", self)
        self.sonuclar.move(600, 100)
        self.sonuclar.setFont(sonuclar)

        self.arama = QListWidget(self)
        self.arama.setGeometry(600, 150, 350, 250)

        self.sil = QPushButton("Sil", self)
        self.sil.setGeometry(1000, 200, 100, 50)
        self.sil.setFont(anaekran_butonlar)
        self.sil.setIcon(QtGui.QIcon("sil.ico"))
        self.sil.setIconSize((QtCore.QSize(25, 25)))

        self.düzenle = QPushButton("Düzenle", self)
        self.düzenle.setGeometry(1000, 270, 100, 50)
        self.düzenle.setFont(anaekran_butonlar)
        self.düzenle.setIcon(QtGui.QIcon("düzenle.ico"))
        self.düzenle.setIconSize((QtCore.QSize(25, 25)))

        self.temizle = QPushButton("Ekranı Temizle", self)
        self.temizle.setGeometry(680, 425, 170, 60)
        self.temizle.setFont(anaekran_butonlar)
        self.temizle.setIcon(QtGui.QIcon("temizle.ico"))
        self.temizle.setIconSize((QtCore.QSize(30, 30)))

    def arama_yap(self):
        etiket.execute("Select * From musteri")
        for i in etiket.fetchall():
            if i[0] == self.tc_girdi.text():
                self.arama.addItem(i[1])
                QMessageBox.information(self, "Bilgi", "Kullanıcı Bulundu")

        baglanti.commit()

    def arama_yap2(self):
        etiket.execute("Select * From musteri")
        for i in etiket.fetchall():
            if i[7] == self.ehliyetno_girdi.text():
                self.arama.addItem(i[1])
                QMessageBox.information(self, "Bilgi", "Kullanıcı Bulundu")
        baglanti.commit()

    def temizlee(self):
        self.arama.clear()

    def kullanici_silme(self):
        self.cevap = QMessageBox.question(self, "Sil", "Silmek istediğinize eminmisiniz?", \
                                          QMessageBox.Yes | QMessageBox.No)
        if self.cevap == QMessageBox.Yes:
            self.secili = self.arama.selectedItems()
            self.silinecek = self.secili[0].text()
            etiket.execute("Delete FROM musteri WHERE Isim= ?", (self.silinecek,))
            baglanti.commit()

    def __init__(self):
        super().__init__()
        self.width = 1200
        self.height = 550
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.listele()
        self.arama_yap()
        self.setGeometry(350, 200, 1200, 550)
        self.tcden_bul.clicked.connect(self.arama_yap)
        self.ehliyetnodanbul.clicked.connect(self.arama_yap2)
        self.arama.itemClicked.connect(self.arama_yap)
        self.arama.itemClicked.connect(self.arama_yap2)
        self.temizle.clicked.connect(self.temizlee)
        self.sil.clicked.connect(self.kullanici_silme)
        self.show()
class arac_ekle(QWidget):

    def araclar(self):
        self.plaka = QLabel("Plaka :", self)
        self.plaka.setFont(anaekran_butonlar)
        self.plaka.move(100, 40)
        self.plaka_girdi = QLineEdit(self)
        self.plaka_girdi.setFont(label_text)
        self.plaka_girdi.setGeometry(172, 38, 200, 23)
        self.plaka_girdi.setPlaceholderText("Araç plakasını giriniz...")

        self.marka = QLabel("Marka :", self)
        self.marka.setFont(anaekran_butonlar)
        self.marka.move(93, 80)
        self.marka_girdi = QLineEdit(self)
        self.marka_girdi.setFont(label_text)
        self.marka_girdi.setGeometry(172, 78, 200, 23)
        self.marka_girdi.setPlaceholderText("Araç markasını giriniz...")

        self.model = QLabel("Model :", self)
        self.model.setFont(anaekran_butonlar)
        self.model.move(93, 120)
        self.model_girdi = QLineEdit(self)
        self.model_girdi.setFont(label_text)
        self.model_girdi.setGeometry(172, 118, 200, 23)
        self.model_girdi.setPlaceholderText("Araç modeli giriniz...")

        self.yıl = QLabel("Yıl :", self)
        self.yıl.setFont(anaekran_butonlar)
        self.yıl.move(119, 160)
        self.yıl_girdi = QLineEdit(self)
        self.yıl_girdi.setFont(label_text)
        self.yıl_girdi.setGeometry(172, 158, 200, 23)
        self.yıl_girdi.setPlaceholderText("Araç üretim yılını giriniz...")

        self.yakıt = QLabel("Yakıt :", self)
        self.yakıt.setFont(anaekran_butonlar)
        self.yakıt.move(99, 200)
        self.yakıt_sec = QComboBox(self)
        self.yakıt_sec.setFont(labelgiris)
        self.yakıt_sec.setGeometry(172, 198, 200, 23)
        self.yakıt_sec.addItems(["Dizel", "Benzin", "LPG", "Elektrik", ])

        self.motor = QLabel("Motor Gücü :", self)
        self.motor.setFont(anaekran_butonlar)
        self.motor.move(50, 240)
        self.motor_gucu_sec = QComboBox(self)
        self.motor_gucu_sec.setFont(labelgiris)
        self.motor_gucu_sec.setGeometry(172, 238, 200, 23)
        self.motor_gucu_sec.addItems(
            ["50HP'ye kada", "51-75 HP", "76-100 HP", "101-125 HP", "126-150 HP", "151-175 HP", "176-200 HP",
             "201-225 HP", "226-250 HP", "251-275 HP",
             "276-300 HP", "301-325 HP", "326-350 HP", "351-375 HP", "376-400 HP", "401-425 HP", "426-450 HP",
             "451-475 HP", "476-500 HP", "501-525 HP", "526-550 HP",
             "551-575 HP", "576-600 HP", "601 HP ve üzeri"])

        self.sonkm = QLabel("Son Km :", self)
        self.sonkm.setFont(anaekran_butonlar)
        self.sonkm.move(78, 280)
        self.sonkm_girdi = QLineEdit(self)
        self.sonkm_girdi.setFont(label_text)
        self.sonkm_girdi.setGeometry(172, 278, 200, 23)
        self.sonkm_girdi.setPlaceholderText("Araç Son kmsini giriniz...")

        self.vites = QLabel("Vites :", self)
        self.vites.setFont(anaekran_butonlar)
        self.vites.move(510, 40)
        self.vites_sec = QComboBox(self)
        self.vites_sec.setFont(labelgiris)
        self.vites_sec.setGeometry(572, 37, 200, 23)
        self.vites_sec.addItems(["Manuel", "Otomatik"])

        self.silindir = QLabel("Silindir :", self)
        self.silindir.setFont(anaekran_butonlar)
        self.silindir.move(495, 80)
        self.silindir_sec = QComboBox(self)
        self.silindir_sec.setFont(labelgiris)
        self.silindir_sec.setGeometry(572, 77, 200, 23)
        self.silindir_sec.addItems(["2", "3", "4", "5", "6", "7", "8", "12", "16"])

        self.cekis = QLabel("Çekiş :", self)
        self.cekis.setFont(anaekran_butonlar)
        self.cekis.move(505, 120)
        self.cekis_sec = QComboBox(self)
        self.cekis_sec.setFont(labelgiris)
        self.cekis_sec.setGeometry(572, 117, 200, 23)
        self.cekis_sec.addItems(["Önden Çekiş", "Arkadan Çekiş", "4WD (Sürekli)", "AWD (Elektronik)"])

        self.kasatipi = QLabel("Kasa Tipi :", self)
        self.kasatipi.setFont(anaekran_butonlar)
        self.kasatipi.move(475, 160)
        self.kasatipi_sec = QComboBox(self)
        self.kasatipi_sec.setFont(labelgiris)
        self.kasatipi_sec.setGeometry(572, 157, 200, 23)
        self.kasatipi_sec.addItems(
            ["Cabrio", "Coupe", "Hatchback ", "Sedan", "Station Wagon", "Crossover", "MPV", "Roadster"])

        self.kapı = QLabel("Kapı Sayısı :", self)
        self.kapı.setFont(anaekran_butonlar)
        self.kapı.move(463, 200)
        self.kapı_sec = QComboBox(self)
        self.kapı_sec.setFont(labelgiris)
        self.kapı_sec.setGeometry(572, 197, 200, 23)
        self.kapı_sec.addItems(["2", "4", "5 ", "5'ten fazla"])

        self.renk = QLabel("Renk :", self)
        self.renk.setFont(anaekran_butonlar)
        self.renk.move(505, 240)
        self.renk_sec = QComboBox(self)
        self.renk_sec.setFont(labelgiris)
        self.renk_sec.setGeometry(572, 237, 200, 23)
        self.renk_sec.addItems(
            ["Bej", "Beyaz", "Bordo", "Füme", "Gri", "Gümüş ", "Kahverengi", "Kırmızı", "Lacivert", "Mavi", "Mor",
             "Pembe", "Sarı", "Siyah", "Şampanya", "Turkuaz", "Turuncu", "Yeşil"])

        self.fren = QLabel("Fren Çeşitleri :", self)
        self.fren.setFont(anaekran_butonlar)
        self.fren.move(445, 280)
        self.fren_Sec = QComboBox(self)
        self.fren_Sec.setFont(labelgiris)
        self.fren_Sec.setGeometry(572, 277, 200, 23)
        self.fren_Sec.addItems(["Mekanik Frenler", "Hidrolik Frenler", "Havalı Frenler", "Elektrikli Frenler"])

        self.kayıtet = QPushButton("Kaydet", self)
        self.kayıtet.setFont(anaekran_butonlar)
        self.kayıtet.setGeometry(90, 360, 190, 70)
        self.kayıtet.setIcon(QtGui.QIcon("kayıtol.ico"))
        self.kayıtet.setIconSize((QtCore.QSize(40, 40)))

        self.düzenle = QPushButton("Düzenle", self)
        self.düzenle.setFont(anaekran_butonlar)
        self.düzenle.setGeometry(320, 360, 190, 70)
        self.düzenle.setIcon(QtGui.QIcon("düzenle.ico"))
        self.düzenle.setIconSize((QtCore.QSize(40, 40)))

        self.sil = QPushButton("Sil", self)
        self.sil.setFont(anaekran_butonlar)
        self.sil.setGeometry(550, 360, 190, 70)
        self.sil.setIcon(QtGui.QIcon("sil.ico"))
        self.sil.setIconSize((QtCore.QSize(40, 40)))

    def gec(self):
        self.gec1 = arac_listele()
        self.gec1.show()

    def kaydett(self):
        self.plakagirdi = self.plaka_girdi.text()
        sec = self.plakagirdi
        fetch = etiket.execute("Select Plaka From araclar WHERE Plaka = ?", (sec,))
        data = fetch.fetchall()
        self.markagirdi = self.marka_girdi.text()
        self.modelgirdi = self.model_girdi.text()
        self.yılgirdi = self.yıl_girdi.text()
        self.yakıtsec = self.yakıt_sec.currentText()
        self.motorgucusec = self.motor_gucu_sec.currentText()
        self.sonkmgirdi = self.sonkm_girdi.text()
        self.vitessec = self.vites_sec.currentText()
        self.silindirsec = self.silindir_sec.currentText()
        self.cekissec = self.cekis_sec.currentText()
        self.kasatipisec = self.kasatipi_sec.currentText()
        self.kapısec = self.kapı_sec.currentText()
        self.renksec = self.renk_sec.currentText()
        self.frensec = self.fren_Sec.currentText()

        if len(self.plakagirdi) == 0 or len(self.markagirdi) == 0 or len(self.modelgirdi) == 0 or len(
                self.yılgirdi) == 0 or len(self.sonkmgirdi) == 0:
            QMessageBox.information(self, "Bilgilendirme", "Boş Bıraktığınız Alanlar Var!")

        elif len(data) != 0:
            QMessageBox.information(self, "Bilgilendirme", "Bu Araç Zaten Sistemde Mevcut !")
        else:
            etiket.execute("Insert Into araclar VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (self.plakagirdi, self.markagirdi, self.modelgirdi, self.yılgirdi, self.yakıtsec,
                            self.motorgucusec, self.sonkmgirdi, self.vitessec, self.silindirsec, self.cekissec,
                            self.kasatipisec, self.kapısec, self.renksec, self.frensec))
            QMessageBox.information(self, "Bilgilendirme", "Kayıt Başarılı !")
            baglanti.commit()

    def __init__(self):
        super().__init__()
        self.araclar()
        self.setGeometry(450, 200, 850, 500)
        self.width = 850
        self.height = 500
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.sil.clicked.connect(self.gec)
        self.düzenle.clicked.connect(self.gec)
        self.kayıtet.clicked.connect(self.kaydett)
        self.show()
class arac_listele(QWidget):

    def listele(self):
        self.plaka = QLabel("Plaka'dan arayınız :", self)
        self.plaka.setFont(label_girdi)
        self.plaka.move(60, 180)
        self.plaka_girdi = QLineEdit(self)
        self.plaka_girdi.setGeometry(220, 177, 150, 23)
        self.plaka_girdi.setPlaceholderText("Plakadan arayınız...")
        self.plakadan_bul = QPushButton("Bul", self)
        self.plakadan_bul.setGeometry(390, 160, 150, 50)
        self.plakadan_bul.setFont(anaekran_butonlar)
        self.plakadan_bul.setIcon(QtGui.QIcon("ara.ico"))
        self.plakadan_bul.setIconSize((QtCore.QSize(30, 30)))

        self.markamodel = QLabel("   Marka veya Model'den" + '\n' + "                     arayınız :", self)
        self.markamodel.move(25, 300)
        self.markamodel.setFont(label_girdi)
        self.markamodel_girdi = QLineEdit(self)
        self.markamodel_girdi.setGeometry(220, 297, 150, 23)
        self.markamodel_girdi.setPlaceholderText("Marka veya Modelden arayınız...")
        self.marka_modeldenbulma = QPushButton("Bul", self)
        self.marka_modeldenbulma.setGeometry(390, 280, 150, 50)
        self.marka_modeldenbulma.setFont(anaekran_butonlar)
        self.marka_modeldenbulma.setIcon(QtGui.QIcon("ara.ico"))
        self.marka_modeldenbulma.setIconSize((QtCore.QSize(30, 30)))

        self.sonuclar = QLabel("Arama Sonuçları :", self)
        self.sonuclar.move(600, 100)
        self.sonuclar.setFont(sonuclar)

        self.arama2 = QListWidget(self)
        self.arama2.setGeometry(600, 150, 350, 250)

        self.sil = QPushButton("Sil", self)
        self.sil.setGeometry(1000, 200, 100, 50)
        self.sil.setFont(anaekran_butonlar)
        self.sil.setIcon(QtGui.QIcon("sil.ico"))
        self.sil.setIconSize((QtCore.QSize(25, 25)))

        self.düzenle = QPushButton("Düzenle", self)
        self.düzenle.setGeometry(1000, 270, 100, 50)
        self.düzenle.setFont(anaekran_butonlar)
        self.düzenle.setIcon(QtGui.QIcon("düzenle.ico"))
        self.düzenle.setIconSize((QtCore.QSize(25, 25)))

        self.temizle = QPushButton("Ekranı Temizle", self)
        self.temizle.setGeometry(680, 425, 170, 60)
        self.temizle.setFont(anaekran_butonlar)
        self.temizle.setIcon(QtGui.QIcon("temizle.ico"))
        self.temizle.setIconSize((QtCore.QSize(30, 30)))

    def temizlee(self):
        self.arama2.clear()

    def plakadan_ara(self):
        etiket.execute("Select * from araclar")
        for i in etiket.fetchall():
            if i[0] == self.plaka_girdi.text():
                self.arama2.addItem(i[0])
                QMessageBox.information(self, "Bilgi", "Araç Bulundu")
                baglanti.commit()

    def markaveyamodeldenbul(self):
        etiket.execute("Select * from araclar")
        for i in etiket.fetchall():
            if i[1] == self.markamodel_girdi.text() or i[2] == self.markamodel_girdi.text():
                self.arama2.addItem(i[0])
                QMessageBox.information(self, "Bilgi", "Araç Bulundu")
                baglanti.commit()

    def arac_sil(self):
        self.cevap = QMessageBox.question(self, "Sil", "Silmek istediğinize eminmisiniz?", \
                                          QMessageBox.Yes | QMessageBox.No)
        if self.cevap == QMessageBox.Yes:
            self.secili = self.arama2.selectedItems()
            self.silinecek = self.secili[0].text()
            etiket.execute("Delete FROM araclar WHERE Plaka= ?", (self.silinecek,))
            baglanti.commit()

    def __init__(self):
        super().__init__()
        self.listele()
        self.width = 1200
        self.height = 550
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.temizle.clicked.connect(self.temizlee)
        self.plakadan_bul.clicked.connect(self.plakadan_ara)
        self.marka_modeldenbulma.clicked.connect(self.markaveyamodeldenbul)
        self.sil.clicked.connect(self.arac_sil)
        self.show()
class kira_ekle(QWidget):

    def ekle(self):
        self.plaka = QLabel("Plaka :", self)
        self.plaka.move(40, 40)
        self.plaka.setFont(anaekran_butonlar)
        self.plaka.setStyleSheet("color:red")
        self.plaka_girdi = QLineEdit(self)
        self.plaka_girdi.setFont(label_text)
        self.plaka_girdi.setGeometry(100, 37, 200, 23)
        self.plaka_girdi.setPlaceholderText("Araç plakasını giriniz...")
        self.plaka_bul = QPushButton("Bul", self)
        self.plaka_bul.setFont(label_girdi)
        self.plaka_bul.setGeometry(320, 33, 100, 30)
        self.plaka_bul.setIcon(QtGui.QIcon("ara.ico"))
        self.plaka_bul.setIconSize((QtCore.QSize(20, 20)))

        self.arama = QListWidget(self)
        self.arama.setGeometry(80, 100, 300, 20)
        self.arama3 = QListWidget(self)
        self.arama3.setGeometry(80, 120, 300, 20)
        self.arama4 = QListWidget(self)
        self.arama4.setGeometry(80, 140, 300, 20)

        self.temizle = QPushButton("Temizle", self)
        self.temizle.setFont(label_girdi)
        self.temizle.setGeometry(390, 120, 90, 45)
        self.temizle.setIcon(QtGui.QIcon("temizle.ico"))
        self.temizle.setIconSize((QtCore.QSize(20, 20)))

        self.tc_ = QLabel("TC :", self)
        self.tc_.move(510, 40)
        self.tc_.setFont(anaekran_butonlar)
        self.tc_.setStyleSheet("color:red")
        self.tc_girdii = QLineEdit(self)
        self.tc_girdii.setFont(label_text)
        self.tc_girdii.setGeometry(570, 37, 200, 23)
        self.tc_girdii.setPlaceholderText("İsminizi giriniz...")
        self.tc_bul = QPushButton("Bul", self)
        self.tc_bul.setFont(label_girdi)
        self.tc_bul.setGeometry(790, 33, 100, 30)
        self.tc_bul.setIcon(QtGui.QIcon("ara.ico"))
        self.tc_bul.setIconSize((QtCore.QSize(20, 20)))

        self.arama2 = QListWidget(self)
        self.arama2.setGeometry(560, 100, 300, 20)
        self.arama5 = QListWidget(self)
        self.arama5.setGeometry(560, 120, 300, 20)
        self.arama6 = QListWidget(self)
        self.arama6.setGeometry(560, 140, 300, 20)

        self.temizle2 = QPushButton("Temizle", self)
        self.temizle2.setFont(label_girdi)
        self.temizle2.setGeometry(870, 120, 90, 45)
        self.temizle2.setIcon(QtGui.QIcon("temizle.ico"))
        self.temizle2.setIconSize((QtCore.QSize(20, 20)))

        self.kaydet = QPushButton("Kiralama İşlemini Kaydet", self)
        self.kaydet.setFont(anaekran_butonlar)
        self.kaydet.setIcon(QtGui.QIcon("kayıtol.ico"))
        self.kaydet.setIconSize((QtCore.QSize(40, 40)))
        self.kaydet.setGeometry(80, 355, 280, 70)

    def temizlee(self):
        self.arama.clear()
        self.plaka_girdi.clear()
        self.arama3.clear()
        self.arama4.clear()
        self.plaka2.clear()
        self.marka2.clear()
        self.model2.clear()

    def temizlee2(self):
        self.tc_girdii.clear()
        self.arama2.clear()
        self.isim2.clear()
        self.tc2.clear()
        self.soyisim2.clear()
        self.arama5.clear()
        self.arama6.clear()

    def kiraya_verildi(self):

        self.kiraya_verilen_arac = QLabel("Kiraya Verilecek", self)
        self.kiraya_verilen_arac.setFont(sonuclar)
        self.kiraya_verilen_arac.move(520, 250)
        self.kiraya_verilen_arac.setStyleSheet("color:red")

        self.tc = QLabel("Müşteri TC'si :", self)
        self.tc.setFont(label_girdi)
        self.tc.move(542, 295)

        self.tc2 = QLabel(self)
        self.tc2.setFont(label_girdi)
        self.tc2.setGeometry(649, 295, 400, 20)
        self.tc2.setStyleSheet("color:red")

        self.isim = QLabel("Müşteri İsmi :", self)
        self.isim.setFont(label_girdi)
        self.isim.move(545, 330)

        self.isim2 = QLabel(self)
        self.isim2.setFont(label_girdi)
        self.isim2.setGeometry(650, 330, 400, 20)
        self.isim2.setStyleSheet("color:red")

        self.soyisim = QLabel("Müşteri Soyismi :", self)
        self.soyisim.setFont(label_girdi)
        self.soyisim.move(521, 365)

        self.soyisim2 = QLabel(self)
        self.soyisim2.setFont(label_girdi)
        self.soyisim2.setGeometry(650, 365, 400, 20)
        self.soyisim2.setStyleSheet("color:red")

        self.plaka = QLabel("Araç Plakası :", self)
        self.plaka.setFont(label_girdi)
        self.plaka.move(546, 400)

        self.plaka2 = QLabel(self)
        self.plaka2.setFont(label_girdi)
        self.plaka2.setGeometry(650, 400, 400, 20)
        self.plaka2.setStyleSheet("color:red")

        self.marka = QLabel("Araç Modeli :", self)
        self.marka.setFont(label_girdi)
        self.marka.move(546, 435)

        self.marka2 = QLabel(self)
        self.marka2.setFont(label_girdi)
        self.marka2.setGeometry(650, 435, 400, 20)
        self.marka2.setStyleSheet("color:red")

        self.model = QLabel("Araç Markası :", self)
        self.model.setFont(label_girdi)
        self.model.move(538, 470)

        self.model2 = QLabel(self)
        self.model2.setFont(label_girdi)
        self.model2.setGeometry(650, 470, 400, 20)
        self.model2.setStyleSheet("color:red")

        self.kirayaverilen_saat = QLabel("Kiraya Verildiği Tarih ve Saat :", self)
        self.kirayaverilen_saat.setFont(label_girdi)
        self.kirayaverilen_saat.move(423, 505)

        self.kirayaverilen_saat2 = QLabel(self)
        self.kirayaverilen_saat2.setFont(label_girdi)
        self.kirayaverilen_saat2.setGeometry(650, 505, 400, 20)
        self.kirayaverilen_saat2.setStyleSheet("color:red")

        self.kac_gün_kira = QLabel("Kaç Gün Kiralanacak :", self)
        self.kac_gün_kira.setFont(anaekran_butonlar)
        self.kac_gün_kira.move(40, 250)

        self.kac_gün_kira_girdi = QLineEdit(self)
        self.kac_gün_kira_girdi.setFont(label_text)
        self.kac_gün_kira_girdi.setGeometry(215, 248, 200, 23)
        self.kac_gün_kira_girdi.setPlaceholderText("Araç kaç gün kiralancak...")

        self.odenecek = QLabel("Ödenecek Miktar :", self)
        self.odenecek.setFont(anaekran_butonlar)
        self.odenecek.move(65, 290)

        self.odenecek_label = QLabel(self)
        self.odenecek_label.setFont(sonuclar)
        self.odenecek_label.setGeometry(215, 288, 200, 23)

    def kayit_et(self):

        self.plakagirdi = self.plaka_girdi.text()
        self.arac_plaka = self.arama.currentItem()
        self.arac_marka = self.arama3.currentItem()
        self.arac_model = self.arama4.currentItem()
        self.musteri_tc = self.arama2.currentItem()
        self.musteri_isim = self.arama5.currentItem()
        self.musteri_soyisim = self.arama6.currentItem()
        self.kac_gün = self.kac_gün_kira_girdi.text()
        self.tcc_girdi = self.tc_girdii.text()

        self.kac_günnn = self.kac_gün

        sec = str(self.tcc_girdi)
        sec2 = str(self.plakagirdi)
        k = int(self.kac_gün) * 1000
        sonuc = str(k)
        self.odenecek_label.setText(sonuc)

        tc_gir_ol = str(self.tc_girdii.text())

        if len(sec) == 0 or len(sec2) == 0 or len(tc_gir_ol) == 0:
            QMessageBox.information(self,"Bilgilendirme","Boş bırakılan yerler var !")

        else:
            date_time = datetime.now()
            d = date_time.strftime("%Y-%m-%d, %H:%M:%S")
            self.kirayaverilen_saat2.setText(d)
            etiket.execute("Insert INTO kira VALUES(?,?,?,?,?,?,?,?,?)", (
                sec, self.musteri_isim.text(), self.musteri_soyisim.text(), sec2,
                self.arac_marka.text(), self.arac_model.text(), d, self.kac_gün, sonuc))
            QMessageBox.information(self, "Bilgilendirme", "Kayıt Başarılı")
            baglanti.commit()

    def arama1(self):
        self.secilecek = self.arama.selectedItems()
        self.sec = self.secilecek[0].text()
        self.fetch = etiket.execute("Select ARAC_PLAKA FROM kira WHERE ARAC_PLAKA = '%s'" % self.sec)
        for i in self.fetch.fetchall():
            if self.sec == i[0]:
                QMessageBox.information(self,"Bilgilendirme","Araç Şuan da kirada !")
                baglanti.commit()
                self.close()


    def arama22(self):
        self.secilecek2 = self.arama2.selectedItems()
        self.sec2 = self.secilecek2[0].text()
        self.fetch2 = etiket.execute("SELECT MUSTERI_TC FROM kira WHERE MUSTERI_TC = '%s'" % self.sec2)
        for i in self.fetch2.fetchall():
            if self.sec2 == i[0]:
                QMessageBox.information(self,"Bilgilendirme","Müşteride zaten bir araç var !")
                baglanti.commit()
                self.close()


    def plakadan_bul(self):
        self.sec2 = self.plaka_girdi.text()
        etiket.execute("Select * from araclar")
        for i in etiket.fetchall():
            if i[0] == self.sec2:
                self.arama.addItem(i[0])
                self.arama3.addItem(i[1])
                self.arama4.addItem(i[2])
                self.plaka2.setText(i[0])
                self.marka2.setText(i[1])
                self.model2.setText((i[2]))
                QMessageBox.information(self, "Bilgi", "Araç Bulundu !")
            baglanti.commit()

    def musteriden_bul(self):
        self.sec = self.tc_girdii.text()
        etiket.execute("Select * from musteri")
        for i in etiket.fetchall():
            if i[0] == self.sec:
                self.arama2.addItem(i[0])
                self.arama5.addItem(i[1])
                self.arama6.addItem(i[2])
                QMessageBox.information(self, "Bilgi", "Kullanıcı Bulundu !")
                self.isim2.setText(i[1])
                self.soyisim2.setText(i[2])
                self.tc2.setText(i[0])
            baglanti.commit()

    def __init__(self):
        super().__init__()
        self.ekle()
        self.width = 1000
        self.height = 650
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setGeometry(450, 200, 1000, 650)
        self.kaydet.clicked.connect(self.kayit_et)
        self.plaka_bul.clicked.connect(self.plakadan_bul)
        self.tc_bul.clicked.connect(self.musteriden_bul)
        self.temizle.clicked.connect(self.temizlee)
        self.temizle2.clicked.connect(self.temizlee2)
        self.arama.itemClicked.connect(self.arama1)
        self.arama2.itemClicked.connect(self.arama22)
        self.kiraya_verildi()
        self.show()
class kira_listele(QWidget):
    def listele(self):
        self.listele_table = QTableWidget(self)
        self.listele_table.setGeometry(100, 10, 1000, 300)
        self.listele_table.setColumnCount(9)
        self.listele_table.setRowCount(10000)
        etiket.execute("SELECT * FROM kira")
        self.listele_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Müşteri TC"))
        self.listele_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Müşteri İsim"))
        self.listele_table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Müşteri Soyisim"))
        self.listele_table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Araç Plaka"))
        self.listele_table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Araç Marka"))
        self.listele_table.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Araç Model"))
        self.listele_table.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("Kira başlama"))
        self.listele_table.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem("Kira Sonlanma"))
        self.listele_table.setHorizontalHeaderItem(8, QtWidgets.QTableWidgetItem("Ödenecek Miktar"))
        self.listele_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.listele_table.setStyleSheet("color:black")
        for satirIndex, satirveri in enumerate(etiket):
            for sutunındex, sutundata in enumerate(satirveri):
                self.listele_table.setItem(satirIndex, sutunındex, QTableWidgetItem(str(sutundata)))

        self.delete = QPushButton("Sil",self)
        self.delete.setFont(sonuclar)
        self.delete.setGeometry(350,370,200,70)
        self.delete.setIcon(QtGui.QIcon("sil.ico"))
        self.delete.setIconSize((QtCore.QSize(50, 50)))

        self.excel_ekle = QPushButton("Excele At",self)
        self.excel_ekle.setGeometry(650,370,200,70)
        self.excel_ekle.setIcon(QtGui.QIcon("excel.ico"))
        self.excel_ekle.setIconSize((QtCore.QSize(50, 50)))
        self.excel_ekle.setFont(sonuclar)

    def sil(self):
        cevap = QMessageBox.question(kira_listele(), "Kayıt Sil", "Kitabı silmek istediğinize eminmisiniz?", \
                                     QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.a = self.listele_table.selectedItems()
            self.b = self.a[0].text()
            etiket.execute("DELETE FROM kira WHERE ARAC_PLAKA = ?",(self.b,))
            baglanti.commit()

    def excel_at(self):
        sql_query = pd.read_sql_query('Select * from kira',baglanti)
        df = pd.DataFrame(sql_query)
        df.to_csv(r'C:\Users\Kaan\PycharmProjects\pythonProject1\data.csv',index= False)


    def __init__(self):
        super().__init__()
        self.listele()
        self.width = 1200
        self.height = 550
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.excel_ekle.clicked.connect(self.excel_at)
        self.delete.clicked.connect(self.sil)
        self.setGeometry(450, 200, 1200, 550)
        self.show()

uygulama = QApplication(sys.argv)
pencere = giris_pencere()
pencere.setWindowTitle("Araç Kiralama İşlemi")
sys.exit(uygulama.exec_())
