#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from config import Config
from eapi import Eapi
from mainwindow import Ui_MainWindow
from preferences import Ui_preferencesDialog

class PreferencesDialog(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.ui = Ui_preferencesDialog()
        self.ui.setupUi(self)
        
        self.loadConfig()
        
        self.savedFlag = True
        
        #connect slots
        QObject.connect(self.ui.cancelButton,SIGNAL('clicked()'),self.onCancel)
        QObject.connect(self.ui.applyButton,SIGNAL('clicked()'),self.onApply)
        QObject.connect(self.ui.okButton,SIGNAL('clicked'),self.onOk)
        QObject.connect(self.ui.fetchButton,SIGNAL('clicked()'),self.onFetch)
        QObject.connect(self.ui.addButton,SIGNAL('clicked()'),self.onAdd)
    def loadConfig(self):
        parser = Config()
    def onCancel(self):
        self.close()
    def onApply(self):
        pass
    def onOk(self):
        pass
    def onFetch(self):
        pass
    def onAdd(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.copyesLabel.hide()
        self.ui.copyesDisplay.hide()
        self.ui.runsLabel.hide()
        self.ui.runsDisplay.hide()
        
        #tray icon setup
        self.setupTrayIcon()
        self.setupTrayMenu()
        
        #connecting action slots
        QObject.connect(self.ui.actionQuit,SIGNAL('activated()'),self.onQuit)
        QObject.connect(self.ui.actionPreferences,SIGNAL('activated()'),self.onPreferences)
    def setupTrayIcon(self):
        icon = QIcon("icons/tray_icon.png")
        self.trayIcon = QSystemTrayIcon(icon)
        self.trayIcon.show()
    def setupTrayMenu(self):
        pass
    def onPreferences(self):
        dlg = PreferencesDialog(self)
        dlg.show()
    def onQuit(self):
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
    sys.exit()