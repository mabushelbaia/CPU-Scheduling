import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, pyqtSignal, QObject
class CPU_Scheduling_GUI(QMainWindow):
    signal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.Flag = True
        ReadyQueue1 = QVBoxLayout()
        self.ReadyQueue1_text = QLabel()
        ReadyQueue1.addWidget(QLabel("Ready Queue 1"))
        ReadyQueue1.addWidget(self.ReadyQueue1_text)
        ReadyQueue2 = QVBoxLayout()
        self.ReadyQueue2_text = QLabel()
        ReadyQueue2.addWidget(QLabel("Ready Queue 2"))
        ReadyQueue2.addWidget(self.ReadyQueue2_text)
        ReadyQueue3 = QVBoxLayout()
        self.ReadyQueue3_text = QLabel()
        ReadyQueue3.addWidget(QLabel("Ready Queue 3"))
        ReadyQueue3.addWidget(self.ReadyQueue3_text)
        ReadyQueue4 = QVBoxLayout()
        self.ReadyQueue4_text = QLabel()
        ReadyQueue4.addWidget(QLabel("Ready Queue 4"))
        ReadyQueue4.addWidget(self.ReadyQueue4_text)
        WaitingQueue = QVBoxLayout()
        self.WaitingQueue_text = QLabel()
        WaitingQueue.addWidget(QLabel("Waiting Queue"))
        WaitingQueue.addWidget(self.WaitingQueue_text)
        self.stop_button = QPushButton("Stop")
        self.message_output_box = QTextEdit()
        RunningOutput = QVBoxLayout()
        self.RuntingOutput_text = QLabel("Running Process: None")
        self.TIME = QLabel("Time: 0")
        self.FinishedOutput = QLabel("Finished Process:")
        RunningOutput.addWidget(self.TIME)
        RunningOutput.addWidget(self.FinishedOutput)
        RunningOutput.addWidget(self.RuntingOutput_text)
        RunningOutput.addWidget(self.stop_button)
        left_layout = QVBoxLayout()
        left_layout.addLayout(ReadyQueue1)
        left_layout.addLayout(ReadyQueue2)
        left_layout.addLayout(ReadyQueue3)
        left_layout.addLayout(ReadyQueue4)
        left_layout.addLayout(WaitingQueue)
        right_layout2 = QVBoxLayout()
        right_layout = QVBoxLayout()
        right_layout.addLayout(RunningOutput)
        right_layout2.addLayout(right_layout)
        ConsoleOutput = QVBoxLayout()
        ConsoleOutput.addWidget(QLabel("Console Output"))
        ConsoleOutput_text = QTextEdit()
        ConsoleOutput.addWidget(ConsoleOutput_text)
        ConsoleOutput_text.setReadOnly(True)
        right_layout2.addLayout(ConsoleOutput)
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout2)
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
        # self.timer.timeout.connect(self.update_queues)
        self.timer.start(1000)

    def update_queues(self, queue1, queue2,queue3,queue4,waiting_queue,running_process,finished_process, timer):
        self.ReadyQueue1_text.setText(queue1)
        self.ReadyQueue2_text.setText(queue2)
        self.ReadyQueue3_text.setText(queue3)
        self.ReadyQueue4_text.setText(queue4)
        self.WaitingQueue_text.setText(waiting_queue)
        self.FinishedOutput.setText(f"Finished Processes: {finished_process}")
        if running_process:
            self.RuntingOutput_text.setText(f"Running Process: P{running_process.id}")
        else:
            self.RuntingOutput_text.setText(f"Running Process: None")
        self.TIME.setText(f"Time: {timer}")
    def stop_clicked(self):
        # Stop the timer
        self.signal.emit(False)
        # Add a message to the message output box
        if self.Flag:
            self.stop_button.setText("Resume")
            self.Flag = False
            return 1
        else:
            self.stop_button.setText("Stop")
            self.Flag = True
            return 0

def run_gui():
    app = QApplication(sys.argv)
    gui = CPU_Scheduling_GUI()
    gui.show()
    sys.exit(app.exec_())
