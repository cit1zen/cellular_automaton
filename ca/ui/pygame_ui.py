"""
User interface created using pygame library.
"""

class CAPygameUI(object):
    """
    User interface created using pygame library.
    """

    def __init__(self, pixel_x, pixel_y, automatons, border=True):
        """
        Constructor.

        Args:
            pixel_x - Pixel width.
            pixel_y - Pixel height.
            automatons - CA automatons.
            border - If cell border should be drawn.
        """

    def draw(self, border=True):
        """
        Draw CA onto window

        :param lines: If border between cels should be drawed.
        :type lines: boolean
        """
        # TODO draw without lines
        for row in range(self.auto._rows + 1):
            for col in range(1, self.auto._cols + 1):
                pygame.draw.rect(self.win, color[self.auto.get_cell(row, col)],
                                 ((col - 1) * self.cell_w, (row - 1) * self.cell_h,
                                  self.cell_w, self.cell_h), 0)
                if border:
                    pygame.draw.rect(self.win, blue,
                                     ((col - 1) * self.cell_w, (row - 1) * self.cell_h,
                                      self.cell_w, self.cell_h), 1)
        pygame.display.update()

    def main_loop(self):
        """
        Main loop of GUI.
        """
        self.draw()
        while True:
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Pressing key
                elif event.type == pygame.KEYDOWN:
                    try:
                        self.keys[event.key]()
                    # Some key we do not map
                    except KeyError:
                        pass
                # Mouse pressed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.set_clicked_cell(pygame.mouse.get_pos())
                self.draw()def draw(self, border=True):
        """
        Draw CA onto window

        :param lines: If border between cels should be drawed.
        :type lines: boolean
        """
        # TODO draw without lines
        for row in range(self.auto._rows + 1):
            for col in range(1, self.auto._cols + 1):
                pygame.draw.rect(self.win, color[self.auto.get_cell(row, col)],
                                 ((col - 1) * self.cell_w, (row - 1) * self.cell_h,
                                  self.cell_w, self.cell_h), 0)
                if border:
                    pygame.draw.rect(self.win, blue,
                                     ((col - 1) * self.cell_w, (row - 1) * self.cell_h,
                                      self.cell_w, self.cell_h), 1)
        pygame.display.update()

    def main_loop(self):
        """
        Main loop of GUI.
        """
        self.draw()
        while True:
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Pressing key
                elif event.type == pygame.KEYDOWN:
                    try:
                        self.keys[event.key]()
                    # Some key we do not map
                    except KeyError:
                        pass
                # Mouse pressed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.set_clicked_cell(pygame.mouse.get_pos())
                self.draw()