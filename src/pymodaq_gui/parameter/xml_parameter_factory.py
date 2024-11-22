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


    @abstractmethod
    def get_options(self,param:Parameter):
        pass

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
    def xml_string_to_dict(params=[], XML_elt=None):
        try:
            if type(XML_elt) is not ET.Element:
                raise TypeError('not valid XML element')

            param_dict = XMLParameter.xml_elt_to_dict(XML_elt)

            if param_dict['type'] == 'group':
                param_dict['children'] = []
                for child in XML_elt:
                    child_params = []
                    children = XMLParameterFactory.xml_string_to_dict(child_params, child)
                    param_dict['children'].extend(children)

            params.append(param_dict)

        except Exception as e:  # Handle exceptions for debugging
            raise e
        return params
    
    @staticmethod
    def parameter_to_xml_string(param:Parameter):
        from pymodaq_gui.parameter.ioxml_factory import dict_from_param
        """ Convert  a Parameter to a XML string.

        Parameters
        ----------
        param: Parameter

        Returns
        -------
        str: XMl string

        See Also
        --------
        add_text_to_elt, walk_parameters_to_xml, dict_from_param

        Examples
        --------
        >>> from pyqtgraph.parametertree import Parameter
        >>>    #Create an instance of Parameter
        >>> settings=Parameter(name='settings')
        >>> converted_xml=parameter_to_xml_string(settings)
        >>>    # The converted Parameter
        >>> print(converted_xml)
        b'<settings title="settings" type="None" />'
        """
        if type(param) is None:
            raise TypeError('No valid param input')

        if parent_elt is None:
            opts = dict_from_param(param)
            parent_elt = ET.Element(param.name(), **opts)

        params_list = param.children()
        for param in params_list:
            opts = dict_from_param(param)
            elt = ET.Element(param.name(), **opts)
            if param.hasChildren():
                XMLParameterFactory.parameter_to_xml_string(elt, param)

            parent_elt.append(elt)

        return ET.tostring(parent_elt)
