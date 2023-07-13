import flet
from flet import MainAxisAlignment, CrossAxisAlignment, alignment, ImageFit

class Box(flet.Container):
    def __init__(self, box_id: tuple[int, int], manager: flet.UserControl):
        super().__init__(expand=True,
                         bgcolor="#C88EA7",
                         padding=5,
                         alignment=alignment.center,
                         border=flet.border.all(1, flet.colors.BLACK),
                         border_radius=flet.border_radius.all(50))
        self.box_id = box_id
        self.manager = manager
        self.symbol = None

        self.on_click = self.setSymbol

    def setSymbol(self, e=None):
        if not self.symbol:
            self.symbol = self.manager.player
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

class BoxRow(flet.Row):

    def __init__(self, row: int, size: int, manager: flet.UserControl):
        super().__init__(expand=True,
                         alignment=MainAxisAlignment.CENTER,
                         vertical_alignment=CrossAxisAlignment.CENTER,
                         spacing=10)
        self.row = row
        self.size = size

        for i in range(size):
            self.controls.append(Box(box_id=(i, row), manager=manager))

class TicTacToeInteractive(flet.UserControl):

    def __init__(self, size: int = 3):
        super().__init__(expand=True)
        self.size = size
        self.player = "X"

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

    def update(self):
        self.playerDisplay.value = f"Player {self.player}'s Turn"
        return super().update()

    def build(self):
        self.view.content = self.inner_view
        self.inner_view.controls = self.rows
        return self.view


def main(page: flet.Page):
    page.title = "Tic Tac Toe"
    page.bgcolor = "#643843"
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 30
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    interactive = TicTacToeInteractive(3)
    page_title = flet.Text("TIC TAC TOE", style=flet.TextThemeStyle.DISPLAY_LARGE, color="#E7CBCB")
    page.add(page_title, interactive)


flet.app(target=main, assets_dir="assets")