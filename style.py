class Style():
    '''
    主要用于储存各式的css的样式
    '''
    # "QPushButton#defaultConfig"字段
    # 使该style只会覆盖对象下的类型为"QPushButton"并且名为"restorationConfig"的对象的style
    defaultConfigButton = "QPushButton#restorationConfig {" \
                              "background-color: #808080;"\
                              "border: 2px solid #4B0082;"\
                              "border-radius: 5px;"\
                              "padding: 5px;"\
                              "}"
    defaultButton = "QPushButton {" \
                    "background-color: #808080;" \
                    "border: 2px solid #4B0082;" \
                    "border-radius: 5px;" \
                    "padding: 5px;" \
                    "}"

    manageQList = "QListWidget::indicator:checked { right: 10px; }"
