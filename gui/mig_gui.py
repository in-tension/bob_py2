
import os

from ij import IJ, ImagePlus, ImageListener
from ij.gui import RoiListener, Roi
from ij.io import DirectoryChooser

from java.net import URL
from java.io import File

from java.awt.event import KeyEvent, InputEvent, KeyAdapter, MouseWheelListener, WindowAdapter, WindowEvent
from java.awt import Color, Rectangle, GridBagLayout, GridBagConstraints as GBC, Dimension, BorderLayout, GridLayout, Toolkit, Component, RenderingHints, Image
from java.awt.image import BufferedImage

from javax.swing import JFrame, JPanel, JLabel, JTextField, JButton, BorderFactory, JOptionPane, AbstractAction, JTree, JScrollPane, BoxLayout, JTextArea, JSplitPane, JComponent, KeyStroke, ImageIcon
from javax.swing.tree import DefaultMutableTreeNode, DefaultTreeCellRenderer
from javax.imageio import ImageIO

from net.miginfocom.swing import MigLayout


import bob_py
import brutils as br


class ActionListenerFactory(AbstractAction) :
    def __init__(self, obj, func) :
        self.obj = obj
        self.func = func


    def actionPerformed(self, e) :
        self.func(e)


def add_key_args(component, action_str, action, *args) :
    # print(args)
    key_stroke = KeyStroke.getKeyStroke(*args)
    add_key_binding(component, action_str, action, key_stroke)

def add_key_binding(component, action_str, action, key_stroke) :
    imap = component.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
    amap = component.getActionMap()
    imap.put(key_stroke, action_str)
    amap.put(action_str, action)



class BobPyTreeCellRenderer(DefaultTreeCellRenderer) :
    gui_folder = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/master/gui/'
    icon_file_names = {'exper':'ExperPurple.png', 'hseg':'HsegDarkBlue.png', 'cell':'CellAqua.png', 'nuc':'NucGreen.png'}


    def getTreeCellRendererComponent(self, tree, node, selected, expanded, has_leaves, row, has_focus) :
        super(BobPyTreeCellRenderer, self).getTreeCellRendererComponent(tree, node, selected, expanded, has_leaves, row, has_focus)

        level = node.getLevel()

        if level == 0 :
            icon = self.load_icon('exper')
            self.setIcon(icon)
        elif level == 1 :
            icon = self.load_icon('hseg')
            self.setIcon(icon)

        return self


    def load_icon(self, icon_name) :
        return self.create_icon(os.path.join(BobPyTreeCellRenderer.gui_folder, BobPyTreeCellRenderer.icon_file_names[icon_name]))


    def create_icon(self, path) :
        try :
            im = ImageIO.read(File(path))
        except :
            raise

        im = im.getScaledInstance(32,32, Image.SCALE_SMOOTH)
        icon = ImageIcon(im)
        return icon


class BobPyGui(JFrame) :


    def __init__(self) :
        super(BobPyGui, self).__init__('BobPy')

        # cls = self.getClass()
        # print(cls)

        # self.setLayout(MigLayout())
        self.setLayout(BorderLayout())
        self.main_panel = JPanel()
        self.main_panel.setLayout(MigLayout())



        dir_panel = JPanel()
        dir_panel.setLayout(BoxLayout(dir_panel, BoxLayout.X_AXIS))

        dir_label = JLabel('Experiment Folder:')
        dir_panel.add(dir_label)

        self.dir_text_field = JTextField(10)
        self.dir_text_field.addActionListener(ActionListenerFactory(self, self.text_field_al))
        dir_panel.add(self.dir_text_field)

        dir_button = JButton('open')
        dir_button.addActionListener(ActionListenerFactory(self, self.choose_dir_al))
        dir_panel.add(dir_button)


        self.main_panel.add(dir_panel, 'growx, spanx, pushx, wrap')


        add_key_args(self.main_panel, 'close_w', ActionListenerFactory(self, self.close_al), KeyEvent.VK_W, Toolkit.getDefaultToolkit().getMenuShortcutKeyMask())


        self.add(self.main_panel, BorderLayout.CENTER)

        self.setPreferredSize(Dimension(500,400))

        self.pack()
        self.setLocationRelativeTo(None)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)

    def show_exper_info_old(self) :
        # sb = br.SimilarityBuilder()
        cab = br.CollectionArchetypeBuilder()

        for hseg in self.exper.hsegs() :
            all_file_dict = hseg.file_dict()
            all_file_dict.update(hseg.cell_file_dict())
            all_file_dict.update(hseg.bin_file_dict())
            cab.add_collection(hseg.name, all_file_dict)

        hseg_at, hseg_at_deviations = cab.get_archetype_info()

        at_str = ''
        for val in hseg_at :
            at_str += str(val) + '\n'

        chf_panel = self.make_chf_panel(at_str)
        hseg_tree_panel = self.make_hseg_tree_panel(hseg_at_deviations)


        self.split_pane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)

        self.split_pane.setOneTouchExpandable(True);
        self.split_pane.setContinuousLayout(True);
        self.split_pane.setResizeWeight(0.5)


        self.split_pane.add(chf_panel)
        self.split_pane.add(hseg_tree_panel)
        self.main_panel.add(self.split_pane, 'grow')
        self.revalidate()

    def show_exper_info(self) :
        # sb = br.SimilarityBuilder()
        # cab = br.CollectionArchetypeBuilder()
        #
        # for hseg in self.exper.hsegs() :
        #     all_file_dict = hseg.file_dict()
        #     all_file_dict.update(hseg.cell_file_dict())
        #     all_file_dict.update(hseg.bin_file_dict())
        #     cab.add_collection(hseg.name, all_file_dict)
        #
        # hseg_at, hseg_at_deviations = cab.get_archetype_info()
        #
        # at_str = ''
        # for val in hseg_at :
        #     at_str += str(val) + '\n'

        chf_panel = self.make_chf_panel()
        hseg_tree_panel = self.make_hseg_tree_panel()


        self.split_pane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)

        self.split_pane.setOneTouchExpandable(True);
        self.split_pane.setContinuousLayout(True);
        self.split_pane.setResizeWeight(0.5)


        self.split_pane.add(chf_panel)
        self.split_pane.add(hseg_tree_panel)
        self.main_panel.add(self.split_pane, 'grow')
        self.revalidate()


    def make_chf_panel_old(self, at_str) :
        """ cf --> common hseg files """

        chf_panel = JPanel()
        # chf_panel.setLayout(BoxLayout(chf_panel, BoxLayout.Y_AXIS))
        chf_panel.setLayout(MigLayout('insets 0'))
        # chf_panel.setAlignmentX(Component.LEFT_ALIGNMENT)

        chf_label = JLabel('Common Hemeisegment Files')
        # chf_label.setAlignmentX(Component.LEFT_ALIGNMENT)

        chf_panel.add(chf_label, 'grow, wrap')

        chf_text_area = JTextArea(at_str)
        chf_panel.add(chf_text_area, 'grow, push, span')
        return chf_panel

    def make_chf_panel(self) :
        """ chf --> common hseg files """

        chf_panel = JPanel()
        # chf_panel.setLayout(BoxLayout(chf_panel, BoxLayout.Y_AXIS))
        chf_panel.setLayout(MigLayout('insets 0'))
        # chf_panel.setAlignmentX(Component.LEFT_ALIGNMENT)




        chf_files_label = JLabel('Hemisegment cells')
        chf_files_text = JTextArea(BobPyGui.archetype_to_str(self.exper.hseg_cell_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow, wrap')


        chf_files_label = JLabel('Hemisegment binary image files')
        chf_files_text = JTextArea(BobPyGui.archetype_to_str(self.exper.hseg_bin_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow, wrap')


        chf_files_label = JLabel('Other hemisegment files')
        chf_files_text = JTextArea(BobPyGui.archetype_to_str(self.exper.hseg_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow')
        # chf_label = JLabel('Common Hemeisegment Files')
        # # chf_label.setAlignmentX(Component.LEFT_ALIGNMENT)
        #
        # chf_panel.add(chf_label, 'grow, wrap')
        #
        # chf_text_area = JTextArea(at_str)
        # chf_panel.add(chf_text_area, 'grow, push, span')
        return chf_panel

    @staticmethod
    def archetype_to_str(archetype) :

        at_str = ''
        for val in archetype :
            at_str += str(val) + '\n'
        return at_str

    # def make_hseg_tree_panel(self, hseg_at_deviations) :
    def make_hseg_tree_panel(self) :
        root = DefaultMutableTreeNode(self.exper.name)



        for hseg in self.exper.hsegs() :
            hseg_node = DefaultMutableTreeNode(hseg.name)
            root.add(hseg_node)
            hseg_at_deviations = self.exper.hseg_all_files_cab().archetype_deviations
            if len(hseg_at_deviations[hseg.name]) > 0 :
                for definer, file_names in hseg_at_deviations[hseg.name].items() :
                    for file_name in file_names :
                        node_str = definer + ': ' + file_name

                        temp = DefaultMutableTreeNode(node_str)
                        hseg_node.add(temp)


        hseg_tree = JTree(root)
        hseg_tree.setCellRenderer(BobPyTreeCellRenderer())


        hseg_scroll_pane = JScrollPane()
        hseg_scroll_pane.getViewport().setView((hseg_tree))




        return hseg_scroll_pane


    def text_field_al(self, e) :
        self.dir_path = self.dir_text_field.getText()
        self.got_exper(self.dir_path)


    def choose_dir_al(self, e) :

        dc = DirectoryChooser('Choose a bob_py experiment folder')
        self.dir_path = dc.getDirectory()

        self.dir_text_field.setText(self.dir_path)
        self.got_exper(self.dir_path)

    def close_al(self, e) :
        self.dispatchEvent(WindowEvent(self, WindowEvent.WINDOW_CLOSING));



    def got_exper(self, dir_path) :
        self.exper = bob_py.Exper(dir_path)
        self.show_exper_info()





bpg = BobPyGui()
