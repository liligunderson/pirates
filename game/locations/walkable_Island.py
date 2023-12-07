from game import location 
#There is some pretence that the gam might not be played over the term
#So we use a custome function announce to print things instead of print
from game.display import announce
import random
import game.config as config
import game.items as items
from game.events import * 
import game.combat as combat
import game.event as event


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
        self.locations["hot springs"] = Hot_Springs(self)
        #self.locations ["forest clearing"] = Forest_Clearing(self)
        self.locations["caves"] = Caves(self)
        #self.locations["shed"] = Shed(self)
        #Where do the pirates start?
        self.starting_location = self.locations["black sand beach"]
        self.events = []
        self.events.append(KrakenEvent())
        self.kraken_chance = 30

    def enter(self, ship):
        # Checks for Kraken event during arrival
        if random.randrange(100) < self.kraken_chance:
            kraken_event = KrakenEvent()
            kraken_event.process(None)
        else:
            announce("Arrived at an island")

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
        self.items = ['seashell']

        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["pickup"] = self
        self.verbs["investigate"] = self
        self.item_on_beach = Seashell()
        self.event = []
        self.event_chance = 100
        self.events.append(GodOfWisdomEvent())

    def enter(self):
        description = "You arrive at the beach. You notice the sand is black. Your ship is at anchor in a small bay to the south."
        if self.item_on_beach != None:
            description = description + " You see something in the sand. You can investigate"
        announce(description)
    #one of the core functions. Contains handling for everything that the player can do here
    #more complex actions should have dedicated functions to handle them.
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            #Text will be printed by "enter" in Tropical_Forest()
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["mushroom field"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caves"]

        elif verb == "investigate":
            description = "You look around on the black sand beach."
            if self.item_on_beach:
                description += f" You see a {self.item_on_beach.name} sticking out of the sand. You can pickup the seashell."
            announce(description)
        elif verb == "pickup":
        # The player will type something like "take saber" or "take all"
            if self.item_on_beach is None:
                announce("You don't see anything to pickup.")
            elif len(cmd_list) < 2:
                announce("Pickup what?")
            else:
                at_least_one = False

                item_name = cmd_list[1].lower()

                # Check the tropical tree item
                i = self.item_on_beach
                if i and (i.name.lower() == item_name or item_name == "all"):
                    announce(f"You take the {i.name}.")
                    config.the_player.add_to_inventory([i])
                    self.item_on_beach = None
                    # This command uses time
                    config.the_player.go = True
                    at_least_one = True

                if not at_least_one:
                    # Perhaps the player types "take Apple"
                    announce(f"You don't see a {item_name} around.")
            


class GodOfWisdomEvent(event.Event):
    def __init__(self):
        self.name = "Encounter with the God of Wisdom"

    def process(self, world):
        announce("As you investigate the beach, a divine presence surrounds you.")
        announce("The God of Wisdom manifests before you.")
        announce("The God imparts profound knowledge and presents you with a riddle:")

        riddle = "I have cities but no houses, mountains but no trees, and water but no fish. What am I?"
        answer = "map"

        player_answer = input(f"{riddle} ").lower()

        if answer in player_answer:
            announce("The God of Wisdom commends your understanding.")
            announce("In return for your wisdom, the God imparts insightful knowledge to you.")
            results = {"message": "You gain insightful knowledge from the God of Wisdom.", "newevents": []}
        else:
            announce("The God of Wisdom shakes their head at your answer.")
            announce("Seek deeper understanding to unravel the mysteries of the riddle.")
            results = {"message": "The God of Wisdom is not satisfied with your answer.", "newevents": []}

        return results 


class Seashell(items.Item):
    def __init__(self):
        super().__init__("seashell", 2)

class Kraken(combat.Monster):
    def __init__(self):
        attacks = {"tentacle_slap": ["slaps", random.randrange(20, 31), (10, 20)]}
        super().__init__("Kraken", random.randrange(50, 71), attacks, 180 + random.randrange(-20, 21))

class KrakenEvent(event.Event):
    def __init__(self):
        self.name = "The Kraken emerges from the depths!"

    def process(self, world):
        announce("A massive Kraken rises from the sea, blocking your path to the island!")
        announce("Prepare for a fierce battle against the Kraken!")
        combat.Combat([Kraken()]).combat()
        result = {}
        result["message"] = "The Kraken has been defeated, and you can now safely arrive at the island."
        return result


 
class Axe(items.Item):
    def __init__(self):
        super().__init__("axe", 4)




class Snakes(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["bite"] = ["bites", random.randrange(70, 101), (10, 20)]
        # 7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7, 20), attacks, 180 + random.randrange(-20, 21))




class SnakesHoard(event.Event):
    '''
    A combat encounter with a group of snakes.
    When the event is drawn, creates a combat encounter with 2 to 6 snakes,
    kicks control over to the combat code to resolve the fight,
    then adds itself and a simple success message to the result
    '''

    def __init__(self):
        self.name = "tropical snakes attack."

    def process(self, world):
        '''Process the event. Populates a combat with Snakes.'''
        result = {}
        announce("You are attacked by a group of snakes!")

        monsters = []

        min_snakes = 2
        max_snakes = 6
        if random.randrange(2) == 0:
            min_snakes = 1
            max_snakes = 5
            monsters.append(Snakes("Alpha snake"))
            monsters[0].speed = 1.2 * monsters[0].speed
            monsters[0].health = 2 * monsters[0].health

        n_appearing = random.randrange(min_snakes, max_snakes + 1)
        n = 1
        while n <= n_appearing:
            monsters.append(Snakes(f"Snake {n}"))
            n += 1

        
        combat_instance = combat.Combat(monsters)
        
        #loop
        while True:
            announce("What will you do?")
            announce("1. Fight")
            announce("2. Run")

            choice = input("Enter your choice (1 or 2): ")
            if choice == "1":
                while combat_instance.monsters and any(crew.health > 0 for crew in config.the_player.get_pirates()):
                    combat_instance.combat()

                # Check if the combat is over
                if not combat_instance.monsters or all(crew.health <= 0 for crew in config.the_player.get_pirates()):
                    result["message"] = "The snakes are defeated!"  
                    break 
            elif choice == "2":
                result["message"] = "You successfully escaped from the snakes."
                break
            else:
                announce("Invalid choice. Please enter 1 or 2.")

        result["newevents"] = [self]
        return result




class Tropical_Forest(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "tropical forest"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self
        self.ghost_soldier = GhostSoldier() 
        self.verbs["approach"] = self.ghost_soldier

        #Add some treasure!
        self.locations = {}
        self.verbs["take"] = self
        self.item_in_tropical_tree = Axe()

        self.event_chance = 50
        self.events.append(SnakesHoard())
        

    def enter (self):
        description = "You walk into a small tropical forest on the island. You can investigate."
        if self.item_in_tropical_tree != None:
            description = description + " You see an " + self.item_in_tropical_tree.name + " stuck in a tropical tree." 
            announce(description)
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            #Text will be printed by "enter" in Tropical_Forest()
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["mushroom field"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caves"]

            config.the_player.visiting = False
 
        elif verb == "investigate":
            print(verb)
            description = "You carefully investigate your surroundings in the tropical forest."
            if self.item_in_tropical_tree:
                description += f" You see a {self.item_in_tropical_tree.name} stuck in a tropical tree."
            elif self.ghost_soldier and not self.ghost_soldier.riddles_solved:
                description += " In the distance, you notice a ghostly figure standing guard over something. You can approach."

            elif self.ghost_soldier and self.ghost_soldier.riddles_solved:
                description += " The ghost soldier is still in the clearing, but the riddle has already been solved."
            announce(description)
           
            if self.item_in_tropical_tree:
                announce(f"You wonder if you can reach the {self.item_in_tropical_tree.name}.")
        elif verb == "take":
        # The player will type something like "take saber" or "take all"
            if self.item_in_tropical_tree is None:
                announce("You don't see anything to take.")
            elif len(cmd_list) < 2:
                announce("Take what?")
            else:
                at_least_one = False

                item_name = cmd_list[1].lower()

                # Check the tropical tree item
                i = self.item_in_tropical_tree
                if i and (i.name.lower() == item_name or item_name == "all"):
                    announce(f"You take the {i.name}. You can continue to investigate.")
                    config.the_player.add_to_inventory([i])
                    self.item_in_tropical_tree = None
                    # This command uses time
                    config.the_player.go = True
                    at_least_one = True

                if not at_least_one:
                    # Perhaps the player types "take Apple"
                    announce(f"You don't see a {item_name} around.")
            
class Excalibur(items.Item):
    def __init__(self):
        super().__init__("Excalibur", 100)  
        self.verb = "take"  


class GhostSoldier:
    def __init__(self):
        self.riddles_solved = 0
        self.ghost_soldier_alive = True

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "approach":
            self.approach()

    def approach(self):
        if not self.ghost_soldier_alive:
            print("The ghost soldier is gone.")
        elif self.riddles_solved == 0:
            print("You approach a ghostly soldier standing guard over a sword stuck in a tree stump.")
            print("To obtain the sword, you need to solve the first riddle.")
            self.solve_riddle("What has keys but can't open locks?", "piano")
        elif self.riddles_solved == 1:
            print("The ghost soldier is still in the clearing. You need to solve the second riddle.")
            self.solve_riddle("I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?", "echo")
        elif self.riddles_solved == 2:
            print("The ghost soldier is still in the clearing. You need to solve the third riddle.")
            self.solve_riddle("The more you take, the more you leave behind. What am I?", "footsteps")
        else:
            print("The ghost soldier is still in the clearing, but all riddles have been solved.")

    def solve_riddle(self, riddle, answer):
        player_answer = input(f"{riddle} ").lower()
        if answer in player_answer:
            print("The ghost soldier nods. The mystical barrier weakens.")
            self.riddles_solved += 1
            if self.riddles_solved < 3:
                print(f"You solved {self.riddles_solved} riddle(s).")
                self.approach()
            else:
                self.acquire_excalibur()

    def acquire_excalibur(self):
        excalibur = Excalibur()
        config.the_player.add_to_inventory([excalibur])
        print(f"You obtained {excalibur.name} from the tree stump! It's the legendary Excalibur.")



class Mushroom_Field(location.SubLocation):

    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "mushroom field"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self
        self.hot_springs_instance = Hot_Springs(self.main_location)
        self.verbs["approach"] = self.hot_springs_instance
        self.event_chance = 100
        self.events.append(FriendlyMushroomPersonEvent())

        #adding mushrooms to collect 
        self.locations = {}
        self.verbs["pick"] = self
        self.item_in_mfield = Mushroom()
    
        
    
    def enter (self):
        description = "You walk into a field full of colorful mushrooms and some seem to glow. You can investigate."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            #Text will be printed by "enter" in Tropical_Forest()
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["hot springs"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caves"]

            config.the_player.visiting = False

        print(verb)
        if verb == "investigate":
            announce(" You see a remarkably colorful " + self.item_in_mfield.name + " in the mushroom field. You can pick it.")
   
        elif verb == "pick":
                #player will have pick something such as pick a colorful mushroom
            if len(cmd_list) > 1:
                i = self.item_in_mfield
                if i and (i.name == cmd_list[1] or cmd_list [1] == "all"):
                    announce("You picked a "+i.name + " from the field of colorful mushrooms. You can go east to continue to the hot springs.")
                    config.the_player.add_to_inventory([i])
                    self.item_in_mfield = None 
                else:
                    print(f"No such item: {cmd_list[1]}")
            else:
                print("Please specify an item to pick.")

    
class Mushroom(items.Item):
    def __init__(self):
        super().__init__("mushroom", 3)
        self.restore_health = (10)
        self.verb = "consume"


class FriendlyMushroomPersonEvent(event.Event):
    def __init__(self):
        self.name = "Friendly Mushroom Person"

    def process(self, world):
        announce("As you explore the mushroom field, you encounter a friendly mushroom person.")
        announce("The mushroom person greets you warmly and offers words of encouragement:")
        announce("\"May your journey be filled with joy and discovery! Remember, positivity is the key to success.\"")
        announce("Feeling inspired, you feel a boost of morale to continue the adventure.")

        # Ensure the "message" key is always present
        results = {"message": "The Friendly Mushroom Person fills you with encouragement.", "newevents": []}

        return results



class Hot_Springs(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "hot springs"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.in_event = False
        self.event_chance = 20
        self.events.append(SnakesHoard())

        # adding fish
        self.verbs["fish"] = self
        self.verbs["investigate"] = self
        self.item_in_hsprings = Fish()

    def enter(self):
        description = "You see a big hot spring that has a series of geysers surrounding it."
        if self.item_in_hsprings:
            description += f" You see many huge spiny {self.item_in_hsprings.name} jumping up and down with the geysers. You can fish here."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "fish":
            self.handle_fish()
        elif verb == "chase":
            announce("You chase away the annoying seagulls.")
        elif verb == "south":
            announce("You return to your ship")
            # boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            # Text will be printed by "enter" in Tropical_Forest()
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["mushroom field"]
        elif verb == "west":
            config.the_player.next_loc = self.main_location.locations["caves"]
    
    def handle_fish(self):
        if self.item_in_hsprings != None:
            i = self.item_in_hsprings
            announce("You go fishing and catch a fish")
            config.the_player.add_to_inventory(Fish().as_list())
            self.item_in_hsprings = None
            # This command uses time
            config.the_player.go = True
        else:
            announce("There are no more fish.")

class Fish(items.Item):
    def __init__(self):
        super().__init__("fish", 3)
        self.restore_health = (10)
        self.verb = "consume"
    def as_list(self):
        return [self]



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
        self.amethyst_count = 0
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["tropical forest"]
            #Text will be printed by "enter" in Tropical_Forest()
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["mushroom field"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caves"]
            config.the_player.visiting = False
        
        elif verb == "investigate":
            print (verb)
            self.handle_investigate()
            
        elif (verb == "mine"):
            self.handle_mine()

    def handle_investigate(self):
        announce(" You see a beautiful purple " + self.item_in_cave.name + " on the cave wall. You can mine it.")

    def handle_mine(self):
        if self.amethyst_count < 5:
            i = Amethyst()
            announce("You have mined an " + i.name + " from the cave wall.")
            config.the_player.add_to_inventory([i])
            self.amethyst_count += 1
        else:
            announce("You've already mined the maximum number of amethysts from this cave.")
    
    def enter (self):
        description = "You enter one of the many caves in this region. Some areas on the wall are sparkling. You can investigate."
        announce(description)

class Amethyst(items.Item):
     def __init__(self):
        super().__init__("amethyst", 50)
        self.verb = "mine"



