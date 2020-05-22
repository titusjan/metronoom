#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets

LABEL_STOP = "Stop"
LABEL_START = "Start"

class MyWidget(QtWidgets.QWidget):

    def __init__(self, periodSec, parent=None):
        super().__init__(parent=parent)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.controlLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.controlLayout)

        self.periodSpinbox = QtWidgets.QDoubleSpinBox()
        self.periodSpinbox.setDecimals(1)
        self.periodSpinbox.setMinimum(0.1)
        self.periodSpinbox.setMaximum(1000.0)
        self.periodSpinbox.setValue(periodSec)
        self.periodSpinbox.valueChanged.connect(self.onPeriodChanged)
        self.controlLayout.addWidget(self.periodSpinbox)

        self.startStopButton = QtWidgets.QPushButton(LABEL_STOP)
        self.startStopButton.clicked.connect(self.onPauseButtonClicked)
        self.controlLayout.addWidget(self.startStopButton)

        self.label = QtWidgets.QLabel()
        self.mainLayout.addWidget(self.label)

        self.mainTimer = QtCore.QTimer()
        self.mainTimer.setInterval(int(self.periodSpinbox.value() * 1000))
        self.mainTimer.timeout.connect(self.onTimeout)
        self.mainTimer.start()

        self.labelTimer = QtCore.QTimer()
        self.labelTimer.setInterval(int(100))
        self.labelTimer.timeout.connect(self.updateLabel)
        self.labelTimer.start()


    def onPeriodChanged(self, period):
        print("Setting period: {}".format(period))
        self.mainTimer.stop()
        self.mainTimer.setInterval(int(period * 1000))
        self.mainTimer.start()


    def onTimeout(self):
        print("----- RESET THE COUNTER ----")
        QtWidgets.qApp.beep()


    def updateLabel(self):
        self.label.setText("{:.1f} seconds".format(self.mainTimer.remainingTime() / 1000))


    def onPauseButtonClicked(self, _):

        if self.startStopButton.text() == LABEL_STOP:
            print("Stopping timer")
            self.mainTimer.stop()
            self.labelTimer.stop()
            self.startStopButton.setText(LABEL_START)
        else:
            print("Starting timer")
            self.mainTimer.start()
            self.labelTimer.start()
            self.startStopButton.setText(LABEL_STOP)


def main():
    app = QtWidgets.QApplication([])
    
    win = MyWidget(5.0)
    win.show()
    win.raise_()
    app.exec_()
    
if __name__ == "__main__":
    main()
