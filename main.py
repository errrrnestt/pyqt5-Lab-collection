from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

# ═══════════════════════════════════════════════════════════════
# 📄 LAB REPORT #42 - TEXT EDITOR WITH PyQt5
# ═══════════════════════════════════════════════════════════════

class W(Qt.QMainWindow):
    fname = ""
    iz = " "
    
    def __init__(self):
        """🏗️ Initialize main window and UI components"""
        Qt.QMainWindow.__init__(self)
        
        # 📑 Tab widget for multiple documents
        self.tab = Qt.QTabWidget()
        self.setCentralWidget(self.tab)
        
        # ─── Status Bar Controls ─────────────────────────────
        # 📂 Open file button
        self.btnOpen = Qt.QPushButton('Открыть')
        self.btnOpen.clicked.connect(self.open)
        self.statusBar().addWidget(self.btnOpen)
        
        # 💾 Save file button
        self.btnSave = Qt.QPushButton('Сохранить')
        self.btnSave.clicked.connect(self.save)
        self.statusBar().addWidget(self.btnSave)
        
        # 🔍 Find text input
        self.ed = Qt.QTextEdit("что заменить")
        self.ed.setFixedSize(100, 25)    
        self.statusBar().addWidget(self.ed)
        
        # 🔄 Replace text input
        self.ed2 = Qt.QTextEdit("на что")
        self.ed2.setFixedSize(100, 25)    
        self.statusBar().addWidget(self.ed2)
        
        # ⚡ Replace button
        self.btnZam = Qt.QPushButton('Заменить')
        self.btnZam.clicked.connect(self.zam)
        self.statusBar().addWidget(self.btnZam)
        
        # ❌ Close tab button
        self.btnClose = Qt.QPushButton('Закрыть')
        self.btnClose.clicked.connect(self.close)
        self.statusBar().addWidget(self.btnClose)
        
    # ─── File Operations ──────────────────────────────────────
    
    def open(self):
        """📂 Open a text file and add as new tab"""
        fname = Qt.QFileDialog.getOpenFileName()[0]
        if not fname: 
            return
        with open(fname) as f:
            txt = f.read()
        idx = self.tab.addTab(Qt.QTextEdit(), fname)
        self.tab.widget(idx).setPlainText(txt)
        self.tab.setCurrentIndex(idx)
    
    # ─── Text Operations ─────────────────────────────────────
    
    def zam(self):
        """🔍 Find and replace text in current document"""
        global fname
        txt = self.tab.currentWidget().toPlainText()
        nay1 = self.ed.toPlainText()
        nay2 = self.ed2.toPlainText()
        txt = txt.replace(nay1, nay2)
        self.tab.currentWidget().setPlainText(txt)
    
    # ─── Save Operations ─────────────────────────────────────
    
    def save(self):
        """💾 Save current document to file"""
        fname = Qt.QFileDialog.getSaveFileName()[0]
        if not fname: 
            return
        txt = self.tab.currentWidget().toPlainText()
        print(txt)
        with open(fname, 'w') as f:
            f.write(txt)
    
    # ─── Tab Management ──────────────────────────────────────
    
    def close(self):
        """❌ Close current tab and clean up"""
        idx = self.tab.currentIndex()
        wgt = self.tab.widget(idx)
        self.tab.removeTab(idx)
        del wgt

# ─── Application Entry Point ────────────────────────────────

if __name__ == "__main__":
    app = Qt.QApplication([])
    t = W()
    t.resize(640, 480)
    t.show()
    app.exec_()