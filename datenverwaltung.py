    # -*- coding: utf-8 -*-
# imports
import cv2
import shutil
import sqlite3
import datetime
import webbrowser
import sys,  os,  csv
import mysql.connector 
from Ui_datenverwaltung import Ui_HAUPTFENSTER
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTranslator
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtPrintSupport import QPrinter,  QPrintDialog

class HAUPTFENSTER(QMainWindow, Ui_HAUPTFENSTER):
    """
    Hauptfenster.
    """
    def __init__(self, parent=None):
        """
        Hauptfunktion das die alle anderen funktionen abruft, wenn benötigt.
        """
        super(HAUPTFENSTER, self).__init__(parent)
        self.setupUi(self)
        self.DB_verbinden()
        self.dialoge_vorbelegen()
        self.tabelle_anzeigen()
        self.voreinstellungen()
        self.add_listwidget_titles()
        # inserting window logo
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        # inserting the logo
        LOGO = QLabel(self)
        LOGO = QPixmap('logo.png')
        self.LOGO.setPixmap(LOGO)
        # set translation
        self.translator = QTranslator()
        self.translator.load("i18n/datenverwaltung_en.qm")
        app.installTranslator(self.translator)
    def dialoge_vorbelegen(self):
        """
        Belegt die Comboboxen mit einem Inhalt aus der Datenbank vor.
        """
        # länder and LKZ get preassgned to the combo box and the empty input field
        mycursor = mydb.cursor()
        mycursor.execute("SELECT länder.LAND,länder.LKZ FROM LÄNDER")
        werte = [] # create empty list
        for i in mycursor:
            werte.append(i) # [0] entfernt die geschwungenen Klammern
    ### self.LAND.addItems (werte) # Werte aus Liste in Combobox übernehmen
        mycursor = mydb.cursor()
        mycursor.execute("SELECT titel.TITEL FROM TITEL")
        werte = [] # create empty list
        for i in mycursor:
            werte.append(i) # removes the brackets
    ### self.LAND.addItems (werte) # Werte aus Liste in Combobox übernehmen
        for item in werte:
            self.TITEL1.addItem(item[0])
            self.TITEL2.addItem(item[0])
            self.TITEL3.addItem(item[0])
        mycursor.close
        # creates tooltips for buttons
#        self.PRINT.setToolTip('Druckt die aktuelle CSV-Esxport Datei aus.')  
        # import flag icons for language combo box
        self.SPRACHE_BOX.addItem(QIcon('icons/flags/translate.png'),'Language')
        self.SPRACHE_BOX.addItem(QIcon('icons/flags/FLGGERM.ico'),'Deutsch')
        self.SPRACHE_BOX.addItem(QIcon('icons/flags/FLGUK.ico'),'Englisch')
        #self.SPRACHE_BOX.addItem(QIcon('icons/flags/FLGFRAN.ico'),'Französisch')
        #self.SPRACHE_BOX.addItem(QIcon('icons/flags/flgitaly.ico'),'Italienisch')
        # import flag icons for combo box länder
        self.LKZ_BOX.setText(self.LAND_BOX.itemData(self.LAND_BOX.currentIndex()))
        self.LAND_BOX.addItem(QIcon('icons/flags/flgausta.ico'),'Austria')
        self.LAND_BOX.addItem(QIcon('icons/flags/flggerm.ico'),'Deutschland')
        self.LAND_BOX.addItem(QIcon('icons/flags/flguk.ico'),'England')
        self.LAND_BOX.addItem(QIcon('icons/flags/flgitaly.ico'),'Italien')
        self.LAND_BOX.addItem(QIcon('icons/flags/flgswitz.ico'),'Schweiz')
        # import icon flags für ländervorwahl 1
        self.VORWAHL1.setCurrentText(self.LAND_BOX.itemData(self.LAND_BOX.currentIndex()))
        self.VORWAHL1.addItem(QIcon(''),'')
        self.VORWAHL1.addItem(QIcon('icons/flags/flgausta.ico'),'+43')
        # import icon flags für ländervorwahl 2
#        self.VORWAHL2.CurrentIndext(self.LAND_BOX.itemData(self.LAND_BOX.currentIndex()))
        self.VORWAHL2.addItem(QIcon(''),'')
        self.VORWAHL2.addItem(QIcon('icons/flags/flgausta.ico'),'+43')
        # startseite icons
        self.SAVE.setIcon(QtGui.QIcon('icons\\buttons\\save.png'))
        self.NEW_ENTRY.setIcon(QtGui.QIcon('icons\\buttons\\new.ico'))
        self.REFRESH.setIcon(QtGui.QIcon('icons\\buttons\\refresh.ico')) 
        self.EXIT.setIcon(QtGui.QIcon('icons\\buttons\\off.png'))
        self.PRINT.setIcon(QtGui.QIcon('icons\\buttons\\printer.png'))
        # camera icons
        self.NEW_PICTURE.setIcon(QtGui.QIcon('icons\\buttons\\new.ico'))
        self.SAVE_PICTURE.setIcon(QtGui.QIcon('icons\\buttons\\save.png'))
        self.DELETE_PICTURE.setIcon(QtGui.QIcon('icons\\buttons\\delete.png'))
        self.UPLOAD.setIcon(QtGui.QIcon('icons\\buttons\\upload.png'))
        # settings icons
        self.TOGGLE_DARK_MODE.setIcon(QtGui.QIcon('icons\\buttons\\darkmode.png'))
        self.HELP.setIcon(QtGui.QIcon('icons\\buttons\\help.png'))
        self.MAPS.setIcon(QtGui.QIcon('icons\\buttons\\map.png'))
        # support icons 
        self.EMAIL_SUPPORT.setIcon(QtGui.QIcon('icons\\buttons\\mail.png'))
        self.PHONE_SUPPORT.setIcon(QtGui.QIcon('icons\\buttons\\phone.png'))
        # datenbanktabellen tab icons 
        self.DELETE.setIcon(QtGui.QIcon('icons\\buttons\\delete.png'))
        self.EMAIL_CREATE.setIcon(QtGui.QIcon('icons\\buttons\\mail.png'))
        self.SEARCH.setIcon(QtGui.QIcon('icons\\buttons\\search.png'))
        self.CSV.setIcon(QtGui.QIcon('icons\\buttons\\export.png'))
        self.REPORT.setIcon(QtGui.QIcon('icons\\buttons\\report.png'))
        self.REPORT_ALL.setIcon(QtGui.QIcon('icons\\buttons\\all.png'))
    def INFO(self,  MELDUNG,  INFO_STAT): # central output for messages save or error
        """
        Verwendet ein Label um dort Meldungen, Hinweise und korrekt ausgeführte funktionen anzuzeigen.
        """
        self.lab_INFO.setText(MELDUNG)  # take text from MELDUNG and output
        if INFO_STAT == "F":  # error
            self.lab_INFO.setStyleSheet("QLabel { background-color : rgb(255,0,0) }")
            res = QMessageBox.critical(
                self,
                self.tr("Fehler"),
                MELDUNG,
                QMessageBox.StandardButtons(QMessageBox.Ok)
            )
            print(res)
        elif INFO_STAT == "H":  # hints
            self.lab_INFO.setStyleSheet("QLabel { background-color : rgb(255,197,20) }")
            res = QMessageBox.information(
                self,
                self.tr("Information"),
                MELDUNG,
                QMessageBox.StandardButtons(QMessageBox.Ok)
            )
        else:
            self.lab_INFO.setStyleSheet("QLabel { background-color : rgb(85,170,127) }")
    def tabelle_anzeigen(self):
        """
        Belegt die Titel von dem Table Widget und verbindet sich mit der Datenbank und füllt die Einträge in das Widget.
        """
        self.DB_verbinden() # calls the function to connect to the database
        # titles in the table widget for the data from the database
        self.Daten_Tabelle.setColumnCount(24)
        colname = QTableWidgetItem ("ID")
        self.Daten_Tabelle.setHorizontalHeaderItem(0, colname)
        colname = QTableWidgetItem ("Firma")
        self.Daten_Tabelle.setHorizontalHeaderItem(1, colname)
        colname = QTableWidgetItem ("Nachname")
        self.Daten_Tabelle.setHorizontalHeaderItem(2, colname)
        colname = QTableWidgetItem ("Vornamen")
        self.Daten_Tabelle.setHorizontalHeaderItem(3, colname)
        colname = QTableWidgetItem ("Titel 1")
        self.Daten_Tabelle.setHorizontalHeaderItem(4, colname)
        colname = QTableWidgetItem ("Titel 2")
        self.Daten_Tabelle.setHorizontalHeaderItem(5, colname)
        colname = QTableWidgetItem ("Titel 3")
        self.Daten_Tabelle.setHorizontalHeaderItem(6, colname)
        colname = QTableWidgetItem ("Land")
        self.Daten_Tabelle.setHorizontalHeaderItem(7, colname)
        colname = QTableWidgetItem ("LKZ")
        self.Daten_Tabelle.setHorizontalHeaderItem(8, colname)
        colname = QTableWidgetItem ("Strasse")
        self.Daten_Tabelle.setHorizontalHeaderItem(9, colname)
        colname = QTableWidgetItem ("Haus Nr.")
        self.Daten_Tabelle.setHorizontalHeaderItem(10, colname)
        colname = QTableWidgetItem ("PLZ")
        self.Daten_Tabelle.setHorizontalHeaderItem(11, colname)
        colname = QTableWidgetItem ("Ort")
        self.Daten_Tabelle.setHorizontalHeaderItem(12, colname)
        colname = QTableWidgetItem ("Mobil Nr.")
        self.Daten_Tabelle.setHorizontalHeaderItem(13, colname)
        colname = QTableWidgetItem ("Business Nr.")
        self.Daten_Tabelle.setHorizontalHeaderItem(14, colname)
        colname = QTableWidgetItem ("Email")
        self.Daten_Tabelle.setHorizontalHeaderItem(15, colname)
        colname = QTableWidgetItem ("Schein")
        self.Daten_Tabelle.setHorizontalHeaderItem(16, colname)
        colname = QTableWidgetItem ("Art")
        self.Daten_Tabelle.setHorizontalHeaderItem(17, colname)
        colname = QTableWidgetItem ("Kinder")
        self.Daten_Tabelle.setHorizontalHeaderItem(18, colname)
        colname = QTableWidgetItem ("Geburtsdatum")
        self.Daten_Tabelle.setHorizontalHeaderItem(19, colname)
        colname = QTableWidgetItem ("SVNR")
        self.Daten_Tabelle.setHorizontalHeaderItem(20, colname)
        colname = QTableWidgetItem ("Karte Nr.")
        self.Daten_Tabelle.setHorizontalHeaderItem(21, colname)
        colname = QTableWidgetItem ("Personal Nr.")
        self.Daten_Tabelle.setHorizontalHeaderItem(22, colname)
        colname = QTableWidgetItem ("Änderungsdatum")
        self.Daten_Tabelle.setHorizontalHeaderItem(23, colname)
        self.Daten_Tabelle.setRowCount(1)
        # connect to database and fetch the values 
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM adressenverwaltung")
        zeile = 0
        for z in mycursor:  # read rows and output
            self.Daten_Tabelle.setRowCount(zeile + 1)
            for s in range(0, 24):  # reads row and column
                self.Daten_Tabelle.setRowCount(zeile + 1)
                header_label = self.Daten_Tabelle.horizontalHeaderItem(s).text()
                if header_label == "Schein":  # Check if it's the 'Schein' column
                    fielditem = QTableWidgetItem("")
                    self.Daten_Tabelle.setItem(zeile, s, fielditem)
                    fielditem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if str(z[s]) == "1":  # Ja
                        fielditem.setCheckState(Qt.Checked)  # checked
                    else:
                        fielditem.setCheckState(Qt.Unchecked)  # not checked
                else:  # fills the rest
                    fielditem = QTableWidgetItem(str(z[s]))
                    self.Daten_Tabelle.setItem(zeile, s, fielditem)
            zeile += 1
        mycursor.close()
        self.Daten_Tabelle.resizeColumnsToContents() # resize columns to contents
        self.Daten_Tabelle.resizeRowsToContents() # resize rows to contents
        self.INFO("Alle Daten werden in der Tabelle angezeigt und aktualisiert.",  "I")
    def set_dark_mode(self, enable):
        """
        Setzt den Darkmode in der Datenbank.
        """
        mycursor = mydb.cursor()
        try:
            sql_select = "SELECT * FROM voreinstellungen"
            mycursor.execute(sql_select)
            settings = mycursor.fetchone()
            if settings is None:
                # if nothing was found create new entry
                sql_insert = "INSERT INTO voreinstellungen (DARKMODE) VALUES (%s)"
                val_insert = (1 if enable else 0,)
                mycursor.execute(sql_insert, val_insert)
            else:
                # if entry was found update the entry
                sql_update = "UPDATE voreinstellungen SET DARKMODE=%s"
                val_update = (1 if enable else 0,)
                mycursor.execute(sql_update, val_update)
            mydb.commit()
        except Exception as e:
            print(e)
            mydb.rollback()
            self.INFO("Fehler bei der Aktualisierung der Einstellungen!", "F")
        finally:
            mycursor.close()
        if enable:
        # Dark mode color settings inspired by Instagram
            self.setStyleSheet("""
            QMainWindow {
                background-color: #000;
                color: #fff;
            }
            QLabel {
                color: #fff;
                color: #fff;
            }
            QComboBox, QLineEdit, QSpinBox, QCheckBox, QRadioButton {
                background-color: #191919;
                color: #fff;
                border: 1px solid #333;
                selection-background-color: #3f729b;
                padding: 5px;
            }
            QComboBox::drop-down {
                background-color: #191919;
            }
            QComboBox::down-arrow {
                image: url('icons/arrow-down.png');
                width: 12px;
                height: 12px;
            }
            QPushButton {
                background-color: #191919;
                color: #fff;
                border: 1px solid #333;
                padding: 8px;
            }
            QTabWidget::pane {
                border: 1px solid #333;
                background-color: #191919;
            }
            QTabBar::tab {
                background-color: #191919;
                color: #fff;
                border: 1px solid #333;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background-color: #3f729b;
            }
            QTableWidget {
                background-color: #191919;
                color: #fff;
                border: 1px solid #333;
                alternate-background-color: #222;
            }
            QHeaderView::section {
                background-color: #191919;
                color: #fff;
                border: 1px solid #333;
            }
            QGroupBox {
                color: #fff;
                border: 1px solid #333;
                padding-top: 20px; 
                margin-top: 10px; 
            }
            QScrollBar:horizontal {
                border: none;
                background: #333;
                height: 8px;
                margin: 0px 21px 0 21px;
            }
            QScrollBar::handle:horizontal {
                background: #3f729b;
                min-width: 25px;
            }
            QScrollBar::add-line:horizontal {
                background: #333;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                background: #333;
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar:vertical {
                border: none;
                background: #333;
                width: 8px;
                margin: 21px 0 21px 0;
            }
            QScrollBar::handle:vertical {
                background: #3f729b;
                min-height: 25px;
            }
            QScrollBar::add-line:vertical {
                background: #333;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #333;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        else:
            self.setStyleSheet("") # light mode
    def DB_verbinden(self): # connects with database
       DB_String = {
           'host' : 'localhost',
           'user' : 'root', 
           'password' : '',  
           'database' : 'daten_verwaltung'
           }
       global mydb
       try: # sql-connection
           mydb = mysql.connector.connect(**DB_String)
       except: # error message
           self.INFO("Es konnte keine Verbindung zur Server-Datenbank hergestellt werden!",  "F")
           exit(0)
    @pyqtSlot()
    def on_SAVE_clicked(self):
        """
        Wenn der Speichern Button gedrückt wird werden neue Werte eingetragen und die alten geupdated.
        """
        # check for required fields
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        mycursor = mydb.cursor()
        sql_select = "SELECT * FROM adressenverwaltung WHERE FIRMEN_NAME = '" + self.FIRMA_BOX.text() + "' AND NACHNAME = '" + self.NACHNAME_BOX.text() + "' AND VORNAMEN = '" + self.VORNAME_BOX.text() + "'"
        mycursor.execute(sql_select)
        sql_satz = mycursor.fetchall()
        satz_len = len(sql_satz)
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
        entry_id =  mycursor.lastrowid
        if satz_len == 0:
            # creates a new entry in the database
            sql_insert = "INSERT INTO adressenverwaltung (FIRMEN_NAME, NACHNAME, VORNAMEN, TITEL_1, TITEL_2, TITEL_3, LAND, LKZ, STRASSE, HAUS_NR, PLZ, ORT, MOBIL_NR, BUSINESS_NR, EMAIL, SCHEIN, ART, KINDER, GEBURTSDATUM, SVNR, KARTE_NR, PERSO_NR, DATETIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            Geburtsdatum = self.BDAY_BOX.text()
            d, m, y = str(Geburtsdatum)[0:2], str(Geburtsdatum)[3:5], str(Geburtsdatum)[6:10]
            Geburtsdatum = y + "-" + m + "-" + d
            
            val_insert = (
                self.FIRMA_BOX.text(), self.NACHNAME_BOX.text(), self.VORNAME_BOX.text(),
                self.TITEL1.currentText(), self.TITEL2.currentText(), self.TITEL3.currentText(),
                self.LAND_BOX.currentText(), self.LKZ_BOX.text(),
                self.STRASSE_BOX.text(), self.HAUSNR_BOX.text(), self.PLZ_BOX.text(),
                self.ORT_BOX.text(), self.MOBIL.text(), self.BUSINESS_NR.text(),
                self.EMAIL_BOX.text(), self.SCHEIN_BOX.isChecked(), self.SCHEIN_ART.currentText(),
                self.KINDER_BOX.value(), str(Geburtsdatum), self.SVNR_BOX.text(), self.KARTE_BOX.text(), self.PERSO_BOX.text(),
                now  # Include the current datetime in the insert query
            )
            
            try:
                mycursor.execute(sql_insert, val_insert)
                mydb.commit()
                self.INFO("Erfolgreich gespeichert!", "")

                # Holen der automatisch generierten ID des eingefügten Datensatzes
                entry_id = mycursor.lastrowid

                # Logging changes after successful insertion
                self.log_changes(entry_id, val_insert, now)
                self.display_changes(entry_id)

            except Exception as e:
                print(e)
                mydb.rollback()
                self.INFO("Fehler beim Speichern des Datensatzes!", "F")
        else:
            # updates the entry that already exists
            Geburtsdatum = self.BDAY_BOX.text()
            d, m, y = str(Geburtsdatum)[0:2], str(Geburtsdatum)[3:5], str(Geburtsdatum)[6:10]
            Geburtsdatum = y + "-" + m + "-" + d
            
            sql_update = "UPDATE adressenverwaltung SET TITEL_1=%s, TITEL_2=%s, TITEL_3=%s, LAND=%s, LKZ=%s, STRASSE=%s, HAUS_NR=%s, PLZ=%s, ORT=%s, MOBIL_NR=%s, BUSINESS_NR=%s, EMAIL=%s, SCHEIN=%s, ART=%s, KINDER=%s, GEBURTSDATUM=%s, SVNR=%s, KARTE_NR=%s, PERSO_NR=%s, DATETIME=%s WHERE FIRMEN_NAME = %s AND NACHNAME = %s AND VORNAMEN = %s"
            
            val_update = (
                self.TITEL1.currentText(), self.TITEL2.currentText(), self.TITEL3.currentText(),
                self.LAND_BOX.currentText(), self.LKZ_BOX.text(),
                self.STRASSE_BOX.text(), self.HAUSNR_BOX.text(), self.PLZ_BOX.text(),
                self.ORT_BOX.text(), self.MOBIL.text(), self.BUSINESS_NR.text(),
                self.EMAIL_BOX.text(), self.SCHEIN_BOX.isChecked(), self.SCHEIN_ART.currentText(),
                self.KINDER_BOX.value(),
                str(Geburtsdatum), self.SVNR_BOX.text(), self.KARTE_BOX.text(), self.PERSO_BOX.text(),
                now,  # Include the current datetime in the update query
                self.FIRMA_BOX.text(), self.NACHNAME_BOX.text(), self.VORNAME_BOX.text()
            )

            try:
                mycursor.execute(sql_update, val_update)
                mydb.commit()

                # Logging changes after successful update
                self.log_changes(entry_id, val_update, now)

                # Hier die Spaltenüberschriften hinzufügen, bevor die Änderungen angezeigt werden
                self.add_listwidget_titles()

                # Jetzt die Änderungen anzeigen
                self.display_changes(entry_id)

                self.INFO("Erfolgreich aktualisiert!", "")

                # Logging changes after successful update
                self.log_changes(entry_id, val_update, now)
                self.display_changes(entry_id)

            except Exception as e:
                print(e)
                mydb.rollback()
                self.INFO("Fehler beim Aktualisieren des Datensatzes!", "F")
    # Function to log changes
    def log_changes(self, entry_id, new_values, change_time):
        mycursor = mydb.cursor()
        changelog_query = "INSERT INTO changelog_table (entry_id, field_changed, old_value, new_value, change_time) VALUES (%s, %s, %s, %s, %s)"
        
        # Fetch old values before the update
        sql_select_old_values = "SELECT * FROM adressenverwaltung WHERE ID = %s"
        mycursor.execute(sql_select_old_values, (entry_id,))
        old_values = mycursor.fetchone()

        if old_values is not None:
            field_names = [
                "FIRMEN_NAME", "NACHNAME", "VORNAMEN", "TITEL_1", "TITEL_2", "TITEL_3", 
                "LAND", "LKZ", "STRASSE", "HAUS_NR", "PLZ", "ORT", "MOBIL_NR", "BUSINESS_NR", 
                "EMAIL", "SCHEIN", "ART", "KINDER", "GEBURTSDATUM", "SVNR", "KARTE_NR", "PERSO_NR"
            ]

            # Pair the field names with their corresponding new and old values for logging
            changes_to_log = [
                (entry_id, field_name, str(old_values[index]), str(new_values[index]), change_time) 
                for index, field_name in enumerate(field_names)
            ]

            try:
                mycursor.executemany(changelog_query, changes_to_log)
                mydb.commit()
            except Exception as e:
                print(e)
                mydb.rollback()
        else:
            print("No data found for the provided entry_id.")


        # Function to fetch and display changes
    def display_changes(self, entry_id):
        mycursor = mydb.cursor()
        sql_select = "SELECT * FROM changelog_table WHERE entry_id = %s ORDER BY change_time DESC"
        mycursor.execute(sql_select, (entry_id,))
        changes = mycursor.fetchall()

        self.CHANGES.clear()  # Clear previous items in the list widget

        for change in changes:
            change_info = f"{change['field_changed']}: {change['old_value']} -> {change['new_value']}"
            item = QListWidgetItem(change_info)
            self.CHANGES.addItem(item)
    def add_listwidget_titles(self):
        titles = ["Field Changed", "Old Value", "New Value"]  # Titel für die Spalten

        # Clear the list widget before adding new titles
        self.CHANGES.clear()

        for title in titles:
            item = QListWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)  # Zentrieren des Texts
            item.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))  # Ändern der Schriftart
            item.setText(title)
            self.CHANGES.addItem(item)
    def is_required_fields_filled(self):
        """
        Überprüft ob mindestens die Pflichtfelder ausgefüllt sind.
        """
        # check for required fields
        required_fields = [self.NACHNAME_BOX, self.VORNAME_BOX]
        for field in required_fields:
            if field.text().strip() == '':
                return False
        return True


    @pyqtSlot()
    def on_EXIT_clicked(self):
        """
        Wenn der Exit Button gedrückt wird, schließt sich die Maske.
        """
        # TODO: not implemented yet
        self.close()
    @pyqtSlot(str)
    def on_LAND_BOX_currentTextChanged(self, p0):
        """
        Wenn sich in der Länderbox das Land ändert wird im LKZ auch das LKZ entsprechend dem Land geändert.
        """
        mycursor = mydb.cursor()
        sql_satz = [] # initialization for the query
        sql = 'SELECT LKZ FROM länder WHERE LAND = "'+ self.LAND_BOX.currentText() + '"'
        mycursor.execute(sql)
        sql_satz = mycursor.fetchall()
        satz_len = len(sql_satz)
        if satz_len == 0: # if 0 = no entry was found
            self.LKZ_BOX.setText('?')
            self.INFO("Es konnte kein Eintrag für in Länder-DB gefunden werden!", "F")
        else: 
            self.LKZ_BOX.setText(sql_satz[0][0])
            self.INFO("Länder-KZ wird angezeigt.", "I")
    @pyqtSlot()
    def on_REFRESH_clicked(self):
        """
        Aktualisiert das Table Widget falls Einträge von einem anderen Standort vorgenommen wurden.
        """
        self.tabelle_anzeigen()
    @pyqtSlot()
    def on_NEW_PICTURE_clicked(self):
        """
        Erstellt ein Bild, speichert dieses ab und zeigt es im Label an.
        """
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        self.NEW_PICTURE.setEnabled(False)
        res = QMessageBox.information(
            self, 
            self.tr("FOTO"), 
            self.tr("""Bitte gerade in die Kamera schauen und Ok-Button anklicken.
        Drücken Sie 'S' zum Speichern oder 'X' um abzubrechen"""), 
            QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))
        if res == QMessageBox.Ok:  # when ok was pressed
            FOTO = self.NACHNAME_BOX.text() + self.VORNAME_BOX.text() + ".jpg" 
            cam = cv2.VideoCapture(0)  # 0 index of the camera
            img = cam.read()
            PFAD = 'pictures/'  # path where the picture is saved
            camera = cv2.VideoCapture(0)
            while True:
                return_value, image = camera.read()
                img = (image)
                cv2.imshow('image', img)
                if cv2.waitKey(1) & 0xFF == ord('s'):  # when the user presses 's' the pictures is saved and displayed
                    try:
                        res = QMessageBox.information(
                            self, 
                            self.tr("GESICHERT"), 
                            self.tr("""Ihr Bild wurde gespeichert."""))
                        self.INFO("Bild wurde gespeichert / gesichert", "I")
                        self.FOTO_delete()  # check for picture and delete old one
                        cv2.imwrite(os.path.join(PFAD, FOTO), img)
                    except:
                        print("kein Bild")
                        cv2.imwrite(os.path.join(PFAD, FOTO), img)
                    break
                if cv2.waitKey(2) & 0xFF == ord('x'):  # when the user presses x the window closes and no picture is saved
                    camera.release()
                    cv2.destroyAllWindows()
                    self.INFO("Es wurde kein Foto erstellt", "H")
                    break
            camera.release()
            cv2.destroyAllWindows()
        self.NEW_PICTURE.setEnabled(True)
        # show the picture in the label
        PICTURE_NAME = self.NACHNAME_BOX.text() + self.VORNAME_BOX.text() + ".jpg"
        PFAD = 'pictures/'
        try:
            FOTO_DATEI = PFAD + '/'+ PICTURE_NAME
            FOTO_SHOW = QPixmap(FOTO_DATEI)
            self.FOTO.setPixmap(FOTO_SHOW)
        except:
            print("auweh")
    @pyqtSlot(int, int)
    def on_Daten_Tabelle_cellClicked(self, row, column):
        """
        Daten aus der Datenbank auslesen und anzeigen lassen.
        """
        # show entrys from the database
        self.FIRMA_BOX.setText(self.Daten_Tabelle.item(row,  1).text())
        self.NACHNAME_BOX.setText(self.Daten_Tabelle.item(row,  2).text())
        self.VORNAME_BOX.setText(self.Daten_Tabelle.item(row, 3).text())
        self.TITEL1.setCurrentText(self.Daten_Tabelle.item(row,  4).text())
        self.TITEL2.setCurrentText(self.Daten_Tabelle.item(row,  5).text())
        self.TITEL3.setCurrentText(self.Daten_Tabelle.item(row,  6).text())
        self.LAND_BOX.setCurrentText(self.Daten_Tabelle.item(row,  7).text())
        self.LKZ_BOX.setText(self.Daten_Tabelle.item(row,  8).text())
        self.STRASSE_BOX.setText(self.Daten_Tabelle.item(row, 9).text())
        self.HAUSNR_BOX.setText(self.Daten_Tabelle.item(row, 10).text())
        self.PLZ_BOX.setText(self.Daten_Tabelle.item(row, 11).text())
        self.ORT_BOX.setText(self.Daten_Tabelle.item(row, 12).text())
        self.MOBIL.setText(self.Daten_Tabelle.item(row, 13).text())
        self.BUSINESS_NR.setText(self.Daten_Tabelle.item(row, 14).text())
        self.EMAIL_BOX.setText(self.Daten_Tabelle.item(row, 15).text())
        self.SCHEIN_ART.setCurrentText(self.Daten_Tabelle.item(row, 16).text())
        self.SCHEIN_BOX.setChecked(self.Daten_Tabelle.item(row, 17).checkState())
#        ANZ_KINDER = int(self.Daten_Tabelle.item(row,  18).text())
#        self.KINDER_BOX.setValue(ANZ_KINDER)
#        date_string = self.Daten_Tabelle.item(row, 19).text()  # Assuming this column holds the date
#        GEB_DATUM = datetime.datetime.strptime(date_string, "%Y-%m-%d")
#        self.BDAY_BOX.setDate(GEB_DATUM)
        self.SVNR_BOX.setText(self.Daten_Tabelle.item(row,  20).text())
        self.KARTE_BOX.setText(self.Daten_Tabelle.item(row,  21).text())
        self.PERSO_BOX.setText(self.Daten_Tabelle.item(row,  22).text())
        
        self.INFO("Feld wird angezeigt.", "I")
        # show picture in label
        PICTURE_NAME = self.NACHNAME_BOX.text() + self.VORNAME_BOX.text() + ".jpg"
        PFAD = 'pictures/'
        try:
            FOTO_DATEI = PFAD + PICTURE_NAME
            FOTO_SHOW = QPixmap(FOTO_DATEI)
            FOTO_SHOW = FOTO_SHOW.scaledToWidth(300)
            self.FOTO.setPixmap(FOTO_SHOW)
        except:
            self.INFO("Es wurde kein Foto gefunden, bitte", "F")
    @pyqtSlot()
    def on_DELETE_clicked(self):
        """
        Löscht einen Eintrag aus der Datenbank, wenn ein bestimmtes Feld im Tabellen Widget ausgewählt worden ist.
        """
        # get the selected row from the table
        selected_row = self.Daten_Tabelle.currentRow()
        if selected_row >= 0:
            # get the values from the selected row that uniquely identify the record
            firmen_name = self.Daten_Tabelle.item(selected_row, 0).text()
            nachname = self.Daten_Tabelle.item(selected_row, 1).text()
            vorname = self.Daten_Tabelle.item(selected_row, 2).text()
            # delete the entry from the database using the unique identifier (the green key in heidisql)
            try:
                mycursor = mydb.cursor()
                sql_delete = "DELETE FROM adressenverwaltung WHERE FIRMEN_NAME = %s AND NACHNAME = %s AND VORNAMEN = %s"
                mycursor.execute(sql_delete, (firmen_name, nachname, vorname))
                mydb.commit()
                self.INFO("Datensatz wurde erfolgreich gelöscht!", "I")
                # refresh the table after deletion
                self.tabelle_anzeigen()
            except Exception as e:
                print(e)
                self.INFO("Fehler beim Löschen des Datensatzes!", "F")
        else:
            self.INFO("Kein Datensatz ausgewählt!", "F")
    @pyqtSlot()
    def on_TOGGLE_DARK_MODE_clicked(self):
        """
        Aktiviert den Darkmode mit einem Button, und umgekehrt.
        """
        # Toggle dark mode
        current_mode = self.TOGGLE_DARK_MODE.isChecked()
        self.set_dark_mode(current_mode)
    @pyqtSlot()
    def on_MAPS_clicked(self):
        """
        Öffnet Google Maps mit dem gewählten Eintrag aus der Tabelle mit dem Standard Browser.
        """
        # variables
        strasse = self.STRASSE_BOX.text()
        hausnr = self.HAUSNR_BOX.text()
        if strasse and hausnr:
            # construct the google maps URL with the address information
            google_maps_url = f"https://www.google.com/maps/place/{strasse}+{hausnr}"
            # ppen the URL in the default web browser
            webbrowser.open(google_maps_url)
        else:
            # inform the user that the address is incomplete
            self.INFO("Die Adresse ist unvollständig. Bitte Straße und Hausnummer angeben.", "F")
    @pyqtSlot()
    def on_EMAIL_CREATE_clicked(self):
        """
        Öffnet das Standard E-Mail Programm und verwendet die Email aus dem gedrückten Feld aus der Tabelle.
        """
        # get the email information
        email = self.EMAIL_BOX.text()
        # check if the email field is not empty
        if email:
            # construct the mailto URL with the email address
            mailto_url = f"mailto:{email}"
            # open the default email program
            webbrowser.open(mailto_url)
        else:
            # inform the user that the email field is empty
            self.INFO("Die E-Mail-Adresse ist leer. Bitte eine E-Mail-Adresse angeben.", "F")
    @pyqtSlot()
    def on_HELP_clicked(self):
        """
        Öffnet das Standard Hilfe Dokument.
        """
        # path to the helpdocument
        if  self.SPRACHE_BOX.currentText() == 'Englisch':
            help_document_path = "help\\help_en.pdf"
        if self.SPRACHE_BOX.currentText() == 'Deutsch':
            help_document_path = "help\\help.pdf"
        # check if the file exists
        if not os.path.exists(help_document_path):
            self.INFO("Das Hilfedokument wurde nicht gefunden. Bitte dem Support melden!", "F")
            return
        # opens the helpdocument with the default pdf - viewer
        QDesktopServices.openUrl(QUrl.fromLocalFile(help_document_path))
    @pyqtSlot()
    def on_NEW_ENTRY_clicked(self):
        """
        Löscht den Text aus den Eingabe Feldern um einen neuen Eintrag zu erstellen und nicht den alten zu überschreiben.
        """
        # clear all input fields
        self.FIRMA_BOX.clear()
        self.NACHNAME_BOX.clear()
        self.VORNAME_BOX.clear()
        self.TITEL1.setCurrentIndex(0)
        self.TITEL2.setCurrentIndex(0)
        self.TITEL3.setCurrentIndex(0)
        self.STRASSE_BOX.clear()
        self.HAUSNR_BOX.clear()
        self.PLZ_BOX.clear()
        self.ORT_BOX.clear()
        self.MOBIL.clear()
        self.BUSINESS_NR.clear()
        self.EMAIL_BOX.clear()
        self.SCHEIN_BOX.setChecked(False)
        self.SCHEIN_ART.setCurrentIndex(0)
        self.SVNR_BOX.clear()
        self.KARTE_BOX.clear()
        self.PERSO_BOX.clear()
        self.KINDER_BOX.clear()
        self.BDAY_BOX.clear()
        # clear the displayed image and info message
        self.FOTO.clear()
        self.INFO("Felder wurden entleert.", "I")

    @pyqtSlot()
    def on_UPLOAD_clicked(self):
        """
        Uploaded ein Bild in den pictures Ordner falls bereits ein Bild vorhanden ist.
        """
        # checks for the required fields
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        # display the file dialog for image selection
        file_name, _ = QFileDialog.getOpenFileName(self, "Bild hochladen", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)
        if file_name:
            # extract the names from input fields
            nachname = self.NACHNAME_BOX.text()
            vorname = self.VORNAME_BOX.text()
            # ensure both input fields have values
            if nachname and vorname:
                # destination path based on nachname and vorname
                destination_path = f"pictures/{nachname}{vorname}.jpg"
                # copy the selected image file to the destination path
                shutil.copy(file_name, destination_path)
                # display the saved image in FOTO
                pixmap = QPixmap(destination_path)
                self.FOTO.setPixmap(pixmap.scaledToWidth(300))
                self.INFO("Datei wurde hochgeladen.", "I")
            else:
                self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus", "F")
    @pyqtSlot()
    def on_SAVE_PICTURE_clicked(self):
        """
        Speichert das Bild aus dem pictures Ordner in dem ausgewählten Pfad von dem Benutzer.
        """
        # check for the required fields 
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        # variables
        nachname = self.NACHNAME_BOX.text()
        vorname = self.VORNAME_BOX.text()
        # construct the file path based on nachname and vorname
        source_path = f"pictures/{nachname}{vorname}.jpg"
        # ask the user to choose the destination path
        destination_path, _ = QFileDialog.getSaveFileName(self, "Save Picture", "", "JPEG files (*.jpg);;All Files (*)")
        try:
            if destination_path:
                # copy the file to the specified destination path
                shutil.copy(source_path, destination_path)
                self.INFO(f"Bild wurde an folgendem Ort gespeichert: {destination_path}", "I")
            else:
                self.INFO("Es wurde kein Zielpfad ausgewählt. Bild konnte nicht gespeichert werden.", "F")
        except Exception as e:
            print(e)
            self.INFO("Bild konnte nicht gespeichert werden.", "F")
    @pyqtSlot()
    def on_DELETE_PICTURE_clicked(self):
        """
        Löscht das gespeichert Bild mit dem jeweilig ausgewählten Nachnamen und Vornamen.
        """
        # check for the required fields
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        # variables
        nachname = self.NACHNAME_BOX.text()
        vorname = self.VORNAME_BOX.text()
        # construct the file path based on nachname and vorname
        file_path = f"pictures/{nachname}{vorname}.jpg"
        try:
            if os.path.exists(file_path):
                # delete the file if it exists
                os.remove(file_path)
                self.INFO("Das Bild wurde erfolgreicht gelöscht.", "I")
            else:
                self.INFO("Es wurde kein Bild gefunden.", "F")
        except Exception as e:
            print(e)
            self.INFO("Bild konnte nicht gelöscht werden.", "F")
        PICTURE_NAME = self.NACHNAME_BOX.text() + self.VORNAME_BOX.text() + ".jpg"
        PFAD = 'pictures/'
        try:
            FOTO_DATEI = PFAD + '/'+ PICTURE_NAME
            FOTO_SHOW = QPixmap(FOTO_DATEI)
            self.FOTO.setPixmap(FOTO_SHOW)
        except:
            print("auweh")
    @pyqtSlot()
    def on_SEARCH_clicked(self):
        """
        Sucht die Datenbanktabelle nach den eingegebenen Daten ab.
        """
        suchtext = self.SEARCH_INPUT.text()
        if suchtext == "":
            self.tabelle_anzeigen()  # display all records when search box is empty
        else:
            # searches every input field, so that anything can be searched
            mycursor = mydb.cursor()
            sql = "SELECT * FROM adressenverwaltung WHERE FIRMEN_NAME LIKE %s OR NACHNAME LIKE %s OR VORNAMEN LIKE %s OR STRASSE LIKE %s OR HAUS_NR LIKE %s OR PLZ LIKE %s OR ORT LIKE %s OR MOBIL_NR LIKE %s OR BUSINESS_NR LIKE %s OR EMAIL LIKE %s OR ART LIKE %s"
            val = ('%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%', '%' + suchtext + '%')
            try:
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                if len(result) > 0:
                    # display the search result in the table widget
                    self.Daten_Tabelle.setRowCount(len(result))
                    for row_index, row_data in enumerate(result):
                        for col_index, col_data in enumerate(row_data[1:]):  # exclude the first column (ID)
                            if col_index == 13:  # adjust index for the 'SCHEIN' column
                                fielditem = QTableWidgetItem("")
                                self.Daten_Tabelle.setItem(row_index, col_index, fielditem)
                                fielditem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                                if str(col_data) == "1":
                                    fielditem.setCheckState(Qt.Checked)
                                else:
                                    fielditem.setCheckState(Qt.Unchecked)
                            else:
                                fielditem = QTableWidgetItem(str(col_data))
                                self.Daten_Tabelle.setItem(row_index, col_index, fielditem)
                    self.INFO("Suchergebnisse werden in der Tabelle angezeigt.", "I")
                else:
                    self.INFO("Keine Ergebnisse gefunden.", "I")
            except Exception as e:
                self.INFO(f"Fehler bei der Suche: {str(e)}", "F")
            mycursor.close()
            self.Daten_Tabelle.resizeColumnsToContents() # resize columns to contents
            self.Daten_Tabelle.resizeRowsToContents() # resize rows to contents

    @pyqtSlot(str)
    def on_SPRACHE_BOX_currentTextChanged(self, p0):
        """
        Wechselt die Sprache.
        """
        # TODO: not implemented yet
       # raise NotImplementedError
        if self.SPRACHE_BOX.currentText() == 'Englisch':
            self.uebersetzen("en")
            LOGO = QLabel(self)
            LOGO = QPixmap('logo.png')
            self.LOGO.setPixmap(LOGO)
            self.INFO("User Interface is written in the English language.", "I")
            # saves the value of the language in the database
            mycursor = mydb.cursor()
            try:
                sql_select = "SELECT * FROM voreinstellungen"
                mycursor.execute(sql_select)
                settings = mycursor.fetchone()
                if settings is None:
                    # if nothing was found create new entry
                    sql_insert = "INSERT INTO voreinstellungen (SPRACHE) VALUES (%s)"
                    val_insert = (1 if self.SPRACHE_BOX.currentText() == 'Englisch' else print(),)
                    mycursor.execute(sql_insert, val_insert)
                else:
                    # if entry was found update the entry
                    sql_update = "UPDATE voreinstellungen SET SPRACHE=%s"
                    val_update = (1 if self.SPRACHE_BOX.currentText() == 'Englisch' else print(),)
                    mycursor.execute(sql_update, val_update)
                mydb.commit()
            except Exception as e:
                print(e)
                mydb.rollback()
                self.INFO("Fehler bei der Aktualisierung der Einstellungen!", "F")
            finally:
                mycursor.close()
        elif self.SPRACHE_BOX.currentText() == 'Deutsch':
            self.uebersetzen("de")
            LOGO = QLabel(self)
            LOGO = QPixmap('logo.png')
            self.LOGO.setPixmap(LOGO)
            self.INFO("Die Maske wird in deutscher Sprache ausgegeben.", "I")
            mycursor = mydb.cursor()
            try:
                sql_select = "SELECT * FROM voreinstellungen"
                mycursor.execute(sql_select)
                settings = mycursor.fetchone()
                if settings is None:
                    # if nothing was found create new entry
                    sql_insert = "INSERT INTO voreinstellungen (SPRACHE) VALUES (%s)"
                    val_insert = (0 if self.SPRACHE_BOX.currentText() == 'Deutsch' else print(),)
                    mycursor.execute(sql_insert, val_insert)
                else:
                    # if entry was found update the entry
                    sql_update = "UPDATE voreinstellungen SET SPRACHE=%s"
                    val_update = (0 if self.SPRACHE_BOX.currentText() == 'Deutsch' else print(),)
                    mycursor.execute(sql_update, val_update)
                mydb.commit()
            except Exception as e:
                print(e)
                mydb.rollback()
                self.INFO("Fehler bei der Aktualisierung der Einstellungen!", "F")
            finally:
                mycursor.close()

    def uebersetzen(self, sprach_kz):
        """
        Ruft die Sprache aus dem .qm file ab.
        """
        try:
            app.removeTranslator(self.translator)
        except:
            print("")
        self.translator = QTranslator()
        self.translator.load("i18n/datenverwaltung_"+sprach_kz+".qm")
        app.installTranslator(self.translator)
        self.retranslateUi(self)
            
    def voreinstellungen(self):
        """
        Holt die zuletzt gespeicherten Einstellungen aus der Datenbank.
        """
        self.DB_verbinden()  # Verbindung zur Datenbank herstellen
        mycursor = mydb.cursor()
        try:
            mycursor.execute("SELECT SPRACHE, DARKMODE FROM voreinstellungen")
            settings = mycursor.fetchone()

            if settings is not None:
                sprache, dark_mode = settings
                if sprache == 1:
                    self.SPRACHE_BOX.setCurrentIndex("Englisch")
                    self.uebersetzen("en")
                if sprache == 0:
                    self.SPRACHE_BOX.setCurrentIndex("Deutsch")
                    self.uebersetzen("de")
                self.set_dark_mode(bool(dark_mode))
        except Exception as e:
            print(e)
            self.INFO("Fehler beim Abrufen der Einstellungen!", "F")
        finally:
            mycursor.close()

    @pyqtSlot()
    def on_CSV_clicked(self):
        """
        Speichert die ganzen Daten aus der Datenbank in einer xml Datei ab.
        """
        # check for required fields
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        sql_satz = []
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM adressenverwaltung")
        sql_satz = mycursor.fetchall()
        mycursor.close()
        csvdatei = "csv_data/database.csv"
        try:
            with open (csvdatei,  'w',  newline = "\n", encoding="cp1252") as csvfile:
                csvwriter = csv.writer(csvfile,  delimiter = ';',  quotechar = '"',  quoting = csv.QUOTE_MINIMAL)
                csvwriter.writerows(sql_satz)
                csvfile.close()
                self.INFO("Alle Daten wurden aus der Datenbank exportiert.",  "I")
        except:
            msb_return = QMessageBox.critical(
                self,
                self.tr("Fehler"),
                self.tr("""Die CSV-Datein konnte nicht erstellt werden!"""),
                (
                    QMessageBox.StandardButton.Ok),
            )
            print(msb_return)
    @pyqtSlot()
    def on_REPORT_clicked(self):
        """
        Speichert die ausgewählten Daten in einer XML Datei ab.
        """
        # check for required fields
        if not self.is_required_fields_filled():
            self.INFO("Bitte füllen Sie mindestens die *Pflichtfelder aus.", "F")
            return
        # path where the individual pictures are saved
        PFAD = 'pictures/'  +self.VORNAME_BOX.text()+self.NACHNAME_BOX.text()+".jpg"
        directory = 'xml_data/'
        full_path = os.path.join(directory, "adressen.XML")
        with open(full_path, "w") as xml_out:
            xml_out.write('<?xml version="1.0" encoding="iso-8859-1" ?>' + '\n')
            xml_out.write('<adressen>' + '\n')
            xml_out.write('  <category name="adressen">' + "\n")
            for i in range(1):
                xml_out.write('     <SATZ id="'+ str(i+1)+ '">' + '\n')
                xml_out.write("     <FIRMEN_NAME>" + self.FIRMA_BOX.text() + "</FIRME_NNAME>" + "\n")
                xml_out.write("     <NACHNAME>" + self.NACHNAME_BOX.text() + "<NACHNAME>" + "\n")
                xml_out.write("     <VORNAMEN>" + self.VORNAME_BOX.text() + "<VORNAMEN>" + "\n")
                xml_out.write("     <TITEL_1>" + self.TITEL1.currentText() + "<TITEL_1>" + "\n")
                xml_out.write("     <TITEL_2>" + self.TITEL2.currentText() + "<TITEL_d2>" + "\n")
                xml_out.write("     <TITEL_3>" + self.TITEL3.currentText() + "<TITEL_2>" + "\n")
                xml_out.write("     <LAND>" + self.LAND_BOX.currentText() + "<ORT>" + "\n")
                xml_out.write("     <LKZ>" + self.LKZ_BOX.text() + "<LKZ>" + "\n")
                xml_out.write("     <STRASSE>" + self.STRASSE_BOX.text() + "<STRASSE>" + "\n")
                xml_out.write("     <HAUS_NR>" + self.HAUSNR_BOX.text() + "<HAUS_NR>" + "\n")
                xml_out.write("     <PLZ>" + self.PLZ_BOX.text() + "<PLZ>" + "\n")
                xml_out.write("     <ORT>" + self.ORT_BOX.text() + "<ORT>" + "\n")
                xml_out.write("     <MOBIL_NR>" + self.MOBIL.text() + "<MOBIL_NR>" + "\n")
                xml_out.write("     <BUSINESS_NR>" + self.BUSINESS_NR.text() + "<MOBIL>" + "\n")
                xml_out.write("     <EMAIL>" + self.EMAIL_BOX.text() + "<EMAIL>" + "\n")
                #xml_out.write("     <SCHEIN>" + self.SCHEIN_BOX.isChecked() + "<SCHEIN>" + "\n")
                xml_out.write("     <ART>" + self.SCHEIN_ART.currentText() + "<ART>" + "\n")
                #xml_out.write("     <KINDER>" + self.KINDER_BOX.value() + "<ART>" + "\n")
                xml_out.write("     <GEBURTSDATUM>" + self.BDAY_BOX.text() + "<GEBURTSDATUM>" + "\n")
                xml_out.write("     <SVNR>" + self.SVNR_BOX.text() + "<SVNR>" + "\n")
                xml_out.write("     <KARTE_NR>" + self.KARTE_BOX.text() + "<KARTE_NR>" + "\n")
                xml_out.write("     <PERSO_NR>" + self.PERSO_BOX.text() + "<PERSO_NR>" + "\n")
                xml_out.write("     <PFAD>" + PFAD + "<PFAD>" + "\n")
        
                xml_out.write("      <SATZ>" + "\n")
            
            xml_out.write('  </category>' + "\n")
            xml_out.write("<daten_verwaltung>" + "\n")
            xml_out.close() # close
            self.INFO("XML-SATZ wurde ausgegeben",  "I") # infot output

    @pyqtSlot()
    def on_SCHEIN_BOX_clicked(self):
        """
        Deaktiviert die Führerschein Combo Box.
        """
        self.SCHEIN_ART.setEnabled(self.SCHEIN_BOX.isChecked())
        if not self.SCHEIN_ART.isEnabled():
            self.SCHEIN_ART.setCurrentIndex(0)

    @pyqtSlot()
    def on_REPORT_ALL_clicked(self):
        """
        Tragt die Daten aus der Datenbank Datenverwaltung in eine SQLite Datenbank ein.
        """
        sqlite_datei="sqlite/datenverwaltung_sqlite.db"
        if os.path.exists(sqlite_datei):
            os.remove(sqlite_datei)
            print("Datei wurde gelöscht",  sqlite_datei)
        connection = sqlite3.connect('datennverwaltung_sqlite.db')
        cursor = connection.cursor()
        nachricht = "Datenbank >" + sqlite_datei + "< wird angelegt!"
        self.INFO(nachricht,  "I")             
        # creates the table if it does not exist
        sql = "CREATE TABLE IF NOT EXISTS datenverwaltung("\
        " \
     )"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        # connect to database
        connection = sqlite3.connect('datenverwaltung_sqlite.db')
        cursor = connection.cursor()
        # read current database and fill sqlite database
        sql_satz = []
        self.mycursor = mydb.cursor()
        self.mycursor.execute("SELECT * FROM daten_verwaltung")
        sql_satz = self.mycursor.fetchall()
        self.mycursor.close()
        # Inhalte der Liste "sql_satz" in SQlite-DB auffüllen
        for zeile,  wert in enumerate(sql_satz):            # enumerate = automatischer Zähler für "zeile"
            sql = "INSERT INTO datenverwaltung VALUES (" \
            + "'" + str(wert[0]) + "', " \
            + "'" + str(wert[1]) + "', " \
            + "'" + str(wert[2]) + "', " \
            + "'" + str(wert[3]) + "', " \
            + "'" + str(wert[4]) + "', " \
            + "'" + str(wert[5]) + "', " \
            + "'" + str(wert[6]) + "', " \
            + "'" + str(wert[7]) + "', " \
            + "'" + str(wert[8]) + "', " \
            + "'" + str(wert[9]) + "', " \
            + "'" + str(wert[10]) + "', " \
            + "'" + str(wert[11]) + "', " \
            + "'" + str(wert[12]) + "', " \
            + "'" + str(wert[13]) + "', " \
            + "'" + str(wert[14]) + "', " \
            + "'" + str(wert[15]) + "', " \
            + "'" + str(wert[16]) + "') " \
            + "'" + str(wert[17]) + "') " \
            + "'" + str(wert[18]) + "') " \
            + "'" + str(wert[19]) + "') " \
            + "'" + str(wert[20]) + "') " \
            + "'" + str(wert[21]) + "') " \
            + "'" + str(wert[22]) + "') " \
            + "'" + str(wert[23]) + "') " 
            cursor.execute(sql) 
        connection.commit()
        connection.close()
    @pyqtSlot()
    def on_EMAIL_SUPPORT_clicked(self):
        """
        Öffnet das Standard E-Mail Programm und verwendet die Email vom Support.
        """
        QMessageBox.information(
            self, 
            self.tr("E-MAIL Support"), 
            self.tr("""Ihr Standard E-MAIL Programm für 
Kontakt mit dem Support wird geöffnet."""), 
            QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))
        # get the email information
        email = "quentin.wagner@live.at"
        # check if the email field is not empty
        if email:
            # construct the mailto URL with the email address
            mailto_url = f"mailto:{email}"
            # open the default email program
            webbrowser.open(mailto_url)
        else:
            # inform the user that the email field is empty
            self.INFO("Die E-Mail-Adresse ist leer. Bitte eine E-Mail-Adresse angeben.", "F")

    @pyqtSlot()
    def on_PHONE_SUPPORT_clicked(self):
        """
        Öffnet ein Fenster und zeigt die Support telefonnummern an.
        """
        QMessageBox.information(
            self, 
            self.tr("Phone Support"), 
            self.tr("""Sie können sich mit folgenden Nummern an den Support wenden.
+43 678 1218891
--------------------"""), 
            QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))
            
    @pyqtSlot()
    def on_PRINT_clicked(self):
        """
        Öffnet ein Dialogfenster das die letzte CSV-Datei druckt.
        """
        csv_folder = 'csv_data/'  # name of your subfolder containing CSV files
        project_path = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(project_path, csv_folder)

        if os.path.exists(csv_path):
            csv_files = [f for f in os.listdir(csv_path) if f.endswith('.csv')]

            if csv_files:
                file_to_print = os.path.join(csv_path, csv_files[0])  # select the first CSV file
                print("Printing file:", file_to_print)  
            else:
                print("No CSV files found in the 'csv' folder.")
        else:
            print("The 'csv' folder does not exist in the project directory.")

    
app = QApplication(sys.argv)
ui = HAUPTFENSTER()
ui.show()
sys.exit(app.exec())
