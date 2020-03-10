
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
# from bob_py.default_meta_data_text import default_meta_data
from bob_py.make_meta_data_str import make_meta_data_str
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
    # gui_folder = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/master/gui/'


    # gui_folder = os.path.join(os.path.dirname(__file__), 'resources')
    # IJ.log(gui_folder)
    gui_folder = '/bob_py/resources'

    icon_file_names = {'exper':'ExperPurple.png', 'hseg':'HsegDarkBlue.png', 'cell':'CellAqua.png', 'nuc':'NucGreen.png'}
    #
    # def __init__(self, resource_path, *args, **kwargs) :
    #     super()

    def getTreeCellRendererComponent(self, tree, node, selected, expanded, has_leaves, row, has_focus) :
        super(BobPyTreeCellRenderer, self).getTreeCellRendererComponent(tree, node, selected, expanded, has_leaves, row, has_focus)

        level = node.getLevel()

        try :
            if level == 0 :
                icon = self.load_icon('exper')
                self.setIcon(icon)
            elif level == 1 :
                icon = self.load_icon('hseg')
                self.setIcon(icon)
        except :
            pass

        return self


    def load_icon(self, icon_name) :
        icon_path = os.path.join(BobPyTreeCellRenderer.gui_folder, BobPyTreeCellRenderer.icon_file_names[icon_name])
        return self.create_icon(icon_path)


    def create_icon(self, path) :
        # try :
            # im = ImageIO.read(File(path))
            # im_url = self.getClass().getResource(path)
            # im = ImageIO.read(im_url)
        ins = self.getClass().getResourceAsStream(path)
            # reader = BufferedReader(InputStreamReader(is))
        im = ImageIO.read(ins)
        # except :
            # raise

        im = im.getScaledInstance(32,32, Image.SCALE_SMOOTH)
        icon = ImageIcon(im)
        return icon



class BobGui(JFrame) :


    def __init__(self) :
        super(BobGui, self).__init__('BobPy')
        # IJ.log('okay?')
        # print('okay??')
        self.setLayout(BorderLayout())
        self.main_panel = JPanel()
        # self.main_panel.setLayout(MigLayout('insets 1 10 1 1'))
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

        self.main_panel.add(dir_panel, 'wrap, growx, spanx, pushx')


        add_key_args(self.main_panel, 'close_w', ActionListenerFactory(self, self.close_al), KeyEvent.VK_W, Toolkit.getDefaultToolkit().getMenuShortcutKeyMask())


        self.add(self.main_panel, BorderLayout.CENTER)

        self.setPreferredSize(Dimension(650,600))

        self.pack()
        self.setLocationRelativeTo(None)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)


    def show_exper_info(self) :

        chf_panel = self.make_chf_panel()
        hseg_tree_panel = self.make_hseg_tree_panel()


        self.split_pane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)

        self.split_pane.setOneTouchExpandable(True);
        self.split_pane.setContinuousLayout(True);
        self.split_pane.setResizeWeight(0.5)


        self.split_pane.add(chf_panel)
        self.split_pane.add(hseg_tree_panel)
        self.main_panel.add(self.split_pane, 'grow, wrap')

        # self.log_text = JTextArea()
        self.main_panel.add(self.log_text, 'grow, wrap')
        self.log_text.setLineWrap(True);
        self.log_text.setWrapStyleWord(True);

        self.revalidate()


    def make_chf_panel(self) :
        """ chf --> common hseg files """

        chf_panel = JPanel()
        chf_panel.setLayout(MigLayout('insets 0'))


        chf_files_label = JLabel('Hemisegment cells')
        chf_files_text = JTextArea(BobGui.archetype_to_str(self.exper.hseg_cell_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow, wrap')


        chf_files_label = JLabel('Hemisegment binary image files')
        chf_files_text = JTextArea(BobGui.archetype_to_str(self.exper.hseg_bin_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow, wrap')


        chf_files_label = JLabel('Possible Intensity Image Files')
        chf_files_text = JTextArea(BobGui.archetype_to_str(self.exper.hseg_intens_im_files_cab().archetype))

        chf_panel.add(chf_files_label, 'growx, wrap')
        chf_panel.add(chf_files_text, 'grow, wrap')


        mdf_create_button = JButton('Create meta_data file from default outline')
        # mdf_create_button = JButton('<html>Create meta_data file<br>from default outline</html>')
        mdf_create_button.addActionListener(ActionListenerFactory(self, self.mdf_create_al))
        mdf_open_button = JButton('Open existing meta_data file')
        mdf_open_button.addActionListener(ActionListenerFactory(self, self.mdf_open_al))

        # meta_data_file_buttton = JButton('Open/Create meta_data file')
        # meta_data_file_buttton.addActionListener(ActionListenerFactory(self, self.meta_data_al))

        # chf_panel.add(meta_data_file_buttton)
        chf_panel.add(mdf_create_button, 'wrap')
        chf_panel.add(mdf_open_button, 'wrap')
        chf_scroll_pane = JScrollPane()
        chf_scroll_pane.getViewport().setView(chf_panel)

        return chf_scroll_pane

    @staticmethod
    def archetype_to_str(archetype) :

        at_str = ''
        for val in archetype :
            at_str += str(val) + '\n'
        return at_str


    def make_hseg_tree_panel(self) :
        root = DefaultMutableTreeNode(self.exper.name)

        for hseg in self.exper.hsegs() :
            hseg_node = DefaultMutableTreeNode(hseg.name)
            root.add(hseg_node)
            hseg_at_deviations = self.exper.hseg_files_cab().archetype_deviations
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

        hseg_panel = JPanel(MigLayout('insets 0'))
        hseg_panel.add(hseg_scroll_pane, 'grow, span, push, wrap')

        run_button = JButton('Run')
        run_button.addActionListener(ActionListenerFactory(self, self.run_al))
        rerun_button = JButton('Rerun')
        rerun_button.addActionListener(ActionListenerFactory(self, self.rerun_al))


        hseg_panel.add(run_button)
        hseg_panel.add(rerun_button)


        return hseg_panel

    def log(self,text) :
        self.log_text.append(str(text)+'\n')

    def text_field_al(self, e) :
        # self.dir_path =
        self.got_exper(self.dir_text_field.getText())


    def choose_dir_al(self, e) :

        dc = DirectoryChooser('Choose a bob_py experiment folder')
        # self.dir_path = dc.getDirectory()

        # self.dir_text_field.setText(self.dir_path)
        # self.dir_text_field.setText('blerg')
        # IJ.log('blerg')
        # print('boop')
        self.got_exper(dc.getDirectory())

    def close_al(self, e) :
        self.dispatchEvent(WindowEvent(self, WindowEvent.WINDOW_CLOSING));

    def run_al(self, e) :
        # dt = br.dtic('Processed experiment {}'.format(self.exper.name))
        t = br.tic()
        self.exper.make_data()
        self.exper.output_cell_cols_def()
        self.exper.output_nuc_cols_def()
        self.exper.output_new_hdings()

        self.exper.log('Processed experiment {} in {:.3f} seconds'.format(self.exper.name, br.toc(t)))
        # br.dtoc(dt)

    def rerun_al(self, e) :
        # dt = br.dtic('Processed experiment {}'.format(self.exper.name))
        # t = br.tic()
        self.exper = None
        self.got_exper(self.dir_path)
        self.run_al(None)
        # self.exper =
        # self.exper.make_data()
        # self.exper.output_cell_cols_def()
        # self.exper.output_nuc_cols_def()
        # self.exper.output_new_hdings()
        #
        # self.exper.log('Created and processed experiment {} in {:.3f} seconds'.format(self.exper.name, br.toc(t)))
        # br.dtoc(dt)

    # def meta_data_al(self, e) :
    #     meta_data_path = self.exper.meta_data_path()
    #     if not os.path.exists(meta_data_path) :
    #         txt = make_meta_data_str(self.exper)
    #         with open(meta_data_path, 'w') as f :
    #             f.write(txt)
    #
    #     IJ.open(meta_data_path)


    def mdf_create_al(self, e) :
        meta_data_path = self.exper.meta_data_path()
        # if not os.path.exists(meta_data_path) :
        txt = make_meta_data_str(self.exper)
        with open(meta_data_path, 'w') as f :
            f.write(txt)

        # IJ.open(meta_data_path)

    def mdf_open_al(self, e) :
        meta_data_path = self.exper.meta_data_path()

        IJ.open(meta_data_path)

    def got_exper(self, dir_path) :
        # IJ.log('exper')
        self.dir_path = dir_path
        self.dir_text_field.setText(self.dir_path)

        self.log_text = JTextArea()

        self.exper = bob_py.Exper(dir_path, gui=self)
        self.show_exper_info()
