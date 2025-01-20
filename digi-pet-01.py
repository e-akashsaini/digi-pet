import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class DigitalPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 150)  # Size of the window
        
        # Get screen geometry to position the window above the taskbar
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() // 2 - 100, screen.height() - 180)  # Center above taskbar

        # Load pet sprite
        self.pet_label = QLabel(self)
        self.sprites = [QPixmap(f"sheep_frame_{i}.png") for i in range(1, 5)]  # Frames for animation
        self.current_frame = 0
        self.pet_label.setPixmap(self.sprites[self.current_frame])
        self.pet_label.setGeometry(0, 0, 200, 150)

        # Set up animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500)  # 500 ms between frames

    def update_animation(self):
        """Update the sprite animation."""
        self.current_frame = (self.current_frame + 1) % len(self.sprites)
        self.pet_label.setPixmap(self.sprites[self.current_frame])

    def paintEvent(self, event):
        """Draw the grass beneath the sheep."""
        painter = QPainter(self)
        painter.setBrush(Qt.green)
        painter.drawRect(0, 120, 200, 30)  # Simple grass

    def mousePressEvent(self, event):
        """Allow user to drag the pet."""
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move the pet with mouse drag."""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DigitalPet()
    pet.show()
    sys.exit(app.exec_())
