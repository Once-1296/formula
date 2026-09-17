import math
import numpy as np


class make_sphere:
    def __init__(self,file:str,r:float,num_points:int = 100, num_layers:int = 50):
        self.num_layers = num_layers
        self.num_points = num_points
        self.file = file
        self.r =  r
        self.count_layers = 0
        self.points = []
    def make_circle(self,z: float)->list:
        angle = np.linspace(0, 2*math.pi,self.num_points)
        r_ = np.sqrt(self.r**2 - z*z)
        x,y = r_*np.cos(angle),r_*np.sin(angle)
        z_arr = self.num_points*[z]
        return [(x,y,z) for x,y,z in zip(x,y,z_arr)]
        # print(z_arr[:10])

    def make_sphere(self)->list:
        step = self.r / self.num_layers
        z = -self.r
        while True:
            self.points.extend(self.make_circle(z))
            self.count_layers += 1
            if(abs(z-self.r) < 1e-7):
                break
            z=min(self.r,z+step)
        return self.points

    
    def process_grid(self,grid:list):
        return [ '[' + (','.join([str(s) for s in f])) +']' for f in grid]

    def write_to_file(self):
        with open(self.file,'w') as f:
            f.write('const vs=\n[\n')
            f.write(',\n'.join(["{"+f"x: {point[0]}, y:  {point[1]}, z:  {point[2]}"+"}"  for point in self.points]))
            f.write('\n]\n')
            f.write('const fs=\n[\n')
            f.write(',\n'.join(self.process_grid([range(start*self.num_points,(start+1)*self.num_points) for start in range(self.count_layers)])))
            f.write(',\n')
            f.write(',\n'.join(self.process_grid([[a + s*self.num_points for s in range(self.count_layers)] for a in range(self.num_points)])))
            f.write('\n]\n')

obj = make_sphere("sphere.js",0.5,num_points=20,num_layers=10)

obj.make_sphere()
obj.write_to_file()

# make_circle(0.10,0.5)
