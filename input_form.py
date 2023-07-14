from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import config

class InputForm():
    def __init__(self, parent, form) -> None:
        self.p = parent
        self.form_1 = form
        self.number_of_translations = 3
        self.counter = [0, 0]

        self.word, self.fr_trad, self.notes_input = QLineEdit(), QLineEdit(), QPlainTextEdit()
        self.type = QComboBox()
        self.type.addItems(["nom féminin", "nom masculin", config.VERB, "adjectif", "autre"])
        self.flag = 0
        self.wword = QWidget()
        layout_h_w = QHBoxLayout(self.wword)
        layout_h_w.addWidget(QLabel(config.LEARNED_LANGUAGED))
        layout_h_w.addWidget(self.word)

        self.b_add_fr = QPushButton("+")
        self.b_add_fr.metadata = 0
        self.b_add_fr.clicked.connect(self.add_translation_row)
        self.widget_fr = QWidget()
        layout_h_fr = QHBoxLayout(self.widget_fr)
        layout_h_fr.addWidget(QLabel(config.KNOWN_LANGUAGED))
        layout_h_fr.addWidget(self.fr_trad)
        layout_h_fr.addWidget(self.b_add_fr)

        self.widget_notes = QWidget()
        layout_h_notes = QHBoxLayout(self.widget_notes)
        layout_h_notes.addWidget(QLabel(config.NOTES))
        layout_h_notes.addWidget(self.notes_input)

        self.widget_type = QWidget()
        layout_h_type = QHBoxLayout(self.widget_type)
        layout_h_type.addWidget(QLabel(config.TYPE))
        layout_h_type.addWidget(self.type)

        self.form_1.addRow(self.wword)
        self.form_1.addRow(self.widget_fr)
        self.form_1.addRow(self.widget_notes)
        self.form_1.addRow(self.widget_type)

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
