from abc import ABCMeta, abstractmethod
from typing import Callable
from xml.etree import ElementTree as ET
from parameter.ioxml import set_dict_from_el
from pyqtgraph.parametertree.Parameter import PARAM_TYPES, PARAM_NAMES, Parameter

class XMLParameter(metaclass=ABCMeta):

    @classmethod
    @property
    @abstractmethod
    def PARAMETER_TYPE(cls):
        raise NotImplementedError

    @abstractmethod
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

    @abstractmethod
    def xml_elt_to_dict(el:ET.Element):
        dic = XMLParameter.set_basic_options(el)
        dic = XMLParameter.set_specific_options(el, dic)
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
            raise ValueError(f"{param_type} is not a supported parameter type.")
        
        return cls.text_adders_registry[param_type]()
    
    @staticmethod
    def xml_string_to_dict(params=[], XML_elt=None):
        try:
            if type(XML_elt) is not ET.Element:
                raise TypeError('not valid XML element')

            if len(XML_elt) == 0:
                param_dict = set_dict_from_el(XML_elt)
                params.append(param_dict)

            for el in XML_elt:
                param_dict = set_dict_from_el(el)
                if param_dict['type'] not in PARAM_TYPES:
                    param_dict['type'] = 'group'  # in case the custom group has been defined somewhere but not
                    # registered again in this session
                if len(el) == 0:
                    children = []
                else:
                    subparams = []
                    children = XMLParameterFactory.xml_string_to_dict(subparams, el)
                param_dict['children'] = children
                params.append(param_dict)

        except Exception as e:  # to be able to debug when there's an issue
            raise e
        return params