import tkinter,numpy
from math import *

class Cube:

    projection_matrix = [[1,0,0],       #x
                        [0,1,0],        #y
                        [0,0,0]]        #z

    cube_points = list(range(8)) #vytvori list v ktorom bude 8 elementov

    cube_points[0] = [[-1], [-1], [1]]  #pridavam jednotlive body kocky
    cube_points[1] = [[1],[-1],[1]]
    cube_points[2] = [[1],[1],[1]]
    cube_points[3] = [[-1],[1],[1]]
    cube_points[4] = [[-1],[-1],[-1]]
    cube_points[5] = [[1],[-1],[-1]]
    cube_points[6] = [[1],[1],[-1]]
    cube_points[7] = [[-1],[1],[-1]]



    def __init__(self,pos_x,pos_y,canvas,tag):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.canvas = canvas
        self.tag = tag


        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.x = 0
        self.y = 0
        self.points = list(range(len(self.cube_points)))

    
    def calc_angle(self,point): #vypocita uhly
    
        self.rotation_x = [[1, 0, 0],
                 [0, cos(self.angle_x), -sin(self.angle_x)],
                 [0, sin(self.angle_x), cos(self.angle_x)]]

        self.rotation_y = [[cos(self.angle_y), 0, sin(self.angle_y)],
                    [0, 1, 0],
                    [-sin(self.angle_y), 0, cos(self.angle_y)]]

        self.rotation_z = [[cos(self.angle_z), -sin(self.angle_z), 0],
                    [sin(self.angle_z), cos(self.angle_z), 0],
                    [0, 0, 1]]
        
        rotate_x = numpy.matmul(self.rotation_x, point)
        rotate_y = numpy.matmul(self.rotation_y, rotate_x)
        rotate_z = numpy.matmul(self.rotation_z, rotate_y)
        point_2d = numpy.matmul(self.projection_matrix,rotate_z)

        self.x = (point_2d[0][0]*50) + self.pos_x
        self.y = (point_2d[1][0]*50) + self.pos_y

        
    def coords_of_every_point(self):
        counter = 0
        for i in self.cube_points:
            self.calc_angle(i)
            self.points[counter] = (self.x,self.y)
            counter += 1
        
        print(self.points)
    

    def get_coords_of_every_point(self):
        counter = 0
        points = list(range(len(self.cube_points)))
        for i in self.cube_points:
            self.calc_angle(i)
            points[counter] = (self.x,self.y)
            counter += 1
        return points


    def draw(self):
        def connect_points(i, j, points):
            self.canvas.create_line(points[i][0], points[i][1] , points[j][0], points[j][1],tags=self.tag,fill='red')
            # print("points: ",points)
            

        self.canvas.delete(self.tag)
        self.points = self.get_coords_of_every_point()
        for point in self.cube_points:
            self.calc_angle(point)

            self.canvas.create_oval(self.x-5,self.y-5,self.x+5,self.y+5,tags=self.tag)
        
        
        #self.canvas.create_rectangle()
        # connect_points(0, 1, self.points)   

        connect_points(0, 1, self.points)    #x
        connect_points(0, 3, self.points)    #y
        connect_points(0, 4, self.points)    #z
        connect_points(1, 2, self.points)
        connect_points(1, 5, self.points)
        connect_points(2, 6, self.points)
        connect_points(2, 3, self.points)
        connect_points(3, 7, self.points)
        connect_points(4, 5, self.points)
        connect_points(4, 7, self.points)
        connect_points(6, 5, self.points)
        connect_points(6, 7, self.points)


    def moving(self,event):
        key = event.keysym.lower()
        
        if key == "right":
            self.angle_x += 0.1
            
        elif key == "left":
            self.angle_x -= 0.1
        elif key == "up":
            self.angle_y += 0.1
        elif key == "down":
            self.angle_y -= 0.1
        elif key == "z":
            self.angle_z += 0.1
        elif key == "x":
            self.angle_z -= 0.1

        

        print(self.angle_x)
        print(self.angle_y)

    #start metodat pre spustenie a ovladanie kocky tlacitkami
    def start(self):
        self.draw()

    #motion pre automaticke vykreslovanie a otacanie kocky
    def motion(self):
        self.draw()
        self.angle_x += 0.1
        self.angle_y += 0.1
        self.angle_z += 0.1

    

if __name__ == "__main__":

    width,height = 500,500
    canvas = tkinter.Canvas(width=width, height=height)
    canvas.pack()

    c=Cube(width/2, height/2,canvas,"cube")

    def play():
        ##ovladanie sipkami 
        #c.start()
        ##automaticke otacanie
        c.motion()

        canvas.after(100,play)


    play()

    """BIND KEYS"""
    canvas.bind_all("<Right>",c.moving)
    canvas.bind_all("<Left>",c.moving)
    canvas.bind_all("<Down>",c.moving)
    canvas.bind_all("<Up>",c.moving)
    canvas.bind_all("<z>",c.moving)
    canvas.bind_all("<x>",c.moving)

tkinter.mainloop()