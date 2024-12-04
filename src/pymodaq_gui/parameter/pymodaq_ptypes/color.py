from pymodaq_gui.parameter.xml_parameter_factory import XMLParameter
from pyqtgraph.parametertree.parameterTypes import ColorParameter
from qtpy import QtGui

class ColorParameter(ColorParameter, XMLParameter):
    def set_specific_options(self, el, param_dict):
        value = el.get('value','')
        param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
        param_dict['value'] = QtGui.QColor(*eval(value))
        
    def get_type_options(self, param):
        opts = {
            "type": self.PARAMETER_TYPE,
            "title": param.opts.get("title", param.name())
        }

        boolean_opts = {
            "visible": param.opts.get("visible", True),
            "removable": param.opts.get("removable", False),
            "readonly": param.opts.get("readonly", False),
            "show_pb": param.opts.get("show_pb", False),
            "value":    param.opts.get("value", False),
        }
        
        opts.update({key: '1' if value else '0' for key, value in boolean_opts.items()})

        for key in ["limits", "addList", "addText", "detlist", "movelist", "filetype"]:
            if key in param.opts:
                opts[key] = str(param.opts[key])

        return opts