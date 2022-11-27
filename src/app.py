import sys
import os
import shutil

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QFileDialog,
    QComboBox,
)
from settings import settings

from render_window import RobotWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRAK RENDERING")
        self.setGeometry(0, 0, 800, 600)

        widget = QWidget()
        widget.setLayout(self.__prepare_main_layout())

        self.setCentralWidget(widget)

    def __prepare_main_layout(self):
        layout = QGridLayout()
        btn = QPushButton("Upload object file")
        btn.setFixedWidth(120)
        btn.clicked.connect(self.show_upload_object_dialog)
        layout.addWidget(btn, 0, 0)

        self.object_name = QLabel(settings.default_object)
        self.object_name.setFixedHeight(20)
        layout.addWidget(self.object_name, 0, 1)

        combobox = QComboBox()
        combobox.addItems(["Ray tracing", "Path tracing", "Photon mapping"])
        layout.addWidget(combobox, 2, 0)
        layout.setRowMinimumHeight(3, 30)

        check = QCheckBox("Use hard shadow")
        check.setChecked(settings.default_use_hard_shadow)
        check.clicked.connect(settings.use_hard_shadow.on_next)
        layout.addWidget(check, 4, 0, 1, 2)

        layout.setRowMinimumHeight(6, 30)

        btn = QPushButton("Start rendering!")
        btn.clicked.connect(self.start_rendering)
        layout.addWidget(btn, 7, 0, 1, 2)

        spacer = QWidget()
        layout.addWidget(spacer)

        return layout

    def show_upload_object_dialog(self):
        file = QFileDialog.getOpenFileName(
            self, "Choose obj file", settings.objects_dir, "Object (*.obj)"
        )

        if file and file[0]:
            file_path = file[0]

            if os.path.normpath(os.path.dirname(file_path)) != os.path.normpath(
                settings.objects_dir
            ):
                shutil.copy2(file_path, settings.objects_dir)
                file_path = os.path.join(
                    settings.objects_dir, os.path.basename(file_path)
                )

            name = os.path.relpath(file_path, start=settings.resource_dir)
            self.object_name.setText(name)
            settings.object.on_next(name)

    def show_upload_skybox_dialog(self):
        file = QFileDialog.getOpenFileName(
            self,
            "Choose skybox texture",
            settings.textures_dir,
            "Image Files (*.jpg;*.jpeg;*.png)",
        )

        if file and file[0]:
            file_path = file[0]

            if os.path.normpath(os.path.dirname(file_path)) != os.path.normpath(
                settings.textures_dir
            ):
                shutil.copy2(file_path, settings.textures_dir)
                file_path = os.path.join(
                    settings.textures_dir, os.path.basename(file_path)
                )

            name = os.path.relpath(file_path, start=settings.resource_dir)
            self.skybox_name.setText(name)
            settings.skybox.on_next(name)

    @staticmethod
    def start_rendering():
        RobotWindow.run()
