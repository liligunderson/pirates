from game import location 
#There is some pretence that the gam might not be played over the term
#So we use a custome function announce to print things instead of print
from game.display import announce
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
        self.locations["beach"] = Beach(self)
        self.locations["trees"] = Trees(self)
        #Where do the pirates start?
        self.starting_location = self.locations["beach"]

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
        self.name = "beach"
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

    def enter(self):
        announce ("You arrive at the beach. Your ship is at anchor in a small bay to the south")
    #one of the core functions. Contains handling for everything that the player can do here
    #more complex actions should have dedicated functions to handle them.
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
            #Text will be printed by "enter" in Trees()
        if (verb == "east" or verb == "west"):
            announce("You walk all the way around the island on the beach. It's not very interesting.")

class Trees(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "trees"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self

        #Add some treasure!
        self.verbs["take"] = self
        self.item_in_tree = Saber()
        self.item_in_clothes = items.Flintlock()
        self.events_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        description = "You walk into a the small forest on the island."
        if self.item_in__tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in__clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor"
        announce(description)
    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["north", "south", "east", "west"]):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if(verb == "take"):
            #The player will type something like "take saber" or "take all"
            if(self.item_in_tree == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #they just typed "take"
            elif( len(cmd_list) < 2):
                announce("Take what?")
            else: 
                at_least_one = False
                [, self.item_in_clothes]
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