from qtpy import QtWidgets
from pyqtgraph.parametertree.parameterTypes.basetypes import WidgetParameterItem, SimpleParameter
from xml_parameter_factory import XMLParameter, XMLParameterFactory


class BoolPushParameterItem(WidgetParameterItem):
    """Registered parameter type which displays a QLineEdit"""

    def makeWidget(self):
        opts = self.param.opts
        w = QtWidgets.QPushButton()
        if 'label' in opts:
            w.setText(opts['label'])
        elif 'title' in opts:
            w.setText(opts['title'])
        else:
            w.setText(opts['name'])
        # w.setMaximumWidth(50)
        w.setCheckable(True)
        w.sigChanged = w.toggled
        w.value = w.isChecked
        w.setValue = w.setChecked
        w.setEnabled(not opts.get('readonly', False))
        self.hideWidget = False
        return w


class BoolPushParameter(SimpleParameter):
    itemClass = BoolPushParameterItem

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@XMLParameterFactory.register_text_adder()
class BoolXMLParameter(XMLParameter):

    PARAMETER_TYPE = 'bool'

    def set_specific_options(self, el, param_dict):
        param_dict['value'] = True if el.text == '1' else False
        param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
       #value 
        
    def get_options(self, param):
        opts = {
            "type": self.PARAMETER_TYPE,
            "title": param.opts.get("title", param.name())
        }

        boolean_opts = {
            "visible": param.opts.get("visible", True),
            "removable": param.opts.get("removable", False),
            "readonly": param.opts.get("readonly", False),
            "show_pb": param.opts.get("show_pb", False)
        }
        opts.update({key: '1' for key, value in boolean_opts.items() if value})

        for key in ["limits", "addList", "addText", "detlist", "movelist", "filetype"]:
            if key in param.opts:
                opts[key] = str(param.opts[key])

        return opts
