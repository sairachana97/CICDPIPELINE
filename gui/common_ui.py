from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction


def add_actions_to_toolbar(toolbar, self):
    
    self.flexible_space = QtWidgets.QWidget()
    self.flexible_space.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    toolbar.addWidget(self.flexible_space)
    go_back_button = QAction(QIcon(":/menu/goback.png"), "Go Back Button",self)
    home_button =  QAction(QIcon(":/menu/download.png"), "Home Button",self)
    toolbar.addAction(go_back_button)
    toolbar.addAction(home_button)
    return toolbar, go_back_button, home_button
  
    
    