from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

from wordTraining import WordTraining
from conjugationTraining import ConjugationTraining
from modifyDictionary import ModifyDictionary

import sys
import json
  
# {"comer": {"fr": "manger", "eng": "eat", "def": "", "type": "verb", "score": 4, "conj": "como_come_comem"}


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
            if i == 1:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'ã')
            elif i == 2:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'á')
            elif i == 3:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'ó')
            elif i == 4:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'õ')
            elif i == 5:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'ú')
            elif i == 6:
                self.lineEditFocused.setText(self.lineEditFocused.text() + 'í')

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
        # add multiple translations
        self.number_of_translations = 3
        self.counter = [0, 0]
        # inputs
        self.title_1 = QLabel("Adicionar uma Nova Palavra :")
        self.title_1.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.word, self.fr_trad, self.eng_trad, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["fn", "mn", "verb", "adj", "other"])
        self.flag = 0
        self.type.currentIndexChanged.connect(self.display_input)
        self.b1 = QPushButton("Adicionar uma Nova Palavra")
        self.b1.clicked.connect(self.fill_dictionary)

        self.b_add_fr = QPushButton("+")
        self.b_add_fr.metadata = 0
        self.b_add_fr.clicked.connect(self.add_translation_row)
        self.widget_fr = QWidget()
        layout_h_fr = QHBoxLayout(self.widget_fr)
        layout_h_fr.addWidget(self.fr_trad)
        layout_h_fr.addWidget(self.b_add_fr)

        self.b_add_eng = QPushButton("+")
        self.b_add_eng.metadata = 1
        self.b_add_eng.clicked.connect(self.add_translation_row)
        self.widget_eng = QWidget()
        layout_h_eng = QHBoxLayout(self.widget_eng)
        layout_h_eng.addWidget(self.eng_trad)
        layout_h_eng.addWidget(self.b_add_eng)
        # form
        self.form_1 = QFormLayout()
        self.form_1.addRow(self.title_1)
        self.form_1.addRow(QLabel("Português"), self.word)
        self.form_1.addRow(QLabel("Francês"), self.widget_fr)
        self.form_1.addRow(QLabel("Inglês"), self.widget_eng)
        self.form_1.addRow(QLabel("Nota"), self.definition_input)
        self.form_1.addRow(QLabel("Tipo"), self.type)
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
        self.traduction_fr = QLabel(database[self.word_id]["fr"])
        self.traduction_eng = QLabel(database[self.word_id]["eng"])
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

    def search_word(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        bra_words = []
        fr_words = []
        eng_words = []
        for k in database.keys():
            bra_words.append(database[k]["bra"])
            fr_words.append(database[k]["fr"])
            eng_words.append(database[k]["eng"])
        word = self.search_bar.text()
        if word in fr_words:
            idx = fr_words.index(word)
            word = bra_words[idx]
        elif word in eng_words:
            idx = eng_words.index(word)
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

        if len(self.word.text()) == 0:
            self.raise_error("Enter a word")
        elif self.type.currentText() == "verb" and (self.conj1.text() == "" or self.conj2.text() == "" or self.conj3.text() == "" or self.conj4.text() == "" or self.conj5.text() == "" or self.conj6.text() == ""):
            self.raise_error("Enter conjugaison")
        elif not self.check(self.word.text(), data, 1) or self.type.currentText() not in self.check(self.word.text(), data, 1):
            if self.type.currentText() == "verb":
                conj_p = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
                conj_pp = self.conj4.text() +"_"+ self.conj5.text() +"_"+ self.conj6.text()
            else:
                conj_p = ""
                conj_pp = ""
                # for i in self.counter[0]:
                #     fr_trad = self.fr_trad.text() + self.form_1.children()
            # print("title",self.form_1.getWidgetPosition(self.title_1), self.form_1.itemAt(0).widget())
            # print("word",self.form_1.getWidgetPosition(self.word), self.form_1.itemAt(1).widget())
            # print("fr",self.form_1.getWidgetPosition(self.widget_fr), self.form_1.itemAt(2).widget())
            # print("eng",self.form_1.getWidgetPosition(self.widget_eng), self.form_1.itemAt(3).widget())
            # print("eng",self.form_1.getWidgetPosition(self.widget_eng), self.form_1.itemAt(3).widget())

            # idx, _ = self.form_1.getWidgetPosition(self.widget_fr)
            # print(self.widget_fr.children())
            # test = self.form_1.itemAt(0)
            # print(test.widget())
            # print(test.widget().children()[1].text())
            # print(ze)
            key = str(int(list(database)[-1])+1)
            database[key] = {"bra": self.word.text(),
                            "fr": self.fr_trad.text(), 
                            "eng": self.eng_trad.text(), 
                            "def": self.definition_input.text(), 
                            "type": self.type.currentText(),
                            "score" : 0,
                            "conj": conj_p,
                            "conj_pp": conj_pp}
            item_to_add = QListWidgetItem()
            item_to_add.setText(self.word.text())   
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

    def display_input(self):
        sender = self.sender()
        idx, _ = self.form_1.getWidgetPosition(sender)
        if self.type.currentText() == "verb":
            
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            self.conj4, self.conj5, self.conj6 = QLineEdit(), QLineEdit(), QLineEdit()

            self.widget0 = QWidget()
            layout_h0 = QHBoxLayout(self.widget0)
            layout_h0.addWidget(QLabel("Eu                               "))
            layout_h0.addWidget(QLabel("Ele/Ela/Você             "))
            layout_h0.addWidget(QLabel("Eles/Elas/Vocês"))
            self.widget1 = QWidget()
            layout_h1 = QHBoxLayout(self.widget1)
            layout_h1.addWidget(self.conj1)
            layout_h1.addWidget(self.conj2)            
            layout_h1.addWidget(self.conj3)
            self.widget2 = QWidget()
            layout_h2 = QHBoxLayout(self.widget2)
            layout_h2.addWidget(self.conj4)
            layout_h2.addWidget(self.conj5)
            layout_h2.addWidget(self.conj6)
            self.form_1.insertRow(idx+1, QLabel("Conjugation :"))
            self.form_1.insertRow(idx+2, QLabel(""), self.widget0)
            self.form_1.insertRow(idx+3, QLabel("Presente"), self.widget1)
            self.form_1.insertRow(idx+4, QLabel("Pretérito Perfeito"), self.widget2)
            self.flag = 1
        else:
            if self.flag:
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.flag = 0

    def selection_changed(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        self.selected_word.setText(self.word_list.currentItem().text())
        self.word_id = self.word_list.currentItem().data(Qt.UserRole)
        self.traduction_fr.setText(database[self.word_id]["fr"])
        self.traduction_eng.setText(database[self.word_id]["eng"])
        self.definition.setText(database[self.word_id]["def"])

    def add_translation_row(self):
        sender = self.sender()
        i = sender.metadata
        b_rm = QPushButton("-")
        b_rm.metadata = i
        b_rm.clicked.connect(self.rm_translation_row)
        tr_input = QLineEdit()
        widget_tr = QWidget()
        layout_h_tr = QHBoxLayout(widget_tr)
        layout_h_tr.addWidget(tr_input)
        layout_h_tr.addWidget(b_rm)
        if self.counter[i] < self.number_of_translations:
            idx, _ = self.form_1.getWidgetPosition(sender.parent())
            self.form_1.insertRow(idx + self.counter[i] + 1, QLabel(''), widget_tr)
            self.counter[i] += 1

    def rm_translation_row(self):
        sender = self.sender()
        i = sender.metadata
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        self.form_1.removeRow(idx)
        self.counter[i] -= 1

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