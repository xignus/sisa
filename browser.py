#!/usr/bin/env python


import sys
import os
import json
from PyQt4 import QtGui, QtCore, QtWebKit, QtNetwork

settings = QtCore.QSettings("matt", "browser")


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget(self,
            tabsClosable=False,
            movable=True,
            elideMode=QtCore.Qt.ElideRight,
            tabCloseRequested=lambda idx:
                self.tabs.widget(idx).deleteLater())
        self.setCentralWidget(self.tabs)
        self.tabWidgets = []
        [self.addTab(QtCore.QUrl(u)) for u in self.get("tabs", [])]
        self.bars = {}

    def finished(self):
        reply = self.sender()
        url = unicode(reply.url().toString())
        bar, _, fname = self.bars[url]
        redirURL = unicode(
            reply.attribute(
                QtNetwork.QNetworkRequest.RedirectionTargetAttribute).\
                    toString())
        del self.bars[url]
        bar.deleteLater()
        if redirURL and redirURL != url:
            return self.fetch(redirURL, fname)
        with open(fname, 'wb') as f:
            f.write(str(reply.readAll()))

    def progress(self, received, total):
        self.bars[unicode(self.sender().url().toString())][0].setValue(
            100. * received / total)

    def closeEvent(self, ev):
        return QtGui.QMainWindow.closeEvent(self, ev)

    def put(self, key, value):
        settings.setValue(key, json.dumps(value))
        settings.sync()

    def get(self, key, default=None):
        v = settings.value(key)
        return json.loads(unicode(v.toString()))\
            if v.isValid() else default

    def addTab(self, url=QtCore.QUrl("")):
        self.tabs.setCurrentIndex(self.tabs.addTab(Tab(url, self), ""))
        return self.tabs.currentWidget()


class Tab(QtWebKit.QWebView):
    def __init__(self, url, container):
        self.container = container
        QtWebKit.QWebView.__init__(self,
            titleChanged=lambda t:
                container.tabs.setTabText(container.tabs.indexOf(self), t) or \
                (container.setWindowTitle(t) if self.amCurrent() else None))
        self.page().setForwardUnsupportedContent(True)


        self.load(url)

    amCurrent = lambda self: self.container.tabs.currentWidget() == self

    def createWindow(self, windowType):
        return self.container.addTab()


def load_web2py():
    """Correr el servidor de web2py"""
    pass


if __name__ == "__main__":
    load_web2py()
    app = QtGui.QApplication(sys.argv)
    wb = MainWindow()
    wb.addTab(QtCore.QUrl('http://127.0.0.1:8000/sisapretty'))
    wb.show()
    sys.exit(app.exec_())
