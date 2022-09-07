'''
turn based
'''

import pygame
import os
import random
import button


pygame.init()

clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont('Times New Roman', 26)

RED = (255,0,0)

GREEN = (0,255,0)


#Window
bottom_panel = 150
WIDTH = 800
HEIGHT = 400 + bottom_panel


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Doms rape cave")


#game variables

current_fighter = 1
total_fighters = 3
action_cooldown= 0
action_waittime = 90
attack = False
potion = False
potion_value = 20
clicked = False


# where i load assets

BACKG = pygame.image.load(os.path.join('Assets','BG.png'))
PANEL = pygame.image.load(os.path.join('Assets', 'panel.png'))
POTION = pygame.image.load(os.path.join('Assets', 'potion.png'))
SWORD = pygame.image.load(os.path.join('Assets', 'sword.png'))

VICTORY = pygame.image.load(os.path.join('Assets', 'victory.png'))
DEFEAT = pygame.image.load(os.path.join('Assets', 'defeat.png'))
RESTART = pygame.image.load(os.path.join('Assets', 'restart.png'))



#draw text

def DrawText(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    WIN.blit(img,(x,y))







#draw function

def DrawBG():

    WIN.blit(BACKG,(0,0))

def DrawPanel():
    #draws the panel asset on at screen
    WIN.blit(PANEL,(0,HEIGHT - bottom_panel))

    #adds text for knight stats
    DrawText(f'{knight.name} HP: {knight.hp}', FONT,RED,100,HEIGHT - bottom_panel + 10)
    for count, i in enumerate(bandit_list): #i = bandit in the list
        DrawText(f'{i.name} HP: {i.hp}', FONT, RED, 550, (HEIGHT - bottom_panel + 10) + count * 60)




#classes

class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0=idle 1=attack 2=hurt 3= dead
        self.update_time = pygame.time.get_ticks()
        #loading idle images
        temp_list = []
        for i in range(8):  #iterates through 8 png for animation
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img) #adds image to image list
        self.animation_list.append(temp_list)

        # loading  attack images
        temp_list = []
        for i in range(8):  # iterates through 8 png for animation
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        #hurt images
        temp_list = []
        for i in range(3):  # iterates through 8 png for animation
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(10):  # iterates through 8 png for animation
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        #adds temp list to master list, creates list of lists, all animations passed through temp list will be added to the master list
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown = 100 #milliseconds
        #handles animation
        #updates image
        self.image = self.animation_list[self.action][self.frame_index]
        # if the current time and update time are greater than 100ms then change to the next image in animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        #if animation is done, loop to first image
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
               self.Idle()


    def Idle(self):

        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()



    def Attack(self,target):
        #damage dealt
        rand = random.randint(-5,5)
        damage = self.strength + rand
        target.hp -=damage
        target.Hurt()
        #check for target death
        if target.hp <1:
            target.hp = 0
            target.alive = False
            target.Death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage) , RED)
        damage_text_group.add(damage_text)

        #set action to +1 = action
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def Hurt(self):
        #hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def Death(self):
        #hurt animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def Reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()





    def Draw(self):
        WIN.blit(self.image, self.rect)



class  HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def Draw(self,hp):
        #update with new health
        self.hp = hp
        #calculate ratio of health got:max_hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(WIN, RED, (self.x,self.y, 150, 20))
        pygame.draw.rect(WIN, GREEN, (self.x, self.y, 150 * ratio, 20))




class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = FONT.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        #float up and then disapear
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill() #removes text




damage_text_group= pygame.sprite.Group()



knight = Fighter(200,260,'Knight',30, 10, 3)
bandit1 = Fighter(550,270,'Bandit', 20, 6,1)
bandit2 = Fighter(700,270,'Bandit', 20, 6,1)


bandit_list =[]
bandit_list.append(bandit1)
bandit_list.append(bandit2)



knight_healthbar = HealthBar(100, HEIGHT - bottom_panel + 40, knight.hp , knight.max_hp)
bandit1_healthbar = HealthBar(550, HEIGHT - bottom_panel + 40, bandit1.hp , bandit1.max_hp)
bandit2_healthbar = HealthBar(550, HEIGHT - bottom_panel + 100, bandit2.hp , bandit2.max_hp)


#potion button

potion_button = button.Button(WIN, 100, HEIGHT - bottom_panel +70, POTION, 64,64)
restart_button = button.Button(WIN, 330,120, RESTART,120,30)

# main game loop
def Main(current_fighter, action_cooldown):

    run = True

    while run:

        clock.tick(FPS)

        DrawBG()

        DrawPanel()
        knight_healthbar.Draw(knight.hp)
        bandit1_healthbar.Draw(bandit1.hp)
        bandit2_healthbar.Draw(bandit2.hp)


        #fighter draw
        knight.update()
        knight.Draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.Draw()

        #draw damage texrt

        damage_text_group.update()
        damage_text_group.draw(WIN)


        #action handling
        #reset action var
        attack = False
        potion = False
        target = None
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos): #if mosue is over one of bandit rectangles
                pygame.mouse.set_visible(False)
                WIN.blit(SWORD, pos)
                if clicked == True and bandit.alive == True:
                    attack = True
                    target = bandit_list[count]

        if potion_button.draw():
            potion = True

        DrawText(str(knight.potions), FONT, RED,150,  HEIGHT - bottom_panel + 70)

        game_over = 0 #0 = player alive, -1 = player dead 1 = all enemy dead
        if game_over == 0:
            #player action
            if knight.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_waittime:
                        #look for action
                        if attack == True and target !=None:
                            knight.Attack(target)
                            current_fighter +=1
                            action_cooldown = 0

                        if potion == True:
                            if knight.potions > 0:
                                #check if potion puts player above max health
                                if knight.max_hp - knight.hp > potion_value:
                                    heal_amount = potion_value
                                else:
                                    heal_amount = knight.max_hp
                                knight.hp =+ heal_amount
                                knight.potions -=1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter =+ 1
                                action_cooldown = 0
            else:
                game_over = - 1




            #enemy action
            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:
                            #check if bandit needs to use potion
                            if (bandit.hp / bandit.max_hp) <0.5 and bandit.potions > 0:
                                if bandit.max_hp - bandit.hp > potion_value:
                                    heal_amount = potion_value
                                else:
                                    heal_amount = bandit.max_hp
                                bandit.hp =+ heal_amount
                                bandit.potions -=1
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter =+ 1
                                action_cooldown = 0


                            else:
                                bandit.Attack(knight)
                                current_fighter +=1
                                action_cooldown = 0
                    else:
                        current_fighter +=1

            #if all fighters havbe gone, reset
            if current_fighter > total_fighters:
                current_fighter = 1

        #check if all bandits are dead
        alive_bandits = 0

        for bandit in bandit_list:
            if bandit.alive == True:
                alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1


        if game_over !=0:
            if game_over ==1:
                WIN.blit(VICTORY, (250,50))
            if game_over == -1:
                WIN.blit(DEFEAT, (275,50))
            if restart_button.draw():
                knight.Reset()
                for bandit in bandit_list:
                    bandit.Reset()
                current_fighter = 1
                action_cooldown = 0
                game_over = 0







        #x in the top right
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False



        pygame.display.update()

    pygame.quit()



if __name__ == "__main__": #only runs main function if you run the file directly
    Main(current_fighter, action_cooldown)