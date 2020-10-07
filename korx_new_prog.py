# Импорты библиотеки PyQt5 для интерфейса
from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport
from PyQt5.QtCore import QTranslator, QLocale

# Импорты необходимых библиотек
import collections
import datetime
import time
import sys
import pathlib

# Импрты окон интерфейса
from korxNew_v4 import Ui_MainWindow
from screws import Ui_Form as UF
from show_table import Ui_Dialog as UD_table

# Импорт мат. модели
import math_model

# Импорт ресурсного файла
# (тут написано что он не используется, не верь этому!!! Еще как используется!)
import source_rc

I18N_QT_PATH = ':/translations/translations/'  # Путь к файлам с переводами

set_log = 'TestBox.txt'
buttons_set = 'Buttons_Set.txt'

class FormTable(QtWidgets.QDialog):
    """Формирует таблицу с результатами"""
    def __init__(self, parent, sets, results, colib):
        super().__init__(parent=None)
        self.ui = UD_table()
        self.ui.setupUi(self)
        self.ui.tbl_btn_print.clicked.connect(self.print_table)
        self.ui.tbl_btn_save.clicked.connect(self.print_to_file_table)

        self.ui.tbl_Dvp.setText(sets['self.Dp_f'])
        self.ui.tbl_Dz.setText(sets['self.Dz_f'])
        self.ui.tbl_Dg.setText(sets['self.Dg_f'])
        self.ui.tbl_Dopr.setText(sets['self.Dopr_f'])
        self.ui.tbl_Lz.setText(sets['self.Lz_f'])
        self.ui.tbl_Lopr.setText(sets['self.Lopr_f'])
        self.ui.tbl_dg.setText(sets['self.dg_f'])
        self.ui.tbl_Sg.setText(sets['self.Sg_f'])
        self.ui.tbl_beta.setText(sets['self.beta_f'])
        self.ui.tbl_fi.setText(sets['self.fee_f'])

        self.ui.tbl_a.setText(str("%.2f" % results['a']))
        self.ui.tbl_b.setText(str("%.2f" % results['b']))
        self.ui.tbl_Een.setText(str("%.2f" % results['En']))
        self.ui.tbl_c.setText(str("%.2f" % results['c']))
        self.ui.tbl_En.setText(str("%.2f" % results['Ep']))
        self.ui.tbl_mu.setText(str("%.2f" % results['mu']))
        self.ui.tbl_Dvh.setText(str("%.2f" % results['Dvh']))
        self.ui.tbl_Dvih.setText(str("%.2f" % results['Dvih']))
        self.ui.tbl_ksi.setText(str("%.2f" % results['ksi']))
        self.ui.tbl_GF.setText(str("%.2f" % results['GF']))
        self.ui.tbl_Lg.setText(str("%.2f" % results['Lr']))

        self.ui.tbl_chart_a.setText(str("%.2f" % results['a']))
        self.ui.tbl_chart_b.setText(str("%.2f" % results['b']))
        self.ui.tbl_chart_c.setText(str("%.2f" % results['c']))
        self.ui.tbl_chart_Dg.setText(sets['self.Dg_f'])
        self.ui.tbl_chart_Dopr.setText(sets['self.Dopr_f'])
        self.ui.tbl_chart_Dz.setText(sets['self.Dz_f'])
        self.ui.tbl_chart_Lopr.setText(sets['self.Lopr_f'])
        self.ui.tbl_chart_Sg.setText(sets['self.Sg_f'])
        self.ui.tbl_chart_X1.setText(str("%.2f" % results['X1']))
        self.ui.tbl_L.setText(str("%.2f" % results['L']))

        if results['IO1'] == 'Нет':  # Смотрит есть винты или нет
            self.ui.tbl_screws.setText(f"{str('%.1f' % results['IO2'])} - {str('%.1f' % results['IO2'])}")
        else:
            self.ui.tbl_screws.setText(f"{str('%.1f' % results['IO1'])} - {str('%.1f' % results['IO1'])}")

        self.ui.tbl_button.setText(f'{colib}')  # Ставит текст с калибром
        month = f'0{datetime.date.today().month}' if datetime.date.today().month < 10 else datetime.date.today().month
        self.ui.tbl_date.setText(
            f'{datetime.date.today().day}.{month}.{datetime.date.today().year}'
        )
        self.ui.label_Dvp_13.setText(f"Длина заготовки Lз, мм/{sets['self.factor_f']}")

        if len(results['err']) != 0:  # Если ошибка то делает это...
            # self.ui.tbl_chart_cross.setWindowOpacity(0.3)
            # self.ui.tbl_chart_cross = QtGui.QPixmap(":/images/red-x-mark-png.png")
            # self.ui.tbl_chart_cross.setPixmap(QtGui.QPixmap(":/images/red-x-mark-png.png"))

            new_pix = QtGui.QPixmap(531, 471)
            new_pix.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(new_pix)
            painter.setOpacity(0.5)
            painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(":/images/red-x-mark-png.png"))
            painter.end()
            self.ui.tbl_chart_cross.setPixmap(new_pix)
            self.ui.tbl_chart_cross.setScaledContents(True)

            self.ui.tbl_chart_err_msg.setText(
                '<html>'
                '<head/>'
                '<body>'
                '<p align="center">'
                '<span style=" font-size:16pt; color:#aa0000;">Некорректный расчет!!!</span>'
                '</p>'
                '</body>'
                '</html>'
            )

            self.msg_table = collections.deque()
            for i in results['err']:
                self.msg_table.appendleft('<p style="color:#840000;">' + \
                                          i \
                                          + '</p>\n')
            self.ui.tbl_chart_err_description.setText(''.join(self.msg_table))
            self.ui.tbl_chart_err_description.setWordWrap(True)
            self.ui.tbl_chart_err_description.setAlignment(QtCore.Qt.AlignLeft)
        else:  # Если нет ошибки то это
            new_pix = QtGui.QPixmap(531, 471)
            new_pix.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(new_pix)
            painter.setOpacity(0)
            painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(":/images/red-x-mark-png.png"))
            painter.end()
            self.ui.tbl_chart_cross.setPixmap(new_pix)
            self.ui.tbl_chart_cross.setScaledContents(True)

            self.ui.tbl_chart_err_msg.setText("")
            self.ui.tbl_chart_err_description.setText("")

    def print_table(self):  # Распечатывает все
        printer = QtPrintSupport.QPrinter()
        printer.setPageOrientation(QtGui.QPageLayout.Landscape)
        painter = QtGui.QPainter()
        self.editor = self.ui.tbl_main_widget
        painter.begin(printer)
        painter.scale(0.8, 0.8)
        screen = self.editor.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()

    def print_to_file_table(self):  # Выводит в pdf
        printer = QtPrintSupport.QPrinter()
        printer.setPageOrientation(QtGui.QPageLayout.Landscape)
        f_name = f'out_{datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")}.pdf'
        printer.setOutputFileName(f_name)
        painter = QtGui.QPainter()
        self.editor = self.ui.tbl_main_widget
        painter.begin(printer)
        painter.scale(0.8, 0.8)
        screen = self.editor.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()



class Screws:
    """Класс для настроек винтов"""
    def __init__(self):
        self.__screws = []

    def update_screws(self, screws_list):
        """Обновляет винты"""
        self.__screws = screws_list

    def get_screws(self):
        """Возвращает винты"""
        return self.__screws


class ScrewsDialog(QtWidgets.QDialog):
    """Диалоговое окно с вводом настр параметров винтов"""
    def __init__(self, parent, screws):
        super().__init__(parent=None)
        self.ui = UF()
        self.ui.setupUi(self)
        self.loc_screws = screws

        self.ui.sc_btn_cancel.clicked.connect(self.close)
        self.ui.sc_btn_ok.clicked.connect(self.acceptd)

    def acceptd(self):  # Если нажать Ок
        self.inp_RPNV_IO = self.ui.inp_RPNV_IO.value()
        self.inp_RPNV_Dvp = self.ui.inp_RPNV_Dvp.value()
        self.inp_RPNV_a = self.ui.inp_RPNV_a.value()

        if self.inp_RPNV_IO != 0 and self.inp_RPNV_Dvp != 0 and self.inp_RPNV_a != 0:
            self.loc_screws.update_screws([self.inp_RPNV_IO, self.inp_RPNV_Dvp, self.inp_RPNV_a])
            # MainProcess.screws = [self.inp_RPNV_IO, self.inp_RPNV_Dvp, self.inp_RPNV_a]
        self.close()

    def get_screws(self):  # Это вроде ненужный кусок
        return self.scr




class MainProcess(QtWidgets.QMainWindow):
    """Основной класс, тут описано все основное поведение программы"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создание основных данных и сущностей
        self.screws = Screws()
        self.colib = ''
        self.button_name = ''
        self.results = {}
        self.sets = {}
        self.c_corr = 0
        self.button_sets = {  # Xa - это корректировка угла подачи
            "K212": {
                'inp_Dvp': 1197.86,
                'inp_l12': 153.03,
                'inp_Lvx': 478.03,
                'inp_a11': 2,
                'inp_lvix': 534.05,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 2.5,
                'inp_m': 9.05,
                'inp_fi': 0,
                'cB_inp_beta': '11',
                'inp_Lcmech': 70,
                'inp_L2': 334.33,
                'inp_gamma1': 3,
                'inp_gamma2': 3,
                'cB_inp_dz': '260',
                'inp_Dr': 262,
                'c_corr': 26.97,
                "Xa": 0,
                "Lcu": 20,
            },  #
            "K360": {
                'inp_Dvp': 1197.44,
                'inp_l12': 149.53,
                'inp_Lvx': 474.53,
                'inp_a11': 2,
                'inp_lvix': 537.54,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 3,
                'inp_m': 12.54,
                'inp_fi': 0,
                'cB_inp_beta': '09',
                'inp_Lcmech': 60,
                'inp_L2': 384,
                'inp_gamma1': 4,
                'inp_gamma2': 2.5,
                'cB_inp_dz': '410',
                'inp_Dr': 421,
                'c_corr': 30.47,
                "Xa": 0.5,
                "Lcu": 20,
            },   #
            "K255_K260": {
                'inp_Dvp': 1197.86,
                'inp_l12': 153.03,
                'inp_Lvx': 478.03,
                'inp_a11': 2,
                'inp_lvix': 534.05,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 2.5,
                'inp_m': 9.05,
                'inp_fi': 0.6,
                'cB_inp_beta': '10',
                'inp_Lcmech': 0,
                'inp_L2': 420,
                'inp_gamma1': 5,
                'inp_gamma2': 3,
                'cB_inp_dz': '340',
                'inp_Dr': 314,
                'c_corr': 26.97,
                "Xa": 0,
                "Lcu": 20,
            },   #
            "K270": {
                'inp_Dvp': 1197.86,
                'inp_l12': 153.03,
                'inp_Lvx': 478.03,
                'inp_a11': 2,
                'inp_lvix': 534.05,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 2.5,
                'inp_m': 9.05,
                'inp_fi': 0,
                'cB_inp_beta': '10',
                'inp_Lcmech': 0,
                'inp_L2': 420,
                'inp_gamma1': 5,
                'inp_gamma2': 3,
                'cB_inp_dz': '340',
                'inp_Dr': 323,
                'c_corr': 26.97,
                "Xa": 0.5,
                "Lcu": 20,
            },  #
            "K435_K444": {
                'inp_Dvp': 1194.86,
                'inp_l12': 128.53,
                'inp_Lvx': 373.53,
                'inp_a11': 2,
                'inp_lvix': 638.55,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 6,
                'inp_m': 113.55,
                'inp_fi': 0,
                'cB_inp_beta': '08',
                'inp_Lcmech': -110,
                'inp_L2': 576,
                'inp_gamma1': 4,
                'inp_gamma2': 6,
                'cB_inp_dz': '410',
                'inp_Dr': 500,
                'c_corr': 31.41,
                "Xa": 0,
                "Lcu": 20,
            },  #
            "K288": {
                'inp_Dvp': 1197.86,
                'inp_l12': 153.03,
                'inp_Lvx': 478.03,
                'inp_a11': 2,
                'inp_lvix': 534.05,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 2.5,
                'inp_m': 9.05,
                'inp_fi': 0,
                'cB_inp_beta': '10',
                'inp_Lcmech': 0,
                'inp_L2': 420,
                'inp_gamma1': 5,
                'inp_gamma2': 3,
                'cB_inp_dz': '340',
                'inp_Dr': 344,
                'c_corr': 26.97,
                "Xa": 0.5,
                "Lcu": 20,
            },   #
            "K372": {
                'inp_Dvp': 1197.44,
                'inp_l12': 149.53,
                'inp_Lvx': 474.53,
                'inp_a11': 2,
                'inp_lvix': 537.54,
                'inp_a12': 3.5,
                'inp_k': 27.92,
                'inp_a2': 3,
                'inp_m': 12.54,
                'inp_fi': 0,
                'cB_inp_beta': '09',
                'inp_Lcmech': 60,
                'inp_L2': 384,
                'inp_gamma1': 4,
                'inp_gamma2': 2.5,
                'cB_inp_dz': '410',
                'inp_Dr': 431,
                'c_corr': 30.47,
                "Xa": 0.5,
                "Lcu": 20,
            },  #
            "K360*": {
                'inp_Dvp': 1200.0,
                'inp_l12': 160,
                'inp_Lvx': 405,
                'inp_a11': 2,
                'inp_lvix': 635,
                'inp_a12': 3.5,
                'inp_k': 0,
                'inp_a2': 6,
                'inp_m': 110,
                'inp_fi': 0,
                'cB_inp_beta': '10',
                'inp_Lcmech': -10,
                'inp_L2': 474,
                'inp_gamma1': 3.5,
                'inp_gamma2': 6.5,
                'cB_inp_dz': '360',
                'inp_Dr': 421,
                'c_corr': 0,
                "Xa": 0,
                "Lcu": 20,
            },
            "K372*": {
                'inp_Dvp': 1200.0,
                'inp_l12': 160,
                'inp_Lvx': 405,
                'inp_a11': 2,
                'inp_lvix': 635,
                'inp_a12': 3.5,
                'inp_k': 0,
                'inp_a2': 6,
                'inp_m': 110,
                'inp_fi': 0,
                'cB_inp_beta': '10',
                'inp_Lcmech': -10,
                'inp_L2': 474,
                'inp_gamma1': 3.5,
                'inp_gamma2': 6.5,
                'cB_inp_dz': '360',
                'inp_Dr': 431,
                'c_corr': 0,
                "Xa": 0,
                "Lcu": 20,
            },
            "temp_koeff": 1,
        }
        self.punch_sets = {
            "K212": {
                "Dopr": ["", 205, 201, 199, 196, 193, 189, 184, 179, 175, 169],
                "Lopr": ["", 485],
            },
            "K360": {
                "Dopr": ["", 350, 345, 340, 335, 330, 323, 320, 315, 310, 305, 300, 294],
                "Lopr": ["", 700],
            },
            "K255_K260": {
                "Dopr": ["", 247, 243, 238, 234, 228, 223, 221, 218, 213, 205, 201, 199, 196],
                "Lopr": ["", 520, 485],
            },
            "K270": {
                "Dopr": ["", 272, 266, 263, 258, 253, 247, 243, 238, 234, 228, 223, 221, 218, 213],
                "Lopr": ["", 520],
            },
            "K435_K444": {
                "Dopr": ["", 420, 416, 412, 410, 407, 402, 396, 389, 382, 378, 376],
                "Lopr": ["", 775],
            },
            "K288": {
                "Dopr": ["", 272, 266, 263, 258, 253, 247, 243, 238, 234, 228, 223, 221, 218, 213],
                "Lopr": ["", 520],
            },
            "K372": {
                "Dopr": ["", 350, 345, 340, 335, 330, 323, 315, 310, 305, 300, 294],
                "Lopr": ["", 700],
            },
            "K360*": {
                "Dopr": ["", 360, 356, 352, 350, 348, 345, 342, 337, 331, 325, 319, 313, 307, 301],
                "Lopr": ["", 730],
            },
            "K372*": {
                "Dopr": ["", 360, 356, 352, 350, 348, 345, 342, 337, 331, 325, 319, 313, 307, 301],
                "Lopr": ["", 730],
            },
        }
        self.ui.inp_Lrab.setReadOnly(True)

        # Установка спотеров для контроля автопересчетов
        self.spotter = 0
        self.anti_clear = 1
        self.counted = 0
        self.ui.K212_btn.clicked.connect(self.K212_choose)
        self.ui.K360_btn.clicked.connect(self.K360_choose)
        self.ui.K255_K260_btn.clicked.connect(self.K255_K260_choose)
        self.ui.K372_btn.clicked.connect(self.K372_choose)
        self.ui.K270_btn.clicked.connect(self.K270_choose)
        self.ui.K435_K444_btn.clicked.connect(self.K435_K444_choose)
        self.ui.K288_btn.clicked.connect(self.K288_choose)
        self.ui.K360_UPRAIS_btn.clicked.connect(self.K360_UPRAIS_choose)
        self.ui.K372_UPRAIS_btn.clicked.connect(self.K372_UPRAIS_choose)
        self.ui.K_clear_btn.clicked.connect(self.K_clear_choose)
        # self.K_clear_choose()
        self.ui.Coun_btn.clicked.connect(self.count_main)
        self.ui.FormTable_btn.clicked.connect(self.form_table)

        self.ui.FormTable_btn.setDisabled(True)

        # GPON radio buttons changed Главные радио кнопки в части с результатами
        self.ui.radio_GPOD_roolsDistance.clicked.connect(self.GPOD_change_rools)
        self.ui.radio_GPOD_pitchReduction.clicked.connect(self.GPOD_change_pitch)

        # Srdr radio buttons changed Толщина стенки или внутренний диаметр
        self.ui.radio_Sr.clicked.connect(self.Srdr_change_Sr)
        self.ui.radio_dr.clicked.connect(self.Srdr_change_dr)

        self.ui.btn_screws.clicked.connect(self.screws_set)

        # Событие при запуске
        self.turned_on()

        # Srdr_recount Пересчет внутреннего диаметра от толщины и наоборот

        self.ui.inp_radio_Sr.valueChanged.connect(self.Sr_val_change)
        self.ui.inp_radio_dr.valueChanged.connect(self.dr_val_change)
        self.ui.inp_Dr.valueChanged.connect(self.Dr_val_change)

        # Включение выключение b, c, ksi
        # self.ui.checkBox_label_GPOD_c.setDisabled(True)
        self.ui.checkBox_label_GPOD_ksi.stateChanged.connect(self.use_ksi)
        self.ui.checkBox_label_GPOD_b.stateChanged.connect(self.use_b)
        self.ui.checkBox_label_GPOD_c.stateChanged.connect(self.use_c)

        # Споттеры всех влияющих на автопересчет параметров
        self.recount_spotter_a = 1
        self.recount_spotter_En = 1
        self.recount_spotter_ksi = 1
        self.recount_spotter_b = 1
        self.recount_spotter_c = 1
        self.ui.inOut_GPOD_a.valueChanged.connect(self.recount_all_change_a)
        self.ui.inOut_GPOD_En.valueChanged.connect(self.recount_all_change_En)
        self.ui.inOut_GPOD_ksi.valueChanged.connect(self.recount_all_change_ksi)
        self.ui.inOut_GPOD_b.valueChanged.connect(self.recount_all_change_b)
        self.ui.inOut_GPOD_c.valueChanged.connect(self.recount_all_change_c)

        # Сообщение об ошибке в виде очереди
        self.msg = collections.deque()

        # Споттер пересчета ksi
        self.ksi_spotter = 0
        # self.ui.inOut_GPOD_ksi.valueChanged.connect(self.ksi_change)

        self.ui.checkBox_label_GPOD_ksi.setDisabled(True)
        self.ui.checkBox_label_GPOD_b.setDisabled(True)
        self.ui.checkBox_label_GPOD_c.setDisabled(True)

        self.ui.Coun_btn.setDisabled(True)
        self.ui.inOut_GPOD_a.setDisabled(True)
        self.ui.inOut_GPOD_En.setDisabled(True)
        self.input_event()
        self.ui.inp_dopr.currentTextChanged.connect(self.input_event)
        self.ui.inp_Lopr.currentTextChanged.connect(self.input_event)
        self.ui.inp_radio_Sr.valueChanged.connect(self.input_event)
        self.ui.inOut_GPOD_a.valueChanged.connect(self.input_event)

    def input_event(self):
        """Когда что то вводят"""
        check_Dopr = float(self.ui.inp_dopr.currentText().replace(",", ".")) if self.ui.inp_dopr.currentText().find(
            ",") != -1 else 0 if self.ui.inp_dopr.currentText() == "" else float(self.ui.inp_dopr.currentText())
        check_Lopr = float(self.ui.inp_Lopr.currentText().replace(",", ".")) if self.ui.inp_Lopr.currentText().find(
            ",") != -1 else 0 if self.ui.inp_Lopr.currentText() == "" else float(self.ui.inp_Lopr.currentText())

        if self.ui.radio_GPOD_roolsDistance.isChecked():
            if check_Dopr != 0 and check_Lopr != 0 and self.ui.inp_radio_Sr.value() != 0:
                self.ui.inOut_GPOD_a.setDisabled(False)
            else:
                self.ui.inOut_GPOD_a.setDisabled(True)

            if check_Dopr != 0 and check_Lopr != 0 and self.ui.inp_radio_Sr.value() != 0 and self.ui.inOut_GPOD_a.value() != 0:
                self.ui.Coun_btn.setDisabled(False)
            else:
                self.ui.Coun_btn.setDisabled(True)
                self.ui.FormTable_btn.setDisabled(True)

        else:
            if check_Dopr != 0 and check_Lopr != 0 and self.ui.inp_radio_Sr.value() != 0:
                self.ui.inOut_GPOD_En.setDisabled(False)
            else:
                self.ui.inOut_GPOD_En.setDisabled(True)

            if check_Dopr != 0 and check_Lopr != 0 and self.ui.inp_radio_Sr.value() != 0 and self.ui.inOut_GPOD_En.value() != 0:
                self.ui.Coun_btn.setDisabled(False)
            else:
                self.ui.Coun_btn.setDisabled(True)
                self.ui.FormTable_btn.setDisabled(True)




    def form_table(self):
        """Создание таблицы результатов, создает экземпляр класса FormTable"""
        table = FormTable(self, self.sets, self.results, self.colib)
        table.exec_()

    def use_b(self):
        """Если отметить b"""
        if self.ui.checkBox_label_GPOD_b.isChecked():
            # self.ui.checkBox_label_GPOD_c.setDisabled(False)
            self.ui.checkBox_label_GPOD_ksi.setChecked(False)
            self.ui.checkBox_label_GPOD_ksi.setDisabled(True)
            self.ui.inOut_GPOD_b.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            self.ui.inOut_GPOD_b.setReadOnly(False)
            self.ui.inOut_GPOD_b.setStyleSheet("background-color: #C0C0FF; color: black;")
        else:
            # self.ui.checkBox_label_GPOD_c.setChecked(False)
            # self.ui.checkBox_label_GPOD_c.setDisabled(True)
            self.ui.checkBox_label_GPOD_ksi.setDisabled(False)
            self.ui.inOut_GPOD_b.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            self.ui.inOut_GPOD_b.setReadOnly(True)
            self.ui.inOut_GPOD_b.setStyleSheet("")

    def use_c(self):
        """Если отметить c"""
        if self.ui.checkBox_label_GPOD_c.isChecked():
            self.ui.inOut_GPOD_c.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            self.ui.inOut_GPOD_c.setReadOnly(False)
            self.ui.inOut_GPOD_c.setStyleSheet("background-color: #C0C0FF; color: black;")
        else:
            # self.ui.checkBox_label_GPOD_ksi.setDisabled(False)
            self.ui.inOut_GPOD_c.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            self.ui.inOut_GPOD_c.setReadOnly(True)
            self.ui.inOut_GPOD_c.setStyleSheet("")

    def use_ksi(self):
        """Если отметить ksi"""
        if self.ui.checkBox_label_GPOD_ksi.isChecked():
            self.ui.checkBox_label_GPOD_c.setDisabled(False)
            # self.ui.inOut_GPOD_ksi.setDisabled(False)
            self.ui.checkBox_label_GPOD_b.setDisabled(True)
            self.ui.inOut_GPOD_ksi.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            self.ui.inOut_GPOD_ksi.setReadOnly(False)
            self.ui.inOut_GPOD_ksi.setStyleSheet("background-color: #C0C0FF; color: black;")
        else:
            self.ui.checkBox_label_GPOD_c.setChecked(False)
            self.ui.checkBox_label_GPOD_c.setDisabled(False)
            # self.ui.inOut_GPOD_ksi.setDisabled(True)
            self.ui.inOut_GPOD_ksi.setReadOnly(True)
            self.ui.inOut_GPOD_ksi.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            self.ui.checkBox_label_GPOD_b.setDisabled(False)
            self.ui.inOut_GPOD_ksi.setStyleSheet("")

    def ksi_change(self):
        """Если изменить ksi"""
        if self.ksi_spotter != 0:
            self.ui.inOut_GPOD_a.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_b.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_c.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_En.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_ksi.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_Een.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_Lr.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_mu.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_GF.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_Dvx.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_Dvix.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_L.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_X1.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_X2.setStyleSheet('background-color: yellow;')
            self.ui.inOut_GPOD_Lod.setStyleSheet('background-color: yellow;')

    def recount_all_change_a(self):
        """Полный пересчет при изменении a"""
        if self.recount_spotter_a == 0:
            # self.recount_spotter_a = 1
            self.recount_spotter_En = 1
            self.recount_spotter_ksi = 1
            self.recount_spotter_b = 1
            self.recount_spotter_c = 1

            self.count_main()
        else:
            self.recount_spotter_a = 0

    def recount_all_change_En(self):
        """Полный пересчет при изменении En"""
        if self.recount_spotter_En == 0:
            self.recount_spotter_a = 1
            # self.recount_spotter_En = 1
            self.recount_spotter_ksi = 1
            self.recount_spotter_b = 1
            self.recount_spotter_c = 1

            self.count_main()
        else:
            self.recount_spotter_En = 0

    def recount_all_change_ksi(self):
        """Полный пересчет при изменении ksi"""
        if self.recount_spotter_ksi == 0:
            self.recount_spotter_a = 1
            self.recount_spotter_En = 1
            # self.recount_spotter_ksi = 1
            self.recount_spotter_b = 1
            self.recount_spotter_c = 1

            self.count_main()
        else:
            self.recount_spotter_ksi = 0

    def recount_all_change_b(self):
        """Полный пересчет при изменении b"""
        if self.recount_spotter_b == 0:
            self.recount_spotter_a = 1
            self.recount_spotter_En = 1
            self.recount_spotter_ksi = 1
            # self.recount_spotter_b = 1
            self.recount_spotter_c = 1

            self.count_main()
        else:
            self.recount_spotter_b = 0

    def recount_all_change_c(self):
        """Полный пересчет при изменении c"""
        if self.recount_spotter_c == 0:
            self.recount_spotter_a = 1
            self.recount_spotter_En = 1
            self.recount_spotter_ksi = 1
            self.recount_spotter_b = 1
            # self.recount_spotter_c = 1

            self.count_main()
        else:
            self.recount_spotter_c = 0

    def Dr_val_change(self):
        """Диаметр гильзы изменен"""
        if self.ui.radio_Sr.isChecked():
            if self.spotter == 0 and self.ui.inp_Dr.value() > self.ui.inp_radio_Sr.value():
                self.spotter = 1

                self.ui.inp_radio_dr.setValue(self.ui.inp_Dr.value() - self.ui.inp_radio_Sr.value() * 2)
            else:
                self.spotter = 0
        else:
            if self.spotter == 0 and self.ui.inp_Dr.value() > self.ui.inp_radio_dr.value():
                self.spotter = 1

                self.ui.inp_radio_Sr.setValue((self.ui.inp_Dr.value() - self.ui.inp_radio_dr.value()) / 2)
            else:
                self.spotter = 0

    def Sr_val_change(self):
        """Толщина стенки гильзы изменена"""
        if self.spotter == 0:
            self.spotter = 1

            self.ui.inp_radio_dr.setValue(self.ui.inp_Dr.value() - self.ui.inp_radio_Sr.value() * 2)
        else:
            self.spotter = 0

    def dr_val_change(self):
        """Внутренний диаметр гильзы изменен"""
        if self.spotter == 0:
            self.spotter = 1

            self.ui.inp_radio_Sr.setValue((self.ui.inp_Dr.value() - self.ui.inp_radio_dr.value()) / 2)
        else:
            self.spotter = 0

    def screws_set(self):
        """При нажатии кнопки с винтами создается и запускается экземпляр класса ScrewsDialog"""
        self.ui.FormTable_btn.setDisabled(True)
        widget_screws_set = ScrewsDialog(self, self.screws)
        widget_screws_set.exec_()

    def K212_choose(self):
        """Выбор калибра К212"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K212_btn
        self.button_name = self.ui.K212_btn.text()
        self.colib = 'K212'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K212"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K212"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K212']['Lcu']
        self.Xa = self.button_sets['K212']['Xa']
        self.c_corr = self.button_sets['K212']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K212']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K212']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K212']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K212']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K212']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K212']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K212']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K212']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K212']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K212']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K212']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K212']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K212']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K212']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K212']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K212']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K212']['inp_Dr'])

    def K360_choose(self):
        """Выбор калибра К360"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K360_btn
        self.button_name = self.ui.K360_btn.text()
        self.colib = 'K360'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K360"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K360"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K360']['Lcu']
        self.Xa = self.button_sets['K360']['Xa']
        self.c_corr = self.button_sets['K360']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K360']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K360']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K360']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K360']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K360']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K360']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K360']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K360']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K360']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K360']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K360']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K360']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K360']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K360']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K360']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K360']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K360']['inp_Dr'])

    def K255_K260_choose(self):
        """Выбор калибра К255-К260"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K255_K260_btn
        self.button_name = self.ui.K255_K260_btn.text()
        self.colib = 'K255/K260'
        self.color_btn()
        self.ui.radio_closeExit.setChecked(True)

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K255_K260"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K255_K260"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K255_K260']['Lcu']
        self.Xa = self.button_sets['K255_K260']['Xa']
        self.c_corr = self.button_sets['K255_K260']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K255_K260']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K255_K260']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K255_K260']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K255_K260']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K255_K260']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K255_K260']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K255_K260']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K255_K260']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K255_K260']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K255_K260']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K255_K260']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K255_K260']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K255_K260']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K255_K260']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K255_K260']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K255_K260']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K255_K260']['inp_Dr'])

    def K372_choose(self):
        """Выбор калибра К372"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K372_btn
        self.button_name = self.ui.K372_btn.text()
        self.colib = 'K372'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K372"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K372"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K372']['Lcu']
        self.Xa = self.button_sets['K372']['Xa']
        self.c_corr = self.button_sets['K372']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K372']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K372']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K372']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K372']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K372']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K372']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K372']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K372']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K372']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K372']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K372']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K372']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K372']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K372']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K372']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K372']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K372']['inp_Dr'])

    def K270_choose(self):
        """Выбор калибра К270"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K270_btn
        self.button_name = self.ui.K270_btn.text()
        self.colib = 'K270'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K270"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K270"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K270']['Lcu']
        self.Xa = self.button_sets['K270']['Xa']
        self.c_corr = self.button_sets['K270']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K270']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K270']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K270']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K270']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K270']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K270']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K270']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K270']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K270']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K270']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K270']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K270']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K270']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K270']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K270']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K270']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K270']['inp_Dr'])

    def K435_K444_choose(self):
        """Выбор калибра К435-К444"""
        if self.anti_clear != 0:
            self.K_clear_choose()
        self.chosen_btn = self.ui.K435_K444_btn
        self.button_name = self.ui.K435_K444_btn.text()
        self.colib = 'K435/K444'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K435_K444"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K435_K444"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K435_K444']['Lcu']
        self.Xa = self.button_sets['K435_K444']['Xa']
        self.c_corr = self.button_sets['K435_K444']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K435_K444']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K435_K444']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K435_K444']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K435_K444']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K435_K444']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K435_K444']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K435_K444']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K435_K444']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K435_K444']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K435_K444']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K435_K444']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K435_K444']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K435_K444']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K435_K444']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K435_K444']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K435_K444']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K435_K444']['inp_Dr'])

    def K288_choose(self):
        """Выбор калибра К288"""
        if self.anti_clear != 0:
            self.K_clear_choose()

        self.chosen_btn = self.ui.K288_btn
        self.button_name = self.ui.K288_btn.text()
        self.colib = 'K288'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K288"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K288"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K288']['Lcu']
        self.Xa = self.button_sets['K288']['Xa']
        self.c_corr = self.button_sets['K288']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K288']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K288']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K288']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K288']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K288']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K288']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K288']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K288']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K288']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K288']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K288']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K288']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K288']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K288']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K288']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K288']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K288']['inp_Dr'])

    def K360_UPRAIS_choose(self):
        """Выбор калибра К360*"""
        if self.anti_clear != 0:
            self.K_clear_choose()

        self.chosen_btn = self.ui.K360_UPRAIS_btn
        self.button_name = self.ui.K360_UPRAIS_btn.text()
        self.colib = 'K360*'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K360*"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K360*"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K360*']['Lcu']
        self.Xa = self.button_sets['K360*']['Xa']
        self.c_corr = self.button_sets['K360*']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K360*']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K360*']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K360*']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K360*']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K360*']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K360*']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K360*']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K360*']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K360*']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K360*']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K360*']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K360*']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K360*']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K360*']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K360*']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K360*']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K360*']['inp_Dr'])

    def K372_UPRAIS_choose(self):
        """Выбор калибра К372*"""
        if self.anti_clear != 0:
            self.K_clear_choose()

        self.chosen_btn = self.ui.K372_UPRAIS_btn
        self.button_name = self.ui.K372_UPRAIS_btn.text()
        self.colib = 'K372*'
        self.color_btn()

        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()
        for item in self.punch_sets["K372*"]["Dopr"]:
            self.ui.inp_dopr.addItem(str(item))
        for item in self.punch_sets["K372*"]["Lopr"]:
            self.ui.inp_Lopr.addItem(str(item))

        self.Lcu = self.button_sets['K372*']['Lcu']
        self.Xa = self.button_sets['K372*']['Xa']
        self.c_corr = self.button_sets['K372*']['c_corr']
        self.ui.inp_Dvp.setValue(self.button_sets['K372*']['inp_Dvp'])
        self.ui.inp_l12.setValue(self.button_sets['K372*']['inp_l12'])
        self.ui.inp_Lvx.setValue(self.button_sets['K372*']['inp_Lvx'])
        self.ui.inp_a11.setValue(self.button_sets['K372*']['inp_a11'])
        self.ui.inp_lvix.setValue(self.button_sets['K372*']['inp_lvix'])
        self.ui.inp_a12.setValue(self.button_sets['K372*']['inp_a12'])
        self.ui.inp_k.setValue(self.button_sets['K372*']['inp_k'])
        self.ui.inp_a2.setValue(self.button_sets['K372*']['inp_a2'])
        self.ui.inp_m.setValue(self.button_sets['K372*']['inp_m'])
        self.ui.inp_fi.setValue(self.button_sets['K372*']['inp_fi'])
        self.ui.cB_inp_beta.setCurrentText(self.button_sets['K372*']['cB_inp_beta'])
        self.ui.inp_Lcmech.setValue(self.button_sets['K372*']['inp_Lcmech'])
        self.ui.inp_L2.setValue(self.button_sets['K372*']['inp_L2'])
        self.ui.inp_gamma1.setValue(self.button_sets['K372*']['inp_gamma1'])
        self.ui.inp_gamma2.setValue(self.button_sets['K372*']['inp_gamma2'])
        self.ui.cB_inp_dz.setCurrentText(self.button_sets['K372*']['cB_inp_dz'])
        self.ui.inp_Dr.setValue(self.button_sets['K372*']['inp_Dr'])

    def K_clear_choose(self):
        """Нажатие кнопки очистить"""
        self.Lcu = 20
        self.Xa = 0
        self.c_corr = 0
        self.chosen_btn = self.ui.K_clear_btn
        self.button_name = '---'
        self.color_btn()
        self.ui.checkBox_label_GPOD_b.setDisabled(True)
        self.ui.checkBox_label_GPOD_b.setChecked(False)
        self.ui.checkBox_label_GPOD_ksi.setDisabled(True)
        self.ui.checkBox_label_GPOD_ksi.setChecked(False)
        self.ui.checkBox_label_GPOD_c.setDisabled(True)
        self.ui.checkBox_label_GPOD_c.setChecked(False)
        self.ui.FormTable_btn.setDisabled(True)
        self.ui.state_label.setText('<p style="color:black;">' + "Расчет..." + '</p>')
        self.ui.inp_dopr.clear()
        self.ui.inp_Lopr.clear()

        self.ui.inp_Dvp.setValue(0)
        self.ui.inp_l12.setValue(0)
        self.ui.inp_Lvx.setValue(0)
        self.ui.inp_Lrab.setValue(0)
        self.ui.inp_a11.setValue(0)
        self.ui.inp_lvix.setValue(0)
        self.ui.inp_a12.setValue(0)
        self.ui.inp_k.setValue(0)
        self.ui.inp_a2.setValue(0)
        self.ui.inp_m.setValue(0)
        self.ui.inp_fi.setValue(0)
        self.ui.cB_inp_beta.setCurrentIndex(0)
        self.ui.inp_Lcmech.setValue(0)
        self.ui.inp_L2.setValue(0)
        self.ui.inp_gamma1.setValue(0)
        self.ui.inp_gamma2.setValue(0)
        self.ui.cB_inp_dz.setCurrentIndex(0)
        self.ui.inp_Dr.setValue(0)
        self.ui.inp_dopr.setCurrentIndex(0)
        self.ui.inp_Lopr.setCurrentIndex(0)
        self.ui.cB_inp_dz.setCurrentIndex(0)
        self.ui.cB_inp_factor.setCurrentIndex(0)
        self.ui.cB_inp_beta.setCurrentIndex(0)
        self.ui.inp_Lz.setValue(0)
        self.ui.inp_radio_Sr.setValue(0)
        self.ui.inp_radio_dr.setValue(0)

        self.recount_spotter_a = 1
        self.recount_spotter_En = 1
        self.recount_spotter_ksi = 1
        self.recount_spotter_b = 1
        self.recount_spotter_c = 1
        self.ui.inOut_GPOD_a.setValue(0)
        self.ui.inOut_GPOD_b.setValue(0)
        self.ui.inOut_GPOD_c.setValue(0)

        self.recount_spotter_a = 1
        self.recount_spotter_En = 1
        self.recount_spotter_ksi = 1
        self.recount_spotter_b = 1
        self.recount_spotter_c = 1
        self.ui.inOut_GPOD_En.setValue(0)
        self.ui.inOut_GPOD_ksi.setValue(0)
        self.ui.inOut_GPOD_Een.setValue(0)
        self.ui.inOut_GPOD_Lr.setValue(0)
        self.ui.inOut_GPOD_mu.setValue(0)
        self.ui.inOut_GPOD_GF.setValue(0)
        self.ui.inOut_GPOD_Dvx.setValue(0)
        self.ui.inOut_GPOD_Dvix.setValue(0)
        self.ui.inOut_GPOD_L.setValue(0)
        self.ui.inOut_GPOD_X1.setValue(0)
        self.ui.inOut_GPOD_X2.setValue(0)
        self.ui.inOut_GPOD_Lod.setValue(0)

        self.recount_spotter_a = 1
        self.recount_spotter_En = 1
        self.recount_spotter_ksi = 1
        self.recount_spotter_b = 1
        self.recount_spotter_c = 1



    def turned_on(self):
        """Выполнить при включении"""


        if pathlib.Path(buttons_set).exists():
            f = open(buttons_set, 'r')
            buttons = str(f.read())

            try:
                self.button_sets = eval(buttons)
            except SyntaxError:
                pass

        if pathlib.Path(set_log).exists():
            f = open(set_log, "r")
            sets = str(f.read())
            try:
                self.sets = eval(sets)

                self.Dp_f = self.ui.inp_Dvp.setValue(float(self.sets['self.Dp_f'].replace(",", ".")))
                self.Lvh_f = self.ui.inp_Lvx.setValue(float(self.sets['self.Lvh_f'].replace(",", ".")))
                self.L12_f = self.ui.inp_l12.setValue(float(self.sets['self.L12_f'].replace(",", ".")))
                self.Lvih_f = self.ui.inp_lvix.setValue(float(self.sets['self.Lvih_f'].replace(",", ".")))
                self.Lk_f = self.ui.inp_k.setValue(float(self.sets['self.Lk_f'].replace(",", ".")))
                self.Lm_f = self.ui.inp_m.setValue(float(self.sets['self.Lm_f'].replace(",", ".")))
                self.a11_f = self.ui.inp_a11.setValue(float(self.sets['self.a11_f'].replace(",", ".")))
                self.a12_f = self.ui.inp_a12.setValue(float(self.sets['self.a12_f'].replace(",", ".")))
                self.a2_f = self.ui.inp_a2.setValue(float(self.sets['self.a2_f'].replace(",", ".")))
                self.fee_f = self.ui.inp_fi.setValue(float(self.sets['self.fee_f'].replace(",", ".")))
                self.beta_f = self.ui.cB_inp_beta.setCurrentText(self.sets['self.beta_f'])
                self.Lsm_f = self.ui.inp_Lcmech.setValue(float(self.sets['self.Lsm_f'].replace(",", ".")))
                self.L2_f = self.ui.inp_L2.setValue(float(self.sets['self.L2_f'].replace(",", ".")))
                self.gamma1_f = self.ui.inp_gamma1.setValue(float(self.sets['self.gamma1_f'].replace(",", ".")))
                self.gamma2_f = self.ui.inp_gamma2.setValue(float(self.sets['self.gamma2_f'].replace(",", ".")))
                self.Dz_f = self.ui.cB_inp_dz.setCurrentText(self.sets['self.Dz_f'])
                self.Lz_f = self.ui.inp_Lz.setValue(float(self.sets['self.Lz_f'].replace(",", ".")))
                self.Kz_f = self.ui.cB_inp_factor.setCurrentText(self.sets['self.Kz_f'])
                self.Dg_f = self.ui.inp_Dr.setValue(float(self.sets['self.Dg_f'].replace(",", ".")))


                self.Sg_f = self.ui.inp_radio_Sr.setValue(float(self.sets['self.Sg_f'].replace(",", ".")))
                self.dg_f = self.ui.inp_radio_dr.setValue(float(self.sets['self.dg_f'].replace(",", ".")))

                self.Lrab_f = self.ui.inp_Lrab.setValue(float(self.sets['self.Lrab_f'].replace(",", ".")))
                self.Lcmech_f = self.ui.inp_Lcmech.setValue(float(self.sets['self.Lcmech_f'].replace(",", ".")))
                self.factor_f = self.ui.cB_inp_factor.setCurrentText(self.sets['self.factor_f'])

                self.ui.checkBox_label_GPOD_ksi.setChecked(False)
                self.ui.checkBox_label_GPOD_ksi.setDisabled(True)

                # if self.sets['self.checkBox_label_GPOD_b'] != 0:
                #     self.ui.checkBox_label_GPOD_b.setChecked(True)
                #     self.ui.inOut_GPOD_b.setValue(float(self.sets['self.inOut_GPOD_b'].replace(",", ".")))
                #
                # if self.sets['self.checkBox_label_GPOD_c'] != 0:
                #     self.ui.checkBox_label_GPOD_c.setChecked(True)
                #     self.ui.inOut_GPOD_c.setValue(float(self.sets['self.inOut_GPOD_c'].replace(",", ".")))
                #
                # if self.sets['self.checkBox_label_GPOD_ksi'] != 0:
                #     self.ui.checkBox_label_GPOD_ksi.setChecked(True)
                #     self.ui.inOut_GPOD_ksi.setValue(float(self.sets['self.inOut_GPOD_ksi'].replace(",", ".")))



                if self.sets['self.Srdr'] == 0:
                    self.ui.radio_Sr.setChecked(True)
                    self.ui.radio_dr.setChecked(False)

                    self.Srdr_change_Sr()
                else:
                    self.ui.radio_Sr.setChecked(False)
                    self.ui.radio_dr.setChecked(True)

                    self.Srdr_change_dr()

                if self.sets['self.GPOD'] == 0:
                    self.ui.radio_GPOD_roolsDistance.setChecked(True)
                    self.ui.radio_GPOD_pitchReduction.setChecked(False)

                    self.GPOD_change_rools()
                    self.A_f = self.ui.inOut_GPOD_a.setValue(float(self.sets['self.A_f'].replace(",", ".")))
                else:
                    self.ui.radio_GPOD_roolsDistance.setChecked(False)
                    self.ui.radio_GPOD_pitchReduction.setChecked(True)

                    self.GPOD_change_pitch()
                    self.ui.inOut_GPOD_En.setValue(float(self.sets['self.inOut_GPOD_En'].replace(",", ".")))

                self.anti_clear = 0

                if self.sets['self.button_name'] == 'K212':
                    self.K212_choose()
                elif self.sets['self.button_name'] == 'K255/K260':
                    self.K255_K260_choose()
                elif self.sets['self.button_name'] == 'K270':
                    self.K270_choose()
                elif self.sets['self.button_name'] == 'K288':
                    self.K288_choose()
                elif self.sets['self.button_name'] == 'K360':
                    self.K360_choose()
                elif self.sets['self.button_name'] == 'K372':
                    self.K372_choose()
                elif self.sets['self.button_name'] == 'K435/K444':
                    self.K435_K444_choose()

                self.Dopr_f = self.ui.inp_dopr.setCurrentText(self.sets['self.Dopr_f'])
                self.Lopr_f = self.ui.inp_Lopr.setCurrentText(self.sets['self.Lopr_f'])

                if self.sets['self.exit'] == 0:
                    self.ui.radio_openExit.setChecked(True)
                    self.ui.radio_closeExit.setChecked(False)
                else:
                    self.ui.radio_openExit.setChecked(False)
                    self.ui.radio_closeExit.setChecked(True)
                self.fee_f = self.ui.inp_fi.setValue(float(self.sets['self.fee_rem'].replace(",", ".")))

                self.anti_clear = 1

            except SyntaxError:
                pass
            f.close()

        self.Sr_val_change()
        self.dr_val_change()
        self.use_ksi()
        self.ui.radio_GPOD_roolsDistance.setChecked(True)
        # self.ui.radio_openExit.setChecked(True)
        self.GPOD_change_rools()
        self.ui.radio_Sr.setChecked(True)
        self.Srdr_change_Sr()

        self.ui.inp_dopr.setStyleSheet("background-color: #C0C0FF; color: black;")
        self.ui.inp_Lopr.setStyleSheet("background-color: #C0C0FF; color: black;")
        # self.ui.inp_Dr.setStyleSheet("background-color: #C0C0FF; color: black;")


    # Дальше идет блок с настройкой отображения и активности кнопок при различных случаях
    def GPOD_change_rools(self):  # Выбрано расстояние между валками
        self.ui.inOut_GPOD_En.setDisabled(True)
        self.ui.inOut_GPOD_a.setDisabled(False)

        self.ui.inOut_GPOD_a.setStyleSheet("background-color: #C0C0FF; color: black;")
        self.ui.inOut_GPOD_En.setStyleSheet("")

        self.input_event()

    def GPOD_change_pitch(self):  # Выбрано обжатие в пережиме
        self.ui.inOut_GPOD_En.setDisabled(False)
        self.ui.inOut_GPOD_a.setDisabled(True)

        self.ui.inOut_GPOD_En.setStyleSheet("background-color: #C0C0FF; color: black;")
        self.ui.inOut_GPOD_a.setStyleSheet("")

        self.input_event()

    def Srdr_change_Sr(self):  # Выбрана толщина стенки
        self.ui.inp_radio_dr.setDisabled(True)
        self.ui.inp_radio_Sr.setDisabled(False)

        self.ui.inp_radio_Sr.setStyleSheet("background-color: #C0C0FF; color: black;")
        self.ui.inp_radio_dr.setStyleSheet("")

    def Srdr_change_dr(self):  # Выбран внутренний диаметр гильзы
        self.ui.inp_radio_dr.setDisabled(False)
        self.ui.inp_radio_Sr.setDisabled(True)

        self.ui.inp_radio_dr.setStyleSheet("background-color: #C0C0FF; color: black;")
        self.ui.inp_radio_Sr.setStyleSheet("")

    def color_btn(self):
        """Покраска кнопок"""
        btns = [
            self.ui.K212_btn, self.ui.K360_btn, self.ui.K255_K260_btn,
            self.ui.K372_btn, self.ui.K270_btn, self.ui.K435_K444_btn,
            self.ui.K288_btn, self.ui.K360_UPRAIS_btn, self.ui.K372_UPRAIS_btn,
        ]

        for i in btns:
            if i == self.chosen_btn:
                i.setStyleSheet("background-color: green; color: white;")
                if i == self.ui.K360_UPRAIS_btn:
                    i.setToolTip(
                        "Прошивка с увеличением диаметра гильзы относительно диаметра заготовки"
                    )
                if i == self.ui.K372_UPRAIS_btn:
                    i.setToolTip(
                        "Прошивка с увеличением диаметра гильзы относительно диаметра заготовки"
                    )

                self.ui.label_pictureTop.setText(
                    f'<html>'
                    f'<head/>'
                    f'<body>'
                    f'<p>'
                    f'<span style=" font-size:10pt; font-weight:600;">'
                    f'{self.button_name}'
                    f'</span>'
                    f'</p>'
                    f'</body>'
                    f'</html>'
                )
            else:
                i.setStyleSheet("color: black;")
            if self.button_name == '---':
                self.ui.label_pictureTop.setText(
                    f'<html>'
                    f'<head/>'
                    f'<body>'
                    f'<p>'
                    f'<span style=" font-size:10pt; font-weight:600;">'
                    f'{self.button_name}'
                    f'</span>'
                    f'</p>'
                    f'</body>'
                    f'</html>'
                )



    # def K212_chose(self):
    #     self.ui.K212_btn.setStyleSheet("background-color: green;")
    #     self.ui.K360_btn.setStyleSheet("")
    #     self.ui.K255_K260_btn.setStyleSheet("")
    #     self.ui.K372_btn.setStyleSheet("")
    #     self.ui.K270_btn.setStyleSheet("")
    #     self.ui.K435_K444_btn.setStyleSheet("")
    #     self.ui.K288_btn.setStyleSheet("")

    def closeEvent(self, e):
        """В случае выключения программы"""
        save_res = QtWidgets.QMessageBox.question(self, "Сохранить ввод?",
                                                  "Сохранить введенные исходные данные?\n"
                                                  "(Все несохраненные данные будут потеряны!)",
                                                  QtWidgets.QMessageBox.Yes |
                                                  QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        ex_res = res = QtWidgets.QMessageBox.question(self, "Подтвердить выход?",
                                                      "Вы действительно хотите закрыть программу?\n"
                                                      "(Все несохраненные данные будут потеряны!)", QtWidgets.QMessageBox.Yes |
                                                      QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if not pathlib.Path(buttons_set).exists():
            f = open(buttons_set, 'w+')
            f.write(str(self.button_sets))
            f.close()

        if save_res == QtWidgets.QMessageBox.Yes and ex_res == QtWidgets.QMessageBox.Yes:
            self.count_main()
            f = open(set_log, 'w+')
            f.write(str(self.sets))
            f.close()

            e.accept()

        elif save_res == QtWidgets.QMessageBox.Yes and ex_res == QtWidgets.QMessageBox.No:
            self.count_main()
            f = open(set_log, 'w+')
            f.write(str(self.sets))
            f.close()

            e.ignore()

        elif ex_res == QtWidgets.QMessageBox.No:
            e.ignore()

        else:
            e.accept()


    def count_main(self):
        """Тут содержится основной расчет, эта функция вызывается всегда когда необходимо посчитать"""

        # Get data from interface Получение всего из интерфейса
        self.ui.FormTable_btn.setDisabled(False)
        self.Dp_f = self.ui.inp_Dvp.text()  # ininp
        self.Lrab_f = self.ui.inp_Lrab.text()
        self.Lvh_f = self.ui.inp_Lvx.text()  # ininp
        self.L12_f = self.ui.inp_l12.text()  # ininp
        self.Lvih_f = self.ui.inp_lvix.text()  # ininp
        self.Lk_f = self.ui.inp_k.text()  # ininp
        self.Lm_f = self.ui.inp_m.text()  # ininp
        self.a11_f = self.ui.inp_a11.text()  # ininp
        self.a12_f = self.ui.inp_a12.text()  # ininp
        self.a2_f = self.ui.inp_a2.text()  # ininp

        if self.ui.radio_openExit.isChecked():
            self.fee_f = self.ui.inp_fi.text()  # ininp
        else:
            self.fee_f = "-" + self.ui.inp_fi.text()  # ininp

        self.beta_f = self.ui.cB_inp_beta.currentText()  # ininp
        self.Lsm_f = self.ui.inp_Lcmech.text()  # ininp
        self.Lcmech_f = self.ui.inp_Lcmech.text()
        self.L2_f = self.ui.inp_L2.text()  # ininp
        self.gamma1_f = self.ui.inp_gamma1.text()  # ininp
        self.gamma2_f = self.ui.inp_gamma2.text()  # ininp
        self.Dopr_f = self.ui.inp_dopr.currentText()  # ininp
        self.Lopr_f = self.ui.inp_Lopr.currentText()  # ininp
        self.Dz_f = self.ui.cB_inp_dz.currentText()  # ininp
        self.factor_f = self.ui.cB_inp_factor.currentText()
        self.Lz_f = self.ui.inp_Lz.text()  # ininp
        self.Kz_f = self.ui.cB_inp_factor.currentText()  # ininp
        self.Dg_f = self.ui.inp_Dr.text()  # ininp

        self.Sg_f = self.ui.inp_radio_Sr.text()  # ininp
        self.dg_f = self.ui.inp_radio_dr.text()


        self.A_f = self.ui.inOut_GPOD_a.text()  # ininp

        self.exit_OC = 0 if self.ui.radio_openExit.isChecked() else 1
        self.fee_rem = self.ui.inp_fi.text()

        self.Srdr = 0 if self.ui.radio_Sr.isChecked() else 1

        self.GPOD = 0 if self.ui.radio_GPOD_roolsDistance.isChecked() else 1

        self.inOut_GPOD_En = self.ui.inOut_GPOD_En.text()

        self.checkBox_label_GPOD_ksi = 0 if not self.ui.checkBox_label_GPOD_ksi.isChecked() else 1
        self.inOut_GPOD_ksi = self.ui.inOut_GPOD_ksi.text()
        self.inOut_GPOD_c = self.ui.inOut_GPOD_c.text()

        self.checkBox_label_GPOD_b = 0 if not self.ui.checkBox_label_GPOD_b.isChecked() else 1
        self.inOut_GPOD_b = self.ui.inOut_GPOD_b.text()

        self.checkBox_label_GPOD_c = 0 if not self.ui.checkBox_label_GPOD_c.isChecked() else 1
        self.inOut_GPOD_c = self.ui.inOut_GPOD_c.text()


        # Запись всего полученного из интерфейса в переменную
        # для сохранения и загрузки при следующем запуске
        self.sets = {

            "self.Dp_f": self.Dp_f,
            "self.Lvh_f": self.Lvh_f,
            "self.Lrab_f": self.Lrab_f,
            "self.L12_f": self.L12_f,
            "self.Lvih_f": self.Lvih_f,
            "self.Lk_f": self.Lk_f,
            "self.Lm_f": self.Lm_f,
            "self.a11_f": self.a11_f,
            "self.a12_f": self.a12_f,
            "self.a2_f": self.a2_f,
            "self.fee_f": self.fee_f,
            "self.beta_f": self.beta_f,
            "self.Lsm_f": self.Lsm_f,
            "self.Lcmech_f": self.Lcmech_f,
            "self.L2_f": self.L2_f,
            "self.gamma1_f": self.gamma1_f,
            "self.gamma2_f": self.gamma2_f,
            "self.Dopr_f": self.Dopr_f,
            "self.Lopr_f": self.Lopr_f,
            "self.Dz_f": self.Dz_f,
            "self.factor_f": self.factor_f,
            "self.Lz_f": self.Lz_f,
            "self.Kz_f": self.Kz_f,
            "self.Dg_f": self.Dg_f,
            "self.Sg_f": self.Sg_f,
            "self.dg_f": self.dg_f,
            "self.A_f": self.A_f,

            "self.exit": self.exit_OC,
            "self.fee_rem": self.fee_rem,
            "self.Srdr": self.Srdr,
            "self.GPOD": self.GPOD,
            "self.inOut_GPOD_En": self.inOut_GPOD_En,
            "self.button_name": self.button_name,

            "self.checkBox_label_GPOD_ksi": self.checkBox_label_GPOD_ksi,
            "self.inOut_GPOD_ksi": self.inOut_GPOD_ksi,

            "self.checkBox_label_GPOD_b": self.checkBox_label_GPOD_b,
            "self.inOut_GPOD_b": self.inOut_GPOD_b,
            "self.checkBox_label_GPOD_c": self.checkBox_label_GPOD_c,
            "self.inOut_GPOD_c": self.inOut_GPOD_c,


        }

        # Блок вызова обращения к мат. модели в зависимости от
        # того какие параметры выбраны (отмечено ли b и тд)
        try:
            if self.checkBox_label_GPOD_ksi == 0 and self.checkBox_label_GPOD_b == 0 and self.checkBox_label_GPOD_c == 0:
                self.results = math_model.Model_Korx.korx_math_model(
                    self.Dp_f, self.Lvh_f, self.L12_f, self.Lvih_f, self.Lk_f, self.Lm_f, self.a11_f,
                    self.a12_f, self.a2_f, self.fee_f, self.beta_f, self.Lsm_f, self.L2_f,
                    self.gamma1_f, self.gamma2_f, self.Dopr_f, self.Lopr_f, self.Dz_f, self.Lz_f,
                    self.Kz_f, self.Dg_f, self.Sg_f, self.A_f, self.inOut_GPOD_En,
                    screws=self.screws.get_screws(), Xa=self.Xa,
                    c_check=self.checkBox_label_GPOD_c, En_check=self.GPOD, temp_koeff=self.button_sets["temp_koeff"],
                    Lcu_f=self.Lcu
                )
            elif self.checkBox_label_GPOD_ksi == 1 and self.checkBox_label_GPOD_b == 0 and self.checkBox_label_GPOD_c == 0:
                self.results = math_model.Model_Korx.korx_math_model(
                    self.Dp_f, self.Lvh_f, self.L12_f, self.Lvih_f, self.Lk_f, self.Lm_f, self.a11_f,
                    self.a12_f, self.a2_f, self.fee_f, self.beta_f, self.Lsm_f, self.L2_f,
                    self.gamma1_f, self.gamma2_f, self.Dopr_f, self.Lopr_f, self.Dz_f, self.Lz_f,
                    self.Kz_f, self.Dg_f, self.Sg_f, self.A_f, self.inOut_GPOD_En,
                    ksi_f=self.inOut_GPOD_ksi, screws=self.screws.get_screws(), Xa=self.Xa,
                    c_check=self.checkBox_label_GPOD_c, En_check=self.GPOD, c_f=str(float(self.inOut_GPOD_c) - self.c_corr),
                    temp_koeff=self.button_sets["temp_koeff"], Lcu_f=self.Lcu
                )
            elif self.checkBox_label_GPOD_ksi == 1 and self.checkBox_label_GPOD_b == 0 and self.checkBox_label_GPOD_c == 1:
                self.results = math_model.Model_Korx.korx_math_model(
                    self.Dp_f, self.Lvh_f, self.L12_f, self.Lvih_f, self.Lk_f, self.Lm_f, self.a11_f,
                    self.a12_f, self.a2_f, self.fee_f, self.beta_f, self.Lsm_f, self.L2_f,
                    self.gamma1_f, self.gamma2_f, self.Dopr_f, self.Lopr_f, self.Dz_f, self.Lz_f,
                    self.Kz_f, self.Dg_f, self.Sg_f, self.A_f, self.inOut_GPOD_En,
                    ksi_f=self.inOut_GPOD_ksi, c_f=str(float(self.inOut_GPOD_c) - self.c_corr),
                    screws=self.screws.get_screws(), Xa=self.Xa,
                    c_check=self.checkBox_label_GPOD_c, En_check=self.GPOD, temp_koeff=self.button_sets["temp_koeff"],
                    Lcu_f=self.Lcu
                )
            elif self.checkBox_label_GPOD_ksi == 0 and self.checkBox_label_GPOD_b == 1:
                self.results = math_model.Model_Korx.korx_math_model(
                    self.Dp_f, self.Lvh_f, self.L12_f, self.Lvih_f, self.Lk_f, self.Lm_f, self.a11_f,
                    self.a12_f, self.a2_f, self.fee_f, self.beta_f, self.Lsm_f, self.L2_f,
                    self.gamma1_f, self.gamma2_f, self.Dopr_f, self.Lopr_f, self.Dz_f, self.Lz_f,
                    self.Kz_f, self.Dg_f, self.Sg_f, self.A_f, self.inOut_GPOD_En,
                    b_f=self.inOut_GPOD_b, c_f=str(float(self.inOut_GPOD_c) - self.c_corr),
                    screws=self.screws.get_screws(), Xa=self.Xa,
                    c_check=self.checkBox_label_GPOD_c, En_check=self.GPOD, temp_koeff=self.button_sets["temp_koeff"],
                    Lcu_f=self.Lcu
                )
            elif self.checkBox_label_GPOD_ksi == 0 and self.checkBox_label_GPOD_b == 0 and self.checkBox_label_GPOD_c == 1:
                self.results = math_model.Model_Korx.korx_math_model(
                    self.Dp_f, self.Lvh_f, self.L12_f, self.Lvih_f, self.Lk_f, self.Lm_f, self.a11_f,
                    self.a12_f, self.a2_f, self.fee_f, self.beta_f, self.Lsm_f, self.L2_f,
                    self.gamma1_f, self.gamma2_f, self.Dopr_f, self.Lopr_f, self.Dz_f, self.Lz_f,
                    self.Kz_f, self.Dg_f, self.Sg_f, self.A_f, self.inOut_GPOD_En,
                    c_f=str(float(self.inOut_GPOD_c) - self.c_corr), screws=self.screws.get_screws(), Xa=self.Xa,
                    c_check=self.checkBox_label_GPOD_c, En_check=self.GPOD, b_f=self.inOut_GPOD_b,
                    temp_koeff=self.button_sets["temp_koeff"], Lcu_f=self.Lcu
                )
            else:
                self.results = [2222, 'Неверный ввод!']

        except BaseException:
            self.results = [2222, 'Неверный ввод!']


        if not self.ui.checkBox_label_GPOD_b.isChecked():
            self.ui.checkBox_label_GPOD_ksi.setDisabled(False)
            self.ui.checkBox_label_GPOD_b.setDisabled(False)
            self.ui.checkBox_label_GPOD_c.setDisabled(False)
        else:
            self.ui.checkBox_label_GPOD_c.setDisabled(False)
        self.counted = 1

        if not isinstance(self.results, list):  # Если нет ошибки мешающей расчету

            # Вывод всего в интерфейс

            # self.recount_spotter_a = 1
            # self.recount_spotter_En = 1
            # self.recount_spotter_ksi = 1
            # self.recount_spotter_b = 1
            # self.recount_spotter_c = 1
            self.ui.inOut_GPOD_a.setValue(float(self.A_f.replace(",", ".")))
            self.ui.inOut_GPOD_a.setValue(float(self.A_f.replace(",", ".")))
            self.ksi_spotter = 0
            self.recount_spotter_ksi = 1

            self.ui.inOut_GPOD_En.setValue(self.results['Ep'])

            self.ui.inOut_GPOD_Een.setValue(self.results['En'])
            self.ui.inOut_GPOD_Lr.setValue(self.results['Lr'])
            self.ui.inOut_GPOD_mu.setValue(self.results['mu'])
            self.ui.inOut_GPOD_GF.setValue(self.results['GF'])
            self.ui.inOut_GPOD_Dvx.setValue(self.results['Dvh'])
            self.ui.inOut_GPOD_Dvix.setValue(self.results['Dvih'])
            self.ui.inOut_GPOD_L.setValue(1111.0)
            self.ui.inOut_GPOD_X1.setValue(self.results['X1'])
            self.ui.inOut_GPOD_X2.setValue(self.results['X2'])
            self.ui.inOut_GPOD_Lod.setValue(self.results['Lod'])
            self.ui.inOut_GPOD_L.setValue(self.results['L'])
            # self.ui.inOut_GPOD_a.setValue(self.results['a'])
            self.ui.inp_Lrab.setValue(self.results['Lrab'])

            if self.checkBox_label_GPOD_ksi == 1 and self.checkBox_label_GPOD_c == 0:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inOut_GPOD_b.setValue(self.results['b'])
                self.ui.inOut_GPOD_c.setValue(self.results['c'] + self.c_corr)
            elif self.checkBox_label_GPOD_ksi == 1 and self.checkBox_label_GPOD_c == 1:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inp_radio_Sr.setValue(self.results['Sg'])
                self.ui.inOut_GPOD_b.setValue(self.results['b'])
            elif self.checkBox_label_GPOD_ksi == 0 and self.checkBox_label_GPOD_c == 1 and self.checkBox_label_GPOD_b == 1:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inp_radio_Sr.setValue(self.results['Sg'])
                self.ui.inOut_GPOD_b.setValue(self.results['b'])
                # self.ui.inOut_GPOD_a.setValue(self.results['a'])
                self.ui.inOut_GPOD_ksi.setValue(self.results['ksi'])
            elif self.checkBox_label_GPOD_ksi == 0 and self.checkBox_label_GPOD_c == 1 and self.checkBox_label_GPOD_b == 0:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inp_radio_Sr.setValue(self.results['Sg'])
                self.ui.inOut_GPOD_b.setValue(self.results['b'])
                # self.ui.inOut_GPOD_a.setValue(self.results['a'])
                self.ui.inOut_GPOD_ksi.setValue(self.results['ksi'])
            elif self.checkBox_label_GPOD_b == 1 and self.checkBox_label_GPOD_c == 0:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inp_radio_Sr.setValue(self.results['Sg'])
                self.ui.inOut_GPOD_ksi.setValue(self.results['ksi'])
                self.ui.inOut_GPOD_c.setValue(self.results['c'] + self.c_corr)
            elif self.checkBox_label_GPOD_b == 1 and self.checkBox_label_GPOD_c == 1:
                self.ui.inp_Dr.setValue(self.results['Dg'])
                self.ui.inp_radio_dr.setValue(self.results['dg'])
                self.ui.inp_radio_Sr.setValue(self.results['Sg'])
                self.ui.inOut_GPOD_ksi.setValue(self.results['ksi'])
            else:
                self.recount_spotter_a = 1
                self.recount_spotter_En = 1
                self.recount_spotter_ksi = 1
                self.recount_spotter_b = 1
                self.recount_spotter_c = 1
                self.ui.inOut_GPOD_a.setValue(self.results['a'])
                self.ui.inOut_GPOD_ksi.setValue(self.results['ksi'])
                self.ui.inOut_GPOD_b.setValue(self.results['b'])
                self.ui.inOut_GPOD_c.setValue(self.results['c'] + self.c_corr)

            if len(self.results['err']) == 0:  # Если нет ОШИБКА!
                self.msg.appendleft('<p style="color:green;">' + "Рассчет выполнен успешно!" + '</p>')
                self.ui.show_messages.setText(''.join(self.msg))

                self.ui.state_label.setText('<p style="color:green; font-size: 12pt;">' + "Расчет выполнен успешно!" + '</p>')

            else:
                self.ui.state_label.setText('<p style="color:red; font-size: 12pt;">' + "Ошибка!" + '</p>')

            if len(self.results['err']) != 0:  # Если есть ОШИБКА!
                for i in self.results['err']:
                    self.msg.appendleft('<p style="color:red;">' + \
                                        i \
                                        + '</p>\n')
                    self.ui.show_messages.setText(''.join(self.msg))

            if len(self.results['warn']) != 0:  # Если есть ВНИМАНИЕ!
                for i in self.results['warn']:
                    self.msg.appendleft('<p style="color:orange;">' + \
                                        i \
                                        + '</p>\n')
                    self.ui.show_messages.setText(''.join(self.msg))

            if self.results['GF'] < 0.8 and self.results['GF'] > 0.6:
                self.msg.appendleft('<p style="color:orange;">' + \
                                    'ВНИМАНИЕ! GF &lt; 0,8 вторичный захват может быть нестабильным' \
                                    + '</p>\n')
                self.ui.show_messages.setText(''.join(self.msg))
            elif self.results['GF'] < 0.6:
                self.msg.appendleft('<p style="color:orange;">' + \
                                    'ВНИМАНИЕ! GF &lt; 0,6 вторичный захват может отсутствовать' \
                                    + '</p>\n')
                self.ui.show_messages.setText(''.join(self.msg))
            elif self.results['GF'] > 1.5:
                self.msg.appendleft('<p style="color:orange;">' + \
                                    'ВНИМАНИЕ! Слишком большое значение GF. Вероятность ' \
                                    'образования внутренних дефектов' \
                                    + '</p>\n')
                self.ui.show_messages.setText(''.join(self.msg))

            self.msg.appendleft('\n--------------------------------------------------------------------')
            self.ui.show_messages.setText(''.join(self.msg))

            self.ksi_spotter = 1

            # Настройка стилей отображения
            if self.GPOD == 0:
                self.ui.inOut_GPOD_En.setStyleSheet('')
            else:
                self.ui.inOut_GPOD_a.setStyleSheet('')
            if self.checkBox_label_GPOD_b == 0:
                self.ui.inOut_GPOD_b.setStyleSheet('')
            if self.checkBox_label_GPOD_c == 0:
                self.ui.inOut_GPOD_c.setStyleSheet('')
            if self.checkBox_label_GPOD_ksi == 0:
                self.ui.inOut_GPOD_ksi.setStyleSheet('')
            else:
                self.ui.inOut_GPOD_ksi.setStyleSheet("background-color: #C0C0FF; color: black;")
            self.ui.inOut_GPOD_Een.setStyleSheet('')
            self.ui.inOut_GPOD_Lr.setStyleSheet('')
            self.ui.inOut_GPOD_mu.setStyleSheet('')
            self.ui.inOut_GPOD_GF.setStyleSheet('')
            self.ui.inOut_GPOD_Dvx.setStyleSheet('')
            self.ui.inOut_GPOD_Dvix.setStyleSheet('')
            self.ui.inOut_GPOD_L.setStyleSheet('')
            self.ui.inOut_GPOD_X1.setStyleSheet('')
            self.ui.inOut_GPOD_X2.setStyleSheet('')
            self.ui.inOut_GPOD_Lod.setStyleSheet('')

            if self.ui.inp_Lz.value() == 0:
                self.ui.inp_Lz.setStyleSheet("background-color: yellow;")
                self.ui.inOut_GPOD_Lr.setStyleSheet("background-color: yellow;")
            else:
                self.ui.inp_Lz.setStyleSheet("")
                self.ui.inOut_GPOD_Lr.setStyleSheet("")

        elif self.results[0] == 1111:
            self.msg.appendleft('<p style="color:red;">' + self.results[1] + '</p>\n')
            self.ui.show_messages.setText(''.join(self.msg))

            self.ui.state_label.setText('<p style="color:red;">' + "Ошибка!" + '</p>')
        elif self.results[0] == 2222:
            QtWidgets.QMessageBox.warning(self, "Ошибка!", self.results[1],
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        # Снова получаем все что есть в интерфейсе и записываем в переменную,
        # чтобы записать рассчитанные значекния тоже
        self.Dp_f = self.ui.inp_Dvp.text()  # ininp
        self.Lrab_f = self.ui.inp_Lrab.text()
        self.Lvh_f = self.ui.inp_Lvx.text()  # ininp
        self.L12_f = self.ui.inp_l12.text()  # ininp
        self.Lvih_f = self.ui.inp_lvix.text()  # ininp
        self.Lk_f = self.ui.inp_k.text()  # ininp
        self.Lm_f = self.ui.inp_m.text()  # ininp
        self.a11_f = self.ui.inp_a11.text()  # ininp
        self.a12_f = self.ui.inp_a12.text()  # ininp
        self.a2_f = self.ui.inp_a2.text()  # ininp

        if self.ui.radio_openExit.isChecked():
            self.fee_f = self.ui.inp_fi.text()  # ininp
        else:
            self.fee_f = "-" + self.ui.inp_fi.text()  # ininp

        self.beta_f = self.ui.cB_inp_beta.currentText()  # ininp
        self.Lsm_f = self.ui.inp_Lcmech.text()  # ininp
        self.Lcmech_f = self.ui.inp_Lcmech.text()
        self.L2_f = self.ui.inp_L2.text()  # ininp
        self.gamma1_f = self.ui.inp_gamma1.text()  # ininp
        self.gamma2_f = self.ui.inp_gamma2.text()  # ininp
        self.Dopr_f = self.ui.inp_dopr.currentText()  # ininp
        self.Lopr_f = self.ui.inp_Lopr.currentText()  # ininp
        self.Dz_f = self.ui.cB_inp_dz.currentText()  # ininp
        self.factor_f = self.ui.cB_inp_factor.currentText()
        self.Lz_f = self.ui.inp_Lz.text()  # ininp
        self.Kz_f = self.ui.cB_inp_factor.currentText()  # ininp
        self.Dg_f = self.ui.inp_Dr.text()  # ininp

        self.Sg_f = self.ui.inp_radio_Sr.text()  # ininp
        self.dg_f = self.ui.inp_radio_dr.text()

        self.A_f = self.ui.inOut_GPOD_a.text()  # ininp

        self.exit_OC = 0 if self.ui.radio_openExit.isChecked() else 1
        self.fee_rem = self.ui.inp_fi.text()

        self.Srdr = 0 if self.ui.radio_Sr.isChecked() else 1

        self.GPOD = 0 if self.ui.radio_GPOD_roolsDistance.isChecked() else 1

        self.inOut_GPOD_En = self.ui.inOut_GPOD_En.text()

        self.checkBox_label_GPOD_ksi = 0 if not self.ui.checkBox_label_GPOD_ksi.isChecked() else 1
        self.inOut_GPOD_ksi = self.ui.inOut_GPOD_ksi.text()
        self.inOut_GPOD_c = self.ui.inOut_GPOD_c.text()

        self.checkBox_label_GPOD_b = 0 if not self.ui.checkBox_label_GPOD_b.isChecked() else 1
        self.inOut_GPOD_b = self.ui.inOut_GPOD_b.text()

        self.checkBox_label_GPOD_c = 0 if not self.ui.checkBox_label_GPOD_c.isChecked() else 1
        self.inOut_GPOD_c = self.ui.inOut_GPOD_c.text()

        self.sets = {

            "self.Dp_f": self.Dp_f,
            "self.Lvh_f": self.Lvh_f,
            "self.Lrab_f": self.Lrab_f,
            "self.L12_f": self.L12_f,
            "self.Lvih_f": self.Lvih_f,
            "self.Lk_f": self.Lk_f,
            "self.Lm_f": self.Lm_f,
            "self.a11_f": self.a11_f,
            "self.a12_f": self.a12_f,
            "self.a2_f": self.a2_f,
            "self.fee_f": self.fee_f,
            "self.beta_f": self.beta_f,
            "self.Lsm_f": self.Lsm_f,
            "self.Lcmech_f": self.Lcmech_f,
            "self.L2_f": self.L2_f,
            "self.gamma1_f": self.gamma1_f,
            "self.gamma2_f": self.gamma2_f,
            "self.Dopr_f": self.Dopr_f,
            "self.Lopr_f": self.Lopr_f,
            "self.Dz_f": self.Dz_f,
            "self.factor_f": self.factor_f,
            "self.Lz_f": self.Lz_f,
            "self.Kz_f": self.Kz_f,
            "self.Dg_f": self.Dg_f,
            "self.Sg_f": self.Sg_f,
            "self.dg_f": self.dg_f,
            "self.A_f": self.A_f,

            "self.exit": self.exit_OC,
            "self.fee_rem": self.fee_rem,
            "self.Srdr": self.Srdr,
            "self.GPOD": self.GPOD,
            "self.inOut_GPOD_En": self.inOut_GPOD_En,
            "self.button_name": self.button_name,

            "self.checkBox_label_GPOD_ksi": self.checkBox_label_GPOD_ksi,
            "self.inOut_GPOD_ksi": self.inOut_GPOD_ksi,

            "self.checkBox_label_GPOD_b": self.checkBox_label_GPOD_b,
            "self.inOut_GPOD_b": self.inOut_GPOD_b,
            "self.checkBox_label_GPOD_c": self.checkBox_label_GPOD_c,
            "self.inOut_GPOD_c": self.inOut_GPOD_c,

        }

        self.recount_spotter_a = 0
        self.recount_spotter_En = 0
        self.recount_spotter_ksi = 0
        self.recount_spotter_b = 0
        self.recount_spotter_c = 0


def main():
    app = QtWidgets.QApplication(sys.argv)

    pixmap = QtGui.QPixmap(":/images/000.jpg")
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    time.sleep(2)

    locale = QLocale.system().name()
    translator = QTranslator(app)
    translator.load('{}qtbase_{}.qm'.format(I18N_QT_PATH, locale))
    app.installTranslator(translator)

    window = MainProcess()
    p = window.palette()
    p.setColor(window.backgroundRole(), QtGui.QColor(QtGui.qRgba(223, 151, 76, 1)))
    window.setPalette(p)
    window.show()

    splash.finish(window)

    app.exec_()


if __name__ == '__main__':
    main()

