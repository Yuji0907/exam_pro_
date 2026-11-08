def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item= layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                clear_layout(item.layout())