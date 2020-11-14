def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            # call added custom destroy function on widget destroy if exists
            destroyFn = getattr(child.widget(), "onDestroy", None)
            if callable(destroyFn):
                destroyFn()
            child.widget().deleteLater()
        elif child.layout():
            clearLayout(child.layout())
            child.layout().setParent(None)