import sys
import random
from PyQt5 import uic
import pygame
from PyQt5.Qt import *
import sqlite3
from datetime import date, time

frasochki = [
    'Единственный способ хорошо работать — это любить то, что вы делаете. Если вы еще не нашли его, продолжайте искать. Не останавливайтесь.',
    'Нужно работать смелее, если действительно хочешь жить',
    'Успех никогда не бывает окончательным; неудача никогда не бывает фатальной.',
    'Неудача — это не противоположность успеха, это часть успеха',
    'Лучшая подготовка к завтрашнему дню — сделать все возможное сегодня',
    'Не желайте, чтобы это было проще. Желайте, чтобы вы были лучше',
    'Сосредоточьте все свои мысли на предстоящей работе. Солнечные лучи не обжигают, пока не сфокусируются.',
    'Люди редко добиваются успеха, если они не получают удовольствия от того, что делают']

current_data = date.today()
week = []
for i in range(7):
    week.append(date(current_data.year, current_data.month, current_data.day + i))

db = sqlite3.connect('Rtime.db')
cur = db.cursor()


class TimeMenedjment(QMainWindow):
    def __init__(self):
        self.countt = 1500
        self.chill = 300
        self.rounds = 1
        super().__init__()
        uic.loadUi('untitled.ui', self)

        self.setWindowTitle("TimeCare")
        self.setFixedSize(860, 500)
        self.concentrathion.clicked.connect(self.Pomodoro)
        self.concentrathion.setToolTip('Концентрация')
        self.back.clicked.connect(self.Backen)
        self.back.setToolTip('Вернуться к списку задач')
        self.settings.clicked.connect(self.sett)
        self.settings.setToolTip('Настроить звук')
        self.motivathion.setReadOnly(True)
        self.motivathion.setAlignment(Qt.AlignCenter)
        self.motivathion.setText(random.choice(frasochki))
        self.day.clicked.connect(self.dayBD)
        self.day.setToolTip('Расписание на сегодня')
        self.week.clicked.connect(self.weekBD)
        self.week.setToolTip('Расписание на неделю')
        self.add.clicked.connect(self.adding)
        self.add.setToolTip('Добавить задачу')
        self.minus.clicked.connect(self.delete)
        self.minus.setToolTip('Удалить задачу')
        self.change.clicked.connect(self.changeTask)
        self.change.setToolTip('Изменить задачу')

        cur.execute(f"""DELETE FROM time
                        WHERE date NOT IN ("{week[0].strftime('%d.%m.%Y')}", "{week[1].strftime('%d.%m.%Y')}", "{week[2].strftime('%d.%m.%Y')}",
                        "{week[3].strftime('%d.%m.%Y')}", "{week[4].strftime('%d.%m.%Y')}", "{week[5].strftime('%d.%m.%Y')}",
                        "{week[6].strftime('%d.%m.%Y')}");""")
        db.commit()

        self.motivathion.setHidden(True)
        self.tttimer.setHidden(True)
        self.back.setHidden(True)
        self.settings.setHidden(True)
        self.weekTasks.setHidden(True)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.counter)
        self.today()
        self.weekTask()

    def today(self):
        layout = QGridLayout()
        today_tasks = list(cur.execute(f"""SELECT task, importance, timeStart, timeEnd, color FROM Time
                                        WHERE date = '{week[0].strftime('%d.%m.%Y')}'"""))

        lab = QLabel(self)
        lab.setStyleSheet(f"QLabel {{background-color: #e6e6e6; color: black;}}")
        lab.setAlignment(Qt.AlignCenter)
        lab.setFont(QFont('Times', 10))
        lab.setMinimumHeight(30)
        lab.setMaximumHeight(30)
        lab.setText(f"{week[0].strftime('%d.%m.%Y')}")
        layout.addWidget(lab, 0, 0)

        if today_tasks:
            today_tasks.sort(key=lambda k: k[3])
            today_tasks.sort(key=lambda k: k[2])

            for i in range(len(today_tasks)):
                if today_tasks[i][1] == 1:
                    wazz = 'Это важная задача!'
                else:
                    wazz = 'Эта задача сегодня не важна'
                lab = QLabel(self)
                lab.setMinimumHeight(80)
                lab.setMaximumHeight(120)
                lab.setStyleSheet(f"QLabel {{background-color: {today_tasks[i][4]}; color: black; text-align: left;}}")
                lab.setFont(QFont('Times', 10))
                lab.setWordWrap(True)
                lab.setText(f"  {today_tasks[i][2]} - {today_tasks[i][3]}   {wazz}\n\n  {today_tasks[i][0]}")
                layout.addWidget(lab, i+1, 0)
        else:
            lab = QLabel(self)
            lab.setStyleSheet(f"QLabel {{background-color: #e6e6e6; color: black;}}")
            lab.setAlignment(Qt.AlignCenter)
            lab.setFont(QFont('Times', 10))
            lab.setText('На сегодня задач нет')
            layout.addWidget(lab, 1, 0)

        w = QWidget()
        w.setLayout(layout)
        self.daysTasks.setWidget(w)

    def weekTask(self):

        layout = QGridLayout()

        for i in range(7):
            today_tasks = list(cur.execute(f"""SELECT task, importance, timeStart, timeEnd, color FROM Time
                                                        WHERE date = '{week[i].strftime('%d.%m.%Y')}'"""))

            lab = QLabel(self)
            lab.setStyleSheet(f"QLabel {{background-color: #e6e6e6; color: black;}}")
            lab.setAlignment(Qt.AlignCenter)
            lab.setFont(QFont('Times', 8))
            lab.setMinimumWidth(200)
            lab.setMaximumWidth(200)
            lab.setMinimumHeight(30)
            lab.setMaximumHeight(30)
            lab.setText(f"{week[i].strftime('%d.%m.%Y')}")
            layout.addWidget(lab, 0, i)

            if today_tasks:
                today_tasks.sort(key=lambda k: k[3])
                today_tasks.sort(key=lambda k: k[2])

                for j in range(len(today_tasks)):
                    if today_tasks[j][1] == 1:
                        wazz = 'Это важная задача!'
                    else:
                        wazz = 'Эта задача сегодня не важна'
                    lab = QLabel(self)
                    lab.setMinimumWidth(200)
                    lab.setMaximumWidth(200)
                    lab.setMinimumHeight(80)
                    lab.setMaximumHeight(120)
                    lab.setStyleSheet(
                        f"QLabel {{background-color: {today_tasks[j][4]}; color: black; text-align: left;}}")
                    lab.setFont(QFont('Times', 8))
                    lab.setWordWrap(True)
                    lab.setText(f"  {today_tasks[j][2]} - {today_tasks[j][3]}   \n\n  {today_tasks[j][0]}")
                    layout.addWidget(lab, j + 1, i)
            else:
                lab = QLabel(self)
                lab.setStyleSheet(f"QLabel {{background-color: #e6e6e6; color: black;}}")
                lab.setAlignment(Qt.AlignCenter)
                lab.setFont(QFont('Times', 8))
                lab.setText('На сегодня задач нет')
                layout.addWidget(lab, 1, i)

        w = QWidget()
        w.setLayout(layout)
        self.weekTasks.setWidget(w)

    def adding(self):

        timeS, timeE = time(12, 0, 0), time(12, 0, 0)
        ok_pressed1, ok_pressed2, ok_pressed3, ok_pressed4, ok_pressed5 = False, False, False, False, False

        data, ok_pressed1 = QInputDialog.getItem(
            self, "Дата", "Выберите дату, на которую хотите назначить задачу",
            (week[0].strftime('%d.%m.%Y'), week[1].strftime('%d.%m.%Y'), week[2].strftime('%d.%m.%Y'),
             week[3].strftime('%d.%m.%Y'), week[4].strftime('%d.%m.%Y'), week[5].strftime('%d.%m.%Y'),
             week[6].strftime('%d.%m.%Y')), 0, False)

        if ok_pressed1:
            zadanie, ok_pressed2 = QInputDialog.getText(self, "Задача",
                                                        "Введите вашу задачу")

        if ok_pressed2:
            timeStart, ok_pressed3 = QInputDialog.getText(
                self, "Время начала",
                "Введите время начала выполнения задачи в формате часы:минуты\nНапример: 03:54, 11:48, 23:07")
            try:
                timeS = time.fromisoformat(timeStart)
            except:
                ok_pressed3 = False

        if ok_pressed3:
            timeEnd, ok_pressed4 = QInputDialog.getText(
                self, "Время окончания",
                "Введите время окончания выполнения задачи в формате часы:минуты\nНапример: 03:54, 11:48, 23:07")
            try:
                timeE = time.fromisoformat(timeEnd)
            except:
                ok_pressed4 = False

        if ok_pressed4:
            vaznoct, ok_pressed5 = QInputDialog.getItem(
                self, "Важность", "Является ли ваша задача важной или нет?",
                ('Да', 'Нет'), 0, False)
            if vaznoct == 'Да':
                vaz = 1
            else:
                vaz = 0

        if (ok_pressed1 and ok_pressed2 and ok_pressed3 and ok_pressed4 and ok_pressed5):

            cur.execute(f"""INSERT INTO time(date, task, importance, timeStart, timeEnd, color) 
                                VALUES ("{data}", '{zadanie}', {vaz}, "{timeS.strftime('%H:%M')}",
                                "{timeE.strftime('%H:%M')}", '#e6e6e6');""")

            db.commit()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Задача успешно записана!")
            msg.setWindowTitle("Оповещение")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка ввода данных, задача не была записана")
            msg.setWindowTitle("Оповещение")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        self.today()
        self.weekTask()

    def delete(self):

        ok_pressed1 = False
        date, ok_pressed = QInputDialog.getItem(
            self, "Удаление", "Выберите дату задачи, которую вы хотите удалить",
            (week[0].strftime('%d.%m.%Y'), week[1].strftime('%d.%m.%Y'), week[2].strftime('%d.%m.%Y'),
             week[3].strftime('%d.%m.%Y'), week[4].strftime('%d.%m.%Y'), week[5].strftime('%d.%m.%Y'),
             week[6].strftime('%d.%m.%Y')), 0, False)

        if ok_pressed:
            tack = list(cur.execute(f"""SELECT task FROM Time
                                        WHERE date = '{date}'"""))

            new_tack = []
            for elem in tack:
                new_tack.append(elem[0])
            items = [" ".join(item) for item in new_tack]
            task_select, ok_pressed1 = QInputDialog.getItem(
                self, "Задача", "Выберите задачу, которую хотите удалить",
                items, 0, False)

            if ok_pressed1:
                items = ''
                task_select = task_select.split('   ')
                for elem in task_select:
                    elem = elem.replace(' ', '')
                    items += elem + ' '
                items = items.strip(' ')
                cur.execute(f"""DELETE FROM time
                               WHERE date = '{date}' AND task = '{items}'""")
                db.commit()

        self.today()
        self.weekTask()

    def changeTask(self):
        date, ok_pressed = QInputDialog.getItem(
            self, "Удаление", "Выберите дату задачи, которую вы хотите изменить",
            (week[0].strftime('%d.%m.%Y'), week[1].strftime('%d.%m.%Y'), week[2].strftime('%d.%m.%Y'),
             week[3].strftime('%d.%m.%Y'), week[4].strftime('%d.%m.%Y'), week[5].strftime('%d.%m.%Y'),
             week[6].strftime('%d.%m.%Y')), 0, False)
        if ok_pressed:
            tack = list(cur.execute(f"""SELECT task FROM Time
                                                    WHERE date = '{date}'"""))

            new_tack = []
            for elem in tack:
                new_tack.append(elem[0])
            items = [" ".join(item) for item in new_tack]
            task_select, ok_pressed1 = QInputDialog.getItem(
                self, "Задача", "Выберите задачу, которую хотите изменить",
                items, 0, False)

            if ok_pressed1:
                items = ''
                task_select = task_select.split('   ')
                for elem in task_select:
                    elem = elem.replace(' ', '')
                    items += elem + ' '
                items = items.strip(' ')

                param, ok_pressed2 = QInputDialog.getItem(
                    self, "Параметр", "Выберите параметр, который вы хотите изменить",
                    ("Дата", "Задание", "Важность", "Время выполнения", "Цвет задачи"), 0, False)

        if ok_pressed2:
            match param:
                case "Дата":
                    data, ok_pressed11 = QInputDialog.getItem(
                        self, "Дата", "Выберите дату, на которую хотите назначить задачу",
                        (week[0].strftime('%d.%m.%Y'), week[1].strftime('%d.%m.%Y'), week[2].strftime('%d.%m.%Y'),
                         week[3].strftime('%d.%m.%Y'), week[4].strftime('%d.%m.%Y'), week[5].strftime('%d.%m.%Y'),
                         week[6].strftime('%d.%m.%Y')), 0, False)
                    cur.execute(f"""UPDATE Time
                                    SET date = '{data}'
                                    WHERE date='{date}' AND task='{items}';""")
                    db.commit()
                    self.today()
                    self.weekTask()

                case "Задание":
                    zadanie, ok_pressed12 = QInputDialog.getText(self, "Задача",
                                                                "Введите вашу задачу")
                    cur.execute(f"""UPDATE Time
                                    SET task = '{zadanie}'
                                    WHERE date='{date}' AND task='{items}';""")
                    db.commit()
                    self.today()
                    self.weekTask()

                case "Важность":
                    vaznoct, ok_pressed13 = QInputDialog.getItem(
                        self, "Важность", "Является ли ваша задача важной или нет?",
                        ('Важная', 'Не важная'), 0, False)
                    if vaznoct == 'Важная':
                        vaz = 1
                    else:
                        vaz = 0
                    cur.execute(f"""UPDATE Time
                                    SET importance = {vaz}
                                    WHERE date='{date}' AND task='{items}';""")
                    db.commit()
                    self.today()
                    self.weekTask()

                case "Время выполнения":

                    timeStart, ok_pressed14 = QInputDialog.getText(
                        self, "Время начала",
                        "Введите время начала выполнения задачи в формате часы:минуты\nНапример: 03:54, 11:48, 23:07")
                    try:
                        timeS = time.fromisoformat(timeStart)
                    except:
                        ok_pressed14 = False

                    timeEnd, ok_pressed15 = QInputDialog.getText(
                        self, "Время окончания",
                        "Введите время окончания выполнения задачи в формате часы:минуты\nНапример: 03:54, 11:48, 23:07")
                    try:
                        timeE = time.fromisoformat(timeEnd)
                    except:
                        ok_pressed15 = False
                    cur.execute(f"""UPDATE Time
                                    SET timeStart = '{timeS.strftime('%H:%M')}', timeEnd = '{timeE.strftime('%H:%M')}' 
                                    WHERE date='{date}' AND task='{items}';""")
                    db.commit()
                    self.today()
                    self.weekTask()

                case "Цвет задачи":
                    color = QColorDialog.getColor()
                    if color.isValid():
                        cur.execute(f"""UPDATE Time
                                        SET color = '{color.name()}'
                                        WHERE date='{date}' AND task='{items}';""")
                        db.commit()
                        self.today()
                        self.weekTask()

    def dayBD(self):
        self.today()
        self.daysTasks.setHidden(False)
        self.weekTasks.setHidden(True)
        self.day.setStyleSheet('QPushButton {background-color: #f0caa3}')
        self.week.setStyleSheet('QPushButton {background-color: #826d58}')

    def weekBD(self):
        self.weekTask()
        self.daysTasks.setHidden(True)
        self.weekTasks.setHidden(False)
        self.day.setStyleSheet('QPushButton {background-color: #826d58}')
        self.week.setStyleSheet('QPushButton {background-color: #f0caa3}')

    def Backen(self):
        self.timer.stop()
        self.motivathion.setHidden(True)
        self.tttimer.setHidden(True)
        self.back.setHidden(True)
        self.settings.setHidden(True)
        self.weekTasks.setHidden(True)
        self.day.setHidden(False)
        self.week.setHidden(False)
        self.daysTasks.setHidden(False)
        self.add.setHidden(False)
        self.minus.setHidden(False)
        self.change.setHidden(False)
        self.day.setStyleSheet('QPushButton {background-color: #f0caa3}')
        self.week.setStyleSheet('QPushButton {background-color: #826d58}')
        self.tttimer.setText("25:00")
        pygame.mixer.music.stop()

    def Pomodoro(self):

        kolRounds, ok_pressed = QInputDialog.getItem(
            self, "Циклы", "Выберите количество рабочих циклов",
            ('1', '2', '3', '4'), 0, False)

        if ok_pressed:
            self.rounds = int(kolRounds)

            self.motivathion.setHidden(False)
            self.tttimer.setHidden(False)
            self.back.setHidden(False)
            self.settings.setHidden(False)
            self.daysTasks.setHidden(True)
            self.day.setHidden(True)
            self.week.setHidden(True)
            self.weekTasks.setHidden(True)
            self.add.setHidden(True)
            self.minus.setHidden(True)
            self.change.setHidden(True)
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load('compress.mp3')
            pygame.mixer.music.play()
            self.countt = 1500
            self.chill = 300
            self.timer.start()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Пожалуйста, выберите количество циклов работы")
            msg.setWindowTitle("Оповещение")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def counter(self):
        self.motivathion.setAlignment(Qt.AlignCenter)
        if self.countt == 1500:
            self.motivathion.setText(random.choice(frasochki))
        if self.countt > 0:
            self.countt -= 1
            if len(str(self.countt // 60)) == 1:
                minut = "0" + str(self.countt // 60)
            else:
                minut = str(self.countt // 60)
            if len(str(self.countt % 60)) == 1:
                second = "0" + str(self.countt % 60)
            else:
                second = str(self.countt % 60)
            self.tttimer.setText(minut + ":" + second)
        if (self.countt == 0) and (self.chill == 300):
            self.motivathion.setText("Пришло время отдохнуть!")
        if (self.countt == 0) and (self.chill > 0) and (self.rounds > 1):
            self.chill -= 1
            if len(str(self.chill // 60)) == 1:
                minut = "0" + str(self.chill // 60)
            else:
                minut = str(self.chill // 60)
            if len(str(self.chill % 60)) == 1:
                second = "0" + str(self.chill % 60)
            else:
                second = str(self.chill % 60)
            self.tttimer.setText(minut + ":" + second)
        if self.rounds > 1 and self.countt == 0 and self.chill == 0:
            self.countt = 1500
            self.chill = 300
            self.rounds -= 1
        if self.rounds == 1 and self.countt == 0 and self.chill == 0:
            self.motivathion.setText(
                "Вы отлично поработали!\nНадеюсь мы помогли вам сконцентрироваться на вашей задаче")

    def sett(self):
        voll, ok_pressed = QInputDialog.getItem(
            self, "Звук", "Выберите громкость музыки",
            ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'), 4, False)

        if ok_pressed:
            pygame.mixer.music.set_volume(int(voll) / 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ev = TimeMenedjment()
    ev.show()
    sys.exit(app.exec())
