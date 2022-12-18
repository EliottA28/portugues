from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class InputForm():
    def __init__(self, parent, form) -> None:
        self.p = parent
        self.form_1 = form
        self.number_of_translations = 3
        self.counter = [0, 0]

        self.word, self.fr_trad, self.eng_trad, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["fn", "mn", "verb", "adj", "other"])
        self.flag = 0
        self.type.currentIndexChanged.connect(self.display_input)
        self.wword = QWidget()
        layout_h_w = QHBoxLayout(self.wword)
        layout_h_w.addWidget(QLabel("Português"))
        layout_h_w.addWidget(self.word)

        self.b_add_fr = QPushButton("+")
        self.b_add_fr.metadata = 0
        self.b_add_fr.clicked.connect(self.add_translation_row)
        self.widget_fr = QWidget()
        layout_h_fr = QHBoxLayout(self.widget_fr)
        layout_h_fr.addWidget(QLabel("Francês"))
        layout_h_fr.addWidget(self.fr_trad)
        layout_h_fr.addWidget(self.b_add_fr)

        self.b_add_eng = QPushButton("+")
        self.b_add_eng.metadata = 1
        self.b_add_eng.clicked.connect(self.add_translation_row)
        self.widget_eng = QWidget()
        layout_h_eng = QHBoxLayout(self.widget_eng)
        layout_h_eng.addWidget(QLabel("Inglês"))
        layout_h_eng.addWidget(self.eng_trad)
        layout_h_eng.addWidget(self.b_add_eng)

        self.widget_def = QWidget()
        layout_h_def = QHBoxLayout(self.widget_def)
        layout_h_def.addWidget(QLabel("Nota"))
        layout_h_def.addWidget(self.definition_input)

        self.widget_type = QWidget()
        layout_h_type = QHBoxLayout(self.widget_type)
        layout_h_type.addWidget(QLabel("Tipo"))
        layout_h_type.addWidget(self.type)

        self.form_1.addRow(self.wword)
        self.form_1.addRow(self.widget_fr)
        self.form_1.addRow(self.widget_eng)
        self.form_1.addRow(self.widget_def)
        self.form_1.addRow(self.widget_type)

    def display_input(self):
        sender = self.p.sender()
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        if self.type.currentText() == "verb":
            
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            self.conj4, self.conj5, self.conj6 = QLineEdit(), QLineEdit(), QLineEdit()

            self.conj1.setPlaceholderText("Eu")
            self.conj2.setPlaceholderText("Ele/Ela/Você")
            self.conj3.setPlaceholderText("Eles/Elas/Vocês")
            self.conj4.setPlaceholderText("Eu")
            self.conj5.setPlaceholderText("Ele/Ela/Você")
            self.conj6.setPlaceholderText("Eles/Elas/Vocês")

            self.widget1 = QWidget()
            self.widget1.metadata = None
            layout_h1 = QHBoxLayout(self.widget1)
            layout_h1.addWidget(QLabel("Presente"))
            layout_h1.addWidget(self.conj1)
            layout_h1.addWidget(self.conj2)            
            layout_h1.addWidget(self.conj3)
            self.widget2 = QWidget()
            self.widget2.metadata = None
            layout_h2 = QHBoxLayout(self.widget2)
            layout_h2.addWidget(QLabel("Pretérito Perfeito"))
            layout_h2.addWidget(self.conj4)
            layout_h2.addWidget(self.conj5)
            layout_h2.addWidget(self.conj6)
            self.form_1.insertRow(idx+1, QLabel("Conjugation :"))
            self.form_1.insertRow(idx+2, self.widget1)
            self.form_1.insertRow(idx+3, self.widget2)
            self.flag = 1
        else:
            if self.flag:
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.flag = 0

    def add_translation_row(self):
        sender = self.p.sender()
        i = sender.metadata
        b_rm = QPushButton("-")
        b_rm.metadata = i
        b_rm.clicked.connect(self.rm_translation_row)
        tr_input = QLineEdit()
        widget_tr = QWidget()
        widget_tr.metadata = 3
        layout_h_tr = QHBoxLayout(widget_tr)
        layout_h_tr.addWidget(tr_input)
        layout_h_tr.addWidget(b_rm)
        if self.counter[i] < self.number_of_translations:
            idx, _ = self.form_1.getWidgetPosition(sender.parent())
            self.form_1.insertRow(idx + self.counter[i] + 1, widget_tr)
            self.counter[i] += 1

    def rm_translation_row(self):
        sender = self.p.sender()
        i = sender.metadata
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        self.form_1.removeRow(idx)
        self.counter[i] -= 1
