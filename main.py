from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

from wordTraining import WordTraining
from modifyDictionary import ModifyDictionary
from input_form import InputForm

import config

import sys
import json
import os

class Clavier(QMainWindow):
    def __init__(self):        
        super().__init__()
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setGeometry(400,450,200,100)
        self.setWindowTitle('accents 🇧🇷')

        self.b1 = QPushButton("ã")
        self.b1.clicked.connect(self.setFocusText)
        self.b1.metadata = 1
        self.b2 = QPushButton("á")
        self.b2.clicked.connect(self.setFocusText)
        self.b2.metadata = 2
        self.b3 = QPushButton("ó")
        self.b3.clicked.connect(self.setFocusText)
        self.b3.metadata = 3
        self.widget1 = QWidget()
        layout_h1 = QHBoxLayout(self.widget1)
        layout_h1.addWidget(self.b1)
        layout_h1.addWidget(self.b2)
        layout_h1.addWidget(self.b3)

        self.b4 = QPushButton("õ")
        self.b4.clicked.connect(self.setFocusText)
        self.b4.metadata = 4
        self.b5 = QPushButton("ú")
        self.b5.clicked.connect(self.setFocusText)
        self.b5.metadata = 5
        self.b6 = QPushButton("í")
        self.b6.clicked.connect(self.setFocusText)
        self.b6.metadata = 6
        self.widget2 = QWidget()
        layout_h2 = QHBoxLayout(self.widget2)
        layout_h2.addWidget(self.b4)
        layout_h2.addWidget(self.b5)
        layout_h2.addWidget(self.b6)

        self.form_1 = QFormLayout()
        self.form_1.addRow(self.widget1)
        self.form_1.addRow(self.widget2)

        layout = QGridLayout()

        layout.addLayout(self.form_1, 0, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def setFocusText(self):
        sender = self.sender()
        i = sender.metadata
        self.lineEditFocused = QApplication.focusWidget()
        if type(self.lineEditFocused) is QLineEdit:
            pos = self.lineEditFocused.cursorPosition()
            text = self.lineEditFocused.text()
            if i == 1:
                self.lineEditFocused.setText(text[:pos] + 'ã' + text[pos:])
            elif i == 2:
                self.lineEditFocused.setText(text[:pos] + 'á' + text[pos:])
            elif i == 3:
                self.lineEditFocused.setText(text[:pos] + 'ó' + text[pos:])
            elif i == 4:
                self.lineEditFocused.setText(text[:pos] + 'õ' + text[pos:])
            elif i == 5:
                self.lineEditFocused.setText(text[:pos] + 'ú' + text[pos:])
            elif i == 6:
                self.lineEditFocused.setText(text[:pos] + 'í' + text[pos:])
            self.lineEditFocused.setCursorPosition(pos+1)

    def closeEvent(self, event):
        global key_flag
        key_flag = 0
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.screen_dim = (width, height)

        self.setGeometry(200,200,1000,800)
        self.setWindowTitle('🇧🇷')

        toolbar = QToolBar("toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("clavier accents", self)
        button_action.triggered.connect(self.openKeyboard)
        toolbar.addAction(button_action)
        global key_flag
        key_flag = 1
 
        self.clavier = Clavier()
        self.clavier.show()

        ### layouts ###

        ## add word to dictionary
        # inputs
        self.title_1 = QLabel("Ajouter un Nouveau Mot :")
        self.title_1.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b1 = QPushButton("Ajouter")
        self.b1.clicked.connect(self.fill_dictionary)

        # form
        self.form_1 = QFormLayout()
        self.form_1.addRow(self.title_1)
        self.input_form = InputForm(self, self.form_1)
        self.form_1.addRow(self.b1)
        ## data interface
        # word list
        self.word_list = QListWidget()
        file = 'database.json'
        if not(os.path.isfile(file) and os.access(file, os.R_OK)):
            with open(file, 'w') as f:
                f.write(json.dumps({}))
        with open('database.json', 'r+') as f:
            database = json.load(f)

        for key in database.keys():
            item_to_add = QListWidgetItem()
            item_to_add.setText(database[key]["unknown"])   
            item_to_add.setData(Qt.UserRole, key) 
            self.word_list.addItem(item_to_add)
        self.word_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.word_list.resetHorizontalScrollMode()
        self.word_list.sortItems()
        self.word_list.setCurrentRow(0)
        self.word_list.itemSelectionChanged.connect(self.selection_changed)

        # search bar
        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search_word)

        # display/modify word info
        self.selected_word = QLabel('')
        self.traduction_fr = QLabel('')
        self.notes = QPlainTextEdit()
        self.notes.setReadOnly(True)
        self.notes.setMaximumSize(int(self.width()*0.4), int(self.height()*0.15))
        if self.word_list.currentItem() is not None:
            self.selected_word.setText(self.word_list.currentItem().text())
            self.word_id = self.word_list.currentItem().data(Qt.UserRole)
            self.traduction_fr.setText(', '.join(database[self.word_id]["known"].split('_')))
            self.notes.setPlainText(database[self.word_id]["notes"])
        self.title_3 = QLabel("Mots ({}) :".format(len(database)))
        self.title_3.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b5 = QPushButton("Modifier/Supprimer")
        self.b5.clicked.connect(self.modify_dictionary)

        # form
        form_3 = QFormLayout()
        form_3.addRow(self.title_3)
        form_3.addRow(QLabel("Rechercher un Mot :"), self.search_bar)
        form_3.addRow(self.word_list)
        form_3.addRow(QLabel("Traduction :"), self.traduction_fr)
        form_3.addRow(QLabel("Notes :"), self.notes)
        form_3.addRow(self.b5)
        
        ## test knowledge
        # words
        self.select_training_1 = QComboBox()
        self.select_training_1.addItems([config.ALL, config.VERB, config.ADJ, config.NOUN, config.OTHER])
        self.mode = QComboBox()
        self.mode.addItems([config.RANDOM, "weighted", "test"])
        self.b3 = QPushButton("Quiz (mots)")
        self.b3.clicked.connect(self.train_word)
        self.widget0 = QWidget()
        layout_h0 = QHBoxLayout(self.widget0)
        layout_h0.addWidget(self.b3)
        layout_h0.addWidget(self.select_training_1)
        layout_h0.addWidget(self.mode)
        
        # form
        form_4 = QFormLayout()
        form_4.addRow(self.widget0)

        ### layout grid ###

        layout = QGridLayout()

        layout.addLayout(self.form_1, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

        layout.addLayout(form_3, 0, 1)
        widget_3 = QWidget()
        widget_3.setLayout(layout)
        self.setCentralWidget(widget_3)

        layout.addLayout(form_4, 1, 0)
        widget_4 = QWidget()
        widget_4.setLayout(layout)
        self.setCentralWidget(widget_4)

        self.init_length = self.form_1.rowCount()

    def search_word(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        bra_words = []
        fr_words = [[],[],[],[]]
        for k in database.keys():
            bra_words.append(database[k]["unknown"])
            fr = database[k]["known"].split('_')
            fr_words[0].append(fr[0])
            for i in range(1, len(fr), 1):
                fr_words[i].append(fr[i])
            for i in range(len(fr), 4, 1):
                fr_words[i].append('')

        word = self.search_bar.text().strip().lower()
        for i in range(4):
            if word in fr_words[i]:
                idx = fr_words[i].index(word)
                word = bra_words[idx]
        model = self.word_list.model()
        match = model.match(
            model.index(0, self.word_list.modelColumn()), 
            Qt.DisplayRole, 
            word, 
            hits=1, 
            flags=Qt.MatchExactly)
        if match:
            self.word_list.setCurrentIndex(match[0])

    def check(self, word, data, i):
        words = []
        for d in data:
            if d[i] == word:
                words.append(d[2])
        return words

    def fill_dictionary(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)

        data = [(key, value["unknown"], value["type"]) for key, value in database.items()]

        if len(self.input_form.word.text().strip().lower()) == 0 and len(self.input_form.fr_trad.text().strip().lower()) == 0:
            self.raise_error("Entrer un mot et au moins une traduction")
        elif len(self.input_form.fr_trad.text().strip().lower()) == 0:
            self.raise_error("Entrer une traduction")
        elif len(self.input_form.word.text().strip().lower()) == 0:
            self.raise_error("Entrer un mot")
        elif not self.check(self.input_form.word.text().strip().lower(), data, 1) or self.input_form.type.currentText() not in self.check(self.input_form.word.text().strip().lower(), data, 1):
            fr = ""
            for i in range(self.init_length, self.form_1.rowCount(), 1):
                widget = self.form_1.itemAt(i).widget()
                if type(widget) is QWidget and widget.metadata == 3:
                    metadata = widget.children()[2].metadata
                    if metadata == 0:
                        fr += '_' + widget.children()[1].text()

            if len(data) > 0:
                key = str(int(list(database)[-1])+1)
            else:
                key = '0'
            database[key] = {"unknown": self.input_form.word.text().strip().lower(),
                            "known": self.input_form.fr_trad.text().strip().lower()+fr, 
                            "notes": self.input_form.notes_input.toPlainText(), 
                            "type": self.input_form.type.currentText(),
                            "score" : 0}
            item_to_add = QListWidgetItem()
            item_to_add.setText(self.input_form.word.text().strip().lower())   
            item_to_add.setData(Qt.UserRole, key) 
            self.word_list.addItem(item_to_add)
            self.word_list.sortItems()
            self.title_3.setText("Mots ({}) :".format(len(database)))
            with open('database.json', 'w') as f:
                json.dump(database, f)
        else:
            self.raise_error("Mot déjà connu")   
    
    def train_word(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        word_type = self.select_training_1.currentText()
        words = list(database.items())
        if word_type == config.ALL:
            word_list = [words[i] for i in range(len(words))]
        else:
            word_list = [words[i] for i in range(len(words)) if words[i][1]["type"] == word_type]
        if len(word_list) > 0:
            self.w1 = WordTraining(word_type, self.screen_dim, self.mode.currentText())
            self.w1.show()
        else:
            msg = QMessageBox()
            msg.setText("Aucun mot de type : {}\n".format(word_type))
            msg.exec_()

    def modify_dictionary(self):
        if self.word_list.currentItem() != None:
            self.w3 = ModifyDictionary(self.word_list.currentItem(), parent=self)
            self.w3.show()

    def raise_error(self, error):
        msg = QMessageBox()
        msg.setText(error)
        msg.exec_()

    def selection_changed(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        if self.word_list.currentItem() is not None:
            self.selected_word.setText(self.word_list.currentItem().text())
            self.word_id = self.word_list.currentItem().data(Qt.UserRole)
            self.traduction_fr.setText(', '.join(database[self.word_id]["known"].split('_')))
            self.notes.setPlainText(database[self.word_id]["notes"])
        else:
            self.selected_word.setText('')
            self.traduction_fr.setText('')
            self.notes.setPlainText('')

    def openKeyboard(self):
        global key_flag
        if key_flag:
            self.clavier.close()
            key_flag = 0
        else:
            self.clavier = Clavier()
            self.clavier.show()
            key_flag = 1

    def closeEvent(self, event):
        QApplication.closeAllWindows()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    win = MainWindow(width, height)
    win.show()
    sys.exit(app.exec_())