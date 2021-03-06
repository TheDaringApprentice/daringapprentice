# -*- coding: utf-8 -*-
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QDataStream, Qt, QVariant, QStringList
from PyQt4.QtGui import *

class TreeModel(QStandardItemModel):
    # code created by _dboddie in #pyqt on the irc.freenode.net IRC server  (THANKS!)
    
    def __init__(self, parent = None):
    
        QStandardItemModel.__init__(self, parent)
        t = QStringList()
        t.append('Card')
        t.append('Amount')
        self.setHorizontalHeaderLabels(t)

    def dropMimeData(self, data, action, row, column, parent):
    
        if data.hasFormat('application/x-qabstractitemmodeldatalist'):
            bytearray = data.data('application/x-qabstractitemmodeldatalist')
            data_items = self.decode_data(bytearray)
            
            # Decode the data, assuming that we get 6 32-bit integers to
            # start with, then a count byte followed by a string.
            text = data_items[Qt.DisplayRole].toString()
            for row in range(self.rowCount()):
                name = self.item(row, 0).text()
                if name == text:
                    number_item = self.item(row, 1)
                    number = int(number_item.text())
                    number_item.setText(str(number + 1))
                    break
            else:
                name_item = QStandardItem(text)
                number_item = QStandardItem("1")
                self.appendRow([name_item, number_item])
            
            return True
        else:
            return QStandardItemModel.dropMimeData(self, data, action, row, column, parent)
    
    def decode_data(self, bytearray):
    
        data = {}
        
        ds = QDataStream(bytearray)
        while not ds.atEnd():
        
            row = ds.readInt32()
            column = ds.readInt32()
            
            map_items = ds.readInt32()
            for i in range(map_items):
            
                key = ds.readInt32()
                
                value = QVariant()
                ds >> value
                data[Qt.ItemDataRole(key)] = value
        
        return data
    
    def itemSelectionChanged(self):
        
    

class DeckWindow(QtGui.QMainWindow):
    def __init__(self):
        super(DeckWindow, self).__init__()
                
        uic.loadUi('deckeditor.ui', self)
        mainDeckModel = TreeModel()
        sideBoardModel = TreeModel()
      
        self.mainDeck.setModel(mainDeckModel)
        self.sideBoard.setModel(sideBoardModel)
                
        
        self.setWindowTitle(self.tr("Daring Apprentice - Deck Editor"))
        
        self.createActions()
        self.createToolBars()
        
        # connect some slots and signals...
        self.connect(self.cardFilter,QtCore.SIGNAL('textChanged(QString)'),self.jumpCard)
        self.connect(self.cardList,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.mainDeck,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.sideBoard,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.btnSearch,QtCore.SIGNAL('clicked()'),self.applyFilters)
        self.connect(self.chkConverted,QtCore.SIGNAL('clicked()'),self.chkConvClicked)
        self.connect(self.chkSplit,QtCore.SIGNAL('clicked()'),self.chkSplitClicked)
        self.connect(self.chkAny,QtCore.SIGNAL('clicked()'),self.chkAnyClicked)
        self.connect(self.btnComment,QtCore.SIGNAL('clicked()'),self.addComment)
        self.connect(self.btnInput,QtCore.SIGNAL('clicked()'),self.addInput)
        self.connect(self.btnAdd,QtCore.SIGNAL('clicked()'),self.addCard)
        self.connect(self.btnRemove,QtCore.SIGNAL('clicked()'),self.removeCard)
        self.connect(self.btnAddSB,QtCore.SIGNAL('clicked()'),self.addCardSB)
        self.connect(self.btnRemoveSB,QtCore.SIGNAL('clicked()'),self.removeCardSB)
        
        self.chkAnyClicked()
      
        import oracle
        
        self.AllCards = oracle.loadOraclefile('g:\pyDA\Oracle.txt')
        
        self.list = []
        sets = []
        rarities = []
       
        for s in self.AllCards.keys():
            self.list += [s]
            sets += self.AllCards[s]['Sets']
            rarities += self.AllCards[s]['Rarities']
        
        rarities = set(rarities)
        sets = set(sets)
        
        self.statusbar.showMessage(str(len(self.list)) + ' / ' + str(len(self.AllCards)))
        
        self.list = sorted(self.list,cmp=lambda x,y: cmp(x.lower(), y.lower()))
        
        self.cardList.addItems(self.list)
        self.fltRarity.addItems(sorted(rarities,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        self.fltSet.addItems(sorted(sets,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        
        self.fltSet.insertItem(0,"All")
        self.fltRarity.insertItem(0,"All")
        
        self.fltSet.setCurrentIndex(0)
        self.fltRarity.setCurrentIndex(0)
        
        # Who knows... I don't have a Mac
        self.setUnifiedTitleAndToolBarOnMac(True)
    
    def syncDeckSB(self):
        widget = self.sender()
        print widget.objectName()
        if widget.objectName() == "mainDeck":
            for i in range(self.mainDeck.count()):
                if self.sideBoard.columnWidth(i) != self.mainDeck.columnWidth(i):
                    self.sideBoard.setColumnWidth(i,self.mainDeck.columnWidth(i))
        elif widget.objectName() == "sideBoard":
            for i in range(self.sideBoard.count()):
                if self.mainDeck.columnWidth(i) != self.sideBoard.columnWidth(i):
                    self.mainDeck.setColumnWidth(i,self.sideBoard.columnWidth(i))
            
            
    
    def addComment(self):
        # TODO: add item to maindeck / sideboard (with // in front)
        text, ok = QtGui.QInputDialog.getText(self,
                self.tr("Enter a Comment"), self.tr("Comment :"),
                QtGui.QLineEdit.Normal, '')
        if ok and not text.isEmpty():
            pass
    
    def addInput(self):
        # TODO: Open Input box, add item to maindeck / sideboard
        text, ok = QtGui.QInputDialog.getText(self,
                self.tr("QInputDialog.getText()"), self.tr("Input :"),
                QtGui.QLineEdit.Normal, '')
        if ok and not text.isEmpty():
            pass
    
    def addCard(self):
        # TODO: Add current selection to Maindeck
        aName = self.cardList.currentItem().text()
    
    def removeCard(self):
        # TODO: Remove 1 card of current selection of Maindeck
        pass
    
    def addCardSB(self):
        # TODO: Add current selection to Maindeck
        pass
    
    def removeCardSB(self):
        # TODO: Add current selection to Maindeck
        pass
    
    
    def jumpCard(self,s):
        
        def anIndex(s,aList):
            i = 0
            for aName in aList:
                if s.lower() < aName.lower():
                    return i
                i = i + 1
        
        index = anIndex(str(s), self.list)
        # print s + ', ' + str(index)
        self.cardList.setCurrentRow(index)
        
    def dropEvent(self, event):
        print event.mimeData().hasText()
        print event.mimeData().hasImage()
        print event.mimeData().hasColor()
        print event.mimeData().hasHtml()
        print event.mimeData().hasUrls()
        
        
            
    def chkAnyClicked(self):
        w = self.chkAny.isChecked()
        self.chkWhite.setEnabled(not w)
        self.chkBlue.setEnabled(not w)
        self.chkBlack.setEnabled(not w)
        self.chkRed.setEnabled(not w)
        self.chkGreen.setEnabled(not w)
        self.chkGold.setEnabled(not w)
        self.chkColorless.setEnabled(not w)
        self.chkLand.setEnabled(not w)
        self.chkExclude.setEnabled(not w)
      
    def chkConvClicked(self):
        w = self.chkConverted.isChecked()
        self.fltCostTo.setVisible(w)
        if w:
            width = 61
        else:
            width = 131
        self.fltCostFrom.setFixedWidth(width)
    
    def chkSplitClicked(self):
        w = self.chkSplit.isChecked()
        self.fltPowTo.setVisible(w)
        self.fltTghFrom.setVisible(w)
        self.fltTghTo.setVisible(w)
        self.lblTghTo.setVisible(w)
        self.lblPowTo.setVisible(w)
        self.lblPtSlash.setVisible(w)
        if w:
            width = 25
        else:
            width = 131
        self.fltPowFrom.setFixedWidth(width)
    
    def setCard(self):
        widget = self.sender()
        if widget.metaObject().className() == 'QListWidget':
            aName = widget.currentItem().text()
        if widget.metaObject().className() == 'QTreeView':
            aName = widget.currentItem().text(0)
        aName = str(aName).decode()
        text = ''
        text = '<b>' + self.AllCards[aName]['Name'] + '&nbsp;&nbsp;&nbsp;'\
         + self.AllCards[aName]['Cost'] + '</b><br>'\
         + self.AllCards[aName]['Type'] + '<br>'\
         + self.AllCards[aName]['Rules Text'].replace('\n','<br>') + '<br>'\
         + self.AllCards[aName]['Pow/Tgh'] + '<br>'\
         + '<HR>'\
         + 'Sets : ' + str(self.AllCards[aName]['Sets']).strip("[]") + '<br>'\
         + 'Rarities: ' + str(self.AllCards[aName]['Rarities']).strip("[]")+ '<br>'\
         + 'Colors : ' + str(self.AllCards[aName]['Colors'])  + '<br>'\
         + 'Hybrid Only : ' + str(self.AllCards[aName]['Only Hybrid']) + '<br>'\
         + 'Converted Cost : ' + str(self.AllCards[aName]['Converted Cost']) + '<br>'\
         + 'Power : ' + self.AllCards[aName]['Power'] + '<br>Toughness : ' + self.AllCards[aName]['Toughness']\
         + '<HR>' \
         + self.AllCards[aName]['Name'] + ' on Gatherer: <a href=' + self.AllCards[aName]['Url']\
         + '>' + self.AllCards[aName]['Url'] + '</a><HR>'
             
        self.cardText.setText(text.decode('utf','replace'))
          
    def newDeck(self):
        # TODO: Empty all fields, and reset the name to blank
        dosomething = True
        reply = QtGui.QMessageBox.information(self, 'New Deck', 'New Deck')
        
    def loadDeck(self):
        # Open a open file dialog
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Select the deck to load..."),
                '',
                self.tr("All Files (*);;Text Files (*.txt)"), '')
        reply = QtGui.QMessageBox.information(self, fileName, fileName)
    
    def saveAsDeck(self):
        # Open a save file dialog
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Select your path and filename"),
                '',
                self.tr("All Files (*);;Text Files (*.txt)"), '')
        reply = QtGui.QMessageBox.information(self, fileName, fileName)
    
    def saveDeck(self):
        reply = QtGui.QMessageBox.information(self, 'Deck saved','Deck saved' )
        
       
    def createActions(self):
        '''
            TODO: Add some proper actions! :-)
            Initial code pasted from dockwidgets.pyw from the examples of QT 
        '''
        
        self.quitAct = QtGui.QAction(self.tr("Close"), self)
        self.quitAct.setShortcut(self.tr("Ctrl+Q"))
        self.quitAct.setStatusTip(self.tr("Close the Deck Editor"))
        self.quitAct.triggered.connect(self.close)

        self.newAct = QtGui.QAction(self.tr("&New"), self)
        self.newAct.setStatusTip(self.tr("Create an empty deck"))
        self.newAct.triggered.connect(self.newDeck)
        
        self.loadAct = QtGui.QAction(self.tr("&Load"), self)
        self.loadAct.setStatusTip(self.tr("Load a Deck"))
        self.loadAct.triggered.connect(self.loadDeck)
        
        self.saveAct = QtGui.QAction(self.tr("Save"), self)
        self.saveAct.setStatusTip(self.tr("Save current deck"))
        self.saveAct.triggered.connect(self.saveDeck)

        self.saveAsAct = QtGui.QAction(self.tr("Save &As"), self)
        self.saveAsAct.setStatusTip(self.tr("Save current deck with a new filename"))
        self.saveAsAct.triggered.connect(self.saveAsDeck)      

    def createToolBars(self):
        self.gameToolBar = self.addToolBar("Actions")
        self.gameToolBar.addAction(self.newAct)
        self.gameToolBar.addAction(self.loadAct)
        self.gameToolBar.addAction(self.saveAct)
        self.gameToolBar.addAction(self.saveAsAct)
        self.gameToolBar.addAction(self.quitAct)
        
    def applyFilters(self):
        
        def filtered(aCard):
            # Filter on Card Name
            test = str(self.fltName.text()).lower()
            if test != '':
                if aCard['Name'].lower().find(test) < 0:  
                    return True
            
            # Filter on Card Type
            test = str(self.fltType.text()).lower()
            if test != '':
                if aCard['Type'].lower().find(test) < 0:  
                    return True
                        
            # Filter on Rules Text
            test = str(self.fltRules.text()).lower()
            if test != '':
                
                def check(haystack,needle):
                    or_result = False
                    for t_ors in needle.split(','):
                        and_result = True
                        for t_ands in t_ors.split(' '):
                            and_result = and_result and haystack.lower().find(t_ands) >= 0
                        or_result = or_result or and_result
                    return or_result
                
                if self.chkRegex.isChecked():
                    if not check(aCard['Rules Text'],test):
                        return True
                else:
                    if aCard['Rules Text'].lower().find(test) < 0:
                        return True
                                
            # Filter on Mana Cost
            test = self.fltCostFrom.text()
            if test != '':
                if self.chkConverted.isChecked():
                    test2 = self.fltCostTo.text()
                    if test2 == "":
                        test2 = test
                    if int(aCard['Converted Cost']) < int(test) or int(aCard['Converted Cost']) > int(test2):
                        return True
                else:
                    if aCard['Cost'].lower() != str(test).lower():
                        return True
            
            # Filter on set
            test = self.fltSet.currentText()
            if test != 'All':
                if test not in aCard['Sets']:
                    return True
            
            # Filter Rarity
            test = self.fltRarity.currentText()
            if test != 'All':
                if test not in aCard['Rarities']:
                    return True
                
            def toint(s):
                try:
                    i = int(s)
                except ValueError:
                    i = 0
                return i
                
            # Filter on Power and Toughness            
            test = self.fltPowFrom.text()
            if test != '':
                if self.chkSplit.isChecked():
                    if 'Power' not in aCard:
                        print aCard
                    test2 = self.fltPowTo.text()
                    if test2 == "":
                        test2 = test
                    if toint(aCard['Power']) < toint(test) or toint(aCard['Power']) > toint(test2):
                        return True
                else:
                    if aCard['Pow/Tgh'].lower().strip('()[]{}') != str(test).lower():
                        return True
            test = self.fltTghFrom.text()
            if test != '':
                if self.chkSplit.isChecked():
                    test2 = self.fltTghTo.text()
                    if test2 == "":
                        test2 = test
                    if toint(aCard['Toughness']) < toint(test) or toint(aCard['Toughness']) > toint(test2):
                        return True
           
            # Filter on Color
            if not self.chkAny.isChecked():
                Colors = dict({'White':self.chkWhite, 'Blue':self.chkBlue, 'Black':self.chkBlack,
                               'Red':self.chkRed, 'Green':self.chkGreen, 'Gold':self.chkGold,
                               'Colorless':self.chkColorless, 'Land':self.chkLand})
                
                SelCols = set([])
                for key in Colors.keys():
                    if Colors[key].isChecked():
                        SelCols = SelCols | set([key])
                
                if self.chkExclude.isChecked():
                    if aCard['Only Hybrid']:
                        if SelCols.isdisjoint(aCard['Colors']):
                            return True
                    else:
                        if not SelCols >= aCard['Colors']:
                            return True    
                else:
                    if SelCols.isdisjoint(aCard['Colors']):
                        return True
            
            return False
        
        self.list = []
        for card in self.AllCards.keys():
            aCard = self.AllCards[card]
            if not filtered(aCard):
                self.list += [card]
                
        self.list = sorted(self.list,cmp=lambda x,y: cmp(x.lower(), y.lower()))
        
        self.cardList.clear()
        self.cardList.addItems(self.list)
        self.statusbar.showMessage(str(len(self.list)) + ' / ' + str(len(self.AllCards)))
        

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    deckWin = DeckWindow()
    deckWin.show()
    sys.exit(app.exec_())

