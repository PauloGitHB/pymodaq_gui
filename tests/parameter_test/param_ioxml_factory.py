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

        print(param_dict)

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


    # def test_dict_to_xml(self):
    #     # Create a sample parameter dictionary
    #     param_dict = {
    #         'name': 'parameter',
    #         'type': 'bool',
    #         'title': 'Test Boolean Parameter',
    #         'visible': True,
    #         'removable': False,
    #         'readonly': True,
    #         'tip': False,  # Default value
    #         'value': True,
    #         'show_pb': True,
    #     }
