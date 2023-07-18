import flet


class SizeSelector(flet.Slider):

    def __init__(self, page: flet.Page, switcher: flet.AnimatedSwitcher):
        super().__init__(divisions=2,
                         label="{value}x{value}",
                         max=5,
                         min=3,
                         value=3,
                         on_change=self.changeSize,
                         active_color="#fe7f9c",
                         thumb_color="#fe7f9c")
        self.page = page
        self.switcher = switcher
        self.sizes = {3: None, 4: None, 5: None}
        for i in self.sizes:
            self.sizes[i] = TicTacToeInteractive(page=self.page, size=i)
        self.switcher.content = self.sizes[3]

    def changeSize(self, e):
        self.switcher.content = self.sizes[self.value]
        self.page.floating_action_button = self.switcher.content.resetButton
        self.page.update()


class TicTacToeInteractive(flet.UserControl):

    def __init__(self, page: flet.Page, size: int = 3):
        super().__init__(expand=True)
        self.page = page
        self.size = size
        self.player = "X"
        self.filled = 0
        self.positions = [[None] * self.size for i in range(self.size)]
        self.winMap = self.generateWinMap()

        self.view = flet.Container(expand=True,
                                   padding=10,
                                   bgcolor="#99627A",
                                   alignment=flet.alignment.center,
                                   border=flet.border.all(2, flet.colors.BLACK),
                                   border_radius=flet.border_radius.all(50))
        self.inner_view = flet.Column(expand=True,
                                      spacing=20,
                                      alignment=flet.MainAxisAlignment.CENTER,
                                      horizontal_alignment=flet.CrossAxisAlignment.CENTER)
        self.playerDisplay = flet.Text(f"Player {self.player}'s Turn",
                                       style=flet.TextThemeStyle.TITLE_LARGE)
        self.rows = [self.playerDisplay] + [BoxRow(i, self.size, self) for i in range(self.size)]
        self.resetButton = None

    def generateWinMap(self):
        row_wins = [[(x, y) for x in range(self.size)] for y in range(self.size)]
        column_wins = [[(y, x) for x in range(self.size)] for y in range(self.size)]
        diagonal_wins = [[(i, i) for i in range(self.size)]
                        ] + [[(-(j - (self.size - 1)), j) for j in range(self.size)]]
        win_combinations = row_wins + diagonal_wins + column_wins

        win_map = {}
        for i in win_combinations:
            for j in i:
                if j not in win_map:
                    win_map[j] = [i]
                else:
                    win_map[j].append(i)
        return win_map

    def reset(self, e):
        self.page.floating_action_button = self.resetButton = None
        for i in self.rows[1:]:
            i.reset()
        self.player = "X"
        self.positions = [[None] * self.size for i in range(self.size)]
        self.filled = 0
        self.update()

    def showWin(self):
        self.page.dialog = flet.AlertDialog(
            open=True,
            title=flet.Text(f"Player {'X' if self.player == 'O' else 'O'} Wins!"),
            content=flet.Text("Do you want to reset the match?"),
            actions=[
                flet.TextButton("Yes", on_click=lambda e: self.reset(e) or self.closeDialog(e)),
                flet.TextButton("No", on_click=self.closeDialog)
            ])
        self.page.update()

    def showTie(self):
        self.page.dialog = flet.AlertDialog(
            open=True,
            title=flet.Text("It's a Tie!"),
            content=flet.Text("Do you want to reset the match?"),
            actions=[
                flet.TextButton("Yes", on_click=lambda e: self.reset(e) or self.closeDialog(e)),
                flet.TextButton("No", on_click=self.closeDialog)
            ])
        self.page.update()

    def closeDialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def update(self):
        if self.filled == 1:
            self.resetButton = flet.FloatingActionButton(icon=flet.icons.RESTART_ALT_OUTLINED,
                                                         bgcolor="#fe7f9c",
                                                         tooltip="Reset Match",
                                                         on_click=self.reset)
            self.page.floating_action_button = self.resetButton
        self.playerDisplay.value = f"Player {self.player}'s Turn"
        self.page.update()
        if self.filled == self.size**2:
            self.showTie()
        return super().update()

    def build(self):
        self.view.content = self.inner_view
        self.inner_view.controls = self.rows
        return self.view


class BoxRow(flet.Row):

    def __init__(self, row: int, size: int, manager: TicTacToeInteractive):
        super().__init__(expand=True,
                         alignment=flet.MainAxisAlignment.CENTER,
                         vertical_alignment=flet.CrossAxisAlignment.CENTER,
                         spacing=10)
        self.row = row
        self.size = size

        for i in range(size):
            self.controls.append(Box(box_id=(i, row), manager=manager))

    def reset(self):
        for i in self.controls:
            i.reset()


class Box(flet.Container):

    def __init__(self, box_id: tuple[int, int], manager: TicTacToeInteractive):
        super().__init__(expand=True,
                         bgcolor="#C88EA7",
                         padding=5,
                         alignment=flet.alignment.center,
                         border=flet.border.all(1, flet.colors.BLACK),
                         shape=flet.BoxShape.CIRCLE,
                         on_click=self.setSymbol)
        self.box_id = box_id
        self.manager = manager
        self.symbol = None
        self.x = flet.Image(src="icons/TicTacToe/X.png",
                            fit=flet.ImageFit.CONTAIN,
                            repeat=flet.ImageRepeat.NO_REPEAT)
        self.o = flet.Image(src="icons/TicTacToe/O.png",
                            fit=flet.ImageFit.CONTAIN,
                            repeat=flet.ImageRepeat.NO_REPEAT)
        self.content = flet.AnimatedSwitcher(expand=True, duration=250)
        self.setIcon()

    def setSymbol(self, e=None):
        if not self.symbol:
            self.symbol = self.manager.player
            self.manager.positions[self.box_id[1]][self.box_id[0]] = self.symbol
            self.manager.player = "X" if self.symbol == "O" else "O"
            self.setIcon()
            if self.checkWin():
                self.manager.showWin()
                self.manager.update()
                return
            self.manager.filled += 1
            self.manager.update()

    def setIcon(self):
        if self.symbol == "X":
            self.content.content = self.x
        elif self.symbol == "O":
            self.content.content = self.o
        else:
            self.content.content = flet.Text()

    def checkWin(self):
        for i in self.manager.winMap[self.box_id]:
            if all(map(lambda i: self.manager.positions[i[1]][i[0]] == self.symbol, i)):
                return True

    def reset(self):
        self.symbol = None
        self.setIcon()


def main(page: flet.Page):
    page.title = "Tic Tac Toe"
    page.bgcolor = "#643843"
    page.theme_mode = flet.ThemeMode.DARK
    page.padding = 30
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    switcher = flet.AnimatedSwitcher(expand=True, duration=250)
    options = flet.PopupMenuButton(items=[
        flet.PopupMenuItem(content=flet.Column(
            controls=[flet.Text("Grid Size"),
                      SizeSelector(page=page, switcher=switcher)]))
    ])
    page.appbar = flet.AppBar(leading=flet.Icon(flet.icons.SHIELD_MOON_SHARP),
                              title=flet.Text("TIC TAC TOE"),
                              color="#E7CBCB",
                              bgcolor="#99627A",
                              actions=[options])
    page.add(switcher)


flet.app(name="Tic Tac Toe", target=main, assets_dir="assets")