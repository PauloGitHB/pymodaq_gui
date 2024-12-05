import unittest
import warnings
import sys
from qtpy import QtGui
from qtpy.QtCore import QDateTime, QTime, QDate
from xml.etree import ElementTree as ET
from pymodaq_gui.parameter.xml_parameter_factory import XMLParameterFactory
from pymodaq_gui.parameter.ioxml_factory import XML_string_to_parameter,parameter_to_xml_string
from pymodaq_gui.parameter.ioxml import parameter_to_xml_string as ptxs
from pymodaq_gui.parameter.ioxml import XML_string_to_parameter as xstp


from pymodaq_gui.parameter import Parameter


def print_parameter(param, indent=0):
    """
    Print a Parameter object with its options and children in a structured format.

    Parameters
    ----------
    param : Parameter
        The parameter to be printed.
    indent : int
        The indentation level for nested children (default is 0).
    """
    # Indentation pour un affichage hiérarchique
    prefix = " " * (indent * 4)

    # Afficher les détails du paramètre principal
    print(f"{prefix}Parameter:")
    print(f"{prefix}  Name: {param.name()}")
    print(f"{prefix}  Type: {param.type()}")
    print(f"{prefix}  Title: {param.opts.get('title', '')}")
    print(f"{prefix}  Value: {param.value() if param.opts.get('type', '') != 'group' else 'N/A'}")
    print(f"{prefix}  Options:")
    for key, value in param.opts.items():
        print(f"{prefix}    {key}: {value}")

    # Si le paramètre a des enfants, les afficher récursivement
    if param.hasChildren():
        print(f"{prefix}  Children:")
        for child in param.children():
            print_parameter(child, indent=indent + 1)


class TestBoolXMLParameter(unittest.TestCase):
    
    def test_start_with_element(self):
        el = ET.Element('parameter')
        el.set('name', 'date_param')
        el.set('type', 'date_time')
        el.set('title', 'Test Date Parameter')
        el.set('visible', '1')
        el.set('removable', '0')
        el.set('readonly', '1')
        el.set('value', "1700000000000")

        param_dict = XML_string_to_parameter(ET.tostring(el))

        param_res = XMLParameterFactory.parameter_list_to_parameter(param_dict)

        elem_res = parameter_to_xml_string(param_res)

        print(f'elem_res = {elem_res}\n\n')

        self.assertEqual(elem_res, ET.tostring(el))
    
    def test_start_with_parameter(self):
        settings = Parameter.create(name='settings', type='group',children=[{
                'name': 'date_param',
                'type': 'date_time',
                'title': 'Test Boolean Parameter',
                'visible': True,
                'removable': False,
                'readonly': True,
                'value': QDateTime.fromMSecsSinceEpoch(1700000000000),
                'show_pb': True,
            }])

        xml_element = parameter_to_xml_string(settings)

        print(xml_element)

        param_dict = XML_string_to_parameter(xml_element)

        param_res = XMLParameterFactory.parameter_list_to_parameter(param_dict)

        print_parameter(param_res)
        print_parameter(settings)

        self.assertEqual(settings, param_res)


if __name__ == '__main__':
    unittest.main()