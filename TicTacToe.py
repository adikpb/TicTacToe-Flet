from pprint import pprint
from random import choice
from time import sleep

import flet


class TicTacToe(flet.UserControl):

    def __init__(self, view: flet.View, size: int = 3, botted=False):
        super().__init__(expand=True,
                         animate_offset=flet.animation.Animation(
                             duration=1500, curve=flet.animation.AnimationCurve.ELASTIC_OUT))
        self.view = view
        self.size = size
        self.botted = botted
        self.current = "X"
        self.filled = 0
        self.end = False
        self.positions = [[None] * self.size for i in range(self.size)]
        self.winMap = self.generateWinMap()
        if botted:
            self.player = "X"
            self.bot = "O"
            self.indexes = [(i, j) for i in range(self.size) for j in range(self.size)]

        self.outer_control = flet.Container(expand=True,
                                            padding=10,
                                            bgcolor="#99627A",
                                            alignment=flet.alignment.center,
                                            border=flet.border.all(2, flet.colors.BLACK),
                                            border_radius=flet.border_radius.all(50))
        self.inner_control = flet.Column(expand=True,
                                         spacing=20,
                                         alignment=flet.MainAxisAlignment.CENTER,
                                         horizontal_alignment=flet.CrossAxisAlignment.CENTER)

        self.playerDisplay = flet.Text("👤's Turn" if botted else f"Player {self.current}'s Turn",
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
        print(f"\n{self.size}x{self.size}\n")
        pprint(win_map)
        return win_map

    def setSymbol(self, box):
        box.symbol = self.current
        self.positions[box.box_id[1]][box.box_id[0]] = box.symbol
        print(self.positions)
        if self.botted:
            self.indexes.remove(box.box_id)
        self.current = "X" if box.symbol == "O" else "O"
        box.setIcon()
        self.filled += 1
        
        if self.checkWin(box) and not self.end:
            self.end = True
            self.showWin()
        self.update()

    def botPlay(self):
        if self.indexes:
            sleep(0.75)
            play = choice(self.indexes)
            print(play)
            self.inner_control.controls[play[1] + 1].controls[play[0]].setSymbol()

    def reset(self, e):
        self.view.floating_action_button = self.resetButton = None
        for i in self.rows[1:]:
            i.reset()
        self.current = "X"
        self.positions = [[None] * self.size for i in range(self.size)]
        self.filled = 0
        self.end = False
        if self.botted:
            self.indexes = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.update()
        self.view.update()

    def checkWin(self, box):
        for i in self.winMap[box.box_id]:
            if all(map(lambda j: self.positions[j[1]][j[0]] == box.symbol, i)):
                return True

    def showWin(self):
        if self.botted:
            text = "👤 Player wins!" if self.current != self.player else "🤖 Bot wins!"
        else:
            text = f"Player {'X' if self.current == 'O' else 'O'} Wins!"
        self.view.page.dialog = flet.AlertDialog(
            open=True,
            title=flet.Text(text),
            content=flet.Text("Do you want to reset the match?"),
            actions=[
                flet.TextButton("Yes", on_click=lambda e: self.reset(e) or self.closeDialog(e)),
                flet.TextButton("No", on_click=self.closeDialog)
            ])
        self.view.page.update()

    def showTie(self):
        self.view.page.dialog = flet.AlertDialog(
            open=True,
            title=flet.Text("It's a Tie!"),
            content=flet.Text("Do you want to reset the match?"),
            actions=[
                flet.TextButton("Yes", on_click=lambda e: self.reset(e) or self.closeDialog(e)),
                flet.TextButton("No", on_click=self.closeDialog)
            ])
        self.view.page.update()

    def closeDialog(self, e):
        self.view.page.dialog.open = False
        self.view.page.update()

    def update(self):
        if self.filled == 1:
            self.resetButton = flet.FloatingActionButton(icon=flet.icons.RESTART_ALT_OUTLINED,
                                                         bgcolor="#FE7F9C",
                                                         tooltip="Reset Match",
                                                         on_click=self.reset)
            self.view.floating_action_button = self.resetButton
            self.view.page.update()
        if self.botted:
            self.playerDisplay.value = "👤's Turn" if self.current == self.player else "🤖's Turn"
            self.outer_control.update()
            if self.current == self.bot:
                self.botPlay()
        else:
            self.playerDisplay.value = f"Player {self.current}'s Turn"
        self.outer_control.update()
        if self.filled == self.size**2:
            self.showTie()
        return super().update()

    def build(self):
        self.outer_control.content = self.inner_control
        self.inner_control.controls = self.rows
        return self.outer_control


class SizeSelector(flet.Slider):

    def __init__(self,
                 view: flet.View,
                 slide_in: flet.Stack,
                 min_size: int = 3,
                 max_size: int = 5,
                 grid=TicTacToe,
                 botted=False):
        super().__init__(divisions=max_size - min_size,
                         label="{value} x {value}",
                         max=max_size,
                         min=min_size,
                         value=3,
                         on_change=self.changeGridSize,
                         active_color="#FE7F9C",
                         thumb_color="#FE7F9C")
        self.view = view
        self.slide_in = slide_in
        self.grids = {i: None for i in range(min_size, max_size + 1)}
        self.currentSize = min_size
        for i in self.grids:
            self.grids[i] = grid(view=self.view, size=i, botted=botted)
            self.slide_in.controls.append(self.grids[i])
            if i != self.currentSize:
                self.grids[i].offset = flet.transform.Offset(1.25, 0)
            else:
                self.grids[i].offset = flet.transform.Offset(0, 0)

    def changeGridSize(self, e):
        if self.currentSize < self.value:
            self.grids[self.currentSize].offset = flet.transform.Offset(-1.25, 0)
            self.grids[self.value].offset = flet.transform.Offset(0, 0)
        elif self.currentSize > self.value:
            self.grids[self.currentSize].offset = flet.transform.Offset(1.25, 0)
            self.grids[self.value].offset = flet.transform.Offset(0, 0)
        self.currentSize = self.value
        self.view.floating_action_button = self.grids[self.value].resetButton
        self.view.page.update()


class BoxRow(flet.Row):

    def __init__(self, row: int, size: int, manager: TicTacToe):
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

    def __init__(self, box_id: tuple[int, int], manager: TicTacToe):
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

    def setSymbol(self, e):
        if not self.symbol:
            self.manager.setSymbol(self)

    def setIcon(self):
        if self.symbol == "X":
            self.content.content = self.x
        elif self.symbol == "O":
            self.content.content = self.o
        else:
            self.content.content = flet.Text()

    def reset(self):
        self.symbol = None
        self.setIcon()


class PlayerVPlayerLocal(flet.View):

    def __init__(self, route: str | None = None):
        super().__init__(route=route, padding=30, bgcolor="#643843")

        self.slide_in = flet.Stack(expand=True)
        self.options = flet.PopupMenuButton(items=[
            flet.PopupMenuItem(content=flet.Column(
                [flet.Text("Grid Size"),
                 SizeSelector(view=self, slide_in=self.slide_in)]))
        ],
                                            tooltip="Show options")
        self.appbar = flet.AppBar(title=flet.Text("TIC TAC TOE"),
                                  color="#E7CBCB",
                                  bgcolor="#99627A",
                                  actions=[
                                      flet.IconButton(
                                          icon=flet.icons.HOME,
                                          url="https://github.com/adikpb/TicTacToe-Flet",
                                          tooltip="github.com/adikpb/TicTacToe-Flet"), self.options
                                  ])
        self.controls = [self.slide_in]


class PlayerVBot(flet.View):

    def __init__(self, route: str | None = None):
        super().__init__(route=route, padding=30, bgcolor="#643843")

        self.slide_in = flet.Stack(expand=True)
        self.options = flet.PopupMenuButton(items=[
            flet.PopupMenuItem(content=flet.Column([
                flet.Text("Grid Size"),
                SizeSelector(view=self, slide_in=self.slide_in, botted=True)
            ]))
        ],
                                            tooltip="Show options")
        self.appbar = flet.AppBar(title=flet.Text("TIC TAC TOE"),
                                  color="#E7CBCB",
                                  bgcolor="#99627A",
                                  actions=[
                                      flet.IconButton(
                                          icon=flet.icons.HOME,
                                          url="https://github.com/adikpb/TicTacToe-Flet",
                                          tooltip="github.com/adikpb/TicTacToe-Flet"), self.options
                                  ])
        self.controls = [self.slide_in]


class Menu(flet.View):

    def __init__(self, route: str | None = None):
        super().__init__(route=route, padding=30, bgcolor="#643843")

        outer_control = flet.Container(expand=True,
                                       padding=10,
                                       bgcolor="#99627A",
                                       alignment=flet.alignment.center,
                                       border=flet.border.all(2, flet.colors.BLACK),
                                       border_radius=flet.border_radius.all(50))

        inner_control = flet.Column(expand=True,
                                    spacing=20,
                                    alignment=flet.MainAxisAlignment.SPACE_EVENLY,
                                    horizontal_alignment=flet.CrossAxisAlignment.CENTER)

        outer_control.content = inner_control
        inner_control.controls = [
            flet.ElevatedButton(color="black",
                                bgcolor="#C88EA7",
                                content=flet.Text("🤖 Play against a bot!",
                                                  style=flet.TextThemeStyle.DISPLAY_SMALL),
                                on_click=lambda e: self.page.go("/bot")),
            flet.Divider(color="#643843"),
            flet.ElevatedButton(color="black",
                                bgcolor="#C88EA7",
                                content=flet.Text("👤 Play against a person locally!",
                                                  style=flet.TextThemeStyle.DISPLAY_SMALL),
                                on_click=lambda e: self.page.go("/local"))
        ]

        self.appbar = flet.AppBar(leading=flet.Icon(flet.icons.SHIELD_MOON_SHARP),
                                  title=flet.Text("TIC TAC TOE"),
                                  color="#E7CBCB",
                                  bgcolor="#99627A",
                                  actions=[
                                      flet.IconButton(
                                          icon=flet.icons.HOME,
                                          url="https://github.com/adikpb/TicTacToe-Flet",
                                          tooltip="github.com/adikpb/TicTacToe-Flet")
                                  ])

        self.controls = [outer_control]


def main(page: flet.Page):
    page.title = "Tic Tac Toe"

    menu = Menu("/")
    local = PlayerVPlayerLocal("/local")
    bot = PlayerVBot("/bot")

    def route_change(route):
        page.views.clear()
        page.views.append(menu)
        if page.route == "/local":
            page.views.append(local)
        elif page.route == "/bot":
            page.views.append(bot)

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


flet.app(name="Tic Tac Toe", target=main, assets_dir="assets")