from tkinter import Canvas, Label, BOTTOM, GROOVE

from willsmith.gui_display_controller import GUIDisplayController


class MCTSDisplay(GUIDisplayController):
    """
    """

    WINDOW_TITLE = "MCTS Agent"

    LABEL_FONT = ("Courier New", 14)
    LABEL_WIDTH = 25
    LABEL_BORDER_WIDTH = 1
    LABEL_RELIEF = GROOVE

    CANVAS_HEIGHT = 500
    CANVAS_WIDTH = 500

    def __init__(self):
        super().__init__()

        self.playouts_label = None
        self.action_label = None
        self.win_pct_label = None
        #self.canvas = None

    def _initialize_widgets(self):
        self.playouts_label = Label(self.root, font = self.LABEL_FONT, 
                                        width = self.LABEL_WIDTH,
                                        bd = self.LABEL_BORDER_WIDTH, 
                                        relief = GROOVE)
        self.action_label = Label(self.root, font = self.LABEL_FONT, 
                                    width = self.LABEL_WIDTH,
                                    bd = self.LABEL_BORDER_WIDTH, 
                                    relief = GROOVE)
        self.win_pct_label = Label(self.root, font = self.LABEL_FONT, 
                                        width = self.LABEL_WIDTH,
                                        bd = self.LABEL_BORDER_WIDTH, 
                                        relief = GROOVE)
#        self.canvas = Canvas(self.root, height = self.CANVAS_HEIGHT,
#                                width = self.CANVAS_WIDTH)

    def _place_widgets(self):
        self.playouts_label.grid(row = 0, column = 0)
        self.action_label.grid(row = 1, column = 0)
        self.win_pct_label.grid(row = 2, column = 0)
        #self.canvas.grid(row = 0, column = 1, rowspan = 4)

    def _update_display(self, agent, action):
        self._update_labels_from_agent(agent, action)
        #self._draw_node_tree_snippet(agent)

    def _reset_display(self, agent):
        self._update_labels_from_agent(agent, None)
        #self.canvas.delete("all")

    def _update_labels_from_agent(self, agent, action):
        self.action_label["text"] = "Latest action:\n{}".format(action)
        self.playouts_label["text"] = "Latest playout count:\n{}".format(agent.playout_total)
        win_pct = 0
        if agent.action_node is not None:
            win_pct = agent.action_node.value_estimate()
        self.win_pct_label["text"] = "Node sim win rate:\n{:.2%}".format(win_pct)
        
    def _draw_node_tree_snippet(self, agent):
        node = agent.root
        while node.has_children():
            ranked = sorted(node.children.items(), key=lambda x: x[1].value_estimate())
            one, two, three  = ranked[:3]
            last = ranked[-1]
            self._draw_level(self, one, two, three, last)

    def _draw_level(self, one, two, three, last):
        pass
