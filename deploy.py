import secrets
import curses
from curses import wrapper
from dotenv import set_key

class Deployer:
    ENV_PATH = '.env'
    TITLE_TEXT = "DEPLOY.PY"
    OPTIONS = [
        "[1] Configuración para desarrollo",
        "[2] Configuración para servidor",
        "[0] Cerrar deploy.py"
    ]

    def __init__(self):
        pass

    def generate_secret_key(self) -> str:
        """Genera un string largo aleatoriamente"""
        characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>/?'
        return ''.join(secrets.choice(characters) for _ in range(50))

    def run(self, stdscr):
        curses.init_pair(1, 46, curses.COLOR_BLACK)
        stdscr.keypad(True)
        curses.curs_set(False)

        TITLE = curses.color_pair(1) | curses.A_BOLD
        TEXT = curses.color_pair(1)
        SELECTED_TEXT = curses.color_pair(1) | curses.A_REVERSE

        position = 2

        set_key(self.ENV_PATH, 'SECRET_KEY', self.generate_secret_key())
        
        while True:
            self.display_menu(stdscr, position, TITLE, TEXT, SELECTED_TEXT)
            key = stdscr.getkey()

            if key == '0' or (key == '\n' and position == 2):
                break
            elif key == '1' or (key == '\n' and position == 0):
                set_key(self.ENV_PATH, 'ENVIRONMENT', 'dev')
                self.display_message(stdscr, "[!] Se configuró el ambiente para desarrollo", TITLE, SELECTED_TEXT)
            elif key == '2' or (key == '\n' and position == 1):
                set_key(self.ENV_PATH, 'ENVIRONMENT', 'production')
                set_key(self.ENV_PATH, 'ALLOWED_HOSTS', '*')
                set_key(self.ENV_PATH, 'CORS_ORIGIN_WHITELIST', 'http://localhost')
                self.display_message(stdscr, "[!] Se configuró el ambiente para el servidor", TITLE, SELECTED_TEXT)
            elif key in ('KEY_DOWN', 'KEY_RIGHT'):
                position = (position+1) % 3
                #position = 1 if position >= 3 else position + 1
            elif key in ('KEY_UP', 'KEY_LEFT'):
                position = (position-1) % 3
                #position = 2 if position <= 0 else position - 1
            else:
                self.display_error(stdscr, key, TEXT)

            stdscr.refresh()

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

    def display_menu(self, stdscr, position, TITLE, TEXT, SELECTED_TEXT):
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        stdscr.addstr(0, (sw - len(self.TITLE_TEXT)) // 2, self.TITLE_TEXT, TITLE)
        for idx, option in enumerate(self.OPTIONS, start=0):
            stdscr.addstr(idx + 1, 1, option, SELECTED_TEXT if position == idx else TEXT)

    def display_message(self, stdscr, message, TITLE, SELECTED_TEXT):
        stdscr.clear()
        curses.curs_set(True)
        sh, sw = stdscr.getmaxyx()
        stdscr.addstr(0, (sw - len(self.TITLE_TEXT)) // 2, self.TITLE_TEXT, TITLE)
        stdscr.addstr(2, 1, message, SELECTED_TEXT)
        stdscr.getch()
        curses.curs_set(False)

    def display_error(self, stdscr, key, TEXT):
        stdscr.addstr(9, 1, f"[Error] No existe opción {key}", TEXT)
        stdscr.getch()

if __name__ == '__main__':
    try:
        deployer = Deployer()
        wrapper(deployer.run)
    except Exception as e:
        print(f"An error occurred: {e}")