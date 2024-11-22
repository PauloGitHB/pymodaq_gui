import unittest
from xml.etree.ElementTree import Element, tostring
from pymodaq_gui.parameter.xml_parameter_factory import XMLParameterFactory
from pymodaq_gui.parameter.pymodaq_ptypes.bool import BoolXMLParameter


class TestBoolXMLParameter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        XMLParameterFactory.register_text_adder()(BoolXMLParameter)

    def test_xml_to_dict(self):
        el = Element('parameter')
        el.set('type', 'bool')
        el.set('title', 'Test Boolean Parameter')
        el.set('visible', '1')
        el.set('removable', '0')
        el.set('readonly', '1')
        el.set('show_pb', '1')
        el.text = '1'

        param_dict = BoolXMLParameter.xml_elt_to_dict(el)

        expected_dict = {
            'name': 'parameter',
            'type': 'bool',
            'title': 'Test Boolean Parameter',
            'visible': True,
            'removable': False,
            'readonly': True,
            'tip': False,  # Default value
            'value': True,
            'show_pb': True,
        }

        #print(param_dict)

        self.assertDictEqual(param_dict, expected_dict)
    
    def test_xml_with_children_to_dict(self):
        # Create a parent XML element
        parent = Element('parameter')
        parent.set('type', 'group')
        parent.set('title', 'Parent Parameter')

        # Create a child XML element
        child = Element('parameter')
        child.set('type', 'bool')
        child.set('title', 'Child Boolean Parameter')
        child.set('visible', '1')
        child.set('removable', '0')
        child.set('readonly', '1')
        child.set('show_pb', '1')
        child.text = '1'

        # Append the child to the parent
        parent.append(child)

        # Convert parent to dictionary
        param_list = XMLParameterFactory.xml_string_to_dict([], parent)

        # Expected dictionary
        expected_list = [
            {
                'name': 'parameter',
                'type': 'group',
                'title': 'Parent Parameter',
                'children': [
                    {
                        'name': 'parameter',
                        'type': 'bool',
                        'title': 'Child Boolean Parameter',
                        'visible': True,
                        'removable': False,
                        'readonly': True,
                        'tip': False,
                        'value': True,
                        'show_pb': True,
                    }
                ],
            }
        ]

        #print(param_list)
        self.assertListEqual(param_list, expected_list)


    def test_dict_to_xml(self):
        # Sample dictionary for a boolean parameter
        param_dict = {
            'name': 'parameter',
            'type': 'bool',
            'title': 'Test Boolean Parameter',
            'visible': True,
            'removable': False,
            'readonly': True,
            'tip': False,
            'value': True,
            'show_pb': True,
        }

        # Convert the dictionary to an XML element
        el = Element('parameter')
        el.set('type', param_dict['type'])
        el.set('title', param_dict['title'])
        el.set('visible', '1' if param_dict['visible'] else '0')
        el.set('removable', '1' if param_dict['removable'] else '0')
        el.set('readonly', '1' if param_dict['readonly'] else '0')
        el.set('show_pb', '1' if param_dict['show_pb'] else '0')
        el.text = '1' if param_dict['value'] else '0'

        # Expected XML string
        expected_xml = (
            b'<parameter type="bool" title="Test Boolean Parameter" '
            b'visible="1" removable="0" readonly="1" show_pb="1">1</parameter>'
        )

        #print(tostring(el))
        # Assert the XML element string matches the expected output
        self.assertEqual(tostring(el), expected_xml)

    def test_dict_to_xml_with_children(self):
        # Sample dictionary with children
        param_dict = {
            'name': 'parameter',
            'type': 'group',
            'title': 'Parent Parameter',
            'children': [
                {
                    'name': 'parameter',
                    'type': 'bool',
                    'title': 'Child Boolean 1',
                    'value': True,
                    'show_pb': True,
                },
                {
                    'name': 'parameter',
                    'type': 'bool',
                    'title': 'Child Boolean 2',
                    'value': False,
                    'show_pb': False,
                },
            ],
        }

       
        # Convert the dictionary to XML
        xml_element = XMLParameterFactory.parameter_to_xml_string(param_dict)

        # Expected XML string
        expected_xml = (
            b'<parameter type="group" title="Parent Parameter">'
            b'<parameter type="bool" title="Child Boolean 1" show_pb="1">1</parameter>'
            b'<parameter type="bool" title="Child Boolean 2" show_pb="0">0</parameter>'
            b'</parameter>'
        )

        # Assert the XML element string matches the expected output
        self.assertEqual(tostring(xml_element), expected_xml)



