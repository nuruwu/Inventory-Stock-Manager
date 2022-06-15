import sys
from os import defpath, path
from typing import Text, ValuesView
from PyQt5.uic import loadUiType

 
import sqlite3 
db=sqlite3.connect("database.db")
cursor=db.cursor()
import sqlite3 
import sontasarim
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication,QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QHBoxLayout, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
db=sqlite3.connect("database.db")
cursor=db.cursor()    
temp = ''
dt = {}
class Main(QMainWindow, sontasarim.Ui_MainWindow):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.setWindowIcon(QtGui.QIcon("logo/logoitu.png"))
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        showq=''' SELECT * from urunler'''
        result=cursor.execute(showq)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.x = ''
        self.iterate()
        self.updateUrun()
    def iterate(self):
        column = 3
        for row in range(self.table.rowCount()):
            _item = self.table.item(row, column) 
            if _item:            
                item = self.table.item(row, column).text()
                if item == "" or item == "0":
                    self.table.item(row, column).setBackground(QtGui.QColor(255,0,0))

    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.add_btn.clicked.connect(self.ADD_DATA)
        self.delete_btn.clicked.connect(self.DELETE_DATA)
        self.update_btn.clicked.connect(self.UPDATE_DATA)
        self.search_btn.clicked.connect(self.SEARCH_DATA)
        self.ekle_buton.clicked.connect(self.ADD_DEPO)
        self.delete_depo_btn.clicked.connect(self.DELETE_DEPO)
        self.ekle_kategori_buton.clicked.connect(self.ADD_CATEGORY)
        self.sil_kategori_buton.clicked.connect(self.DELETE_CATEGORY)
        self.depo_arama.currentIndexChanged.connect(self.updateCombo)
        self.urun_arama.currentIndexChanged.connect(self.updateUrun)
        self.updateCombo(0)

    def DELETE_DEPO(self, i):
        self.show_popup_("Bir deponun silinmesi, O depoya ait ürünlerin de silinmesine sebep olur. Devam etmek istiyor musunuz ?")
        if self.x == "OK":
            index = 1
            dlt = self.depo_sil.currentText()
            index2 = self.depo_sil.findText(dlt)
            index = index + index2
            self.depo_sil.removeItem(index2)
            self.comboSecim.removeItem(index)
            self.urun_arama_depo.clear()
            self.depo.clear()
            if dlt == '':
                self.show_popup("Depo ismi boş bırakılamaz.")
                return None
            silq = "DELETE FROM depolar WHERE  depoIsmi=?"
            value = (dlt,)
            cursor.execute(silq, value)
            cursor.execute("SELECT * FROM depolar")
            depo = cursor.fetchall()
            item3 = QStandardItem("Tüm Depolar")
            for i in depo:
                item = QStandardItem(i[1])
                self.model_urun_arama_depo.appendRow(item)
                item = QStandardItem(i[1])
                self.model_depo.appendRow(item)
            dltq = "DELETE FROM urunler WHERE urunDepo=?"
            value2 = (dlt,)
            cursor.execute(dltq, value2)
            self.depo_arama.clear()
            self.urun_arama.clear()
            cursor.execute("SELECT * from depolar")
            data2 = cursor.fetchall()
            dt = {}
            dt.clear()
            for i in data2:
                urunler = []
                bosListe = []
                urunler.clear()
                dp = i[1]
                valdp = (dp,)
                cursor.execute("SELECT * from urunler WHERE urunDepo=?",valdp)
                urun = cursor.fetchall()
                for item in urun:
                    urunler.append(item[1])
                finalListe = bosListe + urunler
                dt[dp] = finalListe

            for k, v in dt.items():
                depo1 = QStandardItem(k)
                self.model_depo_arama.appendRow(depo1)
                for value in v:
                    urun = QStandardItem(value)
                    depo1.appendRow(urun)
            self.depo_arama.currentIndexChanged.connect(self.updateCombo)
            self.urun_arama.currentIndexChanged.connect(self.updateUrun)
            self.updateCombo(0)       

            ###DEPO TABLO GUNCELLE
            ####################################
            showq=''' SELECT * from depolar'''
            result=cursor.execute(showq)
            self.table_depolar.setRowCount(0)
            for row_number,row_data in enumerate(result):
                self.table_depolar.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.table_depolar.setItem(row_number,column_number, QTableWidgetItem(str(data)))
            ###URUN TABLO GUNCELLE
            ##########################################
            showq1=''' SELECT * from urunler'''
            result=cursor.execute(showq1)
            self.table.setRowCount(0)
            for row_number,row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
            self.iterate()
            #####################################               
            self.show_popup2("Depo silindi.") 
        else:
            return None
        db.commit()
    def GET_DATA(self):               
        showq=''' SELECT * from urunler'''
        result=cursor.execute(showq)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.iterate()
    def ADD_DATA(self):
        urun_Ismi= self.urun_ismi.text()
        urun_Depo= self.depo.currentText()
        urun_Adeti= self.urun_adet.text()
        urun_Birim= self.birim.currentText()
        urun_Kategori= self.kategori_ekleme.currentText()
        stokKod =self.urun_stokKod.text()
        cursor.execute("SELECT * from urunler")
        temp = cursor.fetchall()
        for i in temp:
            if i[1] == urun_Ismi:
                self.show_popup("Ürün mevcut !!")
                self.urun_ismi.setText("")
                return None
        if urun_Ismi == '':
            self.show_popup("Ürün ismi boş bırakılamaz.")
            return None
        if urun_Depo == '':
            self.show_popup("Depo ismi boş bırakılamaz.")
            return None 
        if urun_Birim == '':
            self.show_popup("Ürün birimi boş bırakılamaz.")
            return None 
        if urun_Kategori == '':
            self.show_popup("Kategori boş bırakılamaz.")
            return None 
        if stokKod == '':
            self.show_popup("Stok kodu boş bırakılamaz.")
            return None             
        select = "SELECT * from depolar WHERE depoIsmi=?"
        value = (urun_Depo,)
        cursor.execute(select, value)
        Depo = cursor.fetchall()
        for i in Depo:
            updateDepo = i[2]
            updateDepo += 1
        updateq = "UPDATE depolar SET depoUrun=? WHERE depoIsmi=?"
        vall = (updateDepo, urun_Depo,)
        insertq = "INSERT INTO urunler (stokKod,urunIsmi,urunDepo,UrunAdeti,urunBirimi,urunKategori) VALUES (?,?,?,?,?,?)"
        values=(stokKod,urun_Ismi,urun_Depo,urun_Adeti,urun_Birim,urun_Kategori,)
        cursor.execute(insertq, values)
        self.urun_ismi.setText("")
        self.urun_adet.setText("")
        self.urun_stokKod.setText("")
        cursor.execute(updateq, vall)
        ###DEPO TABLO GUNCELLE
        showq=''' SELECT * from depolar'''
        result=cursor.execute(showq)
        self.table_depolar.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table_depolar.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table_depolar.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        ##################################
        ###URUN TABLO GUNCELLE
        showq1=''' SELECT * from urunler'''
        result1=cursor.execute(showq1)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result1):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.iterate()
        ##################################
        self.depo_arama.clear()
        self.urun_arama.clear()
        cursor.execute("SELECT * from depolar")
        data2 = cursor.fetchall()
        dt = {}
        dt.clear()
        for i in data2:
            urunler = []
            bosListe = []
            urunler.clear()
            dp = i[1]
            valdp = (dp,)
            cursor.execute("SELECT * from urunler WHERE urunDepo=?",valdp)
            urun = cursor.fetchall()
            for item in urun:
                urunler.append(item[1])
            finalListe = bosListe + urunler
            dt[dp] = finalListe
        for k, v in dt.items():
            depo1 = QStandardItem(k)
            self.model_depo_arama.appendRow(depo1)
            for value in v:
                urun = QStandardItem(value)
                depo1.appendRow(urun)
         
        self.depo_arama.currentIndexChanged.connect(self.updateCombo)
        self.urun_arama.currentIndexChanged.connect(self.updateUrun)
        self.updateCombo(0)
        self.show_popup2("Ürün eklendi.")
        db.commit()
    def updateCombo(self, index):
        indx = self.model_depo_arama.index(index, 0, self.depo_arama.rootModelIndex())
        self.urun_arama.setRootModelIndex(indx)
        self.urun_arama.setCurrentIndex(0)
    def updateUrun(self):
        urun = self.urun_arama.currentText()
        vl = (urun,)
        cursor.execute("SELECT * from urunler WHERE urunIsmi=?",vl)
        data = cursor.fetchall()
        for i in data:
            self.urun_arama_stokkod.setText(str(i[0]))
            self.urun_arama_depo.setCurrentText(i[2])
            self.urun_arama_adet.setText(str(i[3]))
            self.urun_arama_birim.setCurrentText(i[4])
            self.kategori_arama.setCurrentText(i[5])   
    def DELETE_DATA(self):
        isim = self.urun_arama.currentText()
        depo = self.depo_arama.currentText()   
        index = self.urun_arama.findText(isim)
        if isim != '':          
            for item in dt.keys():
                if item == depo:
                    bosListe = []
                    liste = dt.get(item)
                    liste.remove(isim)
                    finalListe = bosListe + liste
                    dt[item] = finalListe
        else:
            self.show_popup("Lütfen ürün seçiniz.")
            return None
        dpval = (depo,)
        cursor.execute("SELECT * from depolar WHERE depoIsmi=?", dpval)
        DepoItem = cursor.fetchall()
        for i in DepoItem:
            updateDepo = i[2]
            if updateDepo == 0:
                break
            else:
                updateDepo -= 1
        updateq = "UPDATE depolar SET depoUrun=? WHERE depoIsmi=?"
        vall = (updateDepo, depo,)
        cursor.execute(updateq, vall)
        self.urun_arama.removeItem(index) 
        deleteq = "DELETE FROM urunler WHERE urunIsmi=?"
        values = (isim,)
        cursor.execute(deleteq, values)
        self.urun_arama_adet.setText("")
        self.urun_arama_stokkod.setText("")
        db.commit()
        ###
        index1 = self.depo_arama.currentIndex()
        self.depo_arama.clear()
        self.urun_arama.clear()
        cursor.execute("SELECT * from depolar")
        data2 = cursor.fetchall()
        dt.clear()
        for i in data2:
            urunler = []
            bosListe = []
            urunler.clear()
            dp = i[1]
            valdp = (dp,)
            cursor.execute("SELECT * from urunler WHERE urunDepo=?",valdp)
            urun = cursor.fetchall()
            for item in urun:
                urunler.append(item[1])
            finalListe = bosListe + urunler
            dt[dp] = finalListe
        for k, v in dt.items():
            depo1 = QStandardItem(k)
            self.model_depo_arama.appendRow(depo1)
            for value in v:
                urun = QStandardItem(value)
                depo1.appendRow(urun)
        self.depo_arama.setCurrentIndex(index1)
        #############################
        ##DEPO TABLO GUNCELLE
        showq=''' SELECT * from depolar'''
        result=cursor.execute(showq)
        self.table_depolar.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table_depolar.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table_depolar.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        ########################
        ##URUN LISTE GUNCELLE
        showq=''' SELECT * from urunler'''
        result=cursor.execute(showq)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.iterate()
        #############################
        self.show_popup2("Ürün silindi.") 
        db.commit()
        
    def ADD_DEPO(self):
        newDepo = self.depo_ekleme.text()
        ###ayni depo
        self.i = 1
        cursor.execute("SELECT * from depolar")
        depoSayisi = cursor.fetchall()
        for x in depoSayisi:
            self.i += 1
            if newDepo == x[1]:
                self.show_popup("Depo mevcut.")
                #self.depo_ekleme.setText("")
                return None

        if newDepo != '':
            no = 'D{}'.format(self.i)
            ekleDepo = "INSERT INTO depolar (depoNo,depoIsmi,depoUrun) VALUES (?,?,?)"
            degerler = (no,newDepo,0,)
            cursor.execute(ekleDepo, degerler)

            item = QStandardItem(newDepo)
            self.model.appendRow(item)
            item = QStandardItem(newDepo)
            self.model_depo.appendRow(item)
            item = QStandardItem(newDepo)
            self.model_urun_arama_depo.appendRow(item)
            item = QStandardItem(newDepo)
            self.model_depo_sil.appendRow(item)  
            self.depo_arama.clear()
            self.urun_arama.clear()
            showq=''' SELECT * from depolar'''
            result=cursor.execute(showq)
            self.table_depolar.setRowCount(0)
            for row_number,row_data in enumerate(result):
                self.table_depolar.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.table_depolar.setItem(row_number,column_number, QTableWidgetItem(str(data)))
            cursor.execute("SELECT * from depolar")
            data2 = cursor.fetchall()
            dt = {}
            dt.clear()
            for i in data2:
                urunler = []
                bosListe = []
                urunler.clear()
                dp = i[1]
                valdp = (dp,)
                cursor.execute("SELECT * from urunler WHERE urunDepo=?",valdp)
                urun = cursor.fetchall()
                for item in urun:
                    urunler.append(item[1])
                finalListe = bosListe + urunler
                dt[dp] = finalListe
            for k, v in dt.items():
                depo1 = QStandardItem(k)
                self.model_depo_arama.appendRow(depo1)
                for value in v:
                    urun = QStandardItem(value)
                    depo1.appendRow(urun)
            self.show_popup2("Depo eklendi.")
        else:
            self.show_popup("Depo ismi boş bırakılamaz")
            self.depo_ekleme.setText("")  
        self.depo_ekleme.setText('')        
        db.commit()
        #####
        
    def ADD_CATEGORY(self):
        kategori = self.kategori_ekleme5.text()
        cursor.execute("SELECT * from kategoriler")
        i = cursor.fetchall()
        for item in i:
            if item[0] == kategori:
                self.show_popup("Kategori mevcut.")
                self.kategori_ekleme5.setText("")
                return None
        if kategori != '':
            ekleKategori = "INSERT INTO kategoriler (kategoriler) VALUES (?)"
            value = (kategori,)
            cursor.execute(ekleKategori, value)
            item = QStandardItem(kategori)
            self.model_ekleme_kategori.appendRow(item)
            item = QStandardItem(kategori)
            self.model_kategori.appendRow(item)
            item = QStandardItem(kategori)
            self.model_kategori_sil.appendRow(item)
            showqK=''' SELECT * from kategoriler'''
            result2=cursor.execute(showqK)
            self.table_kategoriler.setRowCount(0)
            for row_number,row_data in enumerate(result2):
                self.table_kategoriler.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.table_kategoriler.setItem(row_number,column_number, QTableWidgetItem(str(data)))
            self.show_popup2("Kategori eklendi.")
        else:
            self.show_popup("Kategori ismi boş bırakılamaz")
            return None
        self.kategori_ekleme5.setText('')
        db.commit()
    def show_popup(self, i):
        msg = QMessageBox()
        msg.setText(i)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Bilgi kutusu")
        msg.setWindowIcon(QtGui.QIcon("logo/logoitu.png"))
        msg.setFixedSize(120, 50)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        x = msg.exec_()
    def show_popup2(self, i):
        msg = QMessageBox()
        msg.setText(i)
        msg.setWindowTitle("Bilgi kutusu")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon("logo/logoitu.png"))
        msg.setFixedSize(120, 50)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        x = msg.exec_()
    def show_popup_(self, i):
        msg = QMessageBox()
        msg.setText(i)
        msg.setWindowTitle("Bilgi kutusu")
        msg.setIcon(QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon("logo/logoitu.png"))
        msg.setFixedSize(120, 50)
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel )
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.buttonClicked.connect(self.pip)

        x = msg.exec_()

    def pip(self, i):
        self.x = i.text()

    def DELETE_CATEGORY(self):
        category = self.kategori_sil.currentText()
        index = self.kategori_sil.findText(category)
        self.kategori_sil.removeItem(index)
        self.kategori_ekleme.removeItem(index)
        self.kategori_arama.removeItem(index)
        silKategori = "DELETE FROM kategoriler WHERE kategoriler=?"
        val = (category,)
        cursor.execute(silKategori, val)

        updateq="UPDATE urunler SET urunKategori=? WHERE urunKategori=?"
        empty = ''
        values=(empty,category,)
        cursor.execute(updateq, values)
        ##################
        ###URUN TABLO GUNCELLE
        showq=''' SELECT * from urunler'''
        result=cursor.execute(showq)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.iterate()
        ##KATEGORI TABLO GUNCELLE
        ###############################
        showqK=''' SELECT * from kategoriler'''
        result2=cursor.execute(showqK)
        self.table_kategoriler.setRowCount(0)
        for row_number,row_data in enumerate(result2):
            self.table_kategoriler.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table_kategoriler.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.show_popup2("Kategori silindi.")
        db.commit()
    def UPDATE_DATA(self):
        Id = self.urun_arama.currentText()
        Par_name = self.urun_arama_depo.currentText()
        Min_area = self.urun_arama_adet.text()
        Max_area = self.urun_arama_birim.currentText()
        Nbr_of_holes = self.kategori_arama.currentText()
        stokKod = self.urun_arama_stokkod.text()
        idt = (Id,)
        if stokKod == '':
            self.show_popup("Stok kodu boş bırakılamaz.")
            return None
        elif Par_name == '':
            self.show_popup("Depo boş bırakılamaz.")
            return None
        elif Max_area == '':
            self.show_popup("Birim boş bırakılamaz.")
            return None 
        elif Nbr_of_holes == '':
            self.show_popup("Ürün ismi boş bırakılamaz.")
            return None   
        cursor.execute("SELECT * from urunler WHERE urunIsmi=?", idt)
        data = cursor.fetchall()
        for i in data:
            depo = i[2]

        if Id != '':
            if depo == Par_name:
                updateq="UPDATE urunler SET stokKod=?, urunIsmi=?,urunDepo=?,UrunAdeti=?,urunBirimi=?,urunKategori=? WHERE urunIsmi=?"
                values=(stokKod,Id,Par_name,Min_area,Max_area,Nbr_of_holes,Id,)
                cursor.execute(updateq, values)
                db.commit()
                self.urun_arama_adet.setText("")
                self.urun_arama_stokkod.setText("")



                self.show_popup2("Ürün güncellendi.")
            else:
                updateq="UPDATE urunler SET stokKod=?, urunIsmi=?,urunDepo=?,UrunAdeti=?,urunBirimi=?,urunKategori=? WHERE urunIsmi=?"
                values=(stokKod,Id,Par_name,Min_area,Max_area,Nbr_of_holes,Id,)
                cursor.execute(updateq, values)
                oldDepo = (depo,)
                cursor.execute("SELECT * from depolar WHERE depoIsmi=?",oldDepo)
                depodata = cursor.fetchone()
                urunSayi = depodata[2]
                urunSayi -= 1
                updatedepo = "UPDATE depolar SET depoUrun=? WHERE depoIsmi=?"
                degerler = (urunSayi,depo,)
                cursor.execute(updatedepo, degerler)
                newDepo = (Par_name,)
                cursor.execute("SELECT * from depolar WHERE depoIsmi=?",newDepo)
                depodata2 = cursor.fetchone()
                urunSayi2 = depodata2[2]
                urunSayi2 += 1
                updatedepo2 = "UPDATE depolar SET depoUrun=? WHERE depoIsmi=?"
                degerler2 = (urunSayi2,Par_name,)
                cursor.execute(updatedepo2, degerler2)
                self.show_popup2("Ürün güncelledi.")
                #############################
                ############################
        else:
            self.show_popup("Lütfen ürün seçiniz. ")
            self.urun_arama_adet.setText("")
            self.urun_arama_birim.setText("")
            self.urun_arama_stokkod.setText("")
            return None

        index1 = self.depo_arama.currentIndex()
        index2 = self.urun_arama.currentIndex()
        self.depo_arama.clear()
        self.urun_arama.clear()
        cursor.execute("SELECT * from depolar")
        data2 = cursor.fetchall()
        dt = {}
        dt.clear()
        for i in data2:
            urunler = []
            bosListe = []
            urunler.clear()
            dp = i[1]
            valdp = (dp,)
            cursor.execute("SELECT * from urunler WHERE urunDepo=?",valdp)
            urun = cursor.fetchall()
            for item in urun:
                urunler.append(item[1])
            finalListe = bosListe + urunler
            dt[dp] = finalListe
        for k, v in dt.items():
            depo1 = QStandardItem(k)
            self.model_depo_arama.appendRow(depo1)
            for value in v:
                urun = QStandardItem(value)
                depo1.appendRow(urun)
        self.depo_arama.setCurrentIndex(index1)
        self.urun_arama.setCurrentIndex(index2)
            ################################
            #############################
            ##DEPO TABLO GUNCELLE
        showq=''' SELECT * from depolar'''
        result=cursor.execute(showq)
        self.table_depolar.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table_depolar.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table_depolar.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        ########################
        ##URUN LISTE GUNCELLE
        showq=''' SELECT * from urunler'''
        result=cursor.execute(showq)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.iterate()
        #############################
        db.commit()
    def SEARCH_DATA(self):
        depo_no = self.comboSecim.currentText()
        showq=''' SELECT * from urunler WHERE urunDepo = ?'''
        values=(depo_no,)
        cursor.execute(showq,values)
        c = cursor.fetchall()
        self.table.setRowCount(0)
        y = 0
        result = {} 
        secim = self.comboBox_4.currentText()
        text = self.secim.text()
        #if text == str():
            #pass
        #elif text == int():
        if depo_no == "Tüm depolar":
            if secim == "Tüm Kriterler":
                if text == "":
                    showq='''SELECT * from urunler'''
                    result=cursor.execute(showq)
                    self.table.setRowCount(0)
                    for row_number,row_data in enumerate(result):
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    self.iterate()
                else:
                    showq=''' SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        for item in i:
                            if str(item) == text:
                                result[y] = i
                                y += 1
                                break 
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    result.clear()
            elif secim == "Kategori":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq='''SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        if i[5] == text:
                            result[y] = i
                            y += 1

                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    self.iterate()
                    result.clear()
            elif secim == "Stok Kod":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[0]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Adı":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[1]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Adeti":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        if text == str(i[3]):
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Birimi":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler'''
                    cursor.execute(showq)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[4]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
        else:    
            if secim == "Tüm Kriterler":
                if text == "":
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    result=cursor.execute(showq, values)
                    self.table.setRowCount(0)
                    for row_number,row_data in enumerate(result):
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    self.iterate()
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        for item in i:
                            if str(item) == text:
                                result[y] = i
                                y += 1
                                break
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    result.clear()
                    y = 0
            elif secim == "Kategori":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        if i[5] == text:
                            result[y] = i
                            y += 1
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    self.iterate()
                    result.clear()
                    y = 0
            elif secim == "Stok Kod":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[0]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                    y = 0
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Adı":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[1]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Adeti":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        if text == str(i[3]):
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
            elif secim == "Ürün Birimi":
                if text == "":
                    self.show_popup("Arama kriteri bos birakilamaz.")
                    return None
                else:
                    showq=''' SELECT * from urunler WHERE urunDepo = ?'''
                    values=(depo_no,)
                    cursor.execute(showq,values)
                    c = cursor.fetchall()
                    for i in c:
                        if text == i[4]:
                            result[y] = i
                            y += 1
                        else:
                            continue
                    for row_number, row_data in result.items():
                        self.table.insertRow(row_number)
                        for column_number,data in enumerate(row_data):
                            self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                            self.iterate()
                    self.iterate()
                    result.clear()
        db.commit()
def main():
     app=QApplication(sys.argv)
     window=Main()
     window.show()
     app.exec()
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())

    