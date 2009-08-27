#!/usr/bin/env python
from PyQt4 import QtCore, QtGui, QtOpenGL
import math

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)
    
class GLWidget(QtOpenGL.QGLWidget):
    
    # Only for now, eventually we'll have the real interface here 
    # (maybe in a seperate physical file, especially as click dragging etc.
    # needs to be implemented.)
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def initializeGL(self):
        self.qglClearColor(self.trolltechPurple.dark())
        # self.qglClearColor(self.black()) # HELP! I want this in black
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        GL.glEnd()
        GL.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.qglColor(self.trolltechGreen)

        GL.glVertex3d(x1, y1, -0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x3, y3, -0.05)
        GL.glVertex3d(x4, y4, -0.05)

        GL.glVertex3d(x4, y4, +0.05)
        GL.glVertex3d(x3, y3, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.qglColor(self.trolltechGreen.dark(250 + int(100 * x1)))

        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        # Add the OpenGL widget
        self.glWidget = GLWidget()
        self.setCentralWidget(self.glWidget)
        
        self.setWindowTitle(self.tr("Daring Apprentice"))
        
        # Who knows... I don't have a Mac
        self.setUnifiedTitleAndToolBarOnMac(True)
        
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Daring Apprentice"),
            self.tr("<a href=http://daringapprentice.wikispaces.com>Daring Apprentice</a><br>"
                "A temporary about box, until I have something better. "
                "<br><br>--- <b>The Daring Apprentice</b>"))
            
    def createActions(self):
        '''
            TODO: Add some proper actions! :-)
            Initial code pasted from dockwidgets.pyw from the examples of QT 
        '''
        
        self.quitAct = QtGui.QAction(self.tr("&Quit"), self)
        self.quitAct.setShortcut(self.tr("Ctrl+Q"))
        self.quitAct.setStatusTip(self.tr("Quit the application"))
        self.quitAct.triggered.connect(self.close)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
        self.aboutAct.triggered.connect(self.about)

        
    def createMenus(self):
        self.gameMenu = self.menuBar().addMenu(self.tr("&Game"))
        self.gameMenu.addAction(self.quitAct)

        self.viewMenu = self.menuBar().addMenu(self.tr("&View"))

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.gameToolBar = self.addToolBar(self.tr("File"))
        self.gameToolBar.addAction(self.quitAct)

        self.helpToolBar = self.addToolBar(self.tr("Help"))
        self.helpToolBar.addAction(self.aboutAct)
    
    def createStatusBar(self):
        self.statusBar().showMessage(self.tr("Ready"))
        
    def createDockWindows(self):
        
        # HELP! Preferably, I'd like to load the positions of all the dock windows
        # from a file, and restore them upon reopening the application.
                
        dock = QtGui.QDockWidget(self.tr("Activity Log"), self)
        dock.setAllowedAreas(
                        QtCore.Qt.LeftDockWidgetArea |
                        QtCore.Qt.RightDockWidgetArea |
                        QtCore.Qt.BottomDockWidgetArea )
        
        if True:  # So we can code fold on the Activity Log
            '''
                Here we create the "Activity Log" docking window.
                It is a RichText Box (QTextEdit), with a line edit and a send button
                below it.
            '''
        
            self.LogV = QtGui.QWidget(dock)         # the Bigger docking widget
            # self.LogV.sizePolicy(QSizePolicy.Minimum)
            self.LogLayout = QtGui.QVBoxLayout()    # the Vert layout for the log dock
            self.LogLayout.setSpacing(1)
            self.LogText = QtGui.QTextEdit()        # Where the log is stored
            self.LogText.sizeHint().setHeight(60)
            # self.LogText.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
            # self.LogText.enabled = False          # HELP! This widget should be read only
                                                    # though it's good to have copy and paste.
        
            self.LogH = QtGui.QWidget()             # the widget for the send button and text
            self.LogHLayout = QtGui.QHBoxLayout()   # the Horz layout for the send boxes
            self.LogHLayout.setSpacing(1)
            self.LogSend = QtGui.QLineEdit(self.tr("Type in text here to chat!"))
            self.LogBtnSend = QtGui.QToolButton()
            self.LogBtnSend.setText("Send")
            self.LogHLayout.addWidget(self.LogSend)
            self.LogHLayout.addWidget(self.LogBtnSend)
            self.LogH.setLayout(self.LogHLayout)
        
            self.LogLayout.addWidget(self.LogText)
            self.LogLayout.addWidget(self.LogH)
            self.LogV.setLayout(self.LogLayout)
                                       
            dock.setWidget(self.LogV)
            self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
            self.viewMenu.addAction(dock.toggleViewAction())
        
        if True:  # So we can code fold on the Hand Dock
            '''
                Here we create a Hand Station.
                It is where the player will have all his cards, and can untap, draw,
                set life, and end his turn.
            '''
            
            # TODO: make this a class, and call it X times for the amount of players
            dock = QtGui.QDockWidget(self.tr("Player1's Hand"), self)
            # dock.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
            self.HandDock1 = QtGui.QWidget(dock)
            self.HandLayout = QtGui.QHBoxLayout()
            self.HandLayout.setSpacing(0)
            self.HandTree = QtGui.QTreeWidget()
            labels = QtCore.QStringList()
            labels << self.tr("Cardname") << self.tr("Cost")
            self.HandTree.setHeaderLabels(labels)
            self.HandTree.setColumnWidth(0, 120)
            self.HandTree.setColumnWidth(1, 40)
            # self.HandTree.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
            self.HandTree.rootIsDecorated = False
            self.HandTree.alternatingRowColors = True
            self.HandLayout.addWidget(self.HandTree)
            
            # HELP! The HandAction buttons are *way* too big, they should be tight,
            # and preferably have some icons on them!
            self.HandActionDock = QtGui.QWidget()
            # self.HandActionDock.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
            self.HandActionLayout = QtGui.QVBoxLayout()
            self.UntapAll = QtGui.QPushButton("Untap All")
            self.DrawCard = QtGui.QPushButton("Draw")
            self.CreateToken = QtGui.QPushButton("Create Token")
            self.EndTurn = QtGui.QPushButton("End Turn")
            
            self.LifeDock = QtGui.QWidget()
            self.LifeLayout = QtGui.QHBoxLayout()
            self.LifeLayout.setSpacing(0)
            self.LifePlus = QtGui.QToolButton()
            self.LifePlus.setText("+")
            self.LifePlus.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
            self.LifeMinus = QtGui.QToolButton()
            self.LifeMinus.setText("-")
            self.LifeMinus.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
            
            self.LifeLayout.addWidget(self.LifePlus)
            self.LifeLayout.addWidget(self.LifeMinus)
            
            self.LifeDock.setLayout(self.LifeLayout)
            
            self.HandActionLayout.addWidget(self.UntapAll)
            self.HandActionLayout.addWidget(self.DrawCard)
            self.HandActionLayout.addWidget(self.CreateToken)
            self.HandActionLayout.addWidget(self.EndTurn)
            self.HandActionLayout.addWidget(self.LifeDock)
            aSpacer = QtGui.QWidget()
            aSpacer.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            self.HandActionLayout.addWidget(aSpacer)
            
            
            self.HandActionDock.setLayout(self.HandActionLayout)
            
            self.HandLayout.addWidget(self.HandActionDock)
 
            self.HandDock1.setLayout(self.HandLayout)
            
            dock.setWidget(self.HandDock1)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            self.viewMenu.addAction(dock.toggleViewAction())
        
        if True: # So we can code fold on the Card Info
            '''
                Here we create the "Card Info" box.
                It is where the Card's Name, and all other info will be displayed.
                
                Note that it is important that we add the Card box last, as this
                makes that the dock is below the hand(s) in the docking area.
            '''
            dock = QtGui.QDockWidget(self.tr("Card Info"), self)
            self.CardDock = QtGui.QWidget(dock)
            self.CardLayout = QtGui.QHBoxLayout()
            self.CardText = QtGui.QTextEdit()
            self.CardText.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
            self.CardLayout.addWidget(self.CardText)
            self.CardDock.setLayout(self.CardLayout)
            
            dock.setWidget(self.CardDock)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            self.viewMenu.addAction(dock.toggleViewAction())

        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
