from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

from wordTraining import WordTraining
from conjugationTraining import ConjugationTraining
from modifyDictionary import ModifyDictionary
from input_form import InputForm

import sys
import json

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

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("accents keyboard", self)
        button_action.triggered.connect(self.openKeyboard)
        toolbar.addAction(button_action)
        global key_flag
        key_flag = 1
 
        self.clavier = Clavier()
        self.clavier.show()

        ### layouts ###

        ## add word to dictionary
        # inputs
        self.title_1 = QLabel("Adicionar uma Nova Palavra :")
        self.title_1.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b1 = QPushButton("Adicionar uma Nova Palavra")
        self.b1.clicked.connect(self.fill_dictionary)

        # form
        self.form_1 = QFormLayout()
        self.form_1.addRow(self.title_1)
        self.input_form = InputForm(self, self.form_1)
        self.form_1.addRow(self.b1)
        ## data interface
        # word list
        self.word_list = QListWidget()
        with open('database.json', 'r+') as f:
            database = json.load(f)
        for key in database.keys():
            item_to_add = QListWidgetItem()
            item_to_add.setText(database[key]["bra"])   
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
        self.selected_word = QLabel(self.word_list.currentItem().text())
        self.word_id = self.word_list.currentItem().data(Qt.UserRole)
        self.traduction_fr = QLabel(', '.join(database[self.word_id]["fr"].split('_')))
        self.traduction_eng = QLabel(', '.join(database[self.word_id]["eng"].split('_')))
        self.definition = QLabel(database[self.word_id]["def"])
        self.definition.setMaximumSize(int(self.width()*0.4), int(self.height()*0.15))
        self.title_3 = QLabel("Palavras ({}) :".format(len(database)))
        self.title_3.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b5 = QPushButton("Modifier/Supprimer")
        self.b5.clicked.connect(self.modify_dictionary)

        # form
        form_3 = QFormLayout()
        form_3.addRow(self.title_3)
        form_3.addRow(QLabel("Search Word :"), self.search_bar)
        form_3.addRow(self.word_list)
        form_3.addRow(QLabel("Tradução Francesa :"), self.traduction_fr)
        form_3.addRow(QLabel("Tradução Inglesa :"), self.traduction_eng)
        form_3.addRow(QLabel("Nota :"), self.definition)
        form_3.addRow(self.b5)
        
        ## test knowledge
        # words
        self.select_training_1 = QComboBox()
        self.select_training_1.addItems(["all", "verb", "adj", "noun", "other"])
        self.mode = QComboBox()
        self.mode.addItems(["random", "weighted"])
        self.b3 = QPushButton("Ensaio (palavras)")
        self.b3.clicked.connect(self.train_word)
        self.widget0 = QWidget()
        layout_h0 = QHBoxLayout(self.widget0)
        layout_h0.addWidget(self.b3)
        layout_h0.addWidget(self.select_training_1)
        layout_h0.addWidget(self.mode)
        
        # conjugation
        self.select_training_2 = QComboBox()
        self.select_training_2.addItems(["all", "regular", "irregular"])
        self.tense = QComboBox()
        self.tense.addItems(["presente", "pretérito perfeito"])
        self.b4 = QPushButton("Ensaio (verbos)")
        self.b4.clicked.connect(self.train_conjugation)
        self.widget1 = QWidget()
        layout_h1 = QHBoxLayout(self.widget1)
        layout_h1.addWidget(self.b4)
        layout_h1.addWidget(self.select_training_2)
        layout_h1.addWidget(self.tense)

        # form
        form_4 = QFormLayout()
        form_4.addRow(self.widget0)
        form_4.addRow(self.widget1)

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
        eng_words = [[],[],[],[]]
        for k in database.keys():
            bra_words.append(database[k]["bra"])
            fr = database[k]["fr"].split('_')
            fr_words[0].append(fr[0])
            for i in range(1, len(fr), 1):
                fr_words[i].append(fr[i])
            for i in range(len(fr), 4, 1):
                fr_words[i].append('')
            eng = database[k]["eng"].split('_')
            eng_words[0].append(eng[0])
            for i in range(1, len(eng), 1):
                eng_words[i].append(eng[i])
            for i in range(len(eng), 4, 1):
                eng_words[i].append('')

        word = self.search_bar.text()
        for i in range(4):
            if word in fr_words[i]:
                idx = fr_words[i].index(word)
                word = bra_words[idx]
            elif word in eng_words[i]:
                idx = eng_words[i].index(word)
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

        data = [(key, value["bra"], value["type"]) for key, value in database.items()]

        if len(self.input_form.word.text()) == 0:
            self.raise_error("Enter a word")
        elif self.input_form.type.currentText() == "verb" and (self.input_form.conj1.text() == "" or self.input_form.conj2.text() == "" or self.input_form.conj3.text() == "" or self.input_form.conj4.text() == "" or self.input_form.conj5.text() == "" or self.input_form.conj6.text() == ""):
            self.raise_error("Enter conjugaison")
        elif not self.check(self.input_form.word.text(), data, 1) or self.input_form.type.currentText() not in self.check(self.input_form.word.text(), data, 1):
            if self.input_form.type.currentText() == "verb":
                conj_p = self.input_form.conj1.text() +"_"+ self.input_form.conj2.text() +"_"+ self.input_form.conj3.text()
                conj_pp = self.input_form.conj4.text() +"_"+ self.input_form.conj5.text() +"_"+ self.input_form.conj6.text()
            else:
                conj_p = ""
                conj_pp = ""
                
            fr = ""
            eng = ""
            for i in range(self.init_length, self.form_1.rowCount(), 1):
                widget = self.form_1.itemAt(i).widget()
                if type(widget) is QWidget and widget.metadata == 3:
                    metadata = widget.children()[2].metadata
                    if metadata == 0:
                        fr += '_' + widget.children()[1].text()
                    elif metadata == 1:
                        eng += '_' + widget.children()[1].text()

            key = str(int(list(database)[-1])+1)
            database[key] = {"bra": self.input_form.word.text(),
                            "fr": self.input_form.fr_trad.text()+fr, 
                            "eng": self.input_form.eng_trad.text()+eng, 
                            "def": self.input_form.definition_input.text(), 
                            "type": self.input_form.type.currentText(),
                            "score" : 0,
                            "conj": conj_p,
                            "conj_pp": conj_pp}
            item_to_add = QListWidgetItem()
            item_to_add.setText(self.input_form.word.text())   
            item_to_add.setData(Qt.UserRole, key) 
            self.word_list.addItem(item_to_add)
            self.word_list.sortItems()
            self.title_3.setText("Palavras ({}) :".format(len(database)))
            with open('database.json', 'w') as f:
                json.dump(database, f)
        else:
            self.raise_error("Você já sabe essa palavra")   
    
    def train_word(self):
        self.w1 = WordTraining(self.select_training_1.currentText(), self.screen_dim, self.mode.currentText())
        self.w1.show()

    def train_conjugation(self):
        self.w2 = ConjugationTraining(self.select_training_2.currentText(), self.tense.currentText())
        self.w2.show()

    def modify_dictionary(self):
        self.w3 = ModifyDictionary(self.word_list.currentItem(), parent=self)
        self.w3.show()

    def raise_error(self, error):
        msg = QMessageBox()
        msg.setText(error)
        msg.exec_()

    def selection_changed(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        self.selected_word.setText(self.word_list.currentItem().text())
        self.word_id = self.word_list.currentItem().data(Qt.UserRole)
        self.traduction_fr.setText(', '.join(database[self.word_id]["fr"].split('_')))
        self.traduction_eng.setText(', '.join(database[self.word_id]["eng"].split('_')))
        self.definition.setText(database[self.word_id]["def"])

    def openKeyboard(self):
        global key_flag
        if key_flag:
            self.clavier.close()
            key_flag = 0
        else:
            self.clavier = Clavier()
            self.clavier.show()
            key_flag = 1

if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    win = MainWindow(width, height)
    win.show()
    sys.exit(app.exec_())