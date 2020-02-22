try:
    import PySide2.QtCore
    from settingswindow_qt import main
except ImportError:
    from settingswindow_wx import main

if __name__ == "__main__":
    main()
