from pprint import pprint

import flet
from flet import CrossAxisAlignment, ImageFit, MainAxisAlignment, alignment


class TicTacToeInteractive(flet.UserControl):

    def __init__(self, size: int = 3):
        super().__init__(expand=True)
        self.size = size
        self.player = "X"
        self.game = [[None] * self.size for i in range(self.size)]
        pprint(self.game)

        self.view = flet.Container(expand=True,
                                   padding=10,
                                   bgcolor="#99627A",
                                   alignment=alignment.center,
                                   border=flet.border.all(2, flet.colors.BLACK),
                                   border_radius=flet.border_radius.all(50))
        self.inner_view = flet.Column(expand=True,
                                      spacing=20,
                                      alignment=MainAxisAlignment.CENTER,
                                      horizontal_alignment=CrossAxisAlignment.CENTER)
        self.playerDisplay = flet.Text(f"Player {self.player}'s Turn",
                                       style=flet.TextThemeStyle.TITLE_LARGE)
        self.rows = [self.playerDisplay] + [BoxRow(i, self.size, self) for i in range(self.size)]

    def reset(self, e):
        for i in self.rows[1:]:
            i.reset()
        self.update()

    def update(self):
        self.playerDisplay.value = f"Player {self.player}'s Turn"
        return super().update()

    def build(self):
        self.view.content = self.inner_view
        self.inner_view.controls = self.rows
        return self.view


class Box(flet.Container):

    def __init__(self, box_id: tuple[int, int], manager: TicTacToeInteractive):
        super().__init__(expand=True,
                         bgcolor="#C88EA7",
                         padding=5,
                         alignment=alignment.center,
                         border=flet.border.all(1, flet.colors.BLACK),
                         border_radius=flet.border_radius.all(50))
        self.x, self.y = box_id
        self.manager = manager
        self.symbol = None

        self.on_click = self.setSymbol

    def setSymbol(self, e=None):
        if not self.symbol:
            self.symbol = self.manager.player
            self.manager.game[self.y][self.x] = self.symbol
            print(self.manager.game)
            self.manager.player = "X" if self.symbol == "O" else "O"
            self.setIcon()
            self.manager.update()

    def setIcon(self):
        if self.symbol in ("X", "O"):
            self.content = flet.Image(src=f"icons/TicTacToe/{self.symbol}.png",
                                      fit=ImageFit.CONTAIN,
                                      repeat=flet.ImageRepeat.NO_REPEAT)
        elif self.symbol == None:
            self.content = None

    def reset(self):
        self.symbol = None
        self.setIcon()


class BoxRow(flet.Row):

    def __init__(self, row: int, size: int, manager: TicTacToeInteractive):
        super().__init__(expand=True,
                         alignment=MainAxisAlignment.CENTER,
                         vertical_alignment=CrossAxisAlignment.CENTER,
                         spacing=10)
        self.row = row
        self.size = size

        for i in range(size):
            self.controls.append(Box(box_id=(i, row), manager=manager))

    def reset(self):
        for i in self.controls:
            i.reset()


def main(page: flet.Page):
    page.title = "Tic Tac Toe"
    page.bgcolor = "#643843"
    page.padding = 30
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    interactive = TicTacToeInteractive(3)
    page.floating_action_button = flet.FloatingActionButton(icon=flet.icons.RESTART_ALT_OUTLINED,
                                                            bgcolor="#fe7f9c"    ,
                                                            tooltip="Reset Match",
                                                            on_click=interactive.reset)
    page_title = flet.Text("TIC TAC TOE", style=flet.TextThemeStyle.DISPLAY_LARGE, color="#E7CBCB")
    page.add(page_title, interactive)


flet.app(name="Tic Tac Toe", target=main, assets_dir="assets")