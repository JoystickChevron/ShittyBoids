import pygame;
import math;
import random;
WIDTH: int = 1200;
HEIGHT: int = 800;
SIZE: int = 10;
MOVESPEED: int = 5;
LIGHT_PINK = (255,204,255);
BLACK = (0,0,0);
BLUE = (0,0,255);
GREEN = (0,255,0);
WHITE = (255,255,255);
GOAL = (WIDTH//2,HEIGHT//4);
GOAL_X = GOAL[0];
GOAL_Y = GOAL[1];


class Boid:
	def __init__(self, x: float, y: float, color = BLUE, weight = SIZE):
		self.rectangle = pygame.Rect(x, y,  weight, weight);
		self.velocityX = random.randint(-5,5);
		self.velocityY = random.randint(-5,5);
		self.weight = weight;
		self.accelerationX = 0;
		self.accelerationY = 0;
		self.radius = 60;
		self.color = color;
		
	def __str__(self):
		return (str(self.rectangle.x) + str(self.rectangle.y));
		
	def __eq__(self,other):	
		return (self.rectangle.x == other.rectangle.x) and (self.rectangle.y == other.rectangle.y);
			
	def getX(self):
		return self.rectangle.x;
		
	def getY(self):
		return self.rectangle.y;
	
	def tooClose(self, boid):
		return distanceBetween(self, boid) < 50;
	def speedLimit(self):
		if self.getVelocityX() > 5:
			self.velocityX = 5;
		if self.getVelocityX() < -5:
			self.velocityX = -5;
		if self.getVelocityY() > 5:
			self.velocityY = 5;
		if self.getVelocityY() < -5:
			self.velocityY = -5;
	
	def calculateAcceleration(self, forceX, forceY):
		ax = (forceX / self.weight) * SIZE;
		ay = (forceY / self.weight) * SIZE;
		self.accelerationX = self.accelerationX + ax;
		self.accelerationY = self.accelerationY + ay;
			
	def update(self):
		self.velocityX += self.accelerationX;
		self.velocityY += self.accelerationY;
		self.speedLimit();
		self.rectangle.x += self.velocityX;
		self.rectangle.y += self.velocityY;
		if self.rectangle.x > WIDTH:
			self.rectangle.x = 0;
		if self.rectangle.x < 0:
			self.rectangle.x = WIDTH;
		if self.rectangle.y > HEIGHT:
			self.rectangle.y = 0;
		if self.rectangle.y < 0:
			self.rectangle.y = HEIGHT;
		self.accelerationX = 0;
		self.accelerationY = 0;
		
	def nearbyBoids(self, allBoids):
		nearbyBoids = [];
		for boid in allBoids:
			if distanceBetween(self, boid) < self.radius and self != boid: 
				nearbyBoids.append(boid);	
		return nearbyBoids;
		
	def moveTowardsGoalMouse(self, listOfBoids):
		x, y = pygame.mouse.get_pos();
		goal_x = x;
		goal_y = y;
		self.calculateAcceleration((goal_x - self.rectangle.x) * 0.25, (goal_y - self.rectangle.y) * 0.25);
		
	def moveTowardsGoal(self, listOfBoids):
		goal_x = 0;
		goal_y = 0;
		if (len(listOfBoids)!= 0):
			
			for boid in listOfBoids:
				goal_x += boid.getX();
				goal_y += boid.getY();
			goal_x = goal_x/len(listOfBoids);
			goal_y = goal_y/len(listOfBoids);
		self.calculateAcceleration((goal_x - self.rectangle.x) * 0.006, (goal_y - self.rectangle.y) * 0.006);
	def avoidOthers(self, listOfBoids):
		steeringForceX = 0;
		steeringForceY = 0;
		avoidX = 0;
		avoidY = 0;
		count = 0;
		for boid in listOfBoids:
			if self.tooClose(boid):
				distanceX = self.rectangle.x - boid.getX();
				distanceY = self.rectangle.y - boid.getY();
				avoidX += distanceX;
				avoidY += distanceY;
				steeringForceX += avoidX;
				steeringForceY += avoidY;
				count+=1;
		if count > 0:
			steeringForceX *= 0.03;
			steeringForceY *= 0.03;

		self.calculateAcceleration(steeringForceX,steeringForceY);
	def draw(self,screen):		
		self.update();
		center = (self.rectangle.x,self.rectangle.y);
		radius = SIZE
		mouse_position = (self.velocityX, self.velocityY)
		leftPoint, rightPoint, middlePoint,= get_points(center, radius, mouse_position)
		#leftPoint = (self.rectangle.x,self.rectangle.y);
		#rightPoint = (self.rectangle.x+self.weight,self.rectangle.y);
		#middlePoint = (self.rectangle.x + self.weight//2,self.rectangle.y + self.weight + 5);
		pygame.draw.polygon(screen,self.color,[rightPoint,leftPoint,middlePoint]);
	
	def getVelocityX(self):
		return self.velocityX;
		
	def getVelocityY(self):
		return self.velocityY;
		
	def matchVelocity(self, listOfBoids):
		pos_x = 0;
		pos_y = 0;
		steeringForceX = 0;
		steeringForceY = 0;
		if len(listOfBoids) > 0:
			for boid in listOfBoids:	
				pos_x += boid.getX();
				pos_y += boid.getY();
			pos_x = pos_x//len(listOfBoids);
			pos_y = pos_y//len(listOfBoids);
			steeringForceX = (pos_x - self.rectangle.x) /10;
			steeringForceY = (pos_y - self.rectangle.y) /10;
		self.calculateAcceleration(steeringForceX,steeringForceY);
		
		
def get_points(center, radius, mouse_position):
	length = math.hypot(mouse_position[0] - center[0], mouse_position[1] - center[1])    
	angle_vector_x = (mouse_position[0] - center[0]) / length     
	angle = math.acos(angle_vector_x) 
	triangle = [0, (3 * math.pi / 4), (5 * math.pi / 4)]
	result = list()
	for t in triangle:
		x = center[0] + radius * math.cos(t + angle)
		y = center[1] + radius * math.sin(t + angle) * -1;
		result.append((x, y))
	return result
def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))
def distanceBetween(point1, point2):
		return math.sqrt((point1.getX()-point2.getX())**2 + (point1.getY()-point2.getY())**2);
		
screen = pygame.display.set_mode((WIDTH,HEIGHT));
clock = pygame.time.Clock();
Boids = [None] * 100;
for i in range(len(Boids)):
	Boids[i] = Boid(random.randint(0,WIDTH), random.randint(0,HEIGHT), BLUE, 10);
while True:
	screen.fill(WHITE);
	for aBoid in Boids:
		listOfBoids = aBoid.nearbyBoids(Boids);
		aBoid.avoidOthers(listOfBoids);
		aBoid.matchVelocity(listOfBoids);
		aBoid.moveTowardsGoal(Boids);
		aBoid.draw(screen);
	pygame.display.update();
	pygame.event.pump();
	clock.tick(60);
	


