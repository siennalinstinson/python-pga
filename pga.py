#to do: choices 9 or 18, bogey/par/etc, funny sounds
#--------------------------------------------------------------------------------------------------------
#IMPORT LIBS
import arcade
import time
import random

#GLOBAL VARS
width=600
height=400
title='PGA'

#DEF CLASSES
class holeView(arcade.View):

    def __init__(self): #initialize game
        super().__init__()
        #game control
        self.paused=False
        #scorekeeping
        self.n_hole = 1 #counter
        self.score = 0
        #first hole setup setup
        self.setup()
        
    def setup(self): #setup visuals (clouds, grass, bunkers, water, hole), player, ball, sounds
        #scorekeeping
        self.n_hits=0 #this hole
        #VISUALS
        #setup clouds
        arcade.schedule(self.add_cloud, 3.0) #add a cloud every three seconds
        #setup clubs dictionary (your virtual golf bag! format "club name": club multiplier)
        self.golfbag= {'driver': 1,'hybrid': 0.80, '4-wood': 0.85, '4-iron': 0.71, '5-iron': 0.67, '6-iron': 0.63, '7-iron': 0.60, '8-iron': 0.56, '9-iron': 0.52, 'pitching wedge': 0.46,'gap wedge': 0.38, 'sand wedge': 0.31, 'lob wedge': 0.25, 'putter': 0.1} #calc multipliers based on James' hit distances
        self.club = "driver" #start with the driver boom big shot wow
        self.club_multiplier = self.golfbag[self.club]
        #setup sprite lists
        self.bunker_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList() #store the things every single one of themmmmm everyTHING
        #setup hole
        self.n_waters=1 #random.randint(0,1)
        self.n_bunkers = random.randint(1,3)
        self.n_par = 2 + self.n_bunkers + self.n_waters #par based on number of obstacles
        self.hole=arcade.Sprite("img/flag_blue.png")
        self.hole.center_x=(random.randint(width-50,width)) #on left
        self.hole.center_y=(random.randint(0,height-55)) #on grass
        self.all_sprites_list.append(self.hole)
        #setup random water body
        for i in range(self.n_waters):
            self.water_hazard = arcade.Sprite("img/water_hazard.png",0.3)
            self.water_hazard.center_x = random.randint(35,width-25) #in frame
            self.water_hazard.center_y = random.randint(35,height-100) #in frame, on grass
            while arcade.check_for_collision_with_list(self.water_hazard, self.all_sprites_list): #if generate on top of something else, regenerate at new coordinates
                self.water_hazard.center_x = random.randint(35,width-25) #in frame
                self.water_hazard.center_y = random.randint(35,height-75) #in frame, on grass
            self.all_sprites_list.append(self.water_hazard)
        #setup random bunkers
        for i in range(self.n_bunkers):
            self.bunker = arcade.Sprite("img/bunker.png",0.3)
            self.bunker.center_x = random.randint(35,width-25) #in frame
            self.bunker.center_y = random.randint(35,height-75) #in frame, on grass
            while arcade.check_for_collision_with_list(self.bunker, self.all_sprites_list): #if generate on top of something else, regenerate at new coordinates
                self.bunker.center_x = random.randint(35,width-25) #in frame
                self.bunker.center_y = random.randint(35,height-75) #in frame, on grass
            self.bunker_list.append(self.bunker)
            self.all_sprites_list.append(self.bunker)
        #setup player
        self.player=arcade.Sprite("img/jamesie.png")
        self.player.center_x=10
        self.player.center_y=10
        self.all_sprites_list.append(self.player) #add player sprite to all sprites list
        #setup ball
        self.ball=arcade.Sprite("img/ball_generic1.png",0.5)
        self.ball.center_x=self.player.center_x+15
        self.ball.center_y=self.player.center_y+15
        self.all_sprites_list.append(self.ball)
        #SOUNDS 
        self.bagrustle=arcade.load_sound("sound/bagrustle.wav")
        self.driver=arcade.load_sound("sound/driver.wav")
        self.iron=arcade.load_sound("sound/iron.wav")
        self.chipper=arcade.load_sound("sound/chipper.wav")
        self.putter=arcade.load_sound("sound/putter.wav")
        self.fore=arcade.load_sound("sound/fore.wav")
        self.splash=arcade.load_sound("sound/splash.wav")
        self.holecup=arcade.load_sound("sound/holecup.wav")
        self.holeinsome=arcade.load_sound("sound/hole.wav")
        self.holeinone=arcade.load_sound("sound/holeinone.wav")
        self.gasp=arcade.load_sound("sound/gasp.wav")
        self.not_good=arcade.load_sound("sound/not_good.wav")
        self.f=arcade.load_sound("sound/f.wav")
        self.ugly=arcade.load_sound("sound/ugly.wav")
        self.cold_one=arcade.load_sound("sound/cold_one.wav")
        #sound helpers
        self.club_sound = {'driver': self.driver, 'hybrid': self.iron, '4-wood': self.iron, '4-iron': self.iron, '5-iron': self.iron, '6-iron': self.iron, '7-iron': self.iron, '8-iron': self.iron, '9-iron': self.iron, 'pitching wedge': self.chipper, 'gap wedge': self.chipper, 'sand wedge': self.chipper, 'lob wedge': self.chipper, 'putter': self.putter}
        self.didweohno = 0
        self.didwewarnthem = 0

    def on_key_press(self, symbol: int, modifiers: int): #player commands
        #quit
        if symbol == arcade.key.Q:
            arcade.close_window() 
        #pause
        elif symbol == arcade.key.W:
            self.paused=not self.paused
        #player move
        if symbol == arcade.key.UP:
            self.player.change_y=1
        elif symbol == arcade.key.DOWN:
            self.player.change_y=-1
        elif symbol == arcade.key.RIGHT:
            self.player.change_x=1
        elif symbol == arcade.key.LEFT:
            self.player.change_x=-1
        #change clubs
        elif symbol == arcade.key.D:
            self.club = "driver"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.H:
            self.club = "hybrid"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.W:
            self.club = "4-wood"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.KEY_4:
            self.club = "4-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.KEY_5:
            self.club = "5-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.KEY_6:
            self.club = "6-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.KEY_7:
            self.club = "7-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.KEY_8:
            self.club = "8-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.KEY_9:
            self.club = "9-iron"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.P:
            self.club = "pitching wedge"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        elif symbol == arcade.key.G:
            self.club = "gap wedge"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.S:
            self.club = "sand wedge"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.L:
            self.club = "lob wedge"
            self.club_multiplier = self.golfbag[self.club]
            arcade.play_sound(self.bagrustle)
        elif symbol == arcade.key.U:
            self.club = "putter"
            arcade.play_sound(self.bagrustle)
            self.club_multiplier = self.golfbag[self.club]
        #hit ball
        elif symbol == arcade.key.SPACE:
            self.backswing=time.time()
        elif symbol == arcade.key.B:
            arcade.play_sound(self.cold_one)

    def on_key_release(self, symbol: int, modifiers: int): #stop player commands
        #player stop moving
        if (symbol == arcade.key.UP or symbol == arcade.key.DOWN):
            self.player.change_y=0
        if (symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT):
            self.player.change_x=0
        #ball stop moving
        if symbol == arcade.key.SPACE:
            self.frontswing=time.time()
            self.big_boy_muscles=(self.frontswing-self.backswing) #wow look at that power! <3
            if abs(self.player.center_x-self.ball.center_x) < 15 and abs(self.player.center_y-self.ball.center_y) < 15: #if close enough to hit ball
                self.hit(self.big_boy_muscles)

    def on_update(self, delta_time: float): #update all sprites

        #don't update if paused
        if self.paused:
            return
        #end hole if made it!
        if arcade.check_for_collision(self.ball, self.hole): #made hole
            #sound
            if self.n_hits == 1: #hole in one
                arcade.play_sound(self.holeinone)
            else:
                arcade.play_sound(self.holecup)
                if (self.n_hits - self.n_par) >= 4: #quadruple bogey
                    arcade.play_sound(self.not_good)
                else:
                    arcade.play_sound(self.holeinsome) #you are the best golfer ever the crowd loves you wowwww <333
            if self.n_hole == 18: #end
                end_view = endView(self.score) #end screen
                self.window.show_view(end_view)
            else: #setup hole
                self.n_hole += 1 #increment hole
                self.setup() #setup new hole
        #update if didn't make it ughhhhh BE BETTER
        self.all_sprites_list.update()
        #ball checks
        #if ball is moving, decrease speed
        if (self.ball.change_x > 0):
            self.ball.change_x -= 0.1
        if (self.ball.change_x < 0):
            self.ball.change_x += 0.1
        if (self.ball.change_y > 0):    
            self.ball.change_y -= 0.1
        if (self.ball.change_y < 0):
            self.ball.change_y += 0.1
        #stop ball
        if abs(self.ball.change_x) < 0.1:
            self.ball.change_x = 0
        if abs(self.ball.change_y) < 0.1:
            self.ball.change_y = 0
        #check if ball lands in bunker, activate bunker multiplier
        if arcade.check_for_collision_with_list(self.ball, self.bunker_list) and self.ball.change_x ==0 and self.ball.change_y == 0:
            if self.didweohno == 0:
                arcade.play_sound(self.ugly)
                self.didweohno = 1
            self.bunker_multiplier = 0.1
        else:
            self.bunker_multiplier = 1
            self.didweohno = 0
        #check if ball lands in water, reset and penalty
        if arcade.check_for_collision(self.ball, self.water_hazard) and self.ball.change_x ==0 and self.ball.change_y == 0:
            arcade.play_sound(self.splash)
            arcade.play_sound(self.f)
            self.ball.center_x = (self.water_hazard.left - 10)
            self.n_hits += 1
            self.score += 1 #add one hit to total score
        #check if ball goes out of bounds OOPPPPSSS if so move back in once stopped and add penalty hit
        if self.ball.top > height-50:
            self.ball.top = height-75
            self.ball.change_y=0
        if self.ball.right > width: #yell fore when OOB
            if self.didwewarnthem == 0:
                arcade.play_sound(self.fore)
                self.didwewarnthem = 1
            if self.ball.change_x == 0 and self.ball.change_y == 0: #bring ball back once it stops
                self.ball.right = width-25
                self.n_hits += 1 #penaltyyyy
                self.score += 1 #add one hit to total score
                self.didwewarnthem = 0
        if self.ball.bottom < 0:
            if self.didwewarnthem == 0:
                arcade.play_sound(self.fore)
                self.didwewarnthem = 1
            if self.ball.change_x == 0 and self.ball.change_y == 0:
                self.ball.bottom = 25
                self.n_hits += 1
                self.score += 1 #add one hit to total score
                self.didwewarnthem = 0
        if self.ball.left < 0:
            if self.didwewarnthem == 0:
                arcade.play_sound(self.fore)
                self.didwewarnthem = 1
            if self.ball.change_x == 0 and self.ball.change_y == 0:
                self.ball.left = 25
                self.n_hits += 1
                self.score += 1 #add one hit to total score
                self.didwewarnthem = 0
        #player checks
        #don't go out of bounds! (brings player back on spring if he tries to move off)
        if self.player.top > height-50:
            self.player.top = height-50
        if self.player.right > width:
            self.player.right = width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self): #draw everything
        arcade.start_render
        #draw sky
        arcade.draw_lrtb_rectangle_filled(0,width,height,height-50,arcade.color.SKY_BLUE)
        #draw grass
        arcade.draw_lrtb_rectangle_filled(0,width,height-50,0,arcade.color.GREEN)
        #draw green
        arcade.draw_circle_filled(self.hole.center_x, self.hole.center_y, 35, arcade.color.LAWN_GREEN)
        #draw all sprites
        self.all_sprites_list.draw()
        #update score
        arcade.draw_text('Hole {} Par {}:'.format(self.n_hole, self.n_par),15,height-15,arcade.color.DARK_ORANGE, 10, bold=True)
        arcade.draw_text('Hole score: {}:'.format(self.n_hits),15,height-30,arcade.color.DARK_ORANGE, 10, bold=True)
        arcade.draw_text('Total score: {}'.format(self.score),15,height-45,arcade.color.DARK_ORANGE, 10, bold=True)
    
    def hit(self, swing_multiplier):
        #club hit sound
        arcade.play_sound(self.club_sound[self.club])
        #calc velocity multipliers based on player and ball tan theta PPHYSICS WOAH yeeeet
        if (self.ball.center_x-self.player.center_x) == 0: #player below/above of beside ball
            if (self.ball.center_y-self.player.center_y) > 0: #player below ball
                x_multiplier = 0
                y_multiplier = 1
            else: #player above ball
                x_multiplier = 0
                y_multiplier = -1
        elif (self.ball.center_y-self.player.center_y) == 0: #player left/right of beside ball
            if (self.ball.center_x-self.player.center_x) > 0: #player left of ball
                x_multiplier = 1
                y_multiplier = 0
            else: #player right of ball
                x_multiplier = -1
                y_multiplier = 0
        else:
            x_multiplier=(self.ball.center_x-self.player.center_x)/abs(self.ball.center_y-self.player.center_y)
            y_multiplier=(self.ball.center_y-self.player.center_y)/abs(self.ball.center_x-self.player.center_x)
        #base speed
        weak_speed=5
        #calc ball velocity and direction based on multipliers
        self.ball.change_x = round(weak_speed*swing_multiplier*self.club_multiplier*self.bunker_multiplier*x_multiplier, 1)
        self.ball.change_y = round(weak_speed*swing_multiplier*self.club_multiplier*self.bunker_multiplier*y_multiplier, 1)
        self.n_hits += 1 #add one hit to score
        self.score += 1 #add one hit to total score

    def add_cloud(self, delta_time: float): #add cloud
        cloud=flying_sprite("img/cloud1.png",0.2)
        cloud.left=random.randint(width, width+10)
        cloud.top=random.randint(height-30, height-5)
        cloud.velocity=(random.uniform(-1.0, -0.5),0)
        self.all_sprites_list.append(cloud)

class instuctionsView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LAWN_GREEN)
    
    def on_draw(self):
        self.clear()
        lineHeight = 25 #height between each line
        start_x = 0
        start_y = height - (lineHeight*2.5)
        arcade.draw_text("Welcome to the PGA!", start_x, start_y, font_size=24, width = width, bold = True, align="center")
        start_y -= lineHeight
        arcade.draw_text("Your golf career has taken off! You've qualified to be on the PGA tour and recieved your pro card! To prep for your next big comp, review below, and press enter when you are ready to play!", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= (lineHeight*3)
        arcade.draw_text("Controls:", start_x, start_y, font_size=12, width = width, bold = True, align="center")
        start_y -= lineHeight
        arcade.draw_text("Q = Quit     P = Pause", start_x, start_y, font_size=12, width = width, align="center")
        start_y -= lineHeight
        arcade.draw_text("D = Driver   H = Hybrid   W = 4-wood   U = Putter", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= lineHeight      
        arcade.draw_text("4 = 4-iron   5 = 5-iron   6 = 6-iron   7 = 7-iron   8 = 8-iron   9 = 9-iron", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= lineHeight        
        arcade.draw_text("P = Pitching wedge   G = Gap wedge   S = Sand wedge   L = Lob wedge", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= lineHeight        
        arcade.draw_text("up arrow = up   down arrow = down   -> = right   <- = left", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= lineHeight        
        arcade.draw_text("space bar = swing (hold down to increase swing power)", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= lineHeight        
        arcade.draw_text("B = Drink a cold one", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            holes = holeView() #will loop through 18 holes
            self.window.show_view(holes)
            arcade.run()

class endView(arcade.View):
    def __init__(self, total_score):
        super().__init__()
        self.medal = arcade.load_texture("img/gold_medal.png")
        self.total_score = total_score
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LAWN_GREEN)
    
    def on_draw(self):
        self.clear()
        lineHeight = 25 #height between each line
        start_x = 0
        start_y = height - (lineHeight*2.5)
        arcade.draw_text("Total score: {}".format(self.total_score), start_x, start_y, font_size=24, width = width, bold = True, align="center")
        start_y -= lineHeight
        arcade.draw_text("Great job!!! You are the best golfer and the hottest golfer and my favorite golfer! <3 And your golf career is taking off! Go James!", start_x, start_y, font_size=12, width = width, align="center", multiline=True)
        start_y -= (lineHeight*3)
        self.medal.draw_sized(width/2, start_y, 100, 100)

class flying_sprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.right < 0:
            self.remove_from_sprite_lists

#DEF MAIN
def PGA():
    #Pro Golfer description:
    #James is a pro golfer and he wants to play 18 holes!
    window = arcade.Window(width, height, title)
    instructions_view = instuctionsView()
    window.show_view(instructions_view)
    arcade.run()

#RUN MAIN
PGA()