from mobAI import Mob


class Boss(Mob):
    def __init__(self,name,health):
        self.name = name
        self.initHealth = health
        self.health = health
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 300 #random.randint(100,900)
        self.cy = 200 #random.randint(50,450)
        self.type = "idle"
        self.state = "idle"
        self.proj = []

    def gotHit(self,dmg):
        self.health -= dmg
        print(self.health)

    def idle(self):
        self.type = "idle"
    
    
    def attack(self):
        #self.type = "attack"
        #self.atk(self, app, 20)
        pass
    
    def prepATK(self):
        
        pass

class StateMachine(object):
    def setState(self,enemy):
        if enemy.state == "attack":
            enemy.attack()
        elif enemy.state == "run":
            enemy.run()
        elif enemy.state == "prepATK":
            enemy.prepATK()