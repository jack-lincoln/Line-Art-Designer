#! python3
# Line-Art-Designer.py - Line Art Designer is an interactive art design program.
# It allows for the user to view and modify various elements of a moving,
# linear art design in a GUI window that is launched when the program is run.

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic


class LineArtDesigner(QWidget):
    """Overall class to create the Designer."""

    def __init__(self):
        """A method to control image settings, as well as run all class methods."""

        super().__init__()

        # Load GUI blueprint
        uic.loadUi("Line-Art-Designer_Layout.ui", self)

        # Create the graphics scene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.allow_image_movement = False
        self.play_forward_true = False
        self.play_backward_true = False

        # General settings
        self.title = 'Line Art Designer'
        self.image_width = 600
        self.window_height = self.image_width + 225

        # Window setup
        self.setWindowTitle(self.title)
        self.setGeometry(50, 100, self.image_width, self.window_height)
        self.setFixedWidth(self.image_width)
        self.setFixedHeight(self.window_height)

        # Create default values for the sliders
        self.slider_vals = [51, 6, 150, 150, 6, 25]

        self.speed = self.slider_vals[0]
        self.color_count = self.slider_vals[1]
        self.color_distance = self.slider_vals[2]
        self.line_distance = self.slider_vals[3]
        self.line_thickness = self.slider_vals[4]
        self.dot_distance = self.slider_vals[5]

        # Create the slider widgets
        self.slider_0 = self.findChild(QSlider, "slider_00_speed")
        self.slider_0.setSliderPosition(self.slider_vals[0])

        self.slider_1 = self.findChild(QSlider, "slider_01_color_count")
        self.slider_1.setSliderPosition(self.slider_vals[1])

        self.slider_2 = self.findChild(QSlider, "slider_02_color_distance")
        self.slider_2.setSliderPosition(self.slider_vals[2])

        self.slider_3 = self.findChild(QSlider, "slider_03_line_distance")
        self.slider_3.setSliderPosition(self.slider_vals[3])

        self.slider_4 = self.findChild(QSlider, "slider_04_line_thickness")
        self.slider_4.setSliderPosition(self.slider_vals[4])

        self.slider_5 = self.findChild(QSlider, "slider_05_dot_distance")
        self.slider_5.setSliderPosition(self.slider_vals[5])

        # Connect the spin box widget
        self.background_stripe_count_spin_box = self.findChild(QSpinBox, "background_stripe_count_spin_box")
        self.background_stripe_count_spin_box.valueChanged.connect(self.background_strip_count_spin_box_changed)

        # Connect the combo box widgets
        self.background_colors_combo_box = self.findChild(QComboBox, "combo_box_01_background_colors")
        self.background_colors_combo_box.currentTextChanged.connect(self.background_color_combo_box_selected)

        self.design_colors_combo_box = self.findChild(QComboBox, "combo_box_00_design_color")
        self.design_colors_combo_box.currentTextChanged.connect(self.design_color_combo_box_selected)

        self.line_type_combo_box = self.findChild(QComboBox, "line_type_combo_box")
        self.line_type_combo_box.currentTextChanged.connect(self.line_type_combo_box_selected)

        # Connect the button widgets
        self.play_forward_button.clicked.connect(self.play_forward)
        self.play_backward_button.clicked.connect(self.play_backward)
        self.reset_button.clicked.connect(self.reset_image)
        self.save_button.clicked.connect(self.save)

        # Background image settings
        self.background_color_scheme = "Twilight"
        self.bg_stripe_count = 1

        # Design settings
        self.design_color_scheme = "Neon"
        self.starting_point = -1000
        self.line_type = "Solid Line"

        self.image = QImage(self.size(), QImage.Format_RGB32)

        self.count = 0

    def play_forward(self):
        """A method to have the image move continuously forward."""
        if not self.play_forward_true:
            self.play_forward_button.setText("Pause")
            self.play_backward_button.setText("Play Backward")
            self.play_backward_true = False
            self.allow_image_movement = True
            self.play_forward_true = True
        else:
            self.play_forward_button.setText("Play Forward")
            self.starting_point += 0
            # self.allow_image_movement = True
            self.play_backward_true = False
            self.play_forward_true = False

    def play_backward(self):
        """A method to have the image move continuously forward."""
        if not self.play_backward_true:
            self.play_backward_button.setText("Pause")
            self.play_forward_button.setText("Play Forward")
            self.play_forward_true = False
            self.allow_image_movement = True
            self.play_backward_true = True
        else:
            self.play_backward_button.setText("Play Backward")
            self.starting_point += 0
            # self.allow_image_movement = True
            self.play_forward_true = False
            self.play_backward_true = False

    def design_color_combo_box_selected(self):
        """A method to change the design color scheme when selected in the combo box."""
        self.design_color_scheme = self.design_colors_combo_box.currentText()

    def background_color_combo_box_selected(self):
        """A method to change the background color scheme when selected in the combo box."""
        self.background_color_scheme = self.background_colors_combo_box.currentText()

    def line_type_combo_box_selected(self):
        """A method to change the line type used in the design when selected in the combo box."""
        self.line_type = self.line_type_combo_box.currentText()

    def background_strip_count_spin_box_changed(self):
        """A method to change the background stripe count when changed in the spin box."""
        self.bg_stripe_count = self.background_stripe_count_spin_box.value()

    def paintEvent(self, event):
        """A method to setup the paint event."""

        self.draw_background()

        if self.allow_image_movement:
            canvas_painter = QPainter()
            canvas_painter.begin(self)
            canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

            self.speed = self.slider_0.value() / 500
            self.color_count = self.slider_1.value()
            self.color_distance = self.slider_2.value()
            self.line_distance = self.slider_3.value()
            self.line_thickness = int(self.slider_4.value())
            self.dot_distance = int(self.slider_5.value())

            self.get_design_colors()
            self.draw_design()
            self.count += 1

            self.scene.update()
            if self.count % 2 == 0:
                self.scene.clear()
                self.draw_design()

            self.scene.setSceneRect(0, 0, self.image_width, self.image_width)

            canvas_painter.end()

    def draw_background(self):
        """A method to draw the background."""

        pen = QPen(QColor(0, 0, 0), 1, )

        grad = QLinearGradient(QPoint(self.image_width, 0), QPoint(self.image_width, self.image_width))

        background_color_set_list = [[10, 30, 60, 110, 30, 60],       # Twilight
                                    [106, 36, 240, 250, 114, 69],     # Sunset
                                    [68, 243, 79, 250, 114, 169],     # Candyland
                                    [10, 40, 10, 80, 130, 185],       # Ocean View
                                    [30, 5, 5, 15, 5, 35]]            # Midnight

        if self.background_color_scheme == "Twilight":
            color_set = background_color_set_list[0]
        elif self.background_color_scheme == "Sunset":
            color_set = background_color_set_list[1]
        elif self.background_color_scheme == "Candyland":
            color_set = background_color_set_list[2]
        elif self.background_color_scheme == "Ocean View":
            color_set = background_color_set_list[3]
        elif self.background_color_scheme == "Midnight":
            color_set = background_color_set_list[4]

        grad_pos = 0
        grad_pos_inc = 1.0 / self.bg_stripe_count

        for i in range(self.bg_stripe_count + 1):
            grad.setColorAt(grad_pos, QColor(color_set[0], color_set[1], color_set[2]))
            grad_pos += grad_pos_inc / 2
            grad.setColorAt(grad_pos, QColor(color_set[3], color_set[4], color_set[5]))
            grad_pos += grad_pos_inc / 2

        r = QRectF(QPointF(0, 0), QSizeF(self.image_width, self.image_width))
        self.scene.setBackgroundBrush(grad)
        self.scene.addRect(r, pen)

    def get_design_colors(self):
        """A method to declare the starting and ending colors, then create a list of colors."""

        self.design_colors = []

        design_color_set_list = [[140, 255, 140, 5, 55, 140],       # Neon
                                [230, 0, 0, 230, 170, 0],           # Warm
                                [190, 160, 90, 130, 90, 5],         # Golden
                                [90, 65, 10, 70, 65, 55],           # Rustic
                                [45, 45, 45, 165, 165, 165]]        # Greytone

        if self.design_color_scheme == "Neon":
            color_set = design_color_set_list[0]
        elif self.design_color_scheme == "Warm":
            color_set = design_color_set_list[1]
        elif self.design_color_scheme == "Golden":
            color_set = design_color_set_list[2]
        elif self.design_color_scheme == "Rustic":
            color_set = design_color_set_list[3]
        elif self.design_color_scheme == "Greytone":
            color_set = design_color_set_list[4]

        self.design_colors.append((color_set[0], color_set[1], color_set[2]))

        red_increment = (color_set[3] - color_set[0]) / self.color_count
        green_increment = (color_set[4] - color_set[1]) / self.color_count
        blue_increment = (color_set[5] - color_set[2]) / self.color_count

        for i in range(self.color_count):
            color_set[0] += red_increment
            color_set[1] += green_increment
            color_set[2] += blue_increment
            self.design_colors.append(
                (int(color_set[0]), int(color_set[1]), int(color_set[2])))

    def draw_design(self):
        """A method to draw the design."""

        for j in range(self.color_count):
            for i in range(0, self.image_width, self.line_distance):

                self.qt_line_str = self.line_type_combo_box.currentText()

                if self.qt_line_str == "Solid Line":
                    self.qt_line = Qt.SolidLine
                elif self.qt_line_str == "Dash Line":
                    self.qt_line = Qt.CustomDashLine
                elif self.qt_line_str == "Dot Line":
                    self.qt_line = Qt.CustomDashLine
                elif self.qt_line_str == "Dash Dot Line":
                    self.qt_line = Qt.CustomDashLine

                pen = QPen(QColor(self.design_colors[j][0], self.design_colors[j][1], self.design_colors[j][2]),
                           self.line_thickness, self.qt_line)

                if self.qt_line_str == "Dash Line":
                    pen.setDashPattern([5, self.dot_distance])
                elif self.qt_line_str == "Dot Line":
                    pen.setDashPattern([1, self.dot_distance])
                elif self.qt_line_str == "Dash Dot Line":
                    pen.setDashPattern([5, self.dot_distance, 1, self.dot_distance])

                # Draw the pattern for the upper left corner.
                self.scene.addLine(self.starting_point + (j * self.color_distance),
                                   self.image_width - i,
                                   0 + i,
                                   self.starting_point + (j * self.color_distance),
                                   pen)

                # Draw the pattern for the upper right corner.
                self.scene.addLine(0 + i,
                                   self.starting_point + (j * self.color_distance),
                                   self.image_width - self.starting_point - (j * self.color_distance),
                                   0 + i,
                                   pen)

                # Draw the pattern for the bottom right corner.
                self.scene.addLine(self.image_width - self.starting_point - (j * self.color_distance),
                                   0 + i,
                                   self.image_width - i,
                                   self.image_width - self.starting_point - (j * self.color_distance),
                                   pen)

                # Draw the pattern for the bottom left corner.
                self.scene.addLine(self.starting_point + (j * self.color_distance),
                                   0 + i,
                                   0 + i,
                                   self.image_width - self.starting_point - (j * self.color_distance),
                                   pen)

            if self.play_forward_true:
                self.starting_point += self.speed
            elif self.play_backward_true:
                self.starting_point -= self.speed

        self.scene.update()

    def save(self):
        """A method to save the image."""

        self.allow_image_movement = False

        # selecting file path
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if file_path == "":
            return

        # Get the size of your graphicsview
        rect = self.graphicsView.viewport().rect()

        # Create a pixmap the same size as your graphicsview
        pixmap = QPixmap(rect.size())
        painter = QPainter(pixmap)

        # Render the graphicsview onto the pixmap and save it out.
        self.graphicsView.render(painter, QRectF(pixmap.rect()), rect)
        pixmap.save(file_path)

    def reset_image(self):
        """A method to reset the image to the starting variables."""

        self.scene.clear()

        self.starting_point = -1000

        # Reset play text
        self.play_forward_button.setText("Play Forward")
        self.play_backward_button.setText("Play Backward")

        # Reset booleans
        self.allow_image_movement = False
        self.play_backward_true = False
        self.play_forward_true = False

        # Reset sliders and their respective values
        self.speed = self.slider_vals[0]
        self.slider_0.setValue(self.slider_vals[0])
        self.color_count = self.slider_vals[1]
        self.slider_1.setValue(self.slider_vals[1])
        self.color_distance = self.slider_vals[2]
        self.slider_2.setValue(self.slider_vals[2])
        self.line_distance = self.slider_vals[3]
        self.slider_3.setValue(self.slider_vals[3])
        self.line_thickness = self.slider_vals[4]
        self.slider_4.setValue(self.slider_vals[4])
        self.dot_distance = self.slider_vals[5]
        self.slider_5.setValue(self.slider_vals[5])

        # Reset combo boxes
        self.design_colors_combo_box.setCurrentIndex(0)
        self.background_colors_combo_box.setCurrentIndex(0)
        self.line_type_combo_box.setCurrentIndex(0)

        # Reset spin box
        self.background_stripe_count_spin_box.setValue(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    designer = LineArtDesigner()
    designer.show()

    sys.exit(app.exec())
