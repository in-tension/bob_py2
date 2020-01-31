

from ij import IJ, ImagePlus, ImageListener
from ij.gui import RoiListener, Roi
from ij.io import DirectoryChooser


from java.awt.event import KeyEvent, KeyAdapter, MouseWheelListener, WindowAdapter
from java.awt import Color, Rectangle, GridBagLayout, GridBagConstraints as GBC, Dimension
from javax.swing import JFrame, JPanel, JLabel, JTextField, JButton, BorderFactory, JOptionPane, AbstractAction, JTree, JScrollPane, BoxLayout, JTextArea
# from javax.swing.tree import *
from javax.swing.tree import DefaultMutableTreeNode

# from bob_py import *
import bob_py
import brutils as br

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
        self.got_exper(self.dir_path)



    def textField_al(self, e) :
        self.dir_path = self.choose_dir_textField.getText()
        self.got_exper(self.dir_path)

    # def run_button_al(self, e) :
        # print('run button al')
        # self.exper = bob_py.Exper(self.dir_path)
        # # self.exper.hsegs()[0].nuc_bin().show()
        # self.make_tree()
    @staticmethod
    def make_gbc(gridx=0, gridx=0, gridwidth=)



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

        stp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        stp.setPreferredSize(Dimension(250, 250));

        stp_panel = JPanel()
        stp_panel.add(stp)

        gc = GBC()
        gc.gridx = 0
        gc.gridy = 1
        gc.gridwidth = 1
        gc.gridheight = 1
        gc.weightx = 1
        gc.weighty = 1
        gc.fill = GBC.BOTH
        self.add(stp_panel, gc)


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
        # scrollPane.setPreferredSize(Dimension(300,250))



        tree_panel = JPanel()
        tree_panel.add(scrollPane)
        # box_layout = BoxLayout(self.panel, BoxLayout.Y_AXIS)
        # self.panel.setLayout(box_layout)
        # self.panel.add(tree_panel)

        gc.gridx = 1
        gc.gridy = 1
        gc.gridwidth = 1
        gc.gridheight = 1
        gc.weightx = 1
        gc.weighty = 1
        gc.fill = GBC.BOTH
        self.add(tree_panel, gc)
        self.revalidate()

    def __init__(self):
        super(BobGui, self).__init__("BobPy")

        self.dir_path = ''


        # self.panel = JPanel()
        grid_bag = GridBagLayout()
        self.setLayout(grid_bag)
        gc = GBC()
        gc.gridx = 0
        gc.gridy = 0
        gc.gridwidth = 2
        gc.gridheight = 1
        gc.weightx = 1
        gc.weighty = 1
        gc.fill = GBC.HORIZONTAL

        # box_layout = BoxLayout(self.panel, BoxLayout.Y_AXIS)
        # self.panel.setLayout(box_layout)
        # self.panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))

        # self.dir_panel = JPanel()
        # box_layout = BoxLayout(self.dir_panel, BoxLayout.X_AXIS)
        # self.dir_panel.setLayout(box_layout)
        # self.dir_panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))


        self.choose_dir_label = JLabel('Experiment Folder:')
        self.choose_dir_textField = JTextField(30)
        self.choose_dir_textField.addActionListener(ActionListenerFactory(self, self.textField_al))
        self.choose_dir_button = JButton('open')
        self.choose_dir_button.addActionListener(ActionListenerFactory(self, self.choose_dir_al))

        self.choose_dir_panel = JPanel()
        self.choose_dir_panel.add(self.choose_dir_label)
        self.choose_dir_panel.add(self.choose_dir_textField)
        self.choose_dir_panel.add(self.choose_dir_button)

        self.add(self.choose_dir_panel, gc)


        # info_panel = self.
        # info_label = self.in
        #
        # gc.gridx = 0
        # gc.gridy = 1
        # gc.gridwidth = 1
        # gc.gridheight = 1
        # gc.fill = GBC.BOTH
        #
        #
        #
        #
        # info_pane = JTextPane()
        # info_scroll = JScrollPane(info_pane)
        #
        # self.add(info_scroll, gc)
        #
        #
        # # root = DefaultMutableTreeNode(self.exper.name)
        # # for hseg in self.exper.hsegs() :
        #     # hseg_node = DefaultMutableTreeNode(hseg.name)
        #     # root.add(hseg_node)
        #     # for file_suf in hseg.file_dict() :
        #     #     hseg_node.add(DefaultMutableTreeNode(file_suf))
        # # self.tree = JTree(root)
        # self.treeScrollPane = JScrollPane()
        # scrollPane.getViewport().setView((self.tree))
        # scrollPane.setPreferredSize(Dimension(300,250))


        # tree_panel = JPanel()
        # tree_panel.add(scrollPane)
        # box_layout = BoxLayout(self.panel, BoxLayout.Y_AXIS)
        # self.panel.setLayout(box_layout)
        # self.panel.add(tree_panel)
        # self.revalidate()
        # gc.gridx = 1
        # self.add(self.treeScrollPane, gc)


        # root = DefaultMutableTreeNode()

        # self.meta_data_mode_label = JLabel('Autogenerated meta_data file mode')
        # self.raw_stack_mode = JRadioButton('raw stack mode')
        # self.projection_mode = JRadioButton('projection files mode')
        #
        # self.meta_data_mode = ButtonGroup()
        # self.meta_data_mode.add(self.raw_stack_mode)
        # self.meta_data_mode.add(self.projection_mode)
        #
        # self.meta_data_mode_panel = JPanel(GridLayout(0, 1))
        # self.meta_data_mode_panel.add(self.meta_data_mode_label)
        # self.meta_data_mode_panel.add(self.raw_stack_mode)
        # self.meta_data_mode_panel.add(self.projection_mode)
        #
        # self.panel.add(self.meta_data_mode_panel)

        # self.run_button = JButton('Run')
        # self.run_button.addActionListener(ActionListenerFactory(self, self.run_button_al))
        # self.panel.add(self.run_button)


        # self.getContentPane().add(self.panel)
        self.pack()
        self.setLocationRelativeTo(None)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)



bpg = BobGui()
