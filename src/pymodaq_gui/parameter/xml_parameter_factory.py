from abc import ABCMeta, abstractmethod
from typing import Callable
from xml.etree import ElementTree as ET
from pyqtgraph.parametertree.Parameter import PARAM_TYPES, PARAM_NAMES, Parameter

class XMLParameter(metaclass=ABCMeta):

    @classmethod
    @property
    @abstractmethod
    def PARAMETER_TYPE(cls):
        raise NotImplementedError

    @staticmethod
    def set_group_options(el:ET.Element):
        group_options = {
            "name": el.tag,
            "type": el.get('type'),
            "title": el.get('title', el.tag),
        }
        return group_options
    
    @staticmethod
    def set_basic_options(el:ET.Element):
        basic_options = {
            "name": el.tag,
            "type": el.get('type'),
            "title": el.get('title', el.tag),
            "visible": el.get('visible', '0') == '1',
            "removable": el.get('removable', '0') == '1',
            "readonly": el.get('readonly', '0') == '1',
            "tip": el.get('tip', '0') == '1',
        }
        return basic_options
                
    @abstractmethod
    def set_specific_options(self, el:ET.Element, param_dict:dict):
        pass

    @staticmethod
    def xml_elt_to_dict(el: ET.Element):
        """Convert XML element to a dictionary."""
        param_type = el.get('type')
        param_instance = XMLParameterFactory.get_parameter_class(param_type)
        if param_instance is not None:
            dic = XMLParameter.set_basic_options(el)
        
            param_instance.set_specific_options(el, dic)
        else:
            dic = XMLParameter.set_group_options(el)
        return dic

    @staticmethod
    def get_group_options(param:Parameter):
        opts = dict([])
        param_type = str(param.type())
        opts.update(dict(type=param_type))
        title = param.opts['title']
        if title is None:
            title = param.name()
        opts.update(dict(title=title))

        boolean_opts = {
            "visible": param.opts.get("visible", True),
            "removable": param.opts.get("removable", False),
            "readonly": param.opts.get("readonly", False),
        }

        opts.update({key: '1' if value else '0' for key, value in boolean_opts.items()})

        for key in ["limits", "addList", "addText", "detlist", "movelist", "filetype"]:
            if key in param.opts:
                opts[key] = str(param.opts[key])


        return opts

    @abstractmethod
    def get_type_options(self,param:Parameter):
        pass

    @staticmethod
    def get_options(param:Parameter):
        param_type = str(param.type())
    
        param_class = XMLParameterFactory.get_parameter_class(param_type)

        if(param_class):
            opts = param_class.get_type_options(param)
        else:
            opts = XMLParameter.get_group_options(param)
            opts['type'] = param_type 
        
        return opts





class XMLParameterFactory:

    text_adders_registry = {}

    @classmethod
    def register_text_adder(cls) -> Callable:

        def inner_wrapper(wrapped_class) -> Callable:

            param_type = wrapped_class.PARAMETER_TYPE
            cls.text_adders_registry[param_type] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get_parameter_class(cls, param_type: str):

        if param_type not in cls.text_adders_registry:
            if param_type == 'group':
                return None
            raise ValueError(f"{param_type} is not a supported parameter type.")
        
        return cls.text_adders_registry[param_type]()
    
    @staticmethod
    def xml_string_to_parameter_factory(params=[], XML_elt=None):
        try:
            if type(XML_elt) is not ET.Element:
                raise TypeError('not valid XML element')

            param_dict = XMLParameter.xml_elt_to_dict(XML_elt)

            if param_dict['type'] == 'group':
                param_dict['children'] = []
                for child in XML_elt:
                    child_params = []
                    children = XMLParameterFactory.xml_string_to_parameter_factory(child_params, child)
                    param_dict['children'].extend(children)

            params.append(param_dict)

        except Exception as e:  # Handle exceptions for debugging
            raise e
        return params
    
    @staticmethod
    def parameter_to_xml_string_factory(parent_elt = None, param = None):
        from pymodaq_gui.parameter.ioxml_factory import dict_from_param
        """
        To convert a parameter object (and children) to xml data tree.

        =============== ================================ ==================================
        **Parameters**   **Type**                         **Description**

        *parent_elt*     XML element                      the root element
        *param*          instance of pyqtgraph parameter  Parameter object to be converted
        =============== ================================ ==================================

        Returns
        -------
        XML element : parent_elt
            XML element with subelements from Parameter object

        See Also
        --------
        add_text_to_elt, walk_parameters_to_xml, dict_from_param

        """
        if type(param) is None:
            raise TypeError('No valid param input')

        if parent_elt is None:
            opts = XMLParameter.get_options(param)
            parent_elt = ET.Element(param.name(), **opts)

        params_list = param.children()
        for param in params_list:
            opts = XMLParameter.get_options(param)
            elt = ET.Element(param.name(), **opts)

            # if elt.text is None:
            #     elt.text = '1'

            if param.hasChildren():
                XMLParameterFactory.parameter_to_xml_string_factory(elt, param)

            parent_elt.append(elt)

        return parent_elt
