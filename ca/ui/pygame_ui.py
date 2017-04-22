"""
User interface created using pygame library.
"""

import sys
import logging

import pygame


LOG = logging.getLogger(__name__)

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

    def __init__(self, cell_x, cell_y, automatons, border=True):
        """
        Constructor.

        Args:
            cell_x - Cell width.
            cell_y - Cell height.
            automatons - CA automatons.
            border - If cell border should be drawn.
        """
        self._cell_x = int(cell_x)
        self._cell_y = int(cell_y)
        self._auto = automatons
        self._index = 0
        self._border = border
        self._win = None
        self.keys = {
            # Next rule
            pygame.K_RIGHT: self.next,
            # Previus rule
            pygame.K_LEFT: self.back,
            # Next generation
            pygame.K_UP: self.next_auto,
            # Previus generation
            pygame.K_DOWN: self.prev_auto,
            # Reset to clean lattice
            pygame.K_c: self.reset,
            # Exit prog
            # TODO
            pygame.K_ESCAPE: self.exit
        }

    def _resize_window(self):
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
                        self.keys[event.key]()
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
                                 COLOR[self._auto[self._index].get(r, c)],
                                 (c * self._cell_x, r * self._cell_y,
                                  self._cell_x, self._cell_y), 0)

        for r in range(proportions[0]):
            for c in range(proportions[1]):
                pygame.draw.rect(self._win,
                                 WHITE,
                                 (c * self._cell_x, r * self._cell_y,
                                  self._cell_x, self._cell_y), 1)
        pygame.display.update()

    def exit(self):
        """
        Exit.
        """
        # TODO
        sys.exit(0)

    def next(self):
        """
        Develop CA, next gen of CA.
        """
        LOG.debug("_next")
        self._auto[self._index].next()

    def back(self):
        """
        Step one generation back.
        """
        LOG.debug("_back")
        self._auto[self._index].back()

    def save_to_img(self):
        """
        Saves lattice to jpeg.
        """
        filename = str(self._auto[self._index]._gen) + ".jpeg"
        LOG.info("Saving lattice as " + filename)
        pygame.image.save(self._win, filename)

    def reset(self):
        """
        Reset lattice to clean state.
        """
        LOG.debug("reset")
        self._auto[self._index].move(-self._auto[self._index]._gen)

    def next_auto(self):
        """
        Load next automaton.
        """
        LOG.debug("next_rule")
        if self._auto:
            self._index = (self._index + 1) % len(self._auto)
            self._resize_window()
            self._draw()

    def prev_auto(self):
        """
        Load previous automaton.
        """
        LOG.debug("prev_rule")
        if self._auto:
            self._index -= 1
            if self._index < 0:
                self._index = len(self._auto) - 1
            self._resize_window()
            self._draw()

    def set_clicked_cell(self, pos):
        """
        Increases state of cell. 
        """
        # TOD
        row = int(pos[1] / self._cell_y)
        col = int(pos[0] / self._cell_x)
        value = ((self._auto[self._index].get(row, col) + 1)
                  % self._auto[self._index]._states)
        self._auto[self._index].set(row, col, value)
