import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

def main():
    """
    The entry point of the application. Creates the QApplication and main window,
    then starts the event loop.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
