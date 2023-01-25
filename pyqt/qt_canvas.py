import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF, QRect
from PyQt5.QtGui import QPainter


class MovingRect(QGraphicsRectItem):
    def __init__(self, x1, y1, x2, y2, x, y):
        super().__init__(x1, y1, x2, y2)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        if updated_cursor_x > 560:
            updated_cursor_x = orig_position.x()
        if updated_cursor_y > 400:
            updated_cursor_y = orig_position.y()
        if updated_cursor_x < 0:
            updated_cursor_x = orig_position.x()
        if updated_cursor_y < 0:
            updated_cursor_y = orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r1, r2):
        super().__init__(0, 0, r1, r2)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        if updated_cursor_x > 560:
            updated_cursor_x = orig_position.x()
        if updated_cursor_y > 400:
            updated_cursor_y = orig_position.y()
        if updated_cursor_x < 0:
            updated_cursor_x = orig_position.x()
        if updated_cursor_y < 0:
            updated_cursor_y = orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))


class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 640, 480)

        self.moveObject = MovingObject(50, 50, 70, 80)
        self.moveObject2 = MovingObject(80, 80, 140, 60)
        self.rect_obj = MovingRect(0, 0, 50, 80, 200, 200)
        # self.moveObject2 = MovingObject(100, 100, 100)
        self.scene.addItem(self.moveObject)
        self.scene.addItem(self.moveObject2)
        self.scene.addItem(self.rect_obj)
        # self.scene.addItem(self.moveObject2)


app = QApplication(sys.argv)
view = GraphicView()
view.show()
sys.exit(app.exec_())
