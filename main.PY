import pygame
import os
import json
import random

DEBUG = False
BLACK=(0,0,0)
WIDTH = 1260
WHITE = (255,255,255)
RED = (225,0,0)
GREEN = (0,255,0)
HEIGHT = 720
FPS = 60
TILE_SIZE = 18

pygame.init()#遊戲初始化
pygame.mixer.init()#初始化音效

screen = pygame.display.set_mode((WIDTH,HEIGHT))#視窗大小 左上角(0,0)右下(WIDTH,HEIGHT)
clock = pygame.time.Clock()#管理遊戲的時間和幀率
pygame.display.set_caption("自主學習")#視窗名稱


#圖片
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

keyboard_img = pygame.image.load(os.path.join("img","keyboard.png")).convert()
keyboard_img = pygame.transform.scale(keyboard_img, (WIDTH,HEIGHT))

ghost_img = pygame.image.load(os.path.join("img","ghost.png")).convert()
boss_img = pygame.image.load(os.path.join("img","boss.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
boss_bullet_img = pygame.image.load(os.path.join("img","boss_bullet.png")).convert()

game_imgs = []#列表
for i in range(1,5):
    img = pygame.image.load(os.path.join("img",f"game{i}.png")).convert()#將載入的圖片加入 img
    img.set_colorkey(BLACK)#一起去背景圖案
    game_imgs.append(img)#把img加入player_imgs要用時打player_imgs[i]

lock_game_imgs = []
for i in range(1,5):
    img = pygame.image.load(os.path.join("img",f"lock_game{i}.png")).convert()
    img.set_colorkey(BLACK)
    lock_game_imgs.append(img)

clear_game_imgs = []
for i in range(1,5):
    img = pygame.image.load(os.path.join("img",f"clear_game{i}.png")).convert()
    img.set_colorkey(BLACK)
    clear_game_imgs.append(img)

end_imgs = []
for i in range(2):
    img = pygame.image.load(os.path.join("img",f"end{i}.png")).convert()
    img = pygame.transform.scale(img, (47,66))
    img.set_colorkey(BLACK)
    end_imgs.append(img)

coin_img = pygame.image.load(os.path.join("img","coin.png")).convert()
heart_img = pygame.image.load(os.path.join("img","heart.png")).convert()
spikes_img = pygame.image.load(os.path.join("img","spikes.png")).convert()
lava_img = pygame.image.load(os.path.join("img","lava.png")).convert()

player_imgs = []
for i in range(4):
    img = pygame.image.load(os.path.join("img",f"player{i}.png")).convert()
    img = pygame.transform.scale(img, (30,40))
    img.set_colorkey(BLACK)
    player_imgs.append(img)

fail_img = pygame.image.load(os.path.join("img","fail.png")).convert()
fail_img = pygame.transform.scale(fail_img, (400,500))
fail_img.set_colorkey(BLACK)

success_img = pygame.image.load(os.path.join("img","success.png")).convert()
success_img = pygame.transform.scale(success_img, (400,500))
success_img.set_colorkey(BLACK)

return_img = pygame.image.load(os.path.join("img","return.png")).convert()
return_img.set_colorkey(BLACK)

player_mini_img = pygame.transform.scale(player_imgs[0], (25,19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)

return1_img = pygame.image.load(os.path.join("img","return1.png")).convert()
return1_img.set_colorkey(BLACK)

go_back_img = pygame.image.load(os.path.join("img","go_back.png")).convert()
go_back_img.set_colorkey(BLACK)

data_cover_img = pygame.image.load(os.path.join("img","data_cover.png")).convert()
data_cover_img.set_colorkey(BLACK)

font_name = os.path.join("font.ttf") #字體
                    
def draw_text(surf, text, size, x, y, color):  #寫字
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0: #最低0血
        hp = 0
    BAR_LENGHT = 60 #血條長度
    BAR_HEIGHT = 10
    fill = (hp/60)*BAR_LENGHT #血量換算
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT) #畫長方形
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2) #2像素邊框

def draw_boss_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGHT = 144
    BAR_HEIGHT = 10
    fill = (hp/144)*BAR_LENGHT 
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT) 
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

def draw_need_coin(level):
    global need_coin, now_coin
    i = f"map{level}" #帶入現在關卡
    if i in map_data: #如果有在關卡資訊裡
        data = map_data[i] #帶入關卡資訊
        need_coin = int(data['need_coin'])  # 轉成 int 才能比較/計算
        draw_text(screen, f"{now_coin}/{need_coin}金幣", 64, 250, 635, BLACK) #寫出來

def load_map(map):    
    tilesets.clear() #清空所有資料
    object_layer.clear()  
    layers.clear()
    with open(f'map/map{map}.json', "r", encoding="utf-8") as f:#打開地圖
        map_data = json.load(f) #把打開地圖丟到變數
        for i in map_data["layers"]:
            if i["type"] == "tilelayer": #存圖塊層
                layers.append(i)
            if i["type"] == "objectgroup": #存物件層
                object_layer.append(i)
        for i in map_data["tilesets"]: #帶入map{map}.json的tilesets 用到的圖塊集 ex:aa.json
            image = pygame.image.load(f"map/{i["image"]}")  #載入圖塊集圖片
            tilesets.append({                   
                "image": image,
                "firstgid": i["firstgid"],  # 該tileset 的起始 GID
                "columns": i["columns"],
                "spacing" : i.get("spacing", 0), #預設 0 抓map1.json的tilesets的spacing
                })
   
def get_tileset(gid): 
    for tileset in reversed(tilesets):  # reversed逆序搜尋，找到最接近的firstgid，從大的開始
        if gid >= tileset["firstgid"]:#輸入的gid大等於圖塊集編號 ex:38只大於第1張圖塊集 傳第一張圖塊集aa
            return tileset #回傳找到的map中圖塊集 ex:aa.json

def draw_map(): 
    floors.clear()
    for i in layers: #帶入layers列表
        width, height = i["width"], i["height"]#帶入地圖寬高
        tiles = i["data"]#存整篇data
        for y in range(height):
            for x in range(width):
                gid = tiles[y * width + x]#只引響函式內 從0開始  ex:(1, 4)變成1*34+4=第38個
                if gid > 0:  # 0 代表空白 如果有圖案
                    tileset = get_tileset(gid)#抓圖塊 ex:gid傳第38個 回傳找到的map中圖塊集 ex:aa.json
                    if tileset: #ex:aa.json
                        id = gid - tileset["firstgid"] #tileset["firstgid"]在map中 id從0開始 gid>0 frist從1開始                                          
                        spacing = tileset.get("spacing", 0) #使用圖塊集中的spacing
                        tile_x = (id % tileset["columns"]) * (TILE_SIZE + spacing)#取餘數 表橫排第幾個 
                        tile_y = (id // tileset["columns"]) * (TILE_SIZE + spacing)#//除法取整數 表直排第幾個
                        tile_rect = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
                        if i['name'] == 'floor': 
                            floor_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE) #框起來後面用碰撞
                            floors.append(floor_rect)                        
                        screen.blit(tileset["image"], (x * 18,  y * 18), tile_rect)

def after_choose_game(): #選遊戲後
    global choose_game, start_game, now_coin, have_boss
    choose_game = False
    start_game = True
    load_map(now_level)
    Coin.join() #重新加載地圖資訊
    Ghost.join()
    End.join()
    Lava.join()
    Spikes.join()
    Heart.join()
    if map_data[f"map{now_level}"]["boss"] == "True": #偵測關卡是否有boss
        have_boss = True
    else:
        have_boss = False

    if have_boss:
        Boss.join()

    all_sprite.add(player)
    now_coin = 0

def return_game():
    all_sprite.empty() #清空資訊
    ghosts.empty()
    spikess.empty()
    lavas.empty()
    boss_bullets.empty()
    bosss.empty()
    bullets.empty()
    player.rect.centerx = WIDTH / 6  #玩家定位
    player.rect.bottom = HEIGHT - 90
    player.health = 60

def load_map_data(): #加載關卡資訊
    global map_data
    with open('map_data/map_data.json', "r", encoding="utf-8") as f:
        map_data = json.load(f)

class Player(pygame.sprite.Sprite):  #定義一個遊戲中的「玩家角色」
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_imgs[0]#設定圖片
        self.rect = self.image.get_rect() #定位框起來
        self.rect.centerx = WIDTH/6 #位置位置
        self.rect.bottom = HEIGHT - 90
        self.width = self.image.get_width() #得到寬高
        self.height = self.image.get_height()
        self.now_img = 0#現在的朝向
        self.on_ground = False #是否在地上
        self.is_shooting = False #是否正在射擊
        self.last_shot_time = 0 #最後射擊的時間
        self.vel_y = 0  # 跳躍初速度（負數代表向上）
        self.gravity = 1
        self.jumping = False #是否在跳
        self.start_jump = None #開始跳的時間
        self.holding = False #是否在長按跳
        self.health = 60 #血條
        self.last_hurt_time = 0 #上次扣血時間
        self.dead = False
        self.won = False
    
    def update(self):  
        dx = 0 #水平垂直速度改變 重置
        dy = 0                
        #pygame.draw.rect(screen, RED, [self.rect.x, self.rect.y, 30,40]) #碰撞
        key_pressed = pygame.key.get_pressed()#回傳一個布林值的列表對到鍵盤按鍵

        if key_pressed[pygame.K_d]:
            dx += 3.9 #水平速度增加
            self.now_img = 0  #看右
            if not self.is_shooting:  #若向右走沒射擊就用向右看圖案
                self.image = player_imgs[0]
        elif key_pressed[pygame.K_a]:
            dx -= 3.9
            self.now_img = 1 #看左
            if not self.is_shooting:
                self.image = player_imgs[1]
                        
        if self.rect.right > WIDTH: #走到牆壁停
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if key_pressed[pygame.K_SPACE] and self.on_ground and self.start_jump is None and not self.holding: #當按跳且在地上且還沒開始跳且沒在長按
            self.holding = True #開始長按
            self.start_jump = pygame.time.get_ticks() #設定開始長按時間

        if self.start_jump is not None:  #當設定開始長按時間
            hold_time = pygame.time.get_ticks() - self.start_jump #計算長按時間
        
        if self.holding and not self.jumping and self.start_jump is not None: #當在長按且還沒起跳且已經設定開始長按時間            
            if hold_time > 90 : #要是長按超過180毫秒
                self.vel_y = -16  #長跳            
                self.holding = False #沒在按
                self.jumping = True #正在跳
                self.on_ground = False #不在地上
                self.start_jump = None #重置起跳時間
                
            elif not key_pressed[pygame.K_SPACE]: #在180毫秒內放開
                self.vel_y = -13 #短跳               
                self.holding = False
                self.jumping = True
                self.on_ground = False
                self.start_jump = None
        
        if self.vel_y > 0:  #只要下落就不在地上
            self.on_ground = False
            
        self.vel_y += self.gravity#-17或-11往上加重力加速度1到零不動變正往下
        
        dy += self.vel_y #位置移動
        
        if self.is_shooting and pygame.time.get_ticks() - self.last_shot_time > 200: #當正在射擊且距離上次射擊已經過了0.2s
            self.image = player_imgs[self.now_img] #變回現在朝向的圖案
            self.is_shooting = False #沒在射擊
        
        for i in floors:
            if i.colliderect(self.rect.move(dx, 0)):  # 發生水平碰撞                
                dx = 0 

            elif i.colliderect(self.rect.move(0, dy)):  # 發生垂直碰撞                
                if self.vel_y < 0:  
                    dy = i.bottom - self.rect.top
                    self.vel_y = 0

                elif self.vel_y >= 0:  
                    dy = i.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumping = False
                    
        self.rect.x += dx #更新位置
        self.rect.y += dy
                            
    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot_time > 400: #距離上次射擊已經過了0.2s
            bullet = Bullet(self.rect.centerx, self.rect.centery - 5, self.now_img) #傳入Bullet函數的x和y和方向
            all_sprite.add(bullet)
            bullets.add(bullet)

            if self.now_img == 0: #若朝右
                self.image = player_imgs[2] #朝右射擊圖案
            elif self.now_img == 1:
                self.image = player_imgs[3]
            
            self.is_shooting = True #變正在射擊
            self.last_shot_time = pygame.time.get_ticks() #上次射擊時間變現在

class Ghost(pygame.sprite.Sprite):  #定義一個遊戲中的「敵人角色」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ghost_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 2
        self.health = 60

    def join():
        for i in object_layer:  #在此地圖的物件層找到ghost
            for j in i["objects"]: 
                 if j["name"] == "ghost":
                    x = j["x"] 
                    y = j["y"]
                    width = j["width"]
                    height = j["height"]
                    ghost = Ghost(x, y, width, height) #資料帶進去
                    all_sprite.add(ghost) #加入群組
                    ghosts.add(ghost)
                      
    def update(self):  
        self.rect.x -= self.speedx
        for i in object_layer:  #在此地圖的物件層找到ghost
            for j in i["objects"]: 
                if j["name"] == "ghost":
                    if self.rect.x == j["x"] and self.rect.y == j["y"]:
                        self.speedx *= -1

                if j["name"] == "ghost_turn":
                    if self.rect.x == j["x"] and self.rect.y == j["y"]:
                        self.speedx *= -1
        
        if self.health < 60: #受到傷害顯示血條
            draw_health(screen, self.health, self.rect.centerx -30, self.rect.top -15)

        if self.health <= 0:
            self.kill()
                               
class Bullet(pygame.sprite.Sprite):  #定義一個遊戲中的「子彈」
    def __init__(self, x, y, direction):#傳入Bullet函數的x和y和方向
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.rect.centerx = x
        self.rect.centery = y + 5
        self.speedx = 10 if direction == 0 else -10  # 根據方向決定速度
    
    def update(self):
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0: #若超出螢幕刪除
            self.kill()
            
        for i in floors:
            if i.colliderect(self.rect):  # 發生碰撞     
                self.kill()

class Coin(pygame.sprite.Sprite):  #定義一個遊戲中的「錢錢」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self) #設定圖片
        self.image = pygame.transform.scale(coin_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位框起來
        self.rect.x = x
        self.rect.y = y

    def join():
        for i in object_layer:
            for j in i["objects"]:
                if j["name"] == "coin":
                    x = j["x"]
                    y = j["y"]
                    width = j["width"]
                    height = j["height"]
                    coin = Coin(x, y, width, height)
                    all_sprite.add(coin)
    
    def join_boss_coin():
        for i in object_layer:
            for j in i["objects"]:
                if j["name"] == "boss_coin":
                    x = j["x"]
                    y = j["y"]
                    width = j["width"]
                    height = j["height"]
                    boss_coin = Coin(x, y, width, height)
                    all_sprite.add(boss_coin)

    def update(self):
        global now_coin
        if self.rect.colliderect(player.rect):  # 發生碰撞
            self.kill()
            now_coin += 1

class Button(pygame.sprite.Sprite): #定義一個遊戲中的「按鈕」
    def __init__(self, x, y, image, lock_image, level, bottom_type,size, clear_img):
        self.size = size
        self.type = bottom_type #按鈕功能
        self.lock_image = lock_image #鎖住的圖
        self.clear_img = clear_img #過關的圖
        self.unlock_img = image
        self.unlock_img = pygame.transform.scale(image, size)
        self.image = image
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.clicked = False #是否被點
        self.level = level #關卡

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()#追蹤鼠標
        
        if self.lock_image != None: #如果是關卡按鈕
            self.lock_image = pygame.transform.scale(self.lock_image, self.size)
        
        if self.clear_img != None:
            self.clear_img = pygame.transform.scale(self.clear_img, self.size)

        if self.type == "game": #如果是關卡按鈕
            map_key = f"map{self.level}"
            if map_key in map_data:
                map_info = map_data[map_key]

            if map_info["lock"] == "True":  #如果鎖住
                self.image = self.lock_image #鎖住圖
            elif map_info["clear"] == "True":
                self.image = self.clear_img
            else:
                self.image = self.unlock_img
        # 偵測是否點擊按鈕

        if self.rect.collidepoint(pos) and not self.clicked: #如果碰到鼠標且沒再按
            if pygame.mouse.get_pressed()[0] == 1: #按左鍵
                    if self.type == "game": #是關卡
                        if map_info["lock"] == "False":
                            self.clicked = True
                            action = True
                        else:
                            hint.show("請解鎖上一關")

                    elif self.type == "funtion":
                        self.clicked = True
                        action = True

        if pygame.mouse.get_pressed()[0] == 0: #沒按左鍵
            self.clicked = False

        surface.blit(self.image, self.rect.topleft) #畫出來
        return action 
      
class End(pygame.sprite.Sprite):  #定義一個遊戲中的「終點」
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def join():
        for i in object_layer:
            for j in i["objects"]:
                if j["name"] == "end":
                    x = j["x"]
                    y = j["y"]
                    end = End(x, y, end_imgs[1])
                    all_sprite.add(end)
    
    def update(self):
        global start_game, now_coin
        if now_coin == need_coin and now_coin != 0: #如果金幣足夠
            self.image = end_imgs[0] #換圖

        if now_coin == need_coin and self.rect.colliderect(player.rect):  #如果金幣足夠 玩家碰到
            if now_level < int(map_data["all_level"]): #不是最後一關
                open_level = int(now_level) + 1 #下一關
                map_key = f"map{open_level}" 
                if map_key in map_data:
                    map_data[map_key]["lock"] = "False" #開啟下一關
                    with open('map/map_data.json', 'w', encoding='utf-8') as f:
                        json.dump(map_data, f, ensure_ascii=False, indent=4)
            player.won = True #過關
                       
class Spikes(pygame.sprite.Sprite):  #定義一個遊戲中的「尖刺」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self) #設定圖片
        self.image = pygame.transform.scale(spikes_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位框起來
        self.rect.x = x
        self.rect.y = y

    def join():
        for i in object_layer:
            if i["name"] == "object":
                for j in i["objects"]:
                    if j["name"] == "spikes":
                        x = j["x"]
                        y = j["y"]
                        width = j["width"]
                        height = j["height"]
                        spikes = Spikes(x, y, width, height)
                        all_sprite.add(spikes)
                        spikess.add(spikes)

class Lava(pygame.sprite.Sprite):  #定義一個遊戲中的「岩漿」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self) #設定圖片
        self.image = pygame.transform.scale(lava_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位框起來
        self.rect.x = x
        self.rect.y = y

    def join():
        for i in object_layer:
            if i["name"] == "object":
                for j in i["objects"]:
                    if j["name"] == "lava":
                        x = j["x"]
                        y = j["y"]
                        width = j["width"]
                        height = j["height"]
                        lava = Lava(x, y, width, height)
                        all_sprite.add(lava)
                        lavas.add(lava)

class Text:
    def __init__(self, pos, fade_in=30, hold=60):
        self.pos = pos
        self.fade_in = fade_in
        self.hold = hold
        self.alpha = 0 #透明度
        self.text_surf = None
        self.state = "no" #狀態
        self.timer = 0 #計時

    def show(self,text, size=36, fade_out=30): #出現
        self.fade_out = fade_out
        self.font = pygame.font.Font(font_name, size)
        self.text_surf = self.font.render(text, True, BLACK).convert_alpha() # 抗鋸齒 能變透明
        self.state = "fade_in" #漸深
        self.alpha = 0
        self.timer = 0

    def update(self):
        if self.state == "no":
            return
        elif self.state == "fade_in": #若漸深
            self.alpha += 255 / self.fade_in #每幀透明加255/30
            if self.alpha >= 255: #加到底
                self.alpha = 255
                self.state = "hold" #變持續
                self.timer = 0 
        elif self.state == "hold": #若持續
            self.timer += 1 #計時
            if self.timer >= self.hold: #加到60
                self.state = "fade_out" #變漸淺
        elif self.state == "fade_out": #若漸淺
            self.alpha -= 255 / self.fade_out #減255/30
            if self.alpha <= 0: #減到底
                self.alpha = 0
                self.state = "no"

    def draw(self, surface):
        if self.state == "no" or self.text_surf == None: #若無狀態或沒文字
            return
        temp_surf = self.text_surf.copy()
        temp_surf.set_alpha(int(self.alpha)) #改變透明度
        rect = temp_surf.get_rect(center = self.pos) #定位
        surface.blit(temp_surf, rect) #畫

class Boss(pygame.sprite.Sprite):  #定義一個遊戲中的「boss」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = random.choice(["up", "middle", "down"]) #隨機射擊
        self.last_shot_time = 0
        self.health = 144

    def join():
        for i in object_layer: 
            for j in i["objects"]: 
                 if j["name"] == "boss":
                    x = j["x"] 
                    y = j["y"]
                    width = j["width"]
                    height = j["height"]
                    boss = Boss(x, y, width, height) 
                    bosss.add(boss)
                    all_sprite.add(boss)

    def up_shoot(self): #三種射擊
        y = 113
        for i in range(2):     
            bullet = Boss_bullet(850 , y)
            y += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)
        y1 = 185
        for i in range(2):     
            bullet = Boss_bullet(850 , y1)
            y1 += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)
    
    def middle_shoot(self):
        y = 41
        for i in range(2):     
            bullet = Boss_bullet(850 , y)
            y += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)
        y1 = 185
        for i in range(2):     
            bullet = Boss_bullet(850 , y1)
            y1 += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)

    def down_shoot(self):
        y = 41
        for i in range(2):     
            bullet = Boss_bullet(850 , y) 
            y += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)
        y1 = 113
        for i in range(2):     
            bullet = Boss_bullet(850 , y1) 
            y1 += 28
            all_sprite.add(bullet)
            boss_bullets.add(bullet)
    
    def update(self):
        draw_boss_health(screen,self.health, self.rect.centerx - 72, self.rect.top -15)
        if pygame.time.get_ticks() - self.last_shot_time > 2000: #計時2秒
            self.type = random.choice(["up", "middle", "down"]) #隨機選一種
            if self.type == "up":
                self.up_shoot()
            elif self.type == "middle":
                self.middle_shoot()
            elif self.type == "down":
                self.down_shoot()
            self.last_shot_time = pygame.time.get_ticks()

        if self.health <= 0: #死了
            Coin.join_boss_coin() #加載boss的金幣
            self.kill() 

class Boss_bullet(pygame.sprite.Sprite):  #定義一個遊戲中的「boss子彈」
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_bullet_img, (50,21))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.rect.top = y
        self.rect.centerx = x
        self.speedx = -6 
    
    def update(self):
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0: #若超出螢幕刪除
            self.kill()

        for i in floors:
            if i.colliderect(self.rect):  # 發生碰撞     
                self.kill()

class Heart(pygame.sprite.Sprite):  #定義一個遊戲中的「心」
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(heart_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def join():
        for i in object_layer:
            for j in i["objects"]:
                if j["name"] == "heart":
                    x = j["x"]
                    y = j["y"]
                    width = j["width"]
                    height = j["height"]
                    heart = Heart(x, y, width, height)
                    all_sprite.add(heart)
    
    def update(self):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.health = 60 #回血

game_buttons = { #設定關卡按鈕
    "1" : Button(315 , 105, game_imgs[0], lock_game_imgs[0], 1, "game",(150,150), clear_game_imgs[0]),
    "2" : Button(315 , 285, game_imgs[1], lock_game_imgs[1], 2, "game",(150,150), clear_game_imgs[1]),
    "3" : Button(315 , 475, game_imgs[2], lock_game_imgs[2], 3, "game",(150,150), clear_game_imgs[2]),
    "4" : Button(935 , 210, game_imgs[3], lock_game_imgs[3], 4, "game",(300,300), clear_game_imgs[3])
}

funtion_buttons = { #設定功能按鈕
    "go_back": Button(500 , 450, go_back_img, None, None, "funtion",(100,100), None),
    "go_back_1": Button(630 , 450, go_back_img, None, None, "funtion",(100,100), None),
    "return1": Button(1200 , 648, return1_img, None, None, "funtion",(64,64), None),
    "return": Button(760 , 450, return_img, None, None, "funtion",(100,100), None),
    "data_cover": Button(1120 , 80, data_cover_img, None, None, "funtion",(100,100), None)
}

credit = [
    ("感謝遊玩!", 130, 130),
    ("這是我做的第一個遊戲", 40, 130),
    ("從以前開始就想試試看", 40, 130),
    ("所以利用這次自主學習機會試著做做看", 40, 130),
    ("在製作的過程中雖然有遇到很多困難",40, 130),
    ("但在製作過程中有很多人幫助我", 40, 130),
    ("不論是老師，朋友，同學", 40, 130),
    ("都給我了很多想法和心理上的協助", 40, 130),
    ("謝謝大家!", 90, 130),
    ("工作人員名單", 50, 130),
    ("製作人          林鼎弘", 40, 130),
    ("遊戲總監        林鼎弘", 40, 130),
    ("美術總監        林鼎弘", 40, 130),
    ("技術總監        林鼎弘", 40, 130),
    ("首席程式設計師   林鼎弘", 40, 130),
    ("遊戲程式設計師   林鼎弘", 40, 130),
    ("效能優化        林鼎弘", 40, 130),
    ("首席美術        林鼎弘", 40, 130),
    ("角色設計師      林鼎弘", 40, 130),
    ("背景/場景設計師    林鼎弘", 40, 130),
    ("道具美術        林鼎弘", 40, 130),
    ("特效材質美術    林鼎弘", 40, 130),
    ("首席遊戲設計師  林鼎弘", 40, 130),
    ("主遊戲設計師    林鼎弘",40, 130),
    ("戰鬥設計師      林鼎弘", 40, 130),
    ("關卡設計師      林鼎弘", 40, 130),
    ("系統設計師      林鼎弘", 40, 130),
    ("平衡設計師      林鼎弘",40, 130),
    ("測試主管       林鼎弘",40, 130),
    ("測試工程師     林鼎弘", 40, 130),
    ("遊戲測試員     林鼎弘", 40, 130),
    ("客服           林鼎弘", 40, 130),
]

text_surface = []
start_y = HEIGHT
stat_start = False

for i, (line, size, space) in enumerate(credit):
    font = pygame.font.Font(font_name, size)
    text = font.render(line, True, WHITE)
    rect = text.get_rect(center = (WIDTH/2, start_y + i * space))
    text_surface.append((text, rect))

hint = Text((WIDTH/2, HEIGHT/2)) 

all_sprite = pygame.sprite.Group()#all_sprite為管理所有sprite的群組
ghosts = pygame.sprite.Group()
bullets = pygame.sprite.Group()
spikess = pygame.sprite.Group()
lavas = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
bosss = pygame.sprite.Group()
player = Player()#player變數是Player物件
 
running = True
choose_game = False
start_game = False
init_game = True
keyboard = False
now_level = 0
need_coin = 0
now_coin = 0
have_boss = None

tilesets = []#列表
layers = []
object_layer = []
floors = []

while running:#遊戲迴圈 當遊戲開啟

    if not player.dead and not player.won:#贏或死不刷新
        screen.fill(BLACK)#去除上一幀的畫面

    if init_game:
        screen.blit(background_img, (0,0))
        draw_text(screen, '※如果有bug請見諒', 20, WIDTH/2, HEIGHT*6/7, BLACK)
        draw_text(screen, '自主學習', 100, WIDTH/2, HEIGHT/4, BLACK)
        draw_text(screen, '林鼎弘', 40, WIDTH/2, HEIGHT/4 + 140, BLACK)
        draw_text(screen, '按空白鍵繼續', 30, WIDTH/2, HEIGHT*3/4, BLACK)
        for event in pygame.event.get(): #按空白繼續
            if event.type == pygame.KEYUP: #怕繼續偵測到下一幕
                if event.key == pygame.K_SPACE:        
                    keyboard = True
                    init_game = False
    
    elif keyboard:
        screen.blit(keyboard_img, (0,0))
        draw_text(screen, '※當你按資料重置時，你的過關資訊會直接被刪除!!!', 30, WIDTH/2, HEIGHT*8/9, WHITE)
        draw_text(screen, '按空白鍵繼續', 30, WIDTH/2, HEIGHT*3/4, WHITE)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            choose_game = True
            keyboard = False

    elif choose_game:  
        load_map_data()
        if map_data["map4"]["clear"] == "True" and map_data["member_list"] == "False" and not stat_start:
            start_time = pygame.time.get_ticks()
            stat_start = True

        if stat_start == True:
            time = pygame.time.get_ticks() - start_time
            screen.fill((80,80,80))
            allabove_screen = True
            if time >= 300:
                for text, rect in text_surface:
                    rect.y -= 2
                    if rect.bottom > 0:
                        allabove_screen = False
                        screen.blit(text, rect)

                if allabove_screen:
                    if time >= 5000:
                        draw_text(screen, '感謝遊玩!!!', 100, WIDTH/2+20, HEIGHT/2-60, WHITE)
                        draw_text(screen, '按空白鍵繼續', 30,WIDTH/2, HEIGHT*4/5, WHITE)
                        key_pressed = pygame.key.get_pressed()
                        if key_pressed[pygame.K_SPACE]:
                            map_data["member_list"] = "True"
                            with open('map_data/map_data.json', 'w', encoding='utf-8') as f:
                                json.dump(map_data, f, ensure_ascii=False, indent=4)
                            stat_start = False

            if time >= 3000 and not allabove_screen:
                draw_text(screen, '按空白鍵跳過', 28, 1150, 660, WHITE)
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_SPACE]:
                    map_data["member_list"] = "True"
                    with open('map_data/map_data.json', 'w', encoding='utf-8') as f:
                        json.dump(map_data, f, ensure_ascii=False, indent=4)
                    stat_start = False
        
        else:
            screen.blit(background_img, (0,0))
            for j in range(1,int(map_data["all_level"]) + 1):
                if game_buttons[str(j)].draw(screen): #當按了關卡按鈕
                    now_level = j #設定現在關卡
                    after_choose_game()
                        
            if funtion_buttons["data_cover"].draw(screen): #按重置按鈕
                with open('map_data/map_data_cover.json', "r", encoding="utf-8") as f:
                    map_data_cover = json.load(f)
                map_data = map_data_cover
                with open('map_data/map_data.json', 'w', encoding='utf-8') as f:
                    json.dump(map_data, f, ensure_ascii=False, indent=4) #重置關卡資訊
                choose_game = False
                init_game = True #回到最初

    clock.tick(FPS)#限制遊戲的幀率
        
                
    for event in pygame.event.get():#獲取所有當前的事件
        if event.type == pygame.QUIT:#如果按關閉
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:#若是按滑鼠
            if event.button == 3: #若是按右鍵
                player.shoot() #射擊
      
    if start_game: #遊戲開始
         
        #偵測碰撞
        hits = pygame.sprite.spritecollide(player,ghosts,False)
        for hit in hits:
            hurt_time = pygame.time.get_ticks()
            if hurt_time - player.last_hurt_time == 0 or hurt_time - player.last_hurt_time > 2000:
                player.health -= 30
                player.last_hurt_time = pygame.time.get_ticks()
        
        hits = pygame.sprite.groupcollide(ghosts, bullets, False, True)
        for hit in hits:
            hit.health -= 30

        pygame.sprite.groupcollide(boss_bullets, bullets, False, True)

        if have_boss:
            hits = pygame.sprite.groupcollide(bosss, bullets, False, True)
            for hit in hits:
                hit.health -= 8

        hits = pygame.sprite.spritecollide(player,lavas,False)
        for hit in hits:
            player.health -= 60

        hits = pygame.sprite.spritecollide(player, boss_bullets, False)
        for hit in hits:
            hurt_time = pygame.time.get_ticks()
            if hurt_time - player.last_hurt_time == 0 or hurt_time - player.last_hurt_time > 2000:
                player.health -= 30
                player.last_hurt_time = pygame.time.get_ticks()

        hits = pygame.sprite.spritecollide(player,spikess,False)
        for hit in hits:
            hurt_time = pygame.time.get_ticks()
            if hurt_time - player.last_hurt_time == 0 or hurt_time - player.last_hurt_time > 2000:
                player.health -= 10
                player.last_hurt_time = pygame.time.get_ticks()
        
        
        draw_map() #畫地圖        
        all_sprite.update()#群組中物件裡的update函式
        draw_health(screen, player.health, player.rect.centerx -30, player.rect.top -15) #畫玩家血
        draw_text(screen, f"{now_level}", 64, 50, 635, BLACK) #寫現在哪關
        if funtion_buttons["return1"].draw(screen): #中離按鈕
            return_game()
            start_game = False
            choose_game = True #回去選關卡

        draw_need_coin(now_level) #畫金幣數量
        all_sprite.draw(screen) 

        if player.health <= 0: #玩家死
            player.dead = True           

    if player.dead: #玩家死
        screen.blit(fail_img, (WIDTH/2-200, HEIGHT/2-250)) #畫死頁面
        start_game = False #不繼續更新
        if funtion_buttons["go_back"].draw(screen): #畫回去選關卡
            return_game()
            choose_game = True
            player.dead = False
        if funtion_buttons["return"].draw(screen): #畫重來
            return_game()
            after_choose_game() #直接選好關卡
            player.dead = False

    if player.won: #贏
        screen.blit(success_img, (WIDTH/2-200, HEIGHT/2-250))
        start_game = False #不繼續更新
        if funtion_buttons["go_back_1"].draw(screen): #畫回去選關卡
            return_game()
            map_data[f"map{now_level}"]["clear"] = "True" #關卡資料寫通關
            with open('map_data/map_data.json', 'w', encoding='utf-8') as f:
                json.dump(map_data, f, ensure_ascii=False, indent=4)
            choose_game = True
            player.won = False

    
        

    hint.update()#漸出漸入文字更新
    hint.draw(screen) 

    pygame.display.update()
    
pygame.quit()