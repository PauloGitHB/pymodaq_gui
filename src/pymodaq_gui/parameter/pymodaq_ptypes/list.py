from qtpy import QtWidgets, QtGui, QtCore
from pyqtgraph.parametertree.parameterTypes.list import ListParameter, ListParameterItem
from pyqtgraph.parametertree.Parameter import ParameterItem
from pymodaq_gui.parameter.xml_parameter_factory import XMLParameterFactory, XMLParameter


class Combo_pb(QtWidgets.QWidget):

    def __init__(self, items=[]):
        super(Combo_pb, self).__init__()
        self.items = items
        self.initUI()
        self.count = self.combo.count

    def initUI(self):
        """
            Init the User Interface.
        """
        self.hor_layout = QtWidgets.QHBoxLayout()
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(self.items)
        self.add_pb = QtWidgets.QPushButton()
        self.add_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_pb.setIcon(icon3)
        self.hor_layout.addWidget(self.combo)
        self.hor_layout.addWidget(self.add_pb)
        self.hor_layout.setSpacing(0)
        self.hor_layout.setContentsMargins(0, 0, 0, 0)
        self.add_pb.setMaximumWidth(25)
        self.setLayout(self.hor_layout)
        self.currentText = self.combo.currentText
        self.setCurrentIndex = self.combo.setCurrentIndex
        self.clear = self.combo.clear
        self.addItem = self.combo.addItem
        self.findText = self.combo.findText


class ListParameterItem(ListParameterItem):
    """
        WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.

    """

    def __init__(self, param, depth):
        super().__init__(param, depth)

    def makeWidget(self):
        """
            Make a widget from self parameter options, connected to the buttonClicked function.

            Returns
            -------
            w:widget
                the initialized widget

            See Also
            --------
            buttonClicked, limitsChanged,
        """
        opts = self.param.opts
        t = opts['type']
        w = Combo_pb()
        w.add_pb.clicked.connect(self.buttonClicked)
        w.setMaximumHeight(20)  # # set to match height of spin box and line edit
        if 'show_pb' in opts:
            w.add_pb.setVisible(opts['show_pb'])
        else:
            w.add_pb.setVisible(False)
        w.sigChanged = w.combo.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w  # # needs to be set before limits are changed
        self.limitsChanged(self.param, self.param.opts['limits'])
        if len(self.forward) > 0:
            self.setValue(self.param.value())
        return w

    def buttonClicked(self):
        """
            |
            | Append the self limits attributes an added parameter with string value.
            | Update parameter and call the limitschanged method to map the added parameter.

            See Also
            --------
            limitsChanged,
        """
        if isinstance(self.param.opts['limits'], list):
            text, ok = QtWidgets.QInputDialog.getText(None, "Enter a value to add to the parameter",
                                                      "String value:", QtWidgets.QLineEdit.Normal)
            if ok and not (text == ""):
                self.param.opts['limits'].append(text)
                self.limitsChanged(self.param, self.param.opts['limits'])
                self.param.setValue(text)
        elif isinstance(self.param.opts['limits'], dict):
            text, ok = QtWidgets.QInputDialog.getText(None, "Enter a text to add to the parameter",
                                                      "String value:", QtWidgets.QLineEdit.Normal)
            if ok and not (text == ""):

                value, ok = QtWidgets.QInputDialog.getInt(None, "Enter an integer value to add to the parameter",
                                                          "integer value:", QtWidgets.QLineEdit.Normal)
                if ok:
                    self.param.opts['limits'].update({text: value})
                    self.limitsChanged(self.param, self.param.opts['limits'])
                    self.param.setValue(text)

    def optsChanged(self, param, opts):
        """
            Called when any options are changed that are not name, value, default, or limits.

            =============== ================================== =======================================
            **Parameters**    **Type**                           **Description**
            *param*           instance of pyqtgraph parameter    The parameter to be checked
            *opts*            string list                        The option dictionnary to be checked
            =============== ================================== =======================================

            See Also
            --------
            optsChanged
        """
        super().optsChanged(param, opts)
        if 'show_pb' in opts:
            self.widget.add_pb.setVisible(opts['show_pb'])
        if 'enabled' in opts:
            self.widget.setEnabled(opts['enabled'])


class ListParameter(ListParameter, XMLParameter):
    """
        =============== =======================================
        **Attributes**    **Type**
        *itemClass*       instance of ListParameterItem_custom
        *sigActivated*    instance of pyqt Signal
        =============== =======================================
    """
    itemClass = ListParameterItem
    sigActivated = QtCore.Signal(object)

    def __init__(self, **opts):
        super().__init__(**opts)

    def activate(self):
        """
            Emit the Activated signal.
        """
        self.sigActivated.emit(self)
        self.emitStateChanged('activated', None)

    @staticmethod
    def set_specific_options(el):
        param_dict = {}
        value = el.get('value',None)    
        try:
            param_dict['value'] = eval(value)
        except Exception:
            param_dict['value'] = value

        return param_dict

    @staticmethod
    def get_specific_options(param):
        param_value = param.opts.get('value', None)

        if isinstance(param_value, str):
            value = "str('{}')".format(param_value)
        elif isinstance(param_value, int):
            value = 'int({})'.format(param_value)
        elif isinstance(param_value, float):
            value = 'float({})'.format(param_value)
        else:
            value = str(param_value)
        
        opts = {
            "value": value,
        }

        return opts


# @XMLParameterFactory.register_text_adder()
# class ListXMLParameter(XMLParameter):

#     PARAMETER_TYPE = 'list'

#     def set_specific_options(self, el, param_dict):
#         value = el.text
#         param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
#         param_dict['value'] = el.get('value','')
#         # try:
#         #     param_dict['value'] = eval(value)
#         # except Exception:
#         #     param_dict['value'] = value

#     def get_type_options(self, param):
#         opts = {
#             "type": self.PARAMETER_TYPE,
#             "title": param.opts.get("title", param.name())
#         }

#         boolean_opts = {
#             "visible": param.opts.get("visible", True),
#             "removable": param.opts.get("removable", False),
#             "readonly": param.opts.get("readonly", False),
#             "show_pb": param.opts.get("show_pb", False),
#             "value":    param.opts.get("value", False),
#         }
        
#         opts.update({key: '1' if value else '0' for key, value in boolean_opts.items()})

#         for key in ["limits", "addList", "addText", "detlist", "movelist", "filetype"]:
#             if key in param.opts:
#                 opts[key] = str(param.opts[key])

#         return opts