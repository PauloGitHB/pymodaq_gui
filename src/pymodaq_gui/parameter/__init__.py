from qtpy import QtWidgets

from pyqtgraph.parametertree import parameterTypes, ParameterTree

from pyqtgraph.parametertree.parameterTypes.basetypes import WidgetParameterItem, SimpleParameter, Parameter

from pymodaq_gui.parameter.xml_parameter_factory import XMLParameter



class ParameterTree(ParameterTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header().setVisible(True)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        #self.header().setMinimumSectionSize(150)


class Parameter(Parameter, XMLParameter):
    pass

class SimpleParameter(SimpleParameter, XMLParameter):

    pass

from . import pymodaq_ptypes  #registration of custom parameter types