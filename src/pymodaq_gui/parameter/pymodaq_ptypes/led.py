from pyqtgraph.parametertree.parameterTypes.basetypes import WidgetParameterItem
from pymodaq_gui.utils.widgets import QLED
from pymodaq_gui.parameter import SimpleParameter

class LedParameterItem(WidgetParameterItem):
    """Registered parameter type which displays a QLineEdit"""

    def makeWidget(self):
        w = QLED()
        w.clickable = False
        w.set_as_false()
        w.sigChanged = w.value_changed
        w.value = w.get_state
        w.setValue = w.set_as
        self.hideWidget = False
        return w


class LedPushParameterItem(LedParameterItem):
    """Registered parameter type which displays a QLineEdit"""

    def makeWidget(self):
        w = QLED()
        w.clickable = True
        w.set_as_false()
        w.sigChanged = w.value_changed
        w.value = w.get_state
        w.setValue = w.set_as
        self.hideWidget = False
        return w


class LedParameter(SimpleParameter):
    itemClass = LedParameterItem

    def _interpretValue(self, v):
        return bool(v)

    @staticmethod
    def set_specific_options(el):
        param_dict = {}
        value = el.get('value','')
        param_dict['value'] = bool(int(value))

        return param_dict

    @staticmethod   
    def get_specific_options(param):
        opts = {
            "value": '1' if param.opts.get("value", False) else '0',
        }

        return opts

class LedPushParameter(SimpleParameter):
    itemClass = LedPushParameterItem

    def _interpretValue(self, v):
        return bool(v)

   
    
# @XMLParameterFactory.register_text_adder()
# class LedXMLParameter(XMLParameter):

#     PARAMETER_TYPE = 'led'

#     def set_specific_options(self, el, param_dict):
#         value = el.text
#         param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
#         param_dict['value'] = el.get('value','') #bool(int(value))
        
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