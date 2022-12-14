import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, x0, y0, w, h, nodes):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.nodes = nodes
        self.children = []
    
    def get_nodes(self):
        return self.nodes
    
class Boundary():
    def __init__(self,xstart,xend,ystart,yend):
        self.xstart = xstart
        self.xend = xend
        self.ystart = ystart
        self.yend = yend

class QTree():

    def __init__(self, boundary, array=[]):
        self.nodes = array
        self.root = Node(boundary.xstart, boundary.ystart, boundary.xend, boundary.yend, self.nodes)
        self.boundary = boundary

    def find_children(self,node):
        if not node.children:
            return [node]
        else:
            children = []
            for child in node.children:
                children += (self.find_children(child))
        return children

    def add_node(self, point):
        if(point.x < self.boundary.xend and point.x > self.boundary.xstart and point.y < self.boundary.yend and point.y > self.boundary.ystart):
            self.nodes.append(point)
    
    def add_random_node(self):
        point=Point(random.uniform(self.boundary.xstart, self.boundary.xend), random.uniform(self.boundary.ystart, self.boundary.yend))
        self.nodes.append(point)
    
    def get_nodes(self):
        return self.nodes
    
    def contains(self,x, y, w, h, nodes):
        pts = []
        for point in nodes:
            if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
                pts.append(point)
        return pts

    def recursive_subdivide(self,node):
        if len(node.nodes)<=1:
            return
        
        w_ = float(node.width/2)
        h_ = float(node.height/2)

        p = self.contains(node.x0, node.y0, w_, h_, node.nodes)
        x1 = Node(node.x0, node.y0, w_, h_, p)
        self.recursive_subdivide(x1)

        p = self.contains(node.x0, node.y0+h_, w_, h_, node.nodes)
        x2 = Node(node.x0, node.y0+h_, w_, h_, p)
        self.recursive_subdivide(x2)

        p = self.contains(node.x0+w_, node.y0, w_, h_, node.nodes)
        x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
        self.recursive_subdivide(x3)

        p = self.contains(node.x0+w_, node.y0+h_, w_, h_, node.nodes)
        x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p)
        self.recursive_subdivide(x4)

        node.children = [x1, x2, x3, x4]

    def subdivide(self):
        self.recursive_subdivide(self.root)
    
    def graph(self):
        self.subdivide()
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        c = self.find_children(self.root)
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        for n in c:
            plt.gcf().gca().add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.nodes]
        y = [point.y for point in self.nodes]
        plt.plot(x, y, 'ro',color='blue')
        plt.show()


#main para su ejecucion
quadtree=QTree(Boundary(0,10,0,10))
for i in range(50):
    quadtree.add_random_node()
quadtree.graph()