from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QPushButton, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QDialog, 
    QFormLayout, QLineEdit, QComboBox, QDateTimeEdit, QMessageBox, QSplitter
)
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont
from plyer import notification  # Import plyer for sending notifications

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setAutoFillBackground(True)
        header_label = QLabel("TaskIT: An Automated To-Do List Using Python")
        font = QFont("Algerian", 30, QFont.Bold)
        header_label.setFont(font)
        header_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(header_label)
        self.setStyleSheet("background-color: #EA5455; color: #151E3D;")


class PriorityTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        return priority_order[self.text()] < priority_order[other.text()]


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskIT")
        self.setGeometry(150, 150, 1700, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_widget.setStyleSheet("background-color: #2D4059;")

        header_widget = HeaderWidget()
        main_layout.addWidget(header_widget)
        main_layout.setAlignment(Qt.AlignTop)

        search_sort_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("background-color: white;")
        self.search_input.textChanged.connect(self.filter_tasks)
        search_sort_layout.addWidget(self.search_input)

        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(["Sort by Name", "Sort by Due Date", "Sort by Priority"])
        self.sort_combobox.setFixedHeight(40)
        self.sort_combobox.setStyleSheet("background-color: white;")
        self.sort_combobox.currentIndexChanged.connect(self.sort_tasks)
        search_sort_layout.addWidget(self.sort_combobox)
        search_sort_layout.addStretch()

        main_layout.addLayout(search_sort_layout)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        task_list_label = QLabel("Task List")
        task_list_label.setStyleSheet("font-size: 20px; font-family: Castellar; color: white;")
        left_layout.addWidget(task_list_label)

        self.todos_table = QTableWidget()
        self.todos_table.setColumnCount(5)
        self.todos_table.setHorizontalHeaderLabels(["Task", "Due Date", "Status", "Priority", "Action"])
        self.todos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.todos_table.setStyleSheet("background-color: #F07B3F; color: #333333; font-family: Courgette; font-size: 18px;")
        header = self.todos_table.horizontalHeader()
        header.setStyleSheet("background-color: #F07B3F; color: #333333;")

        left_layout.addWidget(self.todos_table)

        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        menu_group = QGroupBox("Menu")
        menu_group.setStyleSheet("font-size: 20px; font-family: Castellar; color: white;")
        menu_layout = QVBoxLayout()

        home_button = QPushButton("HOME")
        home_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        home_button.clicked.connect(self.show_main_window)
        menu_layout.addWidget(home_button)

        add_task_button = QPushButton("Add Task")
        add_task_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        add_task_button.clicked.connect(self.open_add_task_window)
        menu_layout.addWidget(add_task_button)

        edit_task_button = QPushButton("Edit Task")
        edit_task_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        edit_task_button.clicked.connect(self.edit_task)
        menu_layout.addWidget(edit_task_button)

        delete_task_button = QPushButton("Delete Task")
        delete_task_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        delete_task_button.clicked.connect(self.delete_task)
        menu_layout.addWidget(delete_task_button)

        delete_all_button = QPushButton("Delete All")
        delete_all_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        delete_all_button.clicked.connect(self.delete_all_tasks)
        menu_layout.addWidget(delete_all_button)

        completed_tasks_button = QPushButton("Completed Tasks")
        completed_tasks_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        completed_tasks_button.clicked.connect(self.show_completed_tasks)
        menu_layout.addWidget(completed_tasks_button)

        upcoming_tasks_button = QPushButton("Upcoming Tasks")
        upcoming_tasks_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        upcoming_tasks_button.clicked.connect(self.show_upcoming_tasks)
        menu_layout.addWidget(upcoming_tasks_button)

        help_button = QPushButton("Help")
        help_button.setStyleSheet("font-size: 18px; background-color: #FFD460; color: black;")
        help_button.clicked.connect(self.open_help_dialog)
        menu_layout.addWidget(help_button)

        menu_group.setLayout(menu_layout)
        right_layout.addWidget(menu_group)

        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

        self.todos = []
        self.animation_duration = 300

    def animate_button_click(self, button):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(self.animation_duration)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.setStartValue(button.geometry())
        anim.setEndValue(QRect(button.x() - 5, button.y() - 5, button.width() + 10, button.height() + 10))
        anim.start()

    def open_add_task_window(self):
        self.animate_button_click(self.sender())
        add_task_window = AddTaskWindow()
        add_task_window.task_added.connect(self.update_todo_list)
        add_task_window.exec_()

    def edit_task(self):
        self.animate_button_click(self.sender())
        selected_indexes = self.todos_table.selectionModel().selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Warning", "Please select a task first.")
            return
        selected_row = selected_indexes[0].row()
        self.open_edit_task_window(selected_row)

    def delete_task(self):
        self.animate_button_click(self.sender())
        selected_indexes = self.todos_table.selectionModel().selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")
            return
        rows = set(index.row() for index in selected_indexes)
        for row in sorted(rows, reverse=True):
            self.todos_table.removeRow(row)
        notification.notify(
            title='Task Deleted',
            message='A task has been deleted.',
            timeout=10
        )

    def delete_all_tasks(self):
        row_count = self.todos_table.rowCount()
        for row in range(row_count - 1, -1, -1):
            self.todos_table.removeRow(row)
        notification.notify(
            title='Tasks Deleted',
            message='All tasks have been deleted.',
            timeout=10
        )

    def show_completed_tasks(self):
        for row in range(self.todos_table.rowCount()):
            if self.todos_table.item(row, 2).text() != "Completed":
                self.todos_table.hideRow(row)

    def show_upcoming_tasks(self):
        for row in range(self.todos_table.rowCount()):
            if self.todos_table.item(row, 2).text() == "Pending":
                self.todos_table.showRow(row)
            else:
                self.todos_table.hideRow(row)

    def open_help_dialog(self):
        pass

    def filter_tasks(self):
        search_text = self.search_input.text().lower()
        for row in range(self.todos_table.rowCount()):
            task_name = self.todos_table.item(row, 0).text().lower()
            if search_text in task_name:
                self.todos_table.setRowHidden(row, False)
            else:
                self.todos_table.setRowHidden(row, True)

    def sort_tasks(self, index):
        if index == 0:  # Sort by Name
            self.todos_table.sortItems(0, Qt.AscendingOrder)

        elif index == 1:  # Sort by Due Date
            self.todos_table.sortItems(1, Qt.AscendingOrder)

        elif index == 2:  # Sort by Priority
            for row in range(self.todos_table.rowCount()):
                item = self.todos_table.takeItem(row, 3)
                self.todos_table.setItem(row, 3, PriorityTableWidgetItem(item.text()))
            self.todos_table.sortItems(3, Qt.AscendingOrder)

    def update_todo_list(self, task_name, due_date, status, priority):
        row_position = self.todos_table.rowCount()
        self.todos_table.insertRow(row_position)
        self.todos_table.setItem(row_position, 0, QTableWidgetItem(task_name))
        self.todos_table.setItem(row_position, 1, QTableWidgetItem(due_date))
        self.todos_table.setItem(row_position, 2, QTableWidgetItem(status))
        self.todos_table.setItem(row_position, 3, QTableWidgetItem(priority))

        mark_as_done_button = QPushButton("Mark as Done")
        mark_as_done_button.clicked.connect(lambda _, row=row_position: self.mark_task_as_done(row))
        self.todos_table.setCellWidget(row_position, 4, mark_as_done_button)
        notification.notify(
            title='Task Added',
            message='A new task has been added.',
            timeout=10
        )

    def mark_task_as_done(self, row):
        self.todos_table.item(row, 0).setBackground(QColor("lime"))
        self.todos_table.item(row, 1).setBackground(QColor("lime"))
        self.todos_table.item(row, 2).setBackground(QColor("lime"))
        self.todos_table.item(row, 3).setBackground(QColor("lime"))
        self.todos_table.item(row, 2).setText("Completed")
        notification.notify(
            title='Task Completed',
            message='A task has been marked as done.',
            timeout=10
        )

    def open_edit_task_window(self, row):
        edit_task_window = EditTaskWindow(self.todos_table, row)
        edit_task_window.task_edited.connect(self.update_todo_list)
        edit_task_window.exec_()

    def show_main_window(self):
        for row in range(self.todos_table.rowCount()):
            self.todos_table.showRow(row)


class AddTaskWindow(QDialog):
    task_added = pyqtSignal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task")
        self.setGeometry(400, 400, 600, 400)

        layout = QFormLayout(self)
        self.task_name_input = QLineEdit()
        layout.addRow("Task Name:", self.task_name_input)

        self.task_description_input = QLineEdit()
        layout.addRow("Task Description:", self.task_description_input)

        self.due_date_input = QDateTimeEdit()
        self.due_date_input.setDateTime(self.due_date_input.dateTime().currentDateTime())
        layout.addRow("Due Date and Time:", self.due_date_input)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        layout.addRow("Priority:", self.priority_input)

        self.reminder_input = QComboBox()
        self.reminder_input.addItems(["YES", "NO"])
        layout.addRow("Reminder:", self.reminder_input)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        layout.addRow(add_button)

    def add_task(self):
        task_name = self.task_name_input.text()
        due_date = self.due_date_input.dateTime().toString(Qt.ISODate)
        status = "Pending"
        priority = self.priority_input.currentText()
        self.task_added.emit(task_name, due_date, status, priority)
        self.close()


class EditTaskWindow(QDialog):
    task_edited = pyqtSignal(str, str, str, str)

    def __init__(self, table, row, parent=None):
        super().__init__(parent)
        self.table = table
        self.row = row
        self.setWindowTitle("Edit Task")
        self.setGeometry(400, 400, 600, 400)

        layout = QFormLayout(self)
        self.task_name_input = QLineEdit(self.table.item(self.row, 0).text())
        layout.addRow("Task Name:", self.task_name_input)
        self.due_date_input = QDateTimeEdit()
        self.due_date_input.setDateTime(self.due_date_input.dateTime().fromString(
            self.table.item(self.row, 1).text(), Qt.ISODate))
        layout.addRow("Due Date and Time:", self.due_date_input)
        self.status_input = QLineEdit(self.table.item(self.row, 2).text())
        layout.addRow("Status:", self.status_input)
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setCurrentText(self.table.item(self.row, 3).text())
        layout.addRow("Priority:", self.priority_input)
        self.edit_button = QPushButton("Edit Task")
        self.edit_button.clicked.connect(self.edit_task)
        layout.addRow(self.edit_button)

    def edit_task(self):
        task_name = self.task_name_input.text()
        due_date = self.due_date_input.dateTime().toString(Qt.ISODate)
        status = self.status_input.text()
        priority = self.priority_input.currentText()
        self.table.removeRow(self.row)
        self.task_edited.emit(task_name, due_date, status, priority)
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
