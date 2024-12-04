import unittest
import warnings
import sys
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
        el.set('type', 'color')
        el.set('title', 'Test Color Parameter')
        el.set('visible', '1')
        el.set('removable', '0')
        el.set('readonly', '1')
        el.set('value', '(255, 100, 50, 255)')

        param_dict = XML_string_to_parameter(ET.tostring(el))

        param_res = XMLParameterFactory.parameter_list_to_parameter(param_dict)

        elem_res = parameter_to_xml_string(param_res)


        self.assertEqual(elem_res, ET.tostring(el))
    
    def test_start_with_parameter(self):
        settings = Parameter.create(name='settings', type='group',children=[{
                'name': 'bool_param',
                'type': 'bool_push',
                'title': 'Test Boolean Parameter',
                'visible': True,
                'removable': False,
                'readonly': True,
                'value': True,
                'show_pb': True,
            }])

        xml_element = parameter_to_xml_string(settings)

        param_dict = XML_string_to_parameter(xml_element)

        param_res = XMLParameterFactory.parameter_list_to_parameter(param_dict)

        self.assertEqual(settings, param_res)

    # def test_xml_with_children_to_param(self):
    #     # Create a parent XML element
    #     parent = ET.Element('paramater')
    #     parent.set('type', 'group')
    #     parent.set('title', 'Parent Parameter')

    #     # Create a child XML element
    #     child = ET.Element('parameter')
    #     child.set('type', 'bool')
    #     child.set('title', 'Child Boolean Parameter')
    #     child.set('visible', '1')
    #     child.set('removable', '0')
    #     child.set('readonly', '1')
    #     child.set('show_pb', '1')
    #     child.text = '1'

    #     parent.append(child)

    #     #print(ET.tostring(parent))

    #     param_list = XML_string_to_parameter(ET.tostring(parent))

    #     # Expected dictionary
    #     expected_list = xstp(ET.tostring(parent))
    #     # expected_list = [{
    #     #     'name': 'paramater',
    #     #     'title': 'Parent Parameter',
    #     #     'type': 'group',
    #     #     'children': [{
    #     #         'name': 'parameter',
    #     #         'readonly': True,
    #     #         'removable': False,
    #     #         'show_pb': True,
    #     #         'tip': False,
    #     #         'title': 'Child Boolean Parameter',
    #     #         'type': 'bool',
    #     #         'value': True,
    #     #         'visible': True
    #     #     }]
    #     # }]

    #     print(param_list)
    #     print(expected_list)
    #     self.assertListEqual(param_list, expected_list)


    # def test_parameter_to_xml(self):
    #     # Create a Parameter object with a single boolean parameter
    #     settings = Parameter.create(name='settings', type='group',children=[{
    #             'name': 'bool_param',
    #             'type': 'bool_push',
    #             'title': 'Test Boolean Parameter',
    #             'visible': True,
    #             'removable': False,
    #             'readonly': True,
    #             'value': True,
    #             'show_pb': True,
    #         }])

    #     # Pass the parameter directly
    #     xml_element = parameter_to_xml_string(settings)

    #     # Expected XML string
    #     expected_xml = ptxs(settings)
    #     # expected_xml = (
    #     #     b'<settings type="group" title="settings" visible="1" removable="0" readonly="0">'
    #     #     b'<bool_param type="bool" title="Test Boolean Parameter" visible="1" removable="0" readonly="1" show_pb="1" value="1" />'
    #     #     b'</settings>'
    #     # )

    #     print(f'xml_element = {xml_element}\n')
    #     print(f'expected = {expected_xml}\n\n')


    #     # Assert the XML element string matches the expected output
    #     self.assertEqual(xml_element, expected_xml)

#     def test_parameter_to_xml_with_children(self):
#         # Create a parent parameter with boolean children
#         settings = Parameter.create(name='settings', type='group',children=[
#             {
#                 'name': 'parent_param',
#                 'type': 'group',
#                 'title': 'Parent Parameter',
#                 'children': [
#                     {
#                         'name': 'child1',
#                         'type': 'bool',
#                         'title': 'Child Boolean 1',
#                         'value': True,
#                         'show_pb': True,
#                     },
#                     {
#                         'name': 'child2',
#                         'type': 'bool',
#                         'title': 'Child Boolean 2',
#                         'value': False,
#                         'show_pb': False,
#                     },
#                 ],
#             }
#         ])

#         # Pass the parent parameter directly
#         xml_element = parameter_to_xml_string(settings)

#         # Expected XML string
#         expected_xml = ptxs(settings)

#         # expected_xml = (
#         #     b'<settings type="group" title="settings" visible="1" removable="0" readonly="0">'
#         #     b'<parent_param type="group" title="Parent Parameter" visible="1" removable="0" readonly="0">'
#         #     b'<child1 type="bool" title="Child Boolean 1" visible="1" removable="0" readonly="0" show_pb="1" value="1" />'
#         #     b'<child2 type="bool" title="Child Boolean 2" visible="1" removable="0" readonly="0" show_pb="0" value="0" />'
#         #     b'</parent_param>'
#         #     b'</settings>'
#         # )

#         print(f'xml_element = {xml_element}\n')
#         print(f'expected = {expected_xml}\n\n')

#         # Assert the XML element string matches the expected output
#         self.assertEqual(xml_element, expected_xml)

    # def test_parameter_to_xml_multiple_types(self):
    #     # Create a Parameter object with various types
    #     settings = Parameter.create(name='settings', type='group', children=[
            
    #     ])

    #     # Convert the parameters to XML
    #     xml_element = parameter_to_xml_string(settings)

    #     # Expected XML string
    #     expected_xml = (
            
    #     )

    #     # Assert the XML element string matches the expected output
    #     self.assertEqual(xml_element, expected_xml)

if __name__ == '__main__':
    unittest.main()