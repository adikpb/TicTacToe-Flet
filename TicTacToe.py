from typing import Literal
import flet
from flet import MainAxisAlignment, CrossAxisAlignment, alignment, ImageFit


class Box(flet.ElevatedButton):

    def __init__(self, box_id: tuple[int, int], symbol: Literal["X", "O"] | None = None):
        super().__init__(expand=True, style=flet.ButtonStyle(shape=flet.CircleBorder()))
        self.box_id = box_id
        self.symbol = symbol

        self.setSymbol()

    def setSymbol(self, e=None):
        self.symbol = "O"
        self.setIcon()

    def setIcon(self):
        if self.symbol == "X":
            self.content = flet.Image(src="icons/TicTacToe/X.png",
                                      fit=ImageFit.CONTAIN,
                                      repeat=flet.ImageRepeat.NO_REPEAT)
        elif self.symbol == "O":
            self.content = flet.Image(src="icons/TicTacToe/O.png",
                                      fit=ImageFit.FIT_WIDTH,
                                      repeat=flet.ImageRepeat.NO_REPEAT)
        elif self.symbol == None:
            self.content.src = None


class BoxRow(flet.Row):

    def __init__(self, row: int, size: int):
        super().__init__(expand=True,
                         alignment=MainAxisAlignment.CENTER,
                         vertical_alignment=CrossAxisAlignment.CENTER,
                         spacing=10)
        self.row = row
        self.size = size

        for i in range(size):
            self.controls.append(Box(box_id=(i, row)))


class TicTacToeInteractive(flet.UserControl):

    def __init__(self, size: int = 3):
        super().__init__(expand=True)
        self.size = size
        self.player = "X"

        self.view = flet.Container(
            expand=True,
            padding=10,
            bgcolor=flet.colors.PRIMARY_CONTAINER,
            alignment=alignment.center,
            border=flet.border.all(2, flet.colors.OUTLINE),
            border_radius=flet.border_radius.all(50),
            theme=flet.Theme(color_scheme_seed=flet.colors.INDIGO))
        self.inner_view = flet.Column(expand=True,
                                      spacing=20,
                                      alignment=MainAxisAlignment.CENTER,
                                      horizontal_alignment=CrossAxisAlignment.CENTER)
        self.playerDisplay = flet.Text(f"Player {self.player}'s Turn",
                                       style=flet.TextThemeStyle.TITLE_LARGE)
        self.rows = [self.playerDisplay
                    ] + [BoxRow(i, self.size) for i in range(self.size)]

    def build(self):
        self.view.content = self.inner_view
        self.inner_view.controls = self.rows
        return self.view


def main(page: flet.Page):
    page.title = "Tic Tac Toe"
    page.theme = flet.Theme(color_scheme_seed="indigo")
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 30
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    interactive = TicTacToeInteractive(3)
    page.add(flet.Text("Tic Tac Toe", style=flet.TextThemeStyle.DISPLAY_LARGE),
             interactive)
    interactive.update()
    page.update()

    # page.add(
    #     flet.Container(content=flet.Column(
    #         controls=rows,
    #         alignment=MainAxisAlignment.SPACE_AROUND,
    #         horizontal_alignment=CrossAxisAlignment.CENTER,
    #         expand=True),
    #                    expand=True,
    #                    bgcolor=flet.colors.PRIMARY_CONTAINER,
    #                    border=flet.border.all(2, flet.colors.OUTLINE),
    #                    border_radius=flet.border_radius.all(50)))


flet.app(target=main, assets_dir="assets")