
import matplotlib.pyplot as plt

class Island():
    def __init__(self):
        self.elements=[] # list of elements on an island
        self.name=None # string (if T1,T2 combines an island, name=island_1_2)
        self.child=[] # list of child of an island
        self.element_names=[] #list of layout component ids of elements
        self.child_names=[] #list of layout component ids of child
        self.mesh_nodes=[]#list of MeshNode objects
        self.elements_v=[]# list of elements in vertical corner stitch on an island
        self.rectangles=[] # list of elements in rectangle objects
        #self.points = []  # list of all points on an island
        #self.boundary_points = {'N': [], 'S': [], 'E': [],'W': []}  # dictionary of boundary points, where key= direction, value=list of points



    def print_island(self,plot=False,size=None):
        print "Name", self.name
        print "Num_elements", len(self.elements)
        for i in range(len(self.elements)):
            print self.elements[i]
        if len(self.child)>0:
            print "Num_child", len(self.child)
            for i in range(len(self.child)):
                print self.child[i]
        if len(self.mesh_nodes)>0:
            if plot==True:
                self.plot_mesh_nodes(size=size)
            else:
                print "Nodes_num", len(self.mesh_nodes)
                for i in range(len(self.mesh_nodes)):
                    print "id:", self.mesh_nodes[i].node_id, "pos", self.mesh_nodes[i].pos

        '''
        if len(self.points)>0:
            print "All_points_num",len(self.points)
            print "All_boundaries",self.boundary_points
            all_points=self.points
            all_boundaries=[]
            for k,v in self.boundary_points.items():
                all_boundaries+=v
            if plot:
                for point in all_points:
                    if point in all_boundaries:
                        all_points.remove(point)
                self.plot_points(all_points,all_boundaries,size)
        '''

    def plot_points(self,all_points,all_boundaries,size=None):
        s = set(tuple(x) for x in all_points)
        print len(all_points)
        x, y = zip(*s)

        # plt.axis([0, 30, 0, 42])
        # plt.show()
        s = set(tuple(x) for x in all_boundaries)
        #print len(all_boundaries)
        x2, y2 = zip(*s)
        # plt.axis([0, 30, 0, 42])
        # plt.show()

        plt.scatter(x, y,s=10,c='b')
        plt.scatter(x2, y2,s=30,c='r')
        if size==None:
            plt.axis([0, 100, 0, 100])
        else:
            plt.axis([0, size[0], 0, size[1]])
        plt.show()

    def plot_mesh_nodes(self,size=None):
        all_points=[]
        all_boundaries=[]
        print "Mesh_nodes_num",len(self.mesh_nodes)
        for node in self.mesh_nodes:
            if len(node.b_type)==0:
                all_points.append(node.pos)
            else:
                all_boundaries.append(node.pos)

        s = set(tuple(x) for x in all_points)
        print len(all_points)
        x, y = zip(*s)

        # plt.axis([0, 30, 0, 42])
        # plt.show()
        s = set(tuple(x) for x in all_boundaries)
        # print len(all_boundaries)
        x2, y2 = zip(*s)
        # plt.axis([0, 30, 0, 42])
        # plt.show()

        plt.scatter(x, y, s=10, c='b')
        #plt.text(x + .03, y + .03, word, fontsize=9)
        plt.scatter(x2, y2, s=30, c='r')
        if size == None:
            plt.axis([0, 100, 0, 100])
        else:
            plt.axis([0, size[0], 0, size[1]])
        plt.show()



class MeshNode():
    def __init__(self,node_id=None,type=None,b_type=[],pos=None):
        self.node_id = node_id
        self.type = type  # Node type
        self.b_type = []  # if type is boundary this will tell if it is N,S,E,W
        self.pos = pos  # Node Position (x , y ,z)




