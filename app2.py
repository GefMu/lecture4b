import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.month_names = []
        self.rainfall_list = []

        self.setWindowTitle("Data Plot")
        self.filename = ""

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        layout.addWidget(load_button)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.setCentralWidget(central_widget)
    

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "All Files (*);;CSV Files (*.csv);;Text Files (*.txt)",
        )

        if filename:

            with open(filename, 'r') as f:
                next(f)

                for line in f:
                    parts = line.split(',')

                    self.month_names.append(parts[0])
                    self.rainfall_list.append(int(parts[1]))

            self.draw_graph()

    def draw_graph(self):
        axes = self.figure.add_subplot(111)
        axes.bar(self.month_names,self.rainfall_list)
        axes.set_title("Example Graph")
        axes.set_xlabel("Months")
        axes.set_ylabel("Rain in [mm]")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec())
