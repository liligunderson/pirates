from game import location 
#There is some pretence that the gam might not be played over the term
#So we use a custome function announce to print things instead of print
from game.display import announce
import random
import game.config as config
import game.items as items
from game.events import * 
import game.combat as combat


#Demo island inherits from location (Demo island is a location)
class DemoIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        # object oriented handling. Super() refers to the parent class
        # (Location in this case)
        # So this runs the initializer of Location
        self.name = "island"
        self.symbol = 'I' #Symbol for map
        self.visitable = True #Mark the island as a place the pirates can 'go ashore'
        self.locations = {} #Dictionary of sub-locations on the island 
        self.locations["black sand beach"] = Beach(self)
        self.locations["tropical forest"] = Tropical_Forest(self)
        self.locations["mushroom field"] = Mushroom_Field(self)
        self.locations["caves"] = Caves(self)
        #Where do the pirates start?
        self.starting_location = self.locations["black sand beach"]

    def enter(self, ship):
        #What to do when the ship visits this loc on the map
        announce("arrived at an island")

    #Boilerplate code for starting a visit.
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
#Sub-locations (Beach and Trees)
class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "black sand beach"
        #the verbs dict was set up by the super() init
        #"go north" has handling that causes sublocations to 
        #just get the direction
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

        #add coconuts for food
        self.verbs["take"] = self
        self.item_on_beach = Coconut()

    def enter(self):
        announce ("You arrive at the beach. You notice the sand is black. Your ship is at anchor in a small bay to the south")
    #one of the core functions. Contains handling for everything that the player can do here
    #more complex actions should have dedicated functions to handle them.
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            #Text will be printed by "enter" in Tropical_Forest()
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["mushroom field"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caves"]

class Coconut(items.Item):
    def __init__(self):
            super().__init__("coconut", 2)
            self.restore_health = 3
            self.verb = "consume"

class Tropical_Forest(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "tropical forest"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self

        #Add some treasure!
        self.verbs["take"] = self
        self.item_in_tropical_tree = Saber()
        self.item_in_clothes = items.Flintlock()
        self.events_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        description = "You walk into a small tropical forest on the island."
        if self.item_in_tropical_tree != None:
            description = description + " You see a " + self.item_in_tropical_tree.name + " stuck in a tropical tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor"
        announce(description)
    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["north", "south", "east", "west"]):
            config.the_player.next_loc = self.main_location.locations["black sand beach"]
        if(verb == "take"):
            #The player will type something like "take saber" or "take all"
            if(self.item_in_tropical_tree == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #they just typed "take"
            elif( len(cmd_list) < 2):
                announce("Take what?")
            else: 
                at_least_one = False
                [self.item_in_clothes]
                i = self.item_in_tree
                if i != None and (i.name == cmd_list[1] or  cmd_list [1] == "all"):
                    announce("You take the "+i.name)
                    config.the_player.add_to_inventory(i)
                    self.item_in_trees = None
                    #this command uses time
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_in_clothes
                if i != None and (i.name == cmd_list[1] or  cmd_list [1] == "all"):
                    announce("You take the "+i.name + " out of the pile of clothes.")
                    config.the_player.add_to_inventory(i)
                    self.item_in_clothes = None
                    #this command uses time
                    config.the_player.go = True
                    at_least_one = True
            if not at_least_one:
                #perhaps the player types "take Apple"
                announce("you don't see one of those around.")
        
        if(verb == "pick"):
            #player will have pick something such as pick colorful mushroom or pick glowing mushroom
            i = self.item_in_mfield
            if i != None and (i.name == cmd_list[1] or cmd_list [1] == "all"):
                announce("You picked a "+i.name + "from the field of colorful mushrooms.")
                config.the_player.add_to_inventory(i)
                self.item_in_mfield

class Mushroom_Field(location.SubLocation):

    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "mushroom field"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        
        #adding mushrooms to collect 
        self.verbs["pick"] = self
        self.item_in_mfield = Mushroom()
    
    #def process_verb(self, verb, cmd_list, nouns):
        #if(verb in ["north", "south", "east", "west"]):
            #config.the_player.next_loc = self.main_location.locations["black sand beach"]
        #if(verb == "investigate"):
            #The player will type something like "take saber" or "take all"

            #if(self.item_inmfield == None and self.item_in_clothes == None):
                #announce("You don't see anything to take.")

    def enter (self):
        description = "You walk into a field full of colorful mushrooms and some seem to glow."
        if self.item_in_mfield != None:
            description = description + " You see a remarkably colorful " + self.item_in_mfield.name + " in the mushroom field."
        announce(description)

class Mushroom(items.Item):
    def __init__(self):
        super().__init__("mushroom", 3)
        self.restore_health = (10)
        self.verb = "consume"

class Caves(location.SubLocation):
     
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "caves"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self
        self.verbs["mine"] = self

        #adding gems in the caves
        self.verbs["pick"] = self
        self.item_in_cave = Amethyst()
        
    def process_verb(self, verb, cmd_list, nouns):
        print (verb)
        if(verb == "investigate"):
            announce(" You see a beautiful purple " + self.item_in_cave.name + " on the cave wall. You can mine it.")

        if (verb == "mine"):
            announce(" You have mined the " + self.item_in_cave.name)
            config.the_player.add_to_inventory(i)

            if(self.item_in_cave == None):
                announce("You don't see anything to mine.")

    def enter (self):
        description = "You enter one of the many caves in this region. Some areas on the wall are sparkling. You can investigate."
        announce(description)

class Amethyst(items.Item):
     def __init__(self):
        super().__init__("amethyst", 50)
        self.verb = "mine"

class Saber(items.Item):
    def __init__(self):
        super().__init__("saber", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class Macaque(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))

#puzzle for the pirates 
def find_treasure(treasure_map):
    rows = len(treasure_map)
    cols = len(treasure_map[0])

    for i in range(rows):
        for j in range(cols):
            if treasure_map[i][j] == 'C':
                return (i, j)
treasure_map = [
    ['S', 'S', 'S', 'S', 'S'],
    ['S', 'L', 'S', 'L', 'S'],
    ['S', 'L', 'S', 'L', 'S'],
    ['S', 'L', 'S', 'L', 'S'],
    ['S', 'S', 'S', 'S', 'C'],
]

result = find_treasure(treasure_map)
print(result)

class ForestClearing(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Forest Clearing"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.item_in_stump = SwordInStump()
        self.ghost_soldier = GhostSoldier()

    def enter(self):
        description = "You find yourself in a peaceful forest clearing. In the center, there is a sword stuck in a tree stump."
        if self.ghost_soldier:
            description += " A ghostly soldier stands guard over the sword."
        elif self.item_in_stump:
            description += f" You notice a {self.item_in_stump.name} in the tree stump."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb in ["north", "south", "east", "west"]:
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
        elif verb == "inspect":
            if self.item_in_stump:
                if self.ghost_soldier:
                    announce("As you approach the sword, a ghostly soldier appears and attacks you!")
                    combat.start_combat(config.the_player, self.ghost_soldier)
                    if config.the_player.is_alive():
                        announce("With the ghost defeated, the sword is now free to be pulled.")
                        self.item_in_stump = Excalibur()
                    else:
                        announce("You have been defeated by the ghost. Game over.")
                        config.the_player.game_over = True
                else:
                    announce("You attempt to pull the sword from the tree stump.")
                    announce("As you successfully pull it free, the sword changes and reveals itself to be the legendary Excalibur!")
                    self.item_in_stump = Excalibur()

class Excalibur(items.Item):
    def __init__(self):
        super().__init__("Excalibur", 20)
        self.verb = "wield"
        self.damage = (15, 30)  # Adjust the damage based on your game's mechanics
        self.skill = "swords"

class SwordInStump(items.Item):
    def __init__(self):
        super().__init__("sword in stump", 100)
        self.verb = "pull"

class GhostSoldier(combat.Monster):
    def __init__(self):
        attacks = {"slash": ["slashes", random.randrange(10, 21), (5, 15)]}
        super().__init__("Ghost Soldier", random.randrange(20, 31), attacks, 200)
