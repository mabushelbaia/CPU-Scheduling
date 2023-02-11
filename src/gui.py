import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer

class CPU_Scheduling_GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the ready queue labels
        self.ready_queue_1_label = QLabel("Ready Queue 1")
        self.ready_queue_2_label = QLabel("Ready Queue 2")
        self.ready_queue_3_label = QLabel("Ready Queue 3")
        self.ready_queue_4_label = QLabel("Ready Queue 4")

        # Create the waiting queue label
        self.waiting_queue_label = QLabel("Waiting Queue")

        # Create the running process label
        self.running_process_label = QLabel("Running Process")

        # Create the stop button
        self.stop_button = QPushButton("Stop")

        # Create the message output box
        self.message_output_box = QTextEdit()

        # Create a layout for the ready queue 1
        ready_queue_layout_1 = QVBoxLayout()
        ready_queue_layout_1.addWidget(self.ready_queue_1_label)

        # Create a layout for the ready queue 2
        ready_queue_layout_2 = QVBoxLayout()
        ready_queue_layout_2.addWidget(self.ready_queue_2_label)

        # Create a layout for the ready queue 3
        ready_queue_layout_3 = QVBoxLayout()
        ready_queue_layout_3.addWidget(self.ready_queue_3_label)

        # Create a layout for the ready queue 4
        ready_queue_layout_4 = QVBoxLayout()
        ready_queue_layout_4.addWidget(self.ready_queue_4_label)

        # Create a layout for the waiting queue
        waiting_queue_layout = QVBoxLayout()
        waiting_queue_layout.addWidget(self.waiting_queue_label)

        # Create a layout for the running process display
        running_process_layout = QVBoxLayout()
        running_process_layout.addWidget(self.running_process_label)
        running_process_layout.addWidget(self.stop_button)

        # Create a layout for the message output box
        message_output_layout = QVBoxLayout()
        message_output_layout.addWidget(self.message_output_box)

        # Create a layout for the left side of the window
        left_layout = QVBoxLayout()
        left_layout.addLayout(ready_queue_layout_1)
        left_layout.addLayout(ready_queue_layout_2)
        left_layout.addLayout(ready_queue_layout_3)
        left_layout.addLayout(ready_queue_layout_4)
        left_layout.addLayout(waiting_queue_layout)

        # Create a layout for the right side of the window
        right_layout = QVBoxLayout()

        right_layout.addLayout(running_process_layout)
        right_layout.addLayout(message_output_layout)

        # Create a layout for the entire window
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Create a central widget and set its layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the window properties
        self.setWindowTitle("CPU Scheduling GUI")
        self.setGeometry(100, 100, 800, 500)

        # Connect the stop button to a function
        self.stop_button.clicked.connect(self.stop_clicked)

        # Start a timer to update the data in the queues in real time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_queues)
        self.timer.start(1000)

    def update_queues(self):
        # Replace this with your code to retrieve the data from your CPU scheduling algorithm
        ready_queue_1_data = [100, 200, 300]
        ready_queue_2_data = [400, 500, 600]
        ready_queue_3_data = [700, 800, 900]
        ready_queue_4_data = [1000, 1100, 1200]
        waiting_queue_data = [1300, 1400, 1500]

        # Update the labels with the retrieved data
        self.ready_queue_1_label.setText("Ready Queue 1\n" + "\n".join(str(x) for x in ready_queue_1_data))
        self.ready_queue_2_label.setText("Ready Queue 2\n" + "\n".join(str(x) for x in ready_queue_2_data))
        self.ready_queue_3_label.setText("Ready Queue 3\n" + "\n".join(str(x) for x in ready_queue_3_data))
        self.ready_queue_4_label.setText("Ready Queue 4\n" + "\n".join(str(x) for x in ready_queue_4_data))
        self.waiting_queue_label.setText("Waiting Queue\n" + "\n".join(str(x) for x in waiting_queue_data))

    def stop_clicked(self):
        # Stop the timer
        self.timer.stop()

        # Add a message to the message output box
        self.message_output_box.append("Stopped")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CPU_Scheduling_GUI()
    gui.show()
    sys.exit(app.exec_())
