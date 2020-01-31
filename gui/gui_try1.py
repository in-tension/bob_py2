

from ij import IJ, ImagePlus, ImageListener
from ij.gui import RoiListener, Roi
from ij.io import DirectoryChooser


from java.awt import *
from java.awt.event import *
from javax.swing import *
from javax.swing import AbstractAction
from javax.swing.tree import *

# from bob_py import *
import bob_py

print(bob_py.__dict__.keys())

class ActionListenerFactory(AbstractAction) :

    def __init__(self, obj, func) :

        self.obj = obj
        self.func = func


    def actionPerformed(self, e) :
        self.func(e)


class BobGui(JFrame) :


    def choose_dir_al(self, e) :

        dc = DirectoryChooser('Choose a bob_py experiment folder')
        self.dir_path = dc.getDirectory()

        self.choose_dir_textField.setText(self.dir_path)



    def textField_al(self, e) :
        self.dir_path = self.choose_dir_textField.getText()

    def run_button_al(self, e) :
        print('run button al')
        exper = bob_py.Exper(self.dir_path)
        exper.hsegs()[0].nuc_bin().show()


    def __init__(self):
        self.dir_path = ''


        self.panel = JPanel()
        box_layout = BoxLayout(self.panel, BoxLayout.Y_AXIS)
        self.panel.setLayout(box_layout)
        self.panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))


        self.choose_dir_label = JLabel('Experiment Folder:')
        self.choose_dir_textField = JTextField(30)
        self.choose_dir_textField.addActionListener(ActionListenerFactory(self, self.textField_al))
        self.choose_dir_button = JButton('open')
        self.choose_dir_button.addActionListener(ActionListenerFactory(self, self.choose_dir_al))

        self.choose_dir_panel = JPanel()
        self.choose_dir_panel.add(self.choose_dir_label)
        self.choose_dir_panel.add(self.choose_dir_textField)
        self.choose_dir_panel.add(self.choose_dir_button)

        self.panel.add(self.choose_dir_panel)


        self.meta_data_mode_label = JLabel('Autogenerated meta_data file mode')
        self.raw_stack_mode = JRadioButton('raw stack mode')
        self.projection_mode = JRadioButton('projection files mode')

        self.meta_data_mode = ButtonGroup()
        self.meta_data_mode.add(self.raw_stack_mode)
        self.meta_data_mode.add(self.projection_mode)

        self.meta_data_mode_panel = JPanel(GridLayout(0, 1))
        self.meta_data_mode_panel.add(self.meta_data_mode_label)
        self.meta_data_mode_panel.add(self.raw_stack_mode)
        self.meta_data_mode_panel.add(self.projection_mode)

        self.panel.add(self.meta_data_mode_panel)

        self.run_button = JButton('Run')
        self.run_button.addActionListener(ActionListenerFactory(self, self.run_button_al))
        self.panel.add(self.run_button)


        super(BobGui, self).__init__("BobPy")
        self.getContentPane().add(self.panel)
        self.pack()
        self.setLocationRelativeTo(None)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)



bpg = BobGui()
