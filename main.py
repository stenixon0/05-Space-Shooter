import sys, logging, os, random, math, open_color, arcade, time

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 20
STARTING_LOCATION = (400, 50)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage, good):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        #assigns whether bullet does damage to enemy if(good)
        self.goodbullet = good

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets\PNG\Sprites\Ships\spaceShips_001.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.dx = 0
        self.dy = 0
        self.health = 10

    def update(self):
        '''
        Moves the Player
        '''
        self.center_x += self.dx
        self.center_y += self.dy

        if self.center_x > SCREEN_WIDTH - 25:
            self.center_x = SCREEN_WIDTH - 25

        if self.center_x < 25:
            self.center_x = 25
        
            

class Enemy(arcade.Sprite):
    def __init__(self, position, speed):
        '''
        initializes a spaceship enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets\PNG\Sprites\Ships\spaceShips_007.png", 0.2)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        self.dx = speed
        self.timesincebullet = random.randint(0, 200)

    def update(self):
        '''
        Moves the Enemy
        '''
        self.center_x += self.dx

        if self.center_x > SCREEN_WIDTH - 25:
            self.center_x = SCREEN_WIDTH - 25
            self.center_y -= 5
            self.dx = -self.dx

        if self.center_x < 25:
            self.center_x = 25
            self.center_y -= 5
            self.dx = -self.dx
        
        if self.center_y < 20:
            self.center_y = SCREEN_HEIGHT
            


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.gray_9)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        
        self.score = 0
        #assigns speed of enemies
        self.speed = 1
        #assigns number of moves made by enemies to 0
        self.movecount = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES // 4):
            for j in range(NUM_ENEMIES // 5):
                y = 60 * (j + 1) + 300
                x = 100 * (i + 1) + 100
                enemy = Enemy((x,y), self.speed)
                self.enemy_list.append(enemy)            

    def update(self, delta_time):
        self.bullet_list.update()
        self.player.update()
        self.enemy_list.update()

        '''
        if all enemies have been killed: restart
        '''
        if (len(self.enemy_list) == 0):
            self.score += 1
            self.setup()
            #increase enemy movement speed
            self.speed += 5
            self.player.health = 10

        '''
        if player has been killed: restart
        '''

        if self.player.health == 0:
            
            print("Game Over")
            print(self.score)
            sys.exit()
        '''
        check for collison with player
        '''
        for b in self.bullet_list:
                # check for collision
                collision = arcade.check_for_collision(self.player, b)
                # for every bullet that hits, decrease the hp and then see if it dies
                if collision and b.goodbullet == False:
                # e.kill() will remove the enemy sprite from the game
                    self.player.health -= 1
                    b.kill()

        for e in self.enemy_list:
            if e.timesincebullet > random.randint(200, 400):
                x = e.center_x
                y = e.center_y - 15
                bullet = Bullet((x,y),(0,-10),BULLET_DAMAGE, False)
                self.bullet_list.append(bullet)
                e.timesincebullet = 0
            else:
                e.timesincebullet += 1

            for b in self.bullet_list:
                if b.goodbullet == True:
                    # check for collision
                    collision = arcade.check_for_collision(e, b)
                    # for every bullet that hits, decrease the hp and then see if it dies
                    if collision:
                        print("this was ran")
                    # e.kill() will remove the enemy sprite from the game
                        e.kill()
                        b.kill()
        
            
            

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.SPACE:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE, True)
            self.bullet_list.append(bullet)
        
        if key == arcade.key.LEFT:
            self.player.dx = -5

        if key == arcade.key.RIGHT:
            self.player.dx = 5

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.player.dx = 0

        if key == arcade.key.RIGHT:
            self.player.dx = 0

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()