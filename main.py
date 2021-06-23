import random
import sys
import pygame
from pygame.locals import *

pygame.init()


surface = pygame.display.set_mode((800, 350))
pygame.display.set_caption("Knight")
vec = pygame.math.Vector2
acc = 0.3
fric = -0.1
clock = pygame.time.Clock()


class Background(pygame.sprite.Sprite):
    """背景类，显示背景图片"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Background.png")

    def render(self, x):
        """渲染背景"""
        surface.blit(self.image, (x, 0))


class Ground(pygame.sprite.Sprite):
    """地面类，显示地面"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground .png")
        self.rect = self.image.get_rect(center=(350, 336))
        # 碰撞检测需要 self.rect 350 -268 =82 66
        # self.rect = self.image.get_rect()
        # print(self.rect.y)
        # print(self.rect.x)

        # print(self.rect.top)
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.rect.centerx)
        # print("midbottom:", self.rect.midbottom)
        # print(self.rect.midtop)
        # print(self.rect.bottomleft)

    def render(self):
        """渲染地面"""
        surface.blit(self.image, (-800 * (player.right_flag - player.left_flag) / 2, 270))


class Stone(pygame.sprite.Sprite):
    """障碍物类，（下Stone1，Stone2...同，其实可合并为一个类）"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("stone2.png")
        self.rect = self.image.get_rect(center=(600 + 52, 272 - 52))
        self.pos = vec(600, 271 - 105)

    def render(self):
        """渲染障碍物"""
        surface.blit(self.image, (600, 272 - 105))


class Stone1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("stone.png")
        self.rect = self.image.get_rect(center=(300 + 100, 272 - 41))
        self.pos = vec(300, 271 - 82)

    def render(self):
        surface.blit(self.image, (300, 272 - 82))


class Stone2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("test.jpg")
        self.rect = self.image.get_rect(center=(180 + 31, 272 - 60))
        self.pos = vec(180, 271 - 120)

    def render(self):
        surface.blit(self.image, (180, 272 - 120))


class Stone3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("stone3.png")
        self.rect = self.image.get_rect(center=(200 + 50, 272 - 47))
        self.pos = vec(200, 272 - 94)

    def render(self):
        surface.blit(self.image, (200, 272 - 94))


class Fire(pygame.sprite.Sprite):
    """最后关卡的火焰类，与玩家碰撞时对玩家造成伤害"""
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("stonekill.png")
        self.rect = self.image.get_rect(center=(x + 19, 272 - 37))
        self.cooldown = 1
        self.posx = x

    def render(self):
        """渲染火焰"""
        surface.blit(self.image, (self.posx, 272 - 74))

    def check(self):
        """火焰对玩家player造成伤害"""
        hit = pygame.sprite.spritecollide(self, player_group, False)
        if hit and (self.cooldown == 1):
            self.cooldown = 0
            pygame.time.set_timer(fire_kill, 1500)

            player.hp -= 1


class Player(pygame.sprite.Sprite):
    """玩家类，由玩家操纵"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        self.vx = 0
        self.pos = vec((400, 100))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = 1
        self.run_flag = 0
        self.jump_flag = 0
        self.left_flag = 0
        self.right_flag = 0
        self.attack_flag = 0

        self.attack_num_l = 0
        self.attack_num_r = 0

        self.run_num_r = 0
        self.run_num_l = 0

        self.hp = 10

        self.hp_cooldown = 1

        self.alive = 1

    def render(self, a=0):
        """渲染玩家"""
        if a == 1:
            dead = pygame.image.load("dead.png")
            surface.blit(dead, (self.pos.x, self.pos.y + 15))
        else:
            surface.blit(self.image, (self.pos.x, self.pos.y))

    def move(self):
        """玩家移动"""

        player_run_r = ["Player_Sprite_R.png", "Player_Sprite2_R.png", "Player_Sprite3_R.png", "Player_Sprite4_R.png",
                        "Player_Sprite5_R.png", "Player_Sprite6_R.png", "Player_Sprite_R.png"]
        player_run_l = ["Player_Sprite_L.png", "Player_Sprite2_L.png", "Player_Sprite3_L.png", "Player_Sprite4_L.png",
                        "Player_Sprite5_L.png", "Player_Sprite6_L.png", "Player_Sprite_L.png"]

        if player.right_flag - player.left_flag == 0:
            fric = -0.15
        elif player.right_flag - player.left_flag == 8:
            fric = -0.12
        else:
            fric = -0.1
        self.acc = vec(0, 0.5)
        if abs(self.vel.x) > 0.1:
            self.run_flag = 1
        else:
            self.run_flag = 0
        key = pygame.key.get_pressed()
        if key[K_d]:
            self.acc.x = 0.3
            self.direction = 1
        elif key[K_a]:
            self.acc.x = -0.3
            self.direction = 0

        self.acc.x += self.vel.x * fric
        self.vel += self.acc
        self.pos += self.vel

        if self.pos.x < 0 and (player.right_flag - player.left_flag) == 8:
            self.pos.x = 800

        elif self.pos.x > 800 and stage.dead_enemy >= stage.enemy_num:
            stage.dead_enemy = 0
            stage.next()
            peach_group.empty()
            self.pos.x = 0
            self.right_flag += 1
            self.left_flag -= 1

        elif self.pos.x > 800:
            self.pos.x = 0

        elif self.pos.x < 0 and player.right_flag - player.left_flag == 0:
            self.pos.x = 800

        elif self.pos.x < 0 and stage.dead_enemy < stage.enemy_num:
            self.pos.x = 800
        elif self.pos.x < 0 and player.right_flag - player.left_flag != 0 and not player.right_flag - player.left_flag > 7:
            peach_group.empty()
            self.pos.x = 800
            self.left_flag += 1
            self.right_flag -= 1

        self.rect.topleft = self.pos

        if self.direction == 1 and self.run_flag == 1 and self.jump_flag == 0:
            self.image = pygame.image.load(player_run_r[self.run_num_r])
            self.run_num_r += 1

        elif self.direction == 0 and self.run_flag == 1 and self.jump_flag == 0:
            self.image = pygame.image.load(player_run_l[self.run_num_l])
            self.run_num_l += 1
            # print(self.direction)

        if self.run_num_r > 6:
            self.run_num_r = 0
        if self.run_num_l > 6:
            self.run_num_l = 0
        if self.run_flag == 0 and self.direction == 1 and self.attack_flag == 0:
            self.image = pygame.image.load(player_run_r[0])
        if self.run_flag == 0 and self.direction == 0 and self.attack_flag == 0:
            self.image = pygame.image.load(player_run_l[0])

        # vec传递给rect.任何topleft     都是传递给x,y
        # print(self.rect.x)
        # print(self.rect.y)

    def attack(self):
        """玩家攻击"""

        player_attack_l = ["Player_Sprite_L.png", "Player_Attack_L.png",
                           "Player_Attack2_L.png", "Player_Attack2_L.png",
                           "Player_Attack3_L.png", "Player_Attack3_L.png",
                           "Player_Attack4_L.png", "Player_Attack4_L.png",
                           "Player_Attack5_L.png", "Player_Attack5_L.png",
                           "Player_Sprite_L.png"]
        player_attack_r = ["Player_Sprite_R.png", "Player_Attack_R.png",
                           "Player_Attack2_R.png", "Player_Attack2_R.png",
                           "Player_Attack3_R.png", "Player_Attack3_R.png",
                           "Player_Attack4_R.png", "Player_Attack4_R.png",
                           "Player_Attack5_R.png", "Player_Attack5_R.png",
                           "Player_Sprite_R.png"]
        # print(self.attack_flag)

        if self.direction == 1:
            self.image = pygame.image.load(player_attack_r[self.attack_num_r])
            # surface.blit(self.image,(self.pos.x,self.pos.y))
            self.attack_num_r += 1
            # print(self.image)
        elif self.direction == 0:
            # correct
            if self.attack_num_l == 0:
                self.pos.x -= 15
            if self.attack_num_l == 10:
                self.pos.x += 15

            self.image = pygame.image.load(player_attack_l[self.attack_num_l])
            self.attack_num_l += 1

        # print(self.pos.x)

        if self.attack_num_l > 10:
            self.attack_num_l = 0
            self.attack_flag = 0
        if self.attack_num_r > 10:
            self.attack_num_r = 0
            self.attack_flag = 0

    def gravity1(self):
        """玩家的重力系统"""
        hits = pygame.sprite.spritecollide(player, ground_group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                self.pos.y = lowest.rect.top - 48
                # print("lowest",self.pos.y)
                self.vel.y = 0
                self.jump_flag = 0

    def chech_stone(self):
        """玩家与障碍物的碰撞检测，（下check_stone1...同，其实可以合并为一个）"""
        hits2 = pygame.sprite.spritecollide(player, stone_group, False)
        if hits2:
            self.jump_flag = 0
            if self.pos.y < stone.pos.y + 5:
                self.pos.y = stone.pos.y - 52 + 10
                # print(lowest2.rect.top+1)
                self.vel.y = 0


            elif self.pos.x <= 600:
                self.pos.x = 560
            elif self.pos.x >= 600:
                self.pos.x = 600 + 105 + 10

    def check_stone1(self):
        hits2 = pygame.sprite.spritecollide(player, stone1_group, False)
        if hits2:
            self.jump_flag = 0
            if self.pos.y < stone1.pos.y + 5:
                self.pos.y = stone1.pos.y - 52 + 10
                # print(lowest2.rect.top+1)
                self.vel.y = 0

            elif self.pos.x <= 300:
                self.pos.x = 260
            elif self.pos.x >= 300 + 80:
                self.pos.x = 300 + 210

    def check_stone2(self):
        hits2 = pygame.sprite.spritecollide(player, stone2_group, False)
        if hits2:
            self.jump_flag = 0
            if self.pos.y + 20 < stone2.pos.y:
                self.pos.y = stone2.pos.y - 52 + 10
                # print(lowest2.rect.top+1)
                self.vel.y = 0

            elif self.pos.x <= 180:
                self.pos.x = 135
            elif self.pos.x >= 180 + 60:
                self.pos.x = 180 + 62 + 10

    def check_stone3(self):
        hits2 = pygame.sprite.spritecollide(player, stone3_group, False)
        if hits2:
            self.jump_flag = 0
            if self.pos.y < stone3.pos.y + 5:
                self.pos.y = stone3.pos.y - 52 + 10
                # print(lowest2.rect.top+1)
                self.vel.y = 0


            elif self.pos.x <= 200:
                self.pos.x = 200 - 40
            elif self.pos.x >= 200:
                self.pos.x = 200 + 94 + 10

    def jump(self):
        """玩家跳跃"""
        hits = pygame.sprite.spritecollide(player, ground_group, False)

        if (hits or self.vel.y == 0) and (not self.jump_flag):
            self.jump_flag = 1
            self.vel.y = -12

    def heart(self):
        """玩家的生命条，显示在屏幕左上方"""
        heart_img = ["6.png", '5.png', '4.png', '3.png', '2.png', '1.png', '1.png', '1.png']
        if boss.alive == 0:
            img = pygame.image.load(heart_img[5])
            self.hp = 9999
        else:
            img = pygame.image.load(heart_img[int(self.hp / 2)])

        surface.blit(img, (40, 40))

        if self.hp == 0:
            self.kill()
            self.alive = 0

            # pygame.display.update()

    def hit(self):
        """玩家受伤"""
        if self.hp_cooldown == 1 and self.hp > 0:
            self.hp_cooldown = 0
            pygame.time.set_timer(player_hit_cooldown, 1500)
            self.hp -= 1


class stage_generation(pygame.sprite.Sprite):
    """舞台更替类"""
    def __init__(self):
        super().__init__()
        self.enemy_num = 3
        self.stage_num = 0
        self.enemy_count = 0
        self.dead_enemy = 0

    def next(self, x=0):
        """进入下一舞台时，重新设置舞台敌人数目和敌人刷新间隔"""
        self.enemy_num = int((player.right_flag - player.left_flag) / 2 + 4)
        self.stage_num = int((player.right_flag - player.left_flag) / 2)
        self.enemy_count = x

        pygame.time.set_timer(enemy_generation, 1500 - 100 * self.stage_num)


class Enemy(pygame.sprite.Sprite):
    """普通敌人类"""
    def __init__(self):
        super().__init__()
        self.pos = vec((0, 0))
        self.pos.y = 272 - 60

        self.velx = random.randint(2, 4)

        self.right_flag = random.randint(0, 1)
        if self.right_flag == 1:
            self.pos.x = random.randint(740, 780)
        else:
            self.pos.x = random.randint(10, 50)
        if player.right_flag - player.left_flag == 0 and self.right_flag == 1:
            self.image = pygame.image.load("monster0_R.png")
        if player.right_flag - player.left_flag == 0 and self.right_flag == 0:
            self.image = pygame.image.load("monster0_L.png")
        if player.right_flag - player.left_flag == 2 and self.right_flag == 1:
            self.image = pygame.image.load("monster1_R.png")
        if player.right_flag - player.left_flag == 2 and self.right_flag == 0:
            self.image = pygame.image.load("monster1_L.png")
        if player.right_flag - player.left_flag == 4 and self.right_flag == 1:
            self.image = pygame.image.load("monster2_R.png")
        if player.right_flag - player.left_flag == 4 and self.right_flag == 0:
            self.image = pygame.image.load("monster2_L.png")
        if player.right_flag - player.left_flag == 6 and self.right_flag == 1:
            self.image = pygame.image.load("monster3_R.png")
        if player.right_flag - player.left_flag == 6 and self.right_flag == 0:
            self.image = pygame.image.load("monster3_L.png")
        if player.right_flag - player.left_flag >= 7 and self.right_flag == 1:
            self.image = pygame.image.load("monster4_R.png")
        if player.right_flag - player.left_flag >= 7 and self.right_flag == 0:
            self.image = pygame.image.load("monster4_L.png")

        self.rect = self.image.get_rect()

    def move(self):
        """普通敌人机械化的移动"""
        if self.right_flag == 1:
            self.pos.x += self.velx
        else:

            self.pos.x -= self.velx
        if self.pos.x >= 800:
            self.right_flag = 0
        elif self.pos.x <= 0:
            self.right_flag = 1
        self.rect.topleft = self.pos
        # print(self.rect.y)

    def render(self):
        """渲染敌人，不同舞台选择不同敌人图片"""
        if player.right_flag - player.left_flag == 0 and self.right_flag == 1:
            self.image = pygame.image.load("monster0_R.png")
        if player.right_flag - player.left_flag == 0 and self.right_flag == 0:
            self.image = pygame.image.load("monster0_L.png")
        if player.right_flag - player.left_flag == 2 and self.right_flag == 1:
            self.image = pygame.image.load("monster1_R.png")
        if player.right_flag - player.left_flag == 2 and self.right_flag == 0:
            self.image = pygame.image.load("monster1_L.png")
        if player.right_flag - player.left_flag == 4 and self.right_flag == 1:
            self.image = pygame.image.load("monster2_R.png")
        if player.right_flag - player.left_flag == 4 and self.right_flag == 0:
            self.image = pygame.image.load("monster2_L.png")
        if player.right_flag - player.left_flag == 6 and self.right_flag == 1:
            self.image = pygame.image.load("monster3_R.png")
        if player.right_flag - player.left_flag == 6 and self.right_flag == 0:
            self.image = pygame.image.load("monster3_L.png")
        if player.right_flag - player.left_flag >= 7 and self.right_flag == 1:
            self.image = pygame.image.load("monster4_R.png")
        if player.right_flag - player.left_flag >= 7 and self.right_flag == 0:
            self.image = pygame.image.load("monster4_L.png")
        surface.blit(self.image, (self.pos.x, self.pos.y))

    def check_player(self):
        """敌人与玩家的攻击"""

        hits = pygame.sprite.spritecollide(self, player_group, False)
        if hits and player.attack_flag == 1:
            # print("?????????????????????????/")
            self.kill()
            i = random.randint(1, 10)
            if i <= 8:
                peach = Peach(self.pos.x, self.pos.y + 20)
                peach_group.add(peach)
            stage.dead_enemy += 1
            pygame.display.update()
        elif hits and player.attack_flag == 0:
            player.hit()


class Boss(pygame.sprite.Sprite):
    """boss——最终的敌人类"""
    def __init__(self):
        super().__init__()
        self.pos = vec(0, 0)
        self.image = pygame.image.load("hun1.png")
        self.pos.y = 272 - 70
        self.pos.x = 600
        self.rect = self.image.get_rect()
        self.cooldown = 1
        self.hp = 2  # random.randint(4, 6)
        self.alive = 1
        self.hit_cooldown = 1

    def render(self, x):
        """渲染boss"""
        if x == 1:
            if self.pos.x - player.pos.x > 0:
                self.image = pygame.image.load("hun0.png")
                # print("right")
            if self.pos.x - player.pos.x < 0:
                self.image = pygame.image.load("hun1.png")
                # print("left")
            if self.pos.x - player.pos.x == 0:
                self.image = pygame.image.load("hun1.png")
                # print("zero")
            surface.blit(self.image, (self.pos.x, self.pos.y))
        if x == 0:
            image = pygame.image.load("dead_hun.png")
            surface.blit(image, (self.pos.x, self.pos.y + 40))

    def move(self):
        """boss特殊的移动方法"""
        if self.pos.x < 0:
            self.pos.x = 800
        if self.pos.x > 800:
            self.pos.x = 0

        if 400 > self.pos.x - player.pos.x > 0:
            self.pos.x += random.randint(1, 2) / 2
        if -400 < self.pos.x - player.pos.x < 0:
            self.pos.x -= random.randint(1, 2) / 2
        if 400 < self.pos.x - player.pos.x:
            self.pos.x -= random.randint(1, 2) / 2
        if self.pos.x - player.pos.x < -401:
            self.pos.x += random.randint(1, 2) / 2
        self.rect.topleft = self.pos

    def attack(self):
        """boss攻击，使用了bullet类"""
        if self.cooldown == 1:
            pygame.time.set_timer(bullet_kill, random.randint(2000, 3000))
            self.cooldown = 0
            bullet = Bullet()
            bullet_group.add(bullet)

    def check(self):
        """boss受到攻击"""
        hit = pygame.sprite.spritecollide(self, player_group, False)

        if hit and player.attack_flag == 1 and self.hit_cooldown == 1:
            self.hit_cooldown = 0
            pygame.time.set_timer(boss_hit, 1300)
            self.hp -= 1
            self.pos.x = random.randint(1, 799)
            print("hithithithithtiithi")
            # self.pos.x=random.randint(1,799)
            if self.hp <= 0:
                self.kill()
                self.alive = 0


class Bullet(pygame.sprite.Sprite):
    """boss的攻击——子弹类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = boss.pos.x
        self.rect.y = boss.pos.y + 10
        if boss.pos.x > player.pos.x:
            self.direction = 0
        if boss.pos.x < player.pos.x:
            self.direction = 1

    def render(self):
        """子弹类的渲染"""
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        """子弹类的移动"""
        if self.direction == 1:
            self.rect.x += 7
        if self.direction == 0:
            self.rect.x -= 7
        if self.rect.x < -40:
            self.kill()
        if self.rect.x > 840:
            self.kill()

    def attack(self):
        """子弹类的攻击——与玩家的碰撞检测"""
        hit = pygame.sprite.spritecollide(self, player_group, False)
        if hit:
            player.hp -= 1
            self.kill()


class Peach(pygame.sprite.Sprite):
    """补给品类，可以为玩家加1点hp"""
    def __init__(self, x, y):
        super().__init__()
        i = random.randint(1, 4)
        if i == 1:
            self.image = pygame.image.load("pea.png")
        if i == 2:
            self.image = pygame.image.load("redbull.png")
        if i == 3:
            self.image = pygame.image.load("pheart.png")
        if i == 4:
            self.image = pygame.image.load("mao.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def render(self):
        """在敌人死亡位置渲染补给品"""

        surface.blit(self.image, self.rect)

    def check(self):
        """补给品为玩家回复hp"""
        hit = pygame.sprite.spritecollide(self, player_group, False)
        if hit and player.hp < 10:
            player.hp += 1
            self.kill()


class Begin_end(pygame.sprite.Sprite):
    """开始和结束时的图片显示，增加游戏剧情"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("test.png")
        self.image2 = pygame.image.load("mua1.png")
        self.rect = self.image.get_rect()
        self.flag = 1

    def render(self):
        """渲染带有文字的图片——介绍剧情"""
        # print("0000000000000000000000000000000")
        if self.flag == 1:
            # print("111111111111111")
            surface.blit(self.image, (200, 50))
        if self.flag == 2:
            self.image = pygame.image.load("end2.png")
            surface.blit(self.image, (50, 50))
            surface.blit(self.image2, (450, 0))


begin_end = Begin_end()

fire = Fire(524)
fire1 = Fire(267)

peach_group = pygame.sprite.Group()
fire_kill = pygame.USEREVENT + 3

bullet_kill = pygame.USEREVENT + 4
boss_hit = pygame.USEREVENT + 5

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_generation = pygame.USEREVENT + 2

stage = stage_generation()

ground = Ground()
background = Background()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

stone = Stone()
stone_group = pygame.sprite.Group()
stone_group.add(stone)

stone1 = Stone1()
stone1_group = pygame.sprite.Group()
stone1_group.add(stone1)

stone2 = Stone2()
stone2_group = pygame.sprite.Group()
stone2_group.add(stone2)

stone3 = Stone3()
stone3_group = pygame.sprite.Group()
stone3_group.add(stone3)

stone_group_check = [player.chech_stone(), player.check_stone1(), player.check_stone2(), player.check_stone3()]
stone_grou = [stone.render(), stone1.render(), stone2.render(), stone3.render()]

enemy_group = pygame.sprite.Group()

boss = Boss()

bullet = Bullet()
bullet_group = pygame.sprite.Group()

player_hit_cooldown = pygame.USEREVENT + 1
i = 1

while True:

    key = pygame.key.get_pressed()

    if boss.alive == 0:
        begin_end.flag = 2
        begin_end.render()

    if key[K_RETURN] and player.right_flag == player.left_flag and i == 1:
        i = 0
        begin_end.flag = 0
        stage.next()
    player.gravity1()
    # print(player.jump_flag)
    # print(player.vel.y)
    # player.check_stone1()
    # player.check_stone2()
    # print(stage.enemy_count)
    # print("00000000000000000:", int((player.right_flag - player.left_flag)))

    # print(player_group)
    # player.check_stone3()
    if int((player.right_flag - player.left_flag) / 2) == 0:
        player.chech_stone()
    if int((player.right_flag - player.left_flag) / 2) == 1:
        player.check_stone1()
    if int((player.right_flag - player.left_flag) / 2) == 2:
        player.check_stone2()
    if int((player.right_flag - player.left_flag) / 2) == 3:
        player.check_stone3()
    if int((player.right_flag - player.left_flag) / 2) == 4:
        fire.check()
        fire1.check()
    boss.check()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == player_hit_cooldown:
            player.hp_cooldown = 1
        if event.type == enemy_generation:
            if player.right_flag - player.left_flag == 8:
                if len(enemy_group) == 0 and boss.alive == 1:
                    enemy = Enemy()
                    enemy_group.add(enemy)
                    stage.enemy_count += 1
            elif stage.enemy_count < stage.enemy_num:
                enemy = Enemy()
                enemy_group.add(enemy)
                stage.enemy_count += 1

        if event.type == fire_kill:
            fire.cooldown = 1
            # print('SSSSSSSSSSSSSSSSSsSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        if event.type == bullet_kill:
            boss.cooldown = 1
        if event.type == boss_hit:
            boss.hit_cooldown = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attack_flag == 0:
                    player.attack_flag = 1
                    player.attack()
        if player.alive == 0:
            pygame.quit()

    #

    background.render(0)
    ground.render()

    for i in peach_group:
        i.render()
        i.check()
    # print(int((player.right_flag - player.left_flag) / 2))
    # print(fire.cooldown)
    if int((player.right_flag - player.left_flag) / 2) == 0:
        stone.render()
    elif int((player.right_flag - player.left_flag) / 2) == 1:
        stone1.render()
    elif int((player.right_flag - player.left_flag) / 2) == 2:
        stone2.render()
    elif int((player.right_flag - player.left_flag) / 2) == 3:
        stone3.render()
    elif int((player.right_flag - player.left_flag) / 2) == 4:
        fire.render()
        fire1.render()
    player.heart()

    # print("stage_enemy", stage.enemy_num)
    # print("stage_dead", stage.dead_enemy)
    # print("stage_num", stage.stage_num)

    if player.attack_flag == 1:
        player.attack()
    if player.alive == 1:
        player.move()
    if player.alive == 1:
        player.render()
    else:
        player.render(1)

    for i in enemy_group:
        i.move()
        i.check_player()
        i.render()

    for i in bullet_group:
        i.move()
        i.attack()
        i.render()

    if player.right_flag - player.left_flag > 7:

        if boss.alive == 1:
            boss.move()
            boss.attack()
        boss.render(boss.alive)

    begin_end.render()

    # print(player.attack_flag)
    # print("l:", player.attack_num_l)
    # print("R:", player.attack_num_r)
    pygame.display.update()
    clock.tick(120)
