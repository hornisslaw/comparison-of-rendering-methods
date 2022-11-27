import sys
from PyQt6.QtWidgets import QApplication
from app import App


def main() -> int:
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
