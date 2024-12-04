from qtpy import QtWidgets
from pyqtgraph.parametertree.parameterTypes.basetypes import WidgetParameterItem
from pymodaq_gui.parameter import Parameter


class BoolParameter(Parameter):
    @staticmethod
    def set_specific_options(el):
        param_dict = {}
        param_dict['value'] = True if el.text == '1' else False

        return param_dict
        
    @staticmethod    
    def get_specific_options(param):
        """
        Generate a dictionary of type options for a given parameter of type bool_push.
        Args:
            param (Parameter): The parameter object containing options.
        Returns:
            dict: A dictionary containing the type options for the parameter.
        """

        opts = {
            "value": '1' if param.opts.get("value", False) else '0',
        }

        return opts
    

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


class BoolPushParameter(BoolParameter):
    itemClass = BoolPushParameterItem

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    

# @XMLParameterFactory.register_text_adder()
# class BoolXMLParameter(XMLParameter):

#     PARAMETER_TYPE = 'bool'

#     def set_specific_options(self, el, param_dict):
#         value = el.get('value','0')
#         param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
#         param_dict['value'] = True if value == '1' else False
        
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
