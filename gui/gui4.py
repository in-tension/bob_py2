

from ij import IJ, ImagePlus, ImageListener
from ij.gui import RoiListener, Roi
from ij.io import DirectoryChooser


from java.awt.event import KeyEvent, KeyAdapter, MouseWheelListener, WindowAdapter
from java.awt import Color, Rectangle, GridBagLayout, GridBagConstraints as GBC, Dimension, BorderLayout, GridLayout
from javax.swing import JFrame, JPanel, JLabel, JTextField, JButton, BorderFactory, JOptionPane, AbstractAction, JTree, JScrollPane, BoxLayout, JTextArea

from javax.swing.tree import DefaultMutableTreeNode

from net.miginfocom.swing import MigLayout

import bob_py
import brutils as br

print(bob_py.__dict__.keys())

class ActionListenerFactory(AbstractAction) :

    def __init__(self, obj, func) :

        self.obj = obj
        self.func = func


    def actionPerformed(self, e) :
        self.func(e)


class BobPyGui(JFrame) :


    def choose_dir_al(self, e) :

        dc = DirectoryChooser('Choose a bob_py experiment folder')
        self.dir_path = dc.getDirectory()

        self.choose_dir_textField.setText(self.dir_path)
        self.got_exper(self.dir_path)



    def textField_al(self, e) :
        self.dir_path = self.choose_dir_textField.getText()
        self.got_exper(self.dir_path)


    def got_exper(self, dir_path) :
        self.exper = bob_py.Exper(dir_path)
        self.make_tree()

    def make_tree(self) :
        print('make_tree')
        root = DefaultMutableTreeNode(self.exper.name)

        sb = br.SimilarityBuilder()

        for hseg in self.exper.hsegs() :
        	all_file_dict = hseg.file_dict()
        	all_file_dict.update(hseg.cell_file_dict())
        	all_file_dict.update(hseg.bin_file_dict())
        	sb.add_group(hseg.name, all_file_dict)

        simprofile, comparisons = sb.simprofile_comparison()

        sim_str = ''
        for val in simprofile :
            sim_str += str(val) + '\n'

        tp = JTextArea(sim_str)

        stp = JScrollPane()
        stp.getViewport().setView(tp)
        #
        # stp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        # stp.setPreferredSize(Dimension(250, 250));
        # tp.setPreferredSize(Dimension(250, 250))
        stp_panel = JPanel(BorderLayout())
        stp_panel.add(tp, BorderLayout.CENTER)


        # self.add(stp_panel, 'grow')


        for hseg in self.exper.hsegs() :
            hseg_node = DefaultMutableTreeNode(hseg.name)
            root.add(hseg_node)
            if len(comparisons[hseg.name]) > 0 :
                for definer, file_names in comparisons[hseg.name].items() :
                    for file_name in file_names :
                        node_str = definer + ': ' + file_name
                        hseg_node.add(DefaultMutableTreeNode(node_str))
            # for file_suf in hseg.file_dict() :
                # hseg_node.add(DefaultMutableTreeNode(file_suf))



        self.tree = JTree(root)
        scrollPane = JScrollPane()
        scrollPane.getViewport().setView((self.tree))
        # scrollPan
        # scrollPane.setPreferredSize(Dimension(300,250))



        tree_panel = JPanel(BorderLayout())
        tree_panel.add(scrollPane, BorderLayout.CENTER)

        combo_panel = JPanel(GridLayout(0,2,10,10))
        # combo_panel.setLayout(BoxLayout(combo_panel, BoxLayout.X_AXIS))
        combo_panel.add(stp_panel)#, BorderLayout.LINE_START)
        combo_panel.add(tree_panel)#, BorderLayout.LINE_END)
        self.panel.add(combo_panel)
        # self.add(scrollPane, 'grow')
        self.revalidate()





    def __init__(self):
        super(BobPyGui, self).__init__("BobPy")

        self.dir_path = ''



        # ml = MigLayout('fill')
        # self.setLayout(ml)
        self.panel = JPanel()
        self.panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))

        box_layout = BoxLayout(self.panel, BoxLayout.Y_AXIS)

        self.panel.setLayout(box_layout)


        self.choose_dir_label = JLabel('Experiment Folder:')
        self.choose_dir_textField = JTextField(20)
        self.choose_dir_textField.addActionListener(ActionListenerFactory(self, self.textField_al))
        self.choose_dir_button = JButton('open')
        self.choose_dir_button.addActionListener(ActionListenerFactory(self, self.choose_dir_al))

        self.choose_dir_panel = JPanel()
        self.choose_dir_panel.add(self.choose_dir_label)
        self.choose_dir_panel.add(self.choose_dir_textField)
        self.choose_dir_panel.add(self.choose_dir_button)

        self.panel.add(self.choose_dir_panel)

        self.add(self.panel)
        self.setPreferredSize(Dimension(500, 300));

        self.pack()
        self.setLocationRelativeTo(None)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)



bpg = BobPyGui()
