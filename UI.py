from typing import Callable
from typing import List, Any

from PyQt5 import QtWidgets

from files.MainWindow import Ui_MainWindow
from files.ResultWindow import Ui_Form
from files.TableWindow import Ui_Form as Ui_Form_Table

from main import Calculation
from functions import change_size
from MyThread import MyThread
from TableLoader import TableLoader
# from ChartPLTWindow import ChartPLTWindow

from settings import DEDUG

import sys


# from functions import get_super, get_sub


class Variables:
    def __init__(self, main_window):
        self.main_window: mywindow = main_window
        self.M_x = None
        self.B_x = None
        self.alpha = None
        self.beta = None
        self.E = None
        self.load()

    def load(self):
        self.M_x = mywindow.is_float(self.main_window.ui.doubleSpinBox_3)
        self.B_x = mywindow.is_float(self.main_window.ui.doubleSpinBox)
        self.alpha = mywindow.is_float(self.main_window.ui.doubleSpinBox_5)
        self.beta = mywindow.is_float(self.main_window.ui.doubleSpinBox_6)
        self.E = mywindow.is_float(self.main_window.ui.doubleSpinBox_2)

    def update(self):
        self.load()
        # self.main_window.table_loader1.n = self.m
        # self.main_window.table_loader2.n = self.n


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()

        self.calculation = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if DEDUG:
            self.ui.doubleSpinBox_3.setValue(7.4)  # M_x
            self.ui.doubleSpinBox.setValue(0.8)  # B_x
            self.ui.doubleSpinBox_5.setValue(7)  # alpha
            self.ui.doubleSpinBox_6.setValue(8.2)  # beta
            self.ui.doubleSpinBox_2.setValue(0.2)  # E

        change_size(self)

        self.lst_Thread = []

        self.variables = Variables(self)

        # loader1_n = self.variables.m
        # loader1_m = 1
        # loader1_label = self.ui.label_3
        # loader1_data = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]
        # loader1_block = False
        # loader1_heading_x = lambda iterator: f"d{get_sub(str(iterator + 1))}"

        # loader2_n = self.variables.n
        # loader2_m = 1
        # loader2_label = self.ui.label_4
        # loader2_data = [[1, 1.6]]
        # loader2_block = False
        # loader2_heading_x = lambda iterator: f"E{get_sub(str(iterator + 1))}"

        # self.table_loader1 = TableLoader(
        #     self, loader1_n, loader1_m, loader1_label,
        #     block=loader1_block,
        #     heading_x=loader1_heading_x
        # )
        # self.table_loader2 = TableLoader(
        #     self, loader2_n, loader2_m, loader2_label,
        #     block=loader2_block,
        #     heading_x=loader2_heading_x
        # )

        if DEDUG:
            pass
            # self.table_loader1.data = loader1_data
            # self.table_loader2.data = loader2_data

        # self.ui.pushButton_2.clicked.connect(self.table_loader1.open_table)
        # self.ui.pushButton_3.clicked.connect(self.table_loader2.open_table)

        # add_def_pushButton = lambda : self.calculation.simple_bid()
        # add_def_pushButton_2 = lambda : self.calculation.difficult_bet()
        # self.ui.pushButton.clicked.connect(lambda : self.calculate(add_def_pushButton))
        # self.ui.pushButton_2.clicked.connect(lambda : self.calculate(add_def_pushButton_2))

        add_def_pushButton = lambda: None
        self.ui.pushButton.clicked.connect(lambda: self.calculate(add_def_pushButton))

    def calculate(self, fun, *args, **kwargs):
        self.variables.update()
        # condition = self.table_loader1.valid(1, self.variables.m) and self.table_loader2.valid(
        # 1, self.variables.n)
        condition = True
        if condition:
            self.calculation = Calculation(
                M_x=self.variables.M_x,
                B_x=self.variables.B_x,
                alpha=self.variables.alpha,
                beta=self.variables.beta,
                E=self.variables.E,
            )
            fun(*args, **kwargs)
            window = Finish(
                self
            )
            window.show()

            # def main():
            #     window.exec_()
            #
            # t = MyThread(main)
            # t.start()
            windowThread = MyThread(lambda: window.exec_())
            windowThread.start()
            self.lst_Thread.append(windowThread)

    def exec_(self) -> int:
        a = super().exec_()
        for i in self.lst_Thread:
            i.wait()
        return a

    @staticmethod
    def is_float(value: QtWidgets.QDoubleSpinBox) -> float:
        try:
            a = float(value.value())
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()

    @staticmethod
    def is_int(value: QtWidgets.QDoubleSpinBox) -> int:
        try:
            a = int(round(float(value.value())))
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()


class Finish(QtWidgets.QDialog):
    def __init__(self, parent: mywindow):
        super(Finish, self).__init__()
        self.ui = Ui_Form()
        self.parent = parent
        self.ui.setupUi(self)
        change_size(self)

        self.ui.doubleSpinBox_2.setValue(round(self.parent.variables.alpha, 3))
        self.ui.doubleSpinBox_3.setValue(round(self.parent.variables.beta, 3))
        self.ui.doubleSpinBox.setValue(round(self.parent.calculation.P_in, 4))
        self.ui.doubleSpinBox_9.setValue(round(self.parent.variables.M_x, 3))
        self.ui.doubleSpinBox_7.setValue(round(self.parent.variables.E, 3))
        self.ui.doubleSpinBox_8.setValue(round(self.parent.calculation.P_out, 4))

        # filter_table = lambda dct: round(dct['value'], 3)
        #
        # loader_v_d_n = self.parent.variables.n
        # loader_v_d_m = self.parent.variables.m
        # loader_cos_b_data = self.parent.calculation.lst_cos_b
        # loader_v_d_block = True
        # loader_v_d_heading_x = lambda iterator: f"E={self.parent.table_loader2.data[0][iterator]}"
        # loader_v_d_heading_y = lambda iterator: f"d={self.parent.table_loader1.data[0][iterator]}"
        # self.table_loader_cos_b = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_cos_b_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )

        # loader_v_y_data = self.parent.calculation.lst_v_y
        # self.table_loader_v_y = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_y_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )
        #
        # loader_v_s_data = self.parent.calculation.lst_v_s
        # self.table_loader_v_s = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_s_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )

        # self.ui.doubleSpinBox_19.setValue(round(self.parent.calculation.y))
        # self.ui.doubleSpinBox_20.setValue(round(self.parent.calculation.dy))
        # self.ui.doubleSpinBox_10.setValue(round(self.parent, 2))
        # self.parent.table_loader1.kwargs['block'] = True
        # self.parent.table_loader2.kwargs['block'] = True

        # self.lst_Thread = []
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_cos_b.open_table()))
        # self.ui.pushButton_6.clicked.connect(
        #     lambda: self.lst_Thread[0].start()
        # )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_s.open_table()))
        # self.ui.pushButton_4.clicked.connect(
        #     lambda: self.lst_Thread[1].start()
        # )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_y.open_table()))
        # self.ui.pushButton_7.clicked.connect(
        #     lambda: self.lst_Thread[2].start()
        # )
        #
        # chart_plt_w = ChartPLTWindow(1)
        # chart_plt_w.line(self.parent.calculation.chart_v_y_data)
        # chart_plt_w.quad_regress(self.parent.calculation.chart_quad_regress_data)
        #
        # self.lst_Thread.append(MyThread(
        #     lambda: chart_plt_w.start())
        # )
        # self.ui.pushButton_8.clicked.connect(
        #     lambda: self.lst_Thread[3].start()
        # )

        self.ui.pushButton.clicked.connect(self.exit_w)
        # self.ui.pushButton_2.clicked.connect(self.view_table)

    def exit_w(self):
        # self.parent.table_loader1.kwargs['block'] = False
        self.close()

    # def exec_(self) -> int:
    #     a = super().exec_()
    #     for i in self.lst_Thread:
    #         i.wait()
    #     return a

    def view_table(self):
        # self.parent.table_loader1.open_table()
        # self.parent.table_loader2.open_table()
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
