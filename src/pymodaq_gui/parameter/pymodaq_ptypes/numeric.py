from pymodaq_gui.parameter import SimpleParameter
from pyqtgraph.parametertree.parameterTypes.numeric import NumericParameterItem
from pymodaq_gui.parameter.xml_parameter_factory import XMLParameterFactory, XMLParameter


class NumericParameter(SimpleParameter):
    itemClass = NumericParameterItem

    def __init__(self, **opts):
        super().__init__(**opts)

    def setLimits(self, limits):
        curVal = self.value()
        if curVal > limits[1]:
            self.setValue(limits[1])
        elif curVal < limits[0]:
            self.setValue(limits[0])
        super().setLimits(limits)
        return limits
    
    def set_specific_options(self, el, param_dict):
        value = el.get('value','0')
        param_type = param_dict['type']

        param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False

        if param_type == "int":
            param_dict['value'] = float(value)
        elif param_type == "float":
            param_dict['value'] = int(float(value))
        
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


# class FloatXMLParameter(XMLParameter):

#     PARAMETER_TYPE = 'float'

#     def set_specific_options(self, el, param_dict):
#         value = el.text
#         param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
#         param_dict['value'] = el.get('value','') #float(value)
        
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
    
# class IntXMLParameter(XMLParameter):

#     PARAMETER_TYPE = 'int'

#     def set_specific_options(self, el, param_dict):
#         value = el.text
#         param_dict['show_pb'] = True if el.get('show_pb', '0') == '1' else False
#         param_dict['value'] = el.get('value','')#int(float(value))
        
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