import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QMainWindow, QVBoxLayout, QLabel,
    QAction, QFileDialog, QApplication, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt


class Editor(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self._fname = ''  # имя редактируемого файла

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        # сетка позиционирования элементов

        self.lbl = QLabel(self)
        # лейбл, на который потом будем передавать pixmap рисунка
        self.layout.addWidget(self.lbl, 0, Qt.AlignCenter)
        # добавление лейбла в сетку с позиционированием по центру

        self.sepia_button = QPushButton('Sepia', self)
        self.layout.addWidget(self.sepia_button)

        self.greyscale_button = QPushButton('Greyscale', self)
        self.layout.addWidget(self.greyscale_button)

        self.negative_button = QPushButton('Negative', self)
        self.layout.addWidget(self.negative_button)

        self.blackwhite_button = QPushButton('Black&White', self)
        self.layout.addWidget(self.blackwhite_button)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 350, 300, 300)
        self.setWindowTitle('Image Editor')

        self.sepia_button.clicked.connect(lambda: self.apply_filter(self._fname, self.sepia))
        self.greyscale_button.clicked.connect(lambda: self.apply_filter(self._fname, self.grayscale))
        self.negative_button.clicked.connect(lambda: self.apply_filter(self._fname, self.negative))
        self.blackwhite_button.clicked.connect(lambda: self.apply_filter(self._fname, self.blackwhite))

        self.show()

    def showDialog(self):

        try:
            self._fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Images (*.png *.jpg)')[0]
        except AttributeError:
            # если в диалоговом окне выбора файла нажато "Отмена"
            pass
        else:
                pixmap = QPixmap(self._fname)
                # self.lbl.resize(300, 300)
                self.lbl.setPixmap(pixmap)

    def apply_filter(self, fname, filter):
        """
        метод для применения и отрисовки фильтра.
        Получает имя файла и метода фильтра
        """
        self._image = Image.open(fname)
        self._draw = ImageDraw.Draw(self._image)
        self._width = self._image.size[0]
        self._height = self._image.size[1]
        self._pix = self._image.load()

        filter(self._image, self._height, self._width, self._pix, self._draw)

        img_tmp = ImageQt(self._image.convert('RGBA'))

        pixmap = QPixmap.fromImage(img_tmp)

        self.lbl.setPixmap(pixmap)

    def sepia(self, image, height, width, pix, draw):

        depth = 30

        for i in range(width):

            for j in range(height):

                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                S = (a + b + c)

                a = S + depth * 2
                b = S + depth

                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255

                draw.point((i, j), (a, b, c))

    def blackwhite(self, image, height, width, pix, draw):

        factor = 50
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                S = a + b + c

                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0

                draw.point((i, j), (a, b, c))

    def negative(self, image, height, width, pix, draw):

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                draw.point((i, j), (255 - a, 255 - b, 255 - c))

    def grayscale(self, image, height, width, pix, draw):

        for i in range(width):
            for j in range(height):

                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                S = (a + b + c) // 3

                draw.point((i, j), (S, S, S))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())
