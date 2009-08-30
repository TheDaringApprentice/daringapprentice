# -*- coding: utf-8 -*-
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui, uic

class DeckWindow(QtGui.QMainWindow):
    def __init__(self):
        super(DeckWindow, self).__init__()
                
        uic.loadUi('deckeditor.ui', self)
        
        self.setWindowTitle(self.tr("Daring Apprentice - Deck Editor"))
        
        self.createActions()
        self.createToolBars()
        
        # connect some slots and signals...
        self.connect(self.cardList,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.mainDeck,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.sideBoard,QtCore.SIGNAL('itemSelectionChanged()'),self.setCard)
        self.connect(self.btnSearch,QtCore.SIGNAL('clicked()'),self.applyFilters)
        self.connect(self.chkConverted,QtCore.SIGNAL('clicked()'),self.chkConvClicked)
        self.connect(self.chkSplit,QtCore.SIGNAL('clicked()'),self.chkSplitClicked)

        import oracle
        
        self.AllCards = oracle.loadOraclefile('g:\pyDA\Oracle.txt')
        
        list = []
        sets = []
        rarities = []
       
        for s in self.AllCards.keys():
            list += [s]
            sets += self.AllCards[s]['Sets']
            rarities += self.AllCards[s]['Rarities']
        
        rarities = set(rarities)
        sets = set(sets)
        
        self.statusbar.showMessage(str(len(list)))
        
        self.cardList.addItems(sorted(list,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        self.fltRarity.addItems(sorted(rarities,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        self.fltSet.addItems(sorted(sets,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        
        self.fltSet.insertItem(0,"All")
        self.fltRarity.insertItem(0,"All")
        
        self.fltSet.setCurrentIndex(0)
        self.fltRarity.setCurrentIndex(0)
        
        # Who knows... I don't have a Mac
        self.setUnifiedTitleAndToolBarOnMac(True)
        
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
        if widget.metaObject().className() == 'QTreeWidget':
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
         + 'Mono Colored : ' + str(self.AllCards[aName]['Mono colored']) + '<br>'\
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
            
            # Filter on Power and Toughness
            
            # Filter on Color
                
            
            return False
        
        list = []
        for card in self.AllCards.keys():
            aCard = self.AllCards[card]
            if not filtered(aCard):
                list += [card]
        
        self.cardList.clear()
        self.cardList.addItems(sorted(list,cmp=lambda x,y: cmp(x.lower(), y.lower())))
        self.statusbar.showMessage(str(len(list)))
        

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    deckWin = DeckWindow()
    deckWin.show()
    sys.exit(app.exec_())

