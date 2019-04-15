from graphics import *
from time import *
import operator
import os
import threading

##x,y=500,500 ##for static purposes
space=10
speed=20
wait=False

###This is for variable map###

def calc_screen(list_p):
    edges = edge_points(list_p)
    min_x=edges[0][0]
    min_y=edges[0][1]
    max_x=edges[1][0]
    max_y=edges[1][1] 
    screen_x = (max_x-min_x)*5/4
    screen_y = (max_y-min_y)*5/4
    return screen_x , screen_y

def dir_to_points(list_d):
    x,y = 0,0
    list_p=[]
    list_p.append(Point(x,y))
    for i in list_d:
        x = x + i[0]*space
        y = y + i[1]*space
        list_p.append(Point(x,y))
    return list_p

def edge_points(list_p):
    max_x , max_y = 0,0
    max_xi , max_yi = 0,0
    min_x , min_y = 0,0
    min_xi , min_yi = 0,0
    for i in range(len(list_p)):
        if(list_p[i].getX() > max_x):
            max_x = list_p[i].getX()
            max_xi = i
        if(list_p[i].getY() > max_y):
            max_y = list_p[i].getY()
            max_yi = i

        if(list_p[i].getX() < min_x):
            min_x = list_p[i].getX()
            min_xi = i
        if(list_p[i].getY() < min_y):
            min_y = list_p[i].getY()
            min_yi = i
    return [(min_x,min_y),(max_x,max_y)]

def edge_polygon(list_p):
    edges = edge_points(list_p)
    min_x=edges[0][0]
    min_y=edges[0][1]
    max_x=edges[1][0]
    max_y=edges[1][1] 
    p =Polygon(Point(min_x,min_y),Point(max_x,min_y),
                   Point(max_x,max_y),Point(min_x,max_y))
    for i in list(p.points):
        i.move(x/10,y/10) 
    return p

def cell_map(list_p):
    map_cells=Polygon(list_p)
    for i in list(map_cells.points):
        i.move(x/10,y/10)
    return map_cells

def gridding(win,edge_polygon):
    p= list(edge_polygon.points)
    start_y = p[0].getY()
    end_y = p[2].getY()
    start_x = p[0].getX()
    end_x = p[1].getX()
    for i in range(int(start_x)+space,int(end_x),space):
        Line(Point(i,start_y),Point(i,end_y)).draw(win)
        if(wait):
            sleep(0.1/speed)
    for i in range(int(start_y)+space,int(end_y),space):
        Line(Point(start_x,i),Point(end_x,i)).draw(win)
        if(wait):
            sleep(0.1/speed)

# list_d return from the robot , number of cells walked

list_d = [(0,20),(10,0),(0,-5),(5,0),(0,5),(10,0),(0,-20)]
list_p = dir_to_points(list_d)
x,y = calc_screen(list_p)
grid = cell_map(list_p)
edge_polygon = edge_polygon(list_p)

##############################

class Cell():
    nb_cells_X=int((4*x/5)/space)
    nb_cells_Y=int((4*y/5)/space)
    current_cell_x,current_cell_y=0,0
    pos_x,pos_y=0,0 #useless
    
    def __init__(self,win,cell_x,cell_y,draw=True):
        
        if(cell_x<self.nb_cells_X):
            self.current_cell_x=cell_x
            self.pos_x=self.current_cell_x*space+x/10
        else:
            self.current_cell_x=self.nb_cells_X-1
            self.pos_x=self.current_cell_x*space+x/10
        
        if(cell_y<self.nb_cells_Y):
            self.current_cell_y=cell_y
            self.pos_y=self.current_cell_y*space+y/10
        else:
            self.current_cell_y=self.nb_cells_Y-1
            self.pos_y=self.current_cell_y*space+y/10
            
        self.draw=Polygon(Point(self.pos_x,self.pos_y),
                          Point(self.pos_x+space,self.pos_y),
                          Point(self.pos_x+space,self.pos_y+space),
                          Point(self.pos_x,self.pos_y+space),)
        
        self.f = 0 #new
        self.g = 0
        self.h = 0

        if(draw):
            self.draw.draw(win)
        
    def __eq__(self,other):
        return (self.current_cell_x==other.current_cell_x) and(
    self.current_cell_y==other.current_cell_y )

    def destroy(self):
        self.draw.undraw()
        
##depricated , not needed
##    def fitness_h(self,g):
##        return ((self.current_cell_x-g.current_cell_x)**2+
##                (self.current_cell_y-g.current_cell_y)**2)
##    
##    def fitness_g(self,w):
##        return ((self.current_cell_x-w.initial_cell_x)**2+
##                (self.current_cell_y-w.initial_cell_y)**2)
##
##    def fitness(self,w,g):
##        return self.fintess_h(g)+self.fitness_g(w)
    
class Wheel(Cell):
    color="#aaff7f"
    initial_cell_x,initial_cell_y=0,0
    def __init__(self,win,cell_x,cell_y):
        Cell.__init__(self,win,cell_x,cell_y)
        self.draw.setFill(self.color)
        self.initial_cell_x=self.current_cell_x
        self.initial_cell_y=self.current_cell_y
    
    def moveR_one(self):
        self.current_cell_x=self.current_cell_x+1
        self.draw.move(space,0)
        sleep(1/speed)
    
    def moveD_one(self):
        self.current_cell_y=self.current_cell_y+1
        self.draw.move(0,space)
        sleep(1/speed)
            
    def moveL_one(self):
        self.current_cell_x=self.current_cell_x-1
        self.draw.move(-space,0)
        sleep(1/speed)
            
    def moveU_one(self):
        self.current_cell_y=self.current_cell_y-1
        self.draw.move(0,-space)
        sleep(1/speed)
    
    def move_t(self,t):
        for i in t:
            if(i=="L"):
                self.moveL_one()
            elif(i=="U"):
                self.moveU_one()
            elif(i=="R"):
                self.moveR_one()
            elif(i=="D"):
                self.moveD_one()

    def get_back(self,win):
        x=(self.initial_cell_x-self.current_cell_x)*space
        y=(self.initial_cell_y-self.current_cell_y)*space
##        print("x = {0}".format(x))
##        print("y = {0}".format(y))
        self.draw.move(x,y)
        self.current_cell_x=self.initial_cell_x
        self.current_cell_y=self.initial_cell_y
        
class Goal(Cell):
    color="#ff341a"
    def __init__(self,win,cell_x,cell_y):
        Cell.__init__(self,win,cell_x,cell_y)
        self.draw.setFill(self.color)

class Block(Cell):
    color="#313533"
    def __init__(self,win,cell_x,cell_y):
        Cell.__init__(self,win,cell_x,cell_y)
        self.draw.setFill(self.color)
    
def build_screen(x,y):
    win = GraphWin("Catch me if you can",x,y)
    grid = Polygon(Point(x/10,y/10),
                   Point(9*x/10,y/10),
                   Point(9*x/10,9*y/10),
                   Point(x/10,9*y/10))
    grid.setWidth(2)
    grid.draw(win)
    for i in range(int(x/10),int(9*x/10)+1,space):
        Line(Point(i,y/10),Point(i,9*y/10)).draw(win)
        if(wait):
            sleep(0.1/speed)
    for i in range(int(y/10),int(9*y/10)+1,space):
        Line(Point(x/10,i),Point(9*x/10,i)).draw(win)
        if(wait):
            sleep(0.1/speed)
    return win,grid

class Node(Cell):
    
    color="#e51647"
    draw = False

    def __init__(self,win,cell_x,cell_y,parent=None):
        Cell.__init__(self,win,cell_x,cell_y,self.draw)
        self.parent = parent
        self.draw.setFill(self.color)

    def show(self,win):
        self.draw.draw(win)

def show_nodes(nodes,win):
    for n in nodes:
        n.show(win)

def conv_path(path):
    
    res=list()
    for index in range(len(path)-1):
        i = path[index]
        j = path[index+1]
        x = j[0]-i[0]
        y = j[1]-i[1]
        if(x==1):
            res.append("R")
        elif(x==-1):
            res.append("L")
        elif(y==1):
            res.append("D")
        elif(y==-1):
            res.append("U")

    return res

def move(win,grid,w,g,list_b=[]): #based on Astar

    start_node = Node(win,w.current_cell_x,w.current_cell_y)

    end_node = Node(win,g.current_cell_x,g.current_cell_y)

    open_nodes = list()
    closed_nodes = list()
    open_nodes.append(start_node)

    while(len(open_nodes)>0):
        current_node = open_nodes[0]
        current_index = 0

        for i,item in enumerate(open_nodes):
            if (item.f < current_node.f):
                current_node = item
                current_index = i

        closed_nodes.append(open_nodes.pop(current_index))

        if( current_node == end_node):
            path = []
            c = current_node
            while c is not None:
                path.append([c.current_cell_x,c.current_cell_y])
                c.show(win)
                c = c.parent
            return conv_path(path[::-1])

        children = []
        for n in [(0,-1),(0,1),(-1,0),(1,0)]:
            node_p = Node(win,current_node.current_cell_x+n[0],
                      current_node.current_cell_y+n[1],current_node)

            if(blocked(grid,node_p,list_b)):
                continue

            children.append(node_p)

        for child in children:

            if child in closed_nodes :
                continue

            child.g = current_node.g +1
            child.h = ((child.current_cell_x - end_node.current_cell_x)**2+
                       (child.current_cell_y - end_node.current_cell_y)**2)
            child.f = child.g + child.h

            for n in open_nodes:
                if (child == n and child.g > n.g ):
                    continue

            open_nodes.append(child)
                    
##def new_move(grid,w,g,f,list_b=[],old_mv=''):
##    if(f==-1):
##        f=w.fitness(g)
##    if(w==g):
##        print('found')
##        return []
##    else:
##        d=['L','U','R','D']
##        w.moveL_one()
##        if(blocked(grid,w,list_b)):
##            d.pop(0)
##        w.moveR_one()
##        
##        w.moveU_one()
##        if(blocked(grid,w,list_b)):
##            d.pop(len(d)-3)
##        w.moveD_one()
##        
##        w.moveR_one()
##        if(blocked(grid,w,list_b)):
##            d.pop(len(d)-2)
##        w.moveL_one()
##        
##        w.moveD_one()
##        if(blocked(grid,w,list_b)):
##            d.pop(len(d)-1)
##        w.moveU_one()
##
##        if(not(old_mv=='')):
##            d=inv_mv(d,old_mv)
##
####        print(d)
##        if(len(d)==0):
##            print("Dafaq")
##            return []
##        elif(len(d)==1):
##            unit_move(w,g,f,d[0],True)
##            return d+new_move(grid,w,g,f,list_b,d[0])
##        for i in d:
##            tmp,x = unit_move(w,g,f,i)
####                print(tmp)
##            if(len(tmp)==1):
##                return tmp+new_move(grid,w,g,x,list_b,tmp[0])
##        print('wat')
##        return []
##
##def inv_mv(d,old_mv):
##    if(old_mv=='L' and 'R' in d):
##        d.remove('R')
##    elif(old_mv=='U' and 'D'in d):
##        d.remove('D')
##    elif(old_mv=='R' and 'L' in d):
##        d.remove('L')
##    elif(old_mv=='D' and 'U' in d):
##        d.remove('U')
##    return d
##        
##def unit_move(w,g,f,d,ignore=False):
##    
##    if(d=='L'):
##        w.moveL_one()
##    elif(d=='U'):
##        w.moveU_one()
##    elif(d=='R'):
##        w.moveR_one()
##    elif(d=='D'):
##        w.moveD_one()
##        
##    x=w.fitness(g)
####    print("f = {0}".format(f))
####    print("x = {0}".format(x))
##    if(ignore or x<f):
##        return [d],x
##    else:
##        if(d=='L'):
##            w.moveR_one()
##        elif(d=='U'):
##            w.moveD_one()
##        elif(d=='R'):
##            w.moveL_one()
##        elif(d=='D'):
##            w.moveU_one()
##        return [],0
    
def blocked(grid,w,list_b):
    p = list(w.draw.points)[0]
    v = not(point_in_polygon(grid,p,space/2))
    for b in list_b:
        if(w==b):
           return True
    return v
        
def point_in_polygon(grid,p,s=0):
    l = [x for x in grid.points]
    j=len(l)-1
    v=False
    px=p.getX()+s
    py=p.getY()+s
    for i in range(len(l)):
        if((l[i].getX()<px and l[j].getX()>=px)
           or (l[j].getX()<px and l[i].getX()>=px)):
            if((l[i].getY()+(px-l[i].getX())/(l[j].getX()-l[i].getX())
               *(l[j].getY()-l[i].getY()))<py):
                v=not(v)
        j=i
    return v

### no longer in use
def mapping(list_d):
    win = GraphWin("Catch me if you can",x,y)
    mp = Polygon(list_p)
    mp.setWidth(2)
    
    for i in list(mp.points):
        i.move(x/10,y/10)
    mp.draw(win)
    
    for i in range(int(x/10)+space,int(9*x/10)-space+1,space):
        tmp_min_y = y/10
        while(not(point_in_polygon(mp,Point(i,tmp_min_y+1)))):
              tmp_min_y = tmp_min_y+space
        tmp_max_y = tmp_min_y
        while(point_in_polygon(mp,Point(i,tmp_max_y+1))):
              tmp_max_y = tmp_max_y+space    
        Line(Point(i,tmp_min_y),Point(i,tmp_max_y)).draw(win)
        if(wait):
            sleep(0.1/speed)

    for i in range(int(y/10)+space,int(9*y/10)-space+1,space):
        tmp_min_x = x/10
        while(not(point_in_polygon(mp,Point(tmp_min_x+1,i)))):
            tmp_min_x = tmp_min_x+space
        tmp_max_x = tmp_min_x
        while(point_in_polygon(mp,Point(tmp_max_x+1,i))):
            tmp_max_x = tmp_max_x+space    
        Line(Point(tmp_min_x,i),Point(tmp_max_x,i)).draw(win)
        if(wait):
            sleep(0.1/speed)       
    return win , mp

def map_with_blocks(win):
    list_b=list()
    test_w = Wheel(win,0,0)
    for i in range(0,test_w.nb_cells_Y):
        if(i%2==0):
            for j in range(0,test_w.nb_cells_X-1):
                p=list(test_w.draw.points)[0]
                if(not(point_in_polygon(grid,p,space/2))
                   and point_in_polygon(edge_polygon,p,space/2)):
                    list_b.append(Block(win,j,i))
                test_w.moveR_one()
        else:
            for j in range(test_w.nb_cells_X-1,0,-1):
                p=list(test_w.draw.points)[0]
                if(not(point_in_polygon(grid,p,space/2))
                   and point_in_polygon(edge_polygon,p,space/2)):
                    tmp_b=Block(win,j,i)
                test_w.moveL_one()
        test_w.moveD_one()
    test_w.get_back(win)
    test_w.destroy()
    return list_b

def build():
    win = GraphWin("Catch me if you can",x,y)
    grid.draw(win)
    grid.setWidth(2)
    gridding(win,edge_polygon)
    return win

def play_music(name):
    os.system("aplay "+name+".wav &")

def main():
    ##break comment if static
##    win,grid = build_screen(x,y)
##    list_b=list()
##    for i in range(10):
##        list_b.append(Block(win,i+1,i))
    win = build()
    win.getMouse()
    #play_music("build")
    list_b = map_with_blocks(win)
    g = Goal(win,39,0)
    w = Wheel(win,9,19)
    win.getMouse()
    t=move(win,grid,w,g,list_b)
    print(t)
    w.get_back(win)
    win.getMouse()
    play_music("move")
    w.move_t(t)
    win.getMouse()
    win.close()
    
main()
