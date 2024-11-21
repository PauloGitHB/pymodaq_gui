from typing import Union
from pathlib import Path

import importlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import OrderedDict
from qtpy import QtGui
from qtpy.QtCore import QDateTime
from pymodaq_gui.parameter import Parameter

from pyqtgraph.parametertree.Parameter import PARAM_TYPES, PARAM_NAMES

from pymodaq_gui.parameter.xml_parameter_factory import XMLParameterFactory

def add_text_to_elt(elt, param):
    """Add a text filed in a xml element corresponding to the parameter value

    Parameters
    ----------
    elt: XML elt
    param: Parameter

    See Also
    --------
    add_text_to_elt, walk_parameters_to_xml, dict_from_param
    """

    param_type = str(param.type())
    adder = XMLParameterFactory.get_parameter_class(param_type)
    text = adder.get_text(param, elt)
    elt.text = text

def dict_from_param(param):
    """Get Parameter properties as a dictionary

    Parameters
    ----------
    param: Parameter

    Returns
    -------
    opts: dict

    See Also
    --------
    add_text_to_elt, walk_parameters_to_xml, dict_from_param
    """

    param_type = str(param.type())
    
    param_class = XMLParameterFactory.get_parameter_class(param_type)

    opts = param_class.get_options(param)

    opts['type'] = param_type
    
    return opts


def elt_to_dict(el):
    """Convert xml element attributes to a dictionnary

    Parameters
    ----------
    el

    Returns
    -------

    """

    param_type = el.get('type')
    
    param_instance = XMLParameterFactory.get_parameter_class(param_type)
    
    return param_instance.XMLParameter.xml_elt_to_dict(el)



def parameter_to_xml_string(param):
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
    xml_elt = XMLParameterFactory.xml_string_to_dict(param=param)
    return ET.tostring(xml_elt)



def elt_to_dict_test():
    el = ET.Element('parameter')

    el = ET.Element('parameter')
    el.set('type', 'bool')
    el.set('title', 'My Boolean Parameter')
    el.set('visible', '1')
    el.set('removable', '0')
    el.set('readonly', '1')
    el.set('show_pb', '1')

    param_dict = elt_to_dict(el)
    print("Parameter dictionary:", param_dict)

def dict_from_param_test():

    param = Parameter.create(
        name='test_param',
        type='bool',
        value=True,
        title='Test Parameter',
        visible=True,
        removable=False,
        readonly=False,
        show_pb=True,
    )

    opts = dict_from_param(param)
    
    print("Extracted Parameter Options:")
    for key, value in opts.items():
        print(f"{key}: {value}")

def main():
    elt_to_dict_test()
    dict_from_param_test()

if __name__ == '__main__':
    main()