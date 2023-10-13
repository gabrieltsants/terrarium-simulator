import threading
import time
import random

def euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def iso(x, y, z):
    iso_x = x - y
    iso_y = (x + y) / 2 - z
    return iso_x, iso_y

class Object:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.energy = 100
    
    def move(self):
        pass
    
    def eat(self, other):
        pass
    
    def reproduce(self, other):
        pass
    
    def die(self):
        terrarium.remove_object(self)
        print(f"{self.__class__.__name__} at ({self.x}, {self.y}) has died.")
    
class Plant(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    
    def eat(self, other):
        pass 

    def move(self):
        pass
    
    def reproduce(self, other):
        if terrarium.humidity > 20 and random.random() < 10:
            baby = Plant(self.x, self.y, self.size)
            terrarium.add_object(baby)
            print(f"A new plant at ({self.x}, {self.y}) has grown!")
            
    
class Insect(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
    
    def move(self):
        # Calculate the velocity vector towards the target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            self.vx = dx / dist
            self.vy = dy / dist
        else:
            self.vx = 0
            self.vy = 0
        
        # Update the position using the velocity vector
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off the walls if the insect goes out of bounds
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
        elif self.x > terrarium.width - 1:
            self.x = terrarium.width - 1
            self.vx = -self.vx
        if self.y < 0:
            self.y = 0
            self.vy = -self.vy
        elif self.y > terrarium.height - 1:
            self.y = terrarium.height - 1
            self.vy = -self.vy


class Ant(Insect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    
    def move(self):
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        self.vx = max(-1, min(self.vx, 1))
        self.vy = max(-1, min(self.vy, 1))
        
        self.x = max(0, min(self.x + self.vx, terrarium.width - 1))
        self.y = max(0, min(self.y + self.vy, terrarium.height - 1))
    
    def eat(self, other):
        if isinstance(other, Plant):
            self.energy += other.size
            other.die()
        elif (isinstance(other, Insect) or isinstance(other, Animal)) and other.size < self.size:
            self.energy += other.energy
            other.die()
        
        print(f"Ant at ({self.x}, {self.y}) ate a {other.__class__.__name__}")

class Ladybug(Insect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    
    def move(self):
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        self.vx = max(-1, min(self.vx, 1))
        self.vy = max(-1, min(self.vy, 1))
        
        self.x = max(0, min(self.x + self.vx, terrarium.width - 1))
        self.y = max(0, min(self.y + self.vy, terrarium.height - 1))
    
    def eat(self, other):
        if isinstance(other, Plant):
            self.energy += other.size
            other.die()
        elif isinstance(other, Insect) and other.size < self.size:
            self.energy += other.energy
            other.die()
        elif isinstance(other, Animal) and other.size > self.size:
            self.energy += other.energy
            other.die()
        
        print(f"Ladybug at ({self.x}, {self.y}) ate a {other.__class__.__name__}")
            

class Animal(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.gestation_period = 10
        self.pregnant = False
        self.pregnancy_time = 0
    
    def move(self):
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        self.vx = max(-1, min(self.vx, 1))
        self.vy = max(-1, min(self.vy, 1))
        
        self.x = max(0, min(self.x + self.vx, terrarium.width - 1))
        self.y = max(0, min(self.y + self.vy, terrarium.height - 1))

    def eat(self, other):
        if isinstance(other, Plant):
            self.energy += other.size
            other.die()
        elif isinstance(other, Animal) and other.size < self.size:
            self.energy += other.energy
            other.die()

    def reproduce(self, other):
        if isinstance(other, Animal) and isinstance(other, self.__class__) and other.size == self.size:
            if self.pregnant:
                self.pregnancy_time += 1
                if self.pregnancy_time >= self.gestation_period:
                    baby = self.__class__(self.x, self.y, self.size)
                    terrarium.add_object(baby)
                    print(f"{self.__class__.__name__} at ({self.x}, {self.y}) has given birth!")
                    self.pregnant = False
                    self.pregnancy_time = 0
            else:
                self.pregnant = True
                self.pregnancy_time = 1
                print(f"{self.__class__.__name__} at ({self.x}, {self.y}) is pregnant!")


class Gecko(Animal):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)

    def move(self):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        self.x = max(0, min(self.x + dx, terrarium.width - 1))
        self.y = max(0, min(self.y + dy, terrarium.height - 1))

    def eat(self, other):
        if isinstance(other, Plant):
            self.energy += other.size
            other.die()
            print(f"Gecko at ({self.x}, {self.y}) ate a {other.__class__.__name__}")
        elif isinstance(other, Insect) or isinstance(other, Animal) and other.size < self.size and self.energy < 90:
            self.energy += other.energy
            other.die()
            print(f"Gecko at ({self.x}, {self.y}) ate a {other.__class__.__name__}")

    def reproduce(self, other):
        if isinstance(other, Gecko) and other.size == self.size:
            baby = Gecko(self.x, self.y, self.size)
            terrarium.add_object(baby)
            print(f"Gecko at ({self.x}, {self.y}) has reproduced!")

class Rock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)

class Terrarium:
    def __init__(self, width, height, temperature, humidity, light):
        self.width = width
        self.height = height
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.objects = []
        self.weather_events = ["sunny", "rainy", "cloudy"]
        self.num_plants = 0
        self.num_insects = 0
        self.num_animals = 0
        self.num_rocks = 0

    def add_object(self, obj):
        self.objects.append(obj)
        if isinstance(obj, Plant):
            self.num_plants += 1
        elif isinstance(obj, Insect):
            self.num_insects += 1
        elif isinstance(obj, Animal):
            self.num_animals += 1
        elif isinstance(obj, Rock):
            self.num_rocks += 1

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
        if isinstance(obj, Plant):
            self.num_plants -= 1
        elif isinstance(obj, Insect):
            self.num_insects -= 1
        elif isinstance(obj, Animal):
            self.num_animals -= 1
        elif isinstance(obj, Rock):
            self.num_rocks -= 1
    
    def generate_art(self):
        terrarium_art = []

        # Top border
        terrarium_art.append("  " + " " * (self.width - 2) + "+---------------+")

        # Upper side borders
        terrarium_art.append(" " * (self.width - 3) + "/" + " " * 7 + "----------| |")
        terrarium_art.append(" " * (self.width - 4) + "/" + " " * 15 + "   |  ")

        # Main content and side borders
        for i in range(self.height - 4):
            row = [" " * (self.width - 4) + "|"]
            for j in range(self.width - 2):
                obj = None
                for o in self.objects:
                    if o.x == j and o.y == i:
                        obj = o
                        break
                if obj is None:
                    row.append(" ")
                else:
                    row.append(obj.__class__.__name__[0])
            row.append("|")
            row.append(" " * (i < self.height - 6) + "|" * (i < self.height - 6))
            terrarium_art.append("".join(row))

        # Bottom border
        terrarium_art.append(" " * (self.width - 4) + "+" + "-" * (self.width - 2) + "+/")
        terrarium_art.append(" " * (self.width - 4) + "|" + " " * (self.width - 2) + "|")
        terrarium_art.append(" " * (self.width - 4) + "+" + "-" * (self.width - 2) + "+/")

        return terrarium_art

    def simulate(self):
        # Print the terrarium stats
        print(f"Temperature: {self.temperature}Cº - Humidity: {self.humidity} - Light: {self.light}")
        print(f"Plants: {self.num_plants} - Insects: {self.num_insects} - Animals: {self.num_animals} - Rocks: {self.num_rocks}")
            
        # Generate the art for the terrarium
        terrarium_art = self.generate_art()

        # Print the art
        print("\n".join(terrarium_art))

        # Sleep for a short period to prevent the CLI from flashing too much
        time.sleep(1)


        for obj in self.objects:
            if random.random() < 0.05: # Chance do the organism to do something
                obj.move()
            
            # Check for collisions with other objects
            for other in self.objects:
                
                if obj == other:
                    continue
                    
                dist = ((obj.x - other.x)**2 + (obj.y - other.y)**2)**0.5
                

                if dist <= obj.size + other.size + 2:
                    if isinstance(obj, Plant) and isinstance(other, Animal):
                        obj.eat(other)
                    elif isinstance(obj, Animal) and isinstance(other, Plant) and random.random() < 0.09:
                        obj.eat(other)
                    elif isinstance(obj, Animal) and isinstance(other, Animal) and other.size == obj.size and random.random() < 0.002:
                        obj.reproduce(other)
                    elif isinstance(obj, Insect) and isinstance(other, Insect) and other.size == obj.size and random.random() < 0.001:
                        obj.reproduce(other)
                    elif isinstance(obj, Animal) and isinstance(other, Animal) and other.size == obj.size and random.random() < 0.001:
                        obj.eat(other)
                        break
                    elif isinstance(obj, Plant) and self.humidity > 20 and random.random() < 0.001:
                        obj.reproduce(obj)
                        break
                    elif isinstance(obj, Insect) and isinstance(other, Animal) and random.random() < 0.002:
                        other.eat(obj)
                        obj.die()
                        break          
                
            if isinstance(obj, Animal):
                obj.energy -= 1
                if obj.energy <= 0:
                    obj.die()
            elif isinstance(obj, Plant) and random.random() < 0.01:
                obj.die()
            elif isinstance(obj, Insect):
                obj.energy -= 1
                if obj.energy <= 0:
                    obj.die()
                    
        self.num_plants = sum(isinstance(obj, Plant) for obj in self.objects)
        self.num_insects = sum(isinstance(obj, Insect) for obj in self.objects)
        self.num_animals = sum(isinstance(obj, Animal) for obj in self.objects)
        self.num_rocks = sum(isinstance(obj, Rock) for obj in self.objects)

        if random.random() < 0.01:
            self.temperature += random.randint(-1, 1)
            self.humidity += random.randint(-1, 1)
            self.light += random.randint(-1, 1)
            print(f"Weather event: {random.choice(self.weather_events)}")
        
        print()
        # Clear the CLI again
        print("\033c", end="")


# Create a terrarium with a size of 20x10, temperature of 25, humidity of 50, and light of 50
terrarium = Terrarium(20, 10, 25, 50, 50)

# Add some objects to the terrarium
for i in range(30):
    x = random.randint(0, terrarium.width-1)
    y = random.randint(0, terrarium.height-1)
    size = 0
    plant = Plant(x, y, size)
    terrarium.add_object(plant)

for i in range(10):
    x = random.randint(0, terrarium.width-1)
    y = random.randint(0, terrarium.height-1)
    size = 1
    ant = Ant(x, y, size)
    terrarium.add_object(ant)

for i in range(5):
    x = random.randint(0, terrarium.width-1)
    y = random.randint(0, terrarium.height-1)
    size = 1
    ladybug = Ladybug(x, y, size)
    terrarium.add_object(ladybug)

for i in range(3):
    x = random.randint(0, terrarium.width-1)
    y = random.randint(0, terrarium.height-1)
    size = 100
    rock = Rock(x, y, size)
    terrarium.add_object(rock)

for i in range(5):
    x = random.randint(0, terrarium.width-1)
    y = random.randint(0, terrarium.height-1)
    size = 3
    gecko = Gecko(x, y, size)
    terrarium.add_object(gecko)

def run_simulation():
    while True:
        terrarium.simulate()
        time.sleep(5.0)

# Start the simulation loop in a separate thread
thread = threading.Thread(target=run_simulation)
thread.start()
