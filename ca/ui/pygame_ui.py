"""
User interface created using pygame library.
"""

import pygame


# Color const.
WHITE = pygame.Color(0xFFFFFF00)
BLACK = pygame.Color(0x00000000)
RED = pygame.Color(0xFF000000)
GREEN = pygame.Color(0x00FF0000)
BLUE = pygame.Color(0x0000FF00)
CYAN = pygame.Color(0x00FFFF00)
MAGENTA = pygame.Color(0xFF00FF00)
YELLOW = pygame.Color(0xFFFF0000)
GRAY = pygame.Color(0x64646400)
PINK = pygame.Color(0xFF087F00)
BROWN = pygame.Color(0x825A2C00)
ORANGE = pygame.Color(0xFA680000)
VIOLET = pygame.Color(0xAA00FF00)
COLOR = [BLACK, RED, GREEN, YELLOW, BROWN, WHITE, ORANGE, CYAN, VIOLET,
         GRAY, MAGENTA, PINK, BLUE]


class CAPygameUI():
    """
    User interface created using pygame library.
    """

    self.keys = {
        # Next rule
        pygame.K_RIGHT: self.next_rule,
        # Previus rule
        pygame.K_LEFT: self.prev_rule,
        # Next generation
        pygame.K_t: self.next_gen,
        pygame.K_UP: self.next_gen,
        pygame.K_SPACE: self.next_gen,
        # Previus generation
        pygame.K_DOWN: self.prev_gen,
        # Reset to clean lattice
        pygame.K_c: self.reset,
        # Exit prog
        # TODO
        pygame.K_ESCAPE: self.exit
    }

    def __init__(self, cell_x, cell_y, automatons, border=True):
        """
        Constructor.

        Args:
            cell_x - Cell width.
            cell_y - Cell height.
            automatons - CA automatons.
            border - If cell border should be drawn.
        """
        self._cell_x = cell_x
        self._cell_y = cell_y
        self._auto = automatons
        self._index = 0
        self._border = border
        self._win = None

    def _fit_ca(self):
        """
        Resizes window to fit CA.
        """
        prop = self._auto[self._index].proportions()
        self._win = pygame.display.set_mode((self._cell_x * prop[1],
                                             self._cell_y * prop[0]))

    def main_loop(self):
        """
        Main loop of GUI.
        """
        # Get PYGAME window
        pygame.init()
        self._resize_window()
        self._draw()
        # Program loop
        while True:
            for event in pygame.event.get():
                # Quit
                # TODO
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Pressing key
                elif event.type == pygame.KEYDOWN:
                    try:
                        self._keys[event.key]()
                    # Some key we do not map
                    except KeyError:
                        pass
                # Mouse pressed
                # TODO
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.set_clicked_cell(pygame.mouse.get_pos())
                self._draw()

    def _draw(self):
        """
        Draw CA onto window
        """
        proportions = self._auto[self._index].proportions()
        for r in range(proportions[0]):
            for c in range(proportions[1]):
                pygame.draw.rect(self._win,
                                 COLOR[self._auto[self._index].get_cell(r, c)],
                                 (c * self._cell_w, r * self._cell_h,
                                  self._cell_w, self._cell_h), 0)

        for r in range(proportions[0]):
            for c in range(proportions[1]):
                pygame.draw.rect(self._win,
                                 WHITE,
                                 (c * self._cell_w, r * self._cell_h,
                                  self._cell_w - 1 , self._cell_h - 1 ), 1)
        pygame.display.update()

    def _exit(self):
        """
        Exit.
        """
        sys.exit(0)

    def _next(self):
        """
        Develop CA, next gen of CA.
        """
        logger.debug("_next")
        self._auto[self._index].next()

    def _back(self):
        """
        Step one generation back.
        """
        logger.debug("_back")
        self._auto[self._index].back()

#     def save_to_img(self):
#         """
#         Saves lattice to jpeg.
#         """
#         filename = str(self.auto.current_save()) + ".jpeg"
#         logger.info("Saving lattice as " + filename)
#         pygame.image.save(self.win, filename)

#     def reset(self):
#         """
#         Reset lattice to clean state.
#         """
#         logger.debug("reset")
#         self.auto.reset()

#     def next_rule(self):
#         """
#         Load next rules into automaton and reset it.
#         """
#         logger.debug("next_rule")
#         if self.rule_file_list:
#             self.rule_index = (self.rule_index + 1) % len(self.rule_file_list)
#             filename = str(self.rule_file_list[self.rule_index])
#             logger.info("Loading CA from" + filename)
#             self._load_from_json(filename)

#     def prev_rule(self):
#         """
#         Load previous rules into automaton and reset it.
#         """
#         logger.debug("prev_rule")
#         if self.rule_file_list:
#             if self.rule_index == 0:
#                 self.rule_index = len(self.rule_file_list) - 1
#             else:
#                 self.rule_index = self.rule_index - 1
#             filename = str(self.rule_file_list[self.rule_index])
#             logger.info("Loading CA from" + filename)
#             self._load_from_json(filename)

#     def _load_from_json(self, filename):
#         """
#         Loads JSON from file and recreates automaton from it.
#         """
#         raise NotImplementedError("load_from_json")
#         with open(filename, "r") as f:
#             json_data = json.load(f)
#             # Check rules
#             for rule in json_data:
#                 pass

#     def set_clicked_cell(self, pos):
#         """
#         Increases state of cell. 
#         """
#         row = int(pos[1] / self.cell_h + 1)
#         col = int(pos[0] / self.cell_w + 1)
#         temp = (self.auto.get_cell(row, col) + 1) % self.auto._states
#         self.auto.set_cell(row, col, temp)
