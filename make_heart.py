import math
import numpy as np


class make_heart:
    def __init__(self,file:str,th:float,num_points:int = 100, num_layers:int = 50,num_onions:int =50, sz:float = 1, epsilon: float = 1e-6):
        self.num_layers = num_layers
        self.num_points = num_points
        self.num_onions = num_onions
        self.file = file
        self.th =  th
        self.count_layers = 0
        self.count_onions = 0
        self.sz = sz
        self.epsilon = epsilon
        self.points = []

    def make_x(self,t, c1=1,c2=1):
        return c1*c2*self.sz *16 * ((np.sin(t))**3)

    def make_y(self,t,c1=1,c2=1):
        return c1*c2*self.sz*((13*np.cos(t)) - (5*np.cos(2*t)) - (2*np.cos(3*t)) - np.cos(4*t))

    def make_heart_2d(self,z:float,c2 = 1)->list:
        angle = np.linspace(0, 2*math.pi,self.num_points)
        x, y = self.make_x(angle,c2=c2), self.make_y(angle,c2=c2)
        z_arr = self.num_points*[z]
        return [(x,y,z) for x,y,z in zip(x,y,z_arr)]

    def make_heart_3d(self, c2 = 1)->list:
        step = 4*self.th / ((self.num_layers+1)*self.num_layers)
        z = -self.th
        self.count_layers = 0
        while True:
            self.points.extend(self.make_heart_2d(z,c2=c2))
            self.count_layers += 1
            if(abs(z-self.th) < 1e-7):
                break
            z=min(self.th,z+step*self.count_layers)

    def make_heart_by_onions(self):
        step = abs(1-(self.epsilon))/self.num_onions
        c2 = 1
        while True:
            self.make_heart_3d(c2=c2)
            self.count_onions += 1
            if abs(c2-self.epsilon) < 1e-7:
                break
            c2 = max(c2 - step, self.epsilon)
        return self.points

    def process_grid(self,grid:list):
        return [ '[' + (','.join([str(s) for s in f])) +']' for f in grid]

    def write_to_file(self):
        print(f"points:{self.num_points}, layers: {self.count_layers}, onions: {self.count_onions}")
        with open(self.file,'w') as f:
            f.write('const vs=\n[\n')
            f.write(',\n'.join(["{"+f"x: {point[0]}, y:  {point[1]}, z:  {point[2]}"+"}"  for point in self.points]))
            f.write('\n]\n')
            f.write('const fs=\n[\n')
            onsz = self.count_layers*self.num_points
            f.write(',\n'.join(self.process_grid([[on*onsz + b for on in range(self.count_onions)] for b in range(onsz)])))
            f.write(',\n')
            cutoff = (2*self.count_onions)//5
            for on in range(self.count_onions):

                f.write(',\n'.join(self.process_grid([range(on*onsz + start*self.num_points,on*onsz + (start+1)*self.num_points) for start in range(self.count_layers)])))
                if on > cutoff:
                    f.write(',\n')
                    f.write(',\n'.join(self.process_grid([[on*onsz+ a + s*self.num_points for s in range(self.count_layers)] for a in range(self.num_points)])))
                if on + 1 != self.count_onions: f.write(',\n')

            f.write('\n]\n')

            f.write('const fs2=\n[\n')
            for on in range(cutoff + 1):
                f.write(',\n'.join(self.process_grid([[on*onsz+ a + s*self.num_points for s in range(self.count_layers)] for a in range(self.num_points)])))
                f.write(',\n')
            f.write('\n]\n')

obj = make_heart("heart.js",0.02,num_points=200,num_layers=2, num_onions = 25,sz=0.02)

obj.make_heart_by_onions()
obj.write_to_file()

# make_circle(0.10,0.5)
