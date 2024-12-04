from pymodaq_gui.parameter.xml_parameter_factory import XMLParameter
from pyqtgraph.parametertree.parameterTypes import ColorParameter
from qtpy import QtGui

class ColorParameter(ColorParameter, XMLParameter):

    @staticmethod
    def set_specific_options(el):
        param_dict = {}
        param_dict['value'] = QtGui.QColor(*eval(el.get('value')))

        return param_dict
        
    @staticmethod
    def get_specific_options(param):
        param_value = param.opts.get('value', None)
        opts = {
            "value": str([param_value.red(), param_value.green(), param_value.blue(), param_value.alpha()])
        }

        return opts