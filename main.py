
import sys

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout,
    QProgressBar, QCheckBox, QMessageBox, QAbstractItemView,
    QHeaderView
)

from task_logic import (
    load_tasks,
    add_task,
    update_task,
    delete_task,
    set_task_completed,
    get_visible_task_indices
)


class TodoListWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "To-Do List | Ugyen Lhaden | [Your Roll Number]"
        )
        self.setMinimumSize(950, 650)

        # Load saved tasks
        self.tasks = load_tasks()
        self.visible_indices = []

        self.create_menu()
        self.create_interface()
        self.apply_style()
        self.refresh_table()

    # -------------------- MENU BAR --------------------

    def create_menu(self):

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About To-Do List", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    # -------------------- USER INTERFACE --------------------

    def create_interface(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(22, 18, 22, 18)

        central_widget.setLayout(main_layout)

        # Heading
        heading = QLabel("To-Do List")
        heading.setObjectName("heading")

        subtitle = QLabel(
            "A simple space to plan, organise and finish your tasks."
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(heading)
        main_layout.addWidget(subtitle)

        # Task input section
        input_layout = QGridLayout()
        input_layout.setHorizontalSpacing(12)
        input_layout.setVerticalSpacing(10)

        input_layout.addWidget(QLabel("Task name"), 0, 0)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(
            "For example: Complete GUI assignment"
        )
        input_layout.addWidget(self.task_input, 0, 1)

        input_layout.addWidget(QLabel("Priority"), 0, 2)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        input_layout.addWidget(self.priority_input, 0, 3)

        input_layout.addWidget(QLabel("Category"), 1, 0)

        self.category_input = QComboBox()
        self.category_input.addItems(
            ["Study", "Personal", "Work", "Other"]
        )
        input_layout.addWidget(self.category_input, 1, 1)

        input_layout.addWidget(QLabel("Due date"), 1, 2)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.date_input.setDate(QDate.currentDate())
        input_layout.addWidget(self.date_input, 1, 3)

        main_layout.addLayout(input_layout)

        # Action buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Task")
        self.update_button = QPushButton("Update Task")
        self.delete_button = QPushButton("Delete Task")
        self.complete_button = QPushButton("Mark Complete")
        self.clear_button = QPushButton("Clear")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Search and filter section
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by task name..."
        )

        self.filter_input = QComboBox()
        self.filter_input.addItems(
            ["All Tasks", "Pending", "Completed"]
        )

        self.hide_completed = QCheckBox(
            "Hide completed tasks"
        )

        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(self.filter_input, 1)
        filter_layout.addWidget(self.hide_completed, 1)

        main_layout.addLayout(filter_layout)

        # Task table
        self.task_table = QTableWidget()

        self.task_table.setColumnCount(5)

        self.task_table.setHorizontalHeaderLabels([
            "Task",
            "Priority",
            "Category",
            "Due Date",
            "Status"
        ])

        self.task_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.task_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.task_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.task_table.verticalHeader().setVisible(False)

        self.task_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        main_layout.addWidget(self.task_table, 1)

        # Progress tracking
        self.progress_label = QLabel("Task progress: 0%")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_bar)

        self.statusBar().showMessage(
            "Welcome to To-Do List"
        )

        # -------------------- SIGNALS AND SLOTS --------------------

        self.add_button.clicked.connect(
            self.add_new_task
        )

        self.update_button.clicked.connect(
            self.update_selected_task
        )

        self.delete_button.clicked.connect(
            self.delete_selected_task
        )

        self.complete_button.clicked.connect(
            self.complete_selected_task
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        self.search_input.textChanged.connect(
            self.refresh_table
        )

        self.filter_input.currentTextChanged.connect(
            self.refresh_table
        )

        self.hide_completed.stateChanged.connect(
            self.refresh_table
        )

        self.task_table.itemSelectionChanged.connect(
            self.load_selected_task
        )

    # -------------------- ADD TASK --------------------

    def add_new_task(self):

        title = self.task_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Missing task",
                "Please enter a task name."
            )
            self.task_input.setFocus()
            return

        # Check duplicate tasks
        if any(
            task["title"].casefold() == title.casefold()
            for task in self.tasks
        ):
            QMessageBox.warning(
                self,
                "Duplicate task",
                "A task with this name already exists."
            )
            self.task_input.setFocus()
            return

        due_date = self.date_input.date().toString(
            "yyyy-MM-dd"
        )

        add_task(
            self.tasks,
            title,
            self.priority_input.currentText(),
            self.category_input.currentText(),
            due_date
        )

        self.clear_form()
        self.refresh_table()

        self.statusBar().showMessage(
            "Task added and saved."
        )

    # -------------------- SELECT TASK --------------------

    def load_selected_task(self):

        selected_rows = (
            self.task_table.selectionModel().selectedRows()
        )

        if not selected_rows:
            return

        row = selected_rows[0].row()

        if row >= len(self.visible_indices):
            return

        task_index = self.visible_indices[row]
        task = self.tasks[task_index]

        self.task_input.setText(task["title"])

        self.priority_input.setCurrentText(
            task["priority"]
        )

        self.category_input.setCurrentText(
            task["category"]
        )

        selected_date = QDate.fromString(
            task["due_date"],
            "yyyy-MM-dd"
        )

        if selected_date.isValid():
            self.date_input.setDate(selected_date)

    # -------------------- UPDATE TASK --------------------

    def update_selected_task(self):

        selected_rows = (
            self.task_table.selectionModel().selectedRows()
        )

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No selection",
                "Select a task to update."
            )
            return

        title = self.task_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Missing task",
                "Task name cannot be empty."
            )
            return

        row = selected_rows[0].row()
        task_index = self.visible_indices[row]

        # Check duplicate task names
        for index, task in enumerate(self.tasks):

            if (
                index != task_index
                and task["title"].casefold() == title.casefold()
            ):
                QMessageBox.warning(
                    self,
                    "Duplicate task",
                    "Another task already uses this name."
                )
                return

        due_date = self.date_input.date().toString(
            "yyyy-MM-dd"
        )

        update_task(
            self.tasks,
            task_index,
            title,
            self.priority_input.currentText(),
            self.category_input.currentText(),
            due_date
        )

        self.clear_form()
        self.refresh_table()

        self.statusBar().showMessage(
            "Task updated and saved."
        )

    # -------------------- DELETE TASK --------------------

    def delete_selected_task(self):

        selected_rows = (
            self.task_table.selectionModel().selectedRows()
        )

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No selection",
                "Select a task to delete."
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirm deletion",
            "Are you sure you want to delete the selected task?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            row = selected_rows[0].row()
            task_index = self.visible_indices[row]

            delete_task(self.tasks, task_index)

            self.clear_form()
            self.refresh_table()

            self.statusBar().showMessage(
                "Task deleted."
            )

    # -------------------- COMPLETE TASK --------------------

    def complete_selected_task(self):

        selected_rows = (
            self.task_table.selectionModel().selectedRows()
        )

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No selection",
                "Select a task first."
            )
            return

        row = selected_rows[0].row()
        task_index = self.visible_indices[row]

        if self.tasks[task_index]["completed"]:

            QMessageBox.information(
                self,
                "Already completed",
                "This task is already completed."
            )
            return

        set_task_completed(
            self.tasks,
            task_index,
            True
        )

        self.clear_form()
        self.refresh_table()

        self.statusBar().showMessage(
            "Task marked as completed."
        )

    # -------------------- REFRESH TABLE --------------------

    def refresh_table(self, *_):

        keyword = (
            self.search_input.text()
            if hasattr(self, "search_input") else ""
        )

        status = (
            self.filter_input.currentText()
            if hasattr(self, "filter_input") else "All Tasks"
        )

        hide_done = (
            self.hide_completed.isChecked()
            if hasattr(self, "hide_completed") else False
        )

        self.visible_indices = get_visible_task_indices(
            self.tasks,
            keyword,
            status,
            hide_done
        )

        self.task_table.setRowCount(
            len(self.visible_indices)
        )

        for row, task_index in enumerate(
            self.visible_indices
        ):

            task = self.tasks[task_index]

            values = [
                task["title"],
                task["priority"],
                task["category"],
                task["due_date"],
                "Completed" if task["completed"] else "Pending"
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(value)

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter
                    | Qt.AlignmentFlag.AlignLeft
                )

                self.task_table.setItem(
                    row,
                    column,
                    item
                )

        # Calculate task progress
        total = len(self.tasks)

        completed = sum(
            1 for task in self.tasks
            if task["completed"]
        )

        percentage = (
            round(completed / total * 100)
            if total else 0
        )

        self.progress_bar.setValue(percentage)

        self.progress_label.setText(
            f"Task progress: {percentage}% "
            f"({completed} of {total} completed)"
        )

    # -------------------- CLEAR FORM --------------------

    def clear_form(self):

        self.task_input.clear()

        self.priority_input.setCurrentIndex(0)

        self.category_input.setCurrentIndex(0)

        self.date_input.setDate(
            QDate.currentDate()
        )

        self.task_table.clearSelection()

        self.task_input.setFocus()

    # -------------------- ABOUT DIALOG --------------------

    def show_about(self):

        QMessageBox.about(
            self,
            "About To-Do List",
            "To-Do List Management System\n\n"
            "Developed by: Ugyen Lhaden\n"
            "Roll Number: [Your Roll Number]\n"
            "Framework: PyQt6\n"
            "Purpose: To organise tasks and track completion."
        )

    # -------------------- STYLING --------------------

    def apply_style(self):

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #FFF6F9;
                color: #563344;
                font-family: Arial;
                font-size: 13px;
            }

            QLabel {
                color: #75465D;
            }

            QLabel#heading {
                color: #B83F72;
                font-size: 30px;
                font-weight: bold;
                padding-top: 4px;
            }

            QLabel#subtitle {
                color: #8D687A;
                font-size: 13px;
                padding-bottom: 8px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #FFFFFF;
                border: 1px solid #E8B7CA;
                border-radius: 7px;
                padding: 8px;
                min-height: 22px;
                selection-background-color: #E88EAD;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #D96F96;
            }

            QPushButton {
                background-color: #E88EAD;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #D96F96;
            }

            QPushButton:pressed {
                background-color: #B83F72;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #FFF0F5;
                border: 1px solid #E8B7CA;
                border-radius: 7px;
                gridline-color: #F3DCE5;
                selection-background-color: #F5C5D7;
                selection-color: #563344;
            }

            QHeaderView::section {
                background-color: #D96F96;
                color: white;
                padding: 9px;
                border: none;
                font-weight: bold;
            }

            QProgressBar {
                background-color: white;
                border: 1px solid #E8B7CA;
                border-radius: 7px;
                text-align: center;
                min-height: 18px;
                color: #75465D;
            }

            QProgressBar::chunk {
                background-color: #D96F96;
                border-radius: 6px;
            }

            QMenuBar {
                background-color: #FCE6EE;
                color: #75465D;
            }

            QMenuBar::item:selected,
            QMenu::item:selected {
                background-color: #F5C5D7;
            }

            QStatusBar {
                background-color: #FCE6EE;
                color: #75465D;
            }
        """)


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = TodoListWindow()
    window.show()

    sys.exit(app.exec())
