import pygame as pg
from battleships import randomly_place_all_ships
import sys, os

#constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
GRID_TOP_X, GRID_TOP_Y = (60, 178)
CELL_SIZE = 32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FANFARE_END = pg.USEREVENT + 1 # custom event for Game's running loop 

#classes
class GridIcon(pg.sprite.Sprite):
    '''
    base representation of all possible grid objects 
    '''
    def __init__(self, row, col):
        super().__init__()
        self._row = row
        self._col = col 
        self.image = self.icon()
        self.rect = self.image.get_rect(topleft=self.position())

    def icon(self):
        '''
        loads and returns the appropriate icon to display on grid 
        '''
        # loads the path to the appropriate sprite icon by utilising Ship/Hit's string method and 0/1 value of Ship/Hit's ext variable
        img = pg.image.load(os.path.join(os.getcwd(), "sprites", f"{self}{self._ext}.png"))
        return img.convert_alpha()

    def position(self):
        '''
        returns pixel coordinates of top left corner of cell in which relevant sprite should be placed
        '''
        # determines the pixel location at which the icon should be positioned, relative to grid placement given by row and col
        return (GRID_TOP_X + (self._col * CELL_SIZE), GRID_TOP_Y + (self._row * CELL_SIZE))

class Ship(GridIcon):
    '''
    represents a ship of the fleet
    '''
    def __init__(self, row, col, hor, lth):
        self._ext = int(hor)
        self._lth = lth
        self._hit = set()
        super().__init__(row, col)

    def already_hit(self, shot):
        '''
        returns Boolean value indicating whether the given shot, already exists in the ship's set of hits
        '''
        # checks through set of hits to determine whether the shot is already there
        return any(map(lambda hit: (hit._row, hit._col) == shot, self._hit)) 

    def add_hit(self, shot):
        '''
        adds shot to set of ship's hits
        '''
        self._hit.add(shot)

    def is_sinking(self):
        '''
        returns Boolean value indicating whether the ship has received as many hits as it is long
        '''
        return self._lth == len(self._hit)

    def sink(self):
        '''
        'kills' all hit sprites in the ship's set of hits, removing them from the vis_sprites group in so doing
        '''
        for i in self._hit:
            i.kill()

    def __str__(self):
        '''
        returns type of ship determined by its length
        '''
        return {
            4: "battleship",
            3: "cruiser",
            2: "destroyer",
            1: "submarine"
        }.get(self._lth)

class Shot(GridIcon):
    '''
    represents a shot fired into the ocean or onto an unsunk ship
    '''
    def __init__(self, row, col, hit):
        # value is determined by ascertaining whether hit has been passed as an argument
        self._ext = int(hit != None)
        super().__init__(row, col)

    def __str__(self):
        '''
        returns the name of the class in lowercase
        '''
        return type(self).__name__.lower()

class Log(object):
    '''
    represents the text output that responds to player actions
    '''
    def __init__(self):
        self._symbol = None # symbol to indicate what message should be displayed
        self._log_topleft = (45, 545)
        # value determined by whether the game is over (larger font for game over message)
        self._font =  {
            0: pg.font.SysFont("Bahnschrift", 11, bold=True),
            1: pg.font.SysFont("Bahnschrift", 18)
        }

    def set_symbol(self, symbol):
        '''
        sets symbol that will determine the in-game message displayed to user
        '''
        self._symbol = symbol

    def in_game_message(self):
        '''
        returns appropriate string to display depending on user's last in-game action
        '''
        if type(self._symbol) == Ship:
            text = f"You sank a {self._symbol}!"
        else: 
            text = {
                -1: "You've already hit that cell!",
                0: "You missed!",
                1: "You have a hit!"
            }.get(self._symbol)

        return self._font[0].render(text, True, BLACK), self._log_topleft
    
    def game_over_message(self, shots):
        '''
        returns 'game over' message, including number of shots required
        '''
        text = self._font[1].render(f"Game over! You required {shots} shots. Press 'Y' key to play again.", True, WHITE)
        return text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # centres text

class Audio(object): 
    '''
    represents the audio content of the game
    '''
    def __init__(self):
        self._exp = pg.mixer.Sound(os.path.join(os.getcwd(), "audio", "explosion.wav"))
        self._exp.set_volume(0.2)
        self._fan = pg.mixer.Sound(os.path.join(os.getcwd(), "audio", "fanfare.wav"))
        self._fan.set_volume(0.8)
        # value determined by whether the game is over
        self._music_path = {
            0: os.path.join(os.getcwd(), "audio", "battleships.ogg"),
            1: os.path.join(os.getcwd(), "audio", "game_over_audio.ogg")
        }

    def load_music(self, game_over=False):
        '''
        returns path to appropriate music depending on whether the game is over or not
        '''
        return self._music_path[int(game_over)]

    def explosion(self):
        '''
        plays explosion sound to signify the sinking of a ship
        '''
        pg.mixer.Channel(0).play(self._exp, maxtime=2000)

    def fanfare(self):
        '''
        play a celebratory fanfare to signify the sinking of the final unsunk ship
        '''
        pg.mixer.Channel(1).set_endevent(FANFARE_END)
        pg.mixer.Channel(1).play(self._fan, maxtime=3000)

class Game(object):
    '''
    represents an instance of the game
    '''
    def __init__(self):
        self._game_over = False
        self._shots = 0
        self._bg = pg.image.load(os.path.join(os.getcwd(), "battleships_bg.png"))
        self._bg.convert_alpha()
        self._unsunk_sprites = pg.sprite.Group() # group for unsunk ships (ships that are not yet visible)
        self._unsunk_sprites.add(*[Ship(*i[:4]) for i in randomly_place_all_ships()]) # generates and adds ships to unsunk_sprites
        self._vis_sprites = pg.sprite.Group() # group for hits, misses and sunk ships (visible)

        # sets up the fade surface that will fade the screen to black once game is over
        self._fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._fade_surface.fill(BLACK)
        self._fade_surface.set_alpha(0)
        
        self._log = Log()
        self._audio = Audio()
        pg.mixer.music.load(self._audio.load_music())

        pg.mixer.music.set_volume(0.6)
        pg.mixer.music.play(-1)
    
    def cell_clicked(self, row, col):
        '''
        returns Boolean value indicating whether user clicked a cell in the grid
        '''
        # converts the pixel coords of location mouseclick given by row and col, into relative position relative to cells of grid
        r_shot, c_shot = ((row - GRID_TOP_Y) // 32, (col - GRID_TOP_X) // 32)
        # checks r_shot and c_shot are within grid range
        return (r_shot, c_shot) if r_shot in range(10) and c_shot in range(10) else False

    def fleet_hit(self, pos, cell):
        '''
        returns Boolean value indicating whether shot hit any unsunk ships
        '''
        for i in self._unsunk_sprites:
            # checks if mouseclick collides with one of the ships in unsunk_ships and that the ship has not been hit already at the given location
            if i.rect.collidepoint(pos) and not i.already_hit(cell):
                return i

    def running(self):
        '''
        checks if user has quit game and if not, processes events and returns Boolean
        indicating whether the user has closed the game window
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                cell = self.cell_clicked(*pos[::-1]) # pos inverted to match x, y with row and col
                if cell and not self._game_over:
                    self._shots += 1
                    # runs game_logic once it has been established that user has made a shot and the fleet has not yet been fully sunk
                    self.game_logic(pos, cell, self.fleet_hit(pos, cell))

            elif event.type == pg.KEYDOWN and event.unicode.lower() == "y" and self.fade_to_black():
                self.__init__()
            
            elif event.type == FANFARE_END:
                pg.mixer.music.load(self._audio.load_music(self._game_over))
                pg.mixer.music.play(-1)

        return True
            
    def game_logic(self, pos, cell, ship_hit):
        '''
        executes game logic
        '''
        shot = Shot(*cell, ship_hit) # creates new instance of Shot

        if not any([i.rect.collidepoint(pos) for i in self._vis_sprites]): # checks if the same shot has already been made
            self._vis_sprites.add(shot)
            self._log.set_symbol(ship_hit != None) # passes Boolean to set_symbol to determine whether shot is a hit
        else:
            self._log.set_symbol(-1) # indicates to log that cell has already been hit
        
        if ship_hit:
            ship_hit.add_hit(shot)
            if ship_hit.is_sinking():
                ship_hit.sink()
                self._audio.explosion()
                self._vis_sprites.add(ship_hit) # makes the ship visible
                self._unsunk_sprites.remove(ship_hit)
                self._log.set_symbol(ship_hit) # indicates to the log that ship_hit has sunk

        if not self._unsunk_sprites:
           self._game_over = True
           pg.mixer.music.stop()
           self._audio.fanfare()

    def fade_to_black(self):
        '''
        fade screen to black following game over. Returns Boolean indicating whether screen has fully faded to black
        '''
        if not self._fade_surface.get_alpha() == 255:
            # increments opacity of black fill surface. When alpha value reaches 254 it increments by 1 to ceiling of 255
            self._fade_surface.set_alpha(self._fade_surface.get_alpha() + 2) 
            return False
        else:
            return True
                
    def update(self, screen):
        '''
        show results of user action and game logic
        '''
        screen.blit(self._bg, (0, 0))
        self._vis_sprites.draw(screen)
        screen.blit(*self._log.in_game_message())
        
        if self._game_over:
            screen.blit(self._fade_surface, (0, 0))
            if self.fade_to_black():
                # draws game over message once the screen has fully faded to black
                screen.blit(*self._log.game_over_message(self._shots))

        pg.display.update()

def main():
    pg.mixer.pre_init(44100, -16, 2, 2048) # pre-initialising mixer to reduce audio lag
    pg.init()
    pg.mixer.init()
    pg.display.set_caption("Battleships")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    game = Game()
    run = True
    while run:
        run = game.running() # checks if user has quit and if not calls game_logic if cell_clicked
        game.update(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()

