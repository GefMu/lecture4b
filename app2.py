import sys
from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
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
        self.resize(1180, 720)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        plot_widget = QWidget()
        layout = QVBoxLayout(plot_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        layout.addWidget(load_button)

        self.figure = Figure(facecolor="#ffffff")
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        main_layout.addWidget(plot_widget, 3)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Months", "Rainfall [mm]"])
        self.table.setMinimumWidth(360)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table, 2)

        self.setCentralWidget(central_widget)

    def populate_table(self):
        self.table.setRowCount(len(self.month_names))

        for row, (month, rainfall) in enumerate(
            zip(self.month_names, self.rainfall_list)
        ):
            self.table.setItem(row, 0, QTableWidgetItem(month))
            self.table.setItem(row, 1, QTableWidgetItem(str(rainfall)))

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
            self.populate_table()

    def draw_graph(self):
        axes = self.figure.add_subplot(111)
        axes.set_facecolor("#ffffff")
        axes.bar(self.month_names, self.rainfall_list, color="#2563eb", width=0.65)
        axes.set_title(
            "Monthly Rainfall",
            color="#1e293b",
            pad=18,
            fontweight="semibold",
        )
        axes.set_xlabel("Months", color="#475569", labelpad=10)
        axes.set_ylabel("Rainfall [mm]", color="#475569", labelpad=10)
        axes.set_axisbelow(True)
        axes.grid(axis="y", color="#e2e8f0", linestyle="--", linewidth=0.8)
        for spine in ("top", "right"):
            axes.spines[spine].set_visible(False)
        for spine in ("bottom", "left"):
            axes.spines[spine].set_color("#cbd5e1")
        axes.tick_params(colors="#64748b")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet_path = Path(__file__).resolve().with_name("style.qss")
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))
    window = PlotWindow()
    window.show()
    sys.exit(app.exec())
