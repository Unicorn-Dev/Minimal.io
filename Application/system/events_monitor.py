from Application.system.game_functions import *
import Application.system.game_functions as gf


settings = None
screen = None
stats = None


def set_global_var(setts, scr, statistics):
    global settings
    global screen
    global stats
    settings = setts
    screen = scr
    stats = statistics


class Monitor:
    def __init__(self, *handlers):
        self.__handlers = [handler() for handler in handlers]
        for i, handler in enumerate(self.__handlers):
            if i + 1 < len(self.__handlers):
                handler.set_next(self.__handlers[i + 1])

    def add_handler(self, handler):
        self.__handlers.append(handler())
        self.__handlers[len(self.__handlers) - 2].set_next(
            self.__handlers[len(self.__handlers) - 1])

    def monitor(self, request, params):
        self.__handlers[0].handle(request, params)


class EventsMonitor(Monitor):
    def __init__(self):
        super().__init__(
            CloseHandler,
            DownHandler,
            UpHandler,
            ButtonHandler,
        )


class BaseHandler:
    def __init__(self):
        self.__next = None

    def set_next(self, handler):
        self.__next = handler

    def handle(self, request, params):
        pass

    def handle_next(self, request, params):
        if self.__next:
            self.__next.handle(request, params)


class CloseHandler(BaseHandler):
    def handle(self, request, params):
        if request.type == pygame.QUIT or \
                (request.type == pygame.KEYDOWN and request.key == pygame.K_q)\
                or (len(params) == 5 and params[4].text == 'Quit'):
            sys.exit()
        else:
            self.handle_next(request, params)


class DownHandler(BaseHandler):
    def handle(self, request, params):
        if request.type == pygame.KEYDOWN:
            mon = Monitor()
            mon.add_handler(ChooseGameTypeHandler)
            mon.add_handler(PauseHandler)
            mon.add_handler(BackToMainMenuHandler)
            mon.add_handler(GameActiveHandler)
            mon.add_handler(ChangeGunHandler)
            mon.add_handler(FirstMoveHandler)
            mon.add_handler(SecondMoveHandler)
            mon.monitor(request, params)
        else:
            self.handle_next(request, params)


class UpHandler(BaseHandler):
    def handle(self, request, params):
        if request.type == pygame.KEYUP:
            mon = Monitor(FirstMoveHandler, SecondMoveHandler)
            mon.monitor(request, params)
        else:
            self.handle_next(request, params)


class ButtonHandler(BaseHandler):
    def handle(self, request, params):
        if request.type == pygame.MOUSEBUTTONDOWN:
            mon = Monitor()
            mon.add_handler(GameNotActiveHandler)
            mon.add_handler(ProcessButtonsHandler)
            mon.monitor(request, params)
        else:
            self.handle_next(request, params)


class ProcessButtonsHandler(BaseHandler):
    def handle(self, request, params):
        params.append(None)
        for button in params[0]:
            params[4] = button
            mon = Monitor()
            mon.add_handler(ButtonClickedHandler)
            mon.add_handler(ButtonContinueHandler)
            mon.add_handler(ButtonChooseGameTypeHandler)
            mon.add_handler(OnePlayerModeHandler)
            mon.add_handler(TwoPlayersModeHandler)
            mon.add_handler(ButtonBackToMainMenuHandler)
            mon.add_handler(CloseHandler)
            mon.monitor(request, params)
        self.handle_next(request, params)


class ButtonClickedHandler(BaseHandler):
    def handle(self, request, params):
        button_clicked = params[4].rect.collidepoint(pygame.mouse.get_pos())
        if button_clicked:
            self.handle_next(request, params)


class ChooseGameTypeHandler(BaseHandler):
    def handle(self, request, params):
        if request.key == pygame.K_p and not stats.game_active:
            stats.choosing_game_type = True
        else:
            self.handle_next(request, params)


class ButtonChooseGameTypeHandler(BaseHandler):
    def handle(self, request, params):
        if len(params) == 5 and (params[4].text == 'Play'
                                 or params[4].text == 'Restart'):
            stats.choosing_game_type = True
        else:
            self.handle_next(request, params)


class ButtonContinueHandler(BaseHandler):
    def handle(self, request, params):
        if params[4].text == 'Continue':
            gf.set_pause(False)
        else:
            self.handle_next(request, params)


class OnePlayerModeHandler(BaseHandler):
    def handle(self, request, params):
        if params[4].text == 'One player':
            stats.single_player = True
            params[1].clear()
            params[1].append(Hero())
            gf.start_game(params[1], params[2], params[3])
        else:
            self.handle_next(request, params)


class TwoPlayersModeHandler(BaseHandler):
    def handle(self, request, params):
        if params[4].text == 'Two players':
            stats.single_player = False
            params[1].clear()
            params[1].append(Hero())
            params[1].append(Hero())
            gf.start_game(params[1], params[2], params[3])
        else:
            self.handle_next(request, params)


class PauseHandler(BaseHandler):
    def handle(self, request, params):
        if request.key == pygame.K_ESCAPE and stats.game_active != stats.pause:
            gf.set_pause(not stats.pause)
        else:
            self.handle_next(request, params)


class BackToMainMenuHandler(BaseHandler):
    def handle(self, request, params):
        if request.key == pygame.K_ESCAPE and stats.choosing_game_type:
            stats.choosing_game_type = False
        else:
            self.handle_next(request, params)


class ButtonBackToMainMenuHandler(BaseHandler):
    def handle(self, request, params):
        if len(params) == 5 and params[4].text == 'Back':
            stats.choosing_game_type = False
        else:
            self.handle_next(request, params)


class GameActiveHandler(BaseHandler):
    def handle(self, request, params):
        if stats.game_active:
            self.handle_next(request, params)


class GameNotActiveHandler(BaseHandler):
    def handle(self, request, params):
        if not stats.game_active:
            self.handle_next(request, params)


class ChangeGunHandler(BaseHandler):
    def handle(self, request, params):
        for hero in params[1]:
            if request.key == pygame.K_n:
                hero.change_bullets("Bullet")
            if request.key == pygame.K_f:
                hero.change_bullets("FastBullet")
            if request.key == pygame.K_b:
                hero.change_bullets("BigBullet")
            if request.key == pygame.K_EQUALS:
                hero.bullet_type = None
        self.handle_next(request, params)


class FirstMoveHandler(BaseHandler):
    def handle(self, request, params):
        if request.key == pygame.K_UP:
            params[1][0].speed_y = -params[1][0].speed if request.type == pygame.KEYDOWN else 0
        elif request.key == pygame.K_DOWN:
            params[1][0].speed_y = params[1][0].speed if request.type == pygame.KEYDOWN else 0
        elif request.key == pygame.K_LEFT:
            params[1][0].speed_x = -params[1][0].speed if request.type == pygame.KEYDOWN else 0
        elif request.key == pygame.K_RIGHT:
            params[1][0].speed_x = params[1][0].speed if request.type == pygame.KEYDOWN else 0
        self.handle_next(request, params)


class SecondMoveHandler(BaseHandler):
    def handle(self, request, params):
        if not stats.single_player:
            if request.key == pygame.K_w:
                params[1][1].speed_y = -params[1][1].speed if request.type == pygame.KEYDOWN else 0
            elif request.key == pygame.K_s:
                params[1][1].speed_y = params[1][1].speed if request.type == pygame.KEYDOWN else 0
            elif request.key == pygame.K_a:
                params[1][1].speed_x = -params[1][1].speed if request.type == pygame.KEYDOWN else 0
            elif request.key == pygame.K_d:
                params[1][1].speed_x = params[1][1].speed if request.type == pygame.KEYDOWN else 0
        self.handle_next(request, params)
