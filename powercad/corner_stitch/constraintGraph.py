from sets import Set
import numpy as np
import constraint
import networkx as nx
from matplotlib import pylab
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import copy
from random import randint
import scipy as sp


class constraintGraph:
    """
    the graph representation of constraints pertaining to cells and variables, informed by several different 
    sources
    """

    def __init__(self, vertices, edges):
        """
        create from a given set of edges and vertices
        vertexMatrix is a 2d list n vertices long that shows the connectivity between the vertices
        edges is just a set of edges
        zeroDimensionList is where, independent of orientation, the list index corresponds to the graph's orientation
        zero dimension representation. For example, in a very simple horizontally oriented 30 x30 plane,
        where the only cell has a lower left corner of 5,15 and an upper right corner of 10, 25, zeroDimensionList will 
        be as follows: [0]:0, [1]:5, [2]:10, [3]:30. Notice that it is arranged in increasing order, and we are only 
        concerned with the x values, since this is horizontally oriented.
        """
        self.vertexMatrixh = int[len(vertices)][len(vertices)]
        self.vertexMatrixv = int[len(vertices)][len(vertices)]
        self.edges = edges
        self.zeroDimensionList = []

    def __init__(self, name1, name2):
        """
        Default constructor
        """
        # self.vertexMatrixh = None
        # self.vertexMatrixv = None
        # self.vertexMatrixh = int[][len(vertices)]
        # self.vertexMatrixv = int[len(vertices)][len(vertices)]
        self.edgesv = []  ### saves initial vertical constraint graph edges (without adding missing edges)
        self.edgesh = []  ### saves initial horizontal constraint graph edges (without adding missing edges)
        self.edgesv_new = []  ###saves vertical constraint graph edges (with adding missing edges)
        self.edgesh_new = []  ###saves horizontal constraint graph edges (with adding missing edges)
        # self.zeroDimensionList = []
        self.zeroDimensionListh = []  ### All X cuts of tiles
        self.zeroDimensionListv = []  ### All Y cuts of tiles
        # self.newXlocation=[]
        # self.newYlocation = []
        self.NEWXLOCATION = []  ####Array of all X locations after optimization
        self.NEWYLOCATION = []  ####Array of all Y locations after optimization
        self.name1 = name1
        self.name2 = name2
        self.paths_h = []  ### all paths in HCG from leftmost node to right most node
        self.paths_v = []  ### all paths in VCG from bottom most node to top most node

        self.special_location_x = []
        self.special_location_y = []
        self.special_cell_id_h = []
        self.special_cell_id_v = []
        self.special_edgev = []
        self.special_edgeh = []

    '''
    def getVertexMatrixh(self):
        return self.vertexMatrixh
    def getVertexMatrixv(self):
        return self.vertexMatrixv
    '''

    def getNeighbors(self, vertex):
        """
        return the edge types and neighbors of the vertex passed in
        vertexMatrix shows the connectivity between the vertices, it is a 2d list n vertices long
        edges is just a set of edges
        zeroDimensionList is where, independent of orientation, the list index corresponds to the graph's orientation
        zero dimension representation. For example, in a very simple horizontally oriented 30 x30 plane,
        where the only cell has a lower left corner of 5,15 and an upper right corner of 10, 25, zeroDimensionList will 
        be as follows: [0]:0, [1]:5, [2]:10, [3]:30. Notice that it is arranged in increasing order, and we are only 
        concerned with the x values, since this is horizontally oriented.

        """
        return

    def getEdgeType(self, v1, v2):
        """
        return the edge type from v1 to v2. If negative, then the edge type is from v2 to v1
        """
        return

    def graphFromLayer(self, cornerStitch_h, cornerStitch_v):
        """
        given a cornerStitch, construct a constraint graph detailing the dependencies of
        one dimension point to another
        """
        self.dimListFromLayer(cornerStitch_h, cornerStitch_v)
        # self.matrixFromDimList()
        self.setEdgesFromLayer(cornerStitch_h, cornerStitch_v)

    '''
    def matrixFromDimList(self):
        """
        initializes a N x N matrix of 0's as self's matrix object
        """
        #if cornerStitch.orientation == 'v':
        #n = len(self.zeroDimensionList)

        n1 = len(self.zeroDimensionListh)
        n2= len(self.zeroDimensionListv)
        self.vertexMatrixh=[[[] for i in range(n1)] for j in range(n1)]
        self.vertexMatrixv = [[[] for i in range(n2)] for j in range(n2)]
        #self.vertexMatrixh = np.zeros((n1, n1), np.int8)
        #self.vertexMatrixv = np.zeros((n2, n2), np.int8)


    def printVM(self,name):
        f = open(name, 'w')

        for i in self.vertexMatrixh:
            print >> f, i
        return
     '''

    def printVM(self, name1, name2):
        f1 = open(name1, 'w')
        # for k, v in self.vertexMatrixh.iteritems():
        # print >>f1,k, v
        for i in self.vertexMatrixh:
            print >> f1, i

        f2 = open(name2, 'w')
        # for k, v in self.vertexMatrixv.iteritems():
        # print >>f2,k, v
        for i in self.vertexMatrixv:
            print >> f2, i
        return

    def printZDL(self):
        index = 0
        for i in self.zeroDimensionList:
            print index, ": ", i
            index += 1

    '''
    def merge_dicts(self, dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        #print result
        return result
    '''
    """
    def setEdgesFromLayer(self, cornerStitch):

        #given a cornerStitch and orientation, set the connectivity matrix of this constraint graph


        if cornerStitch.orientation == 'v':
            print"stitchlist"
            for rect in cornerStitch.stitchList:
                origin = self.zeroDimensionList.index(rect.cell.y)
                # print"origin-",origin
                dest = self.zeroDimensionList.index(rect.getNorth().cell.y)
                self.vertexMatrix[origin][dest] = rect.getHeight()
                if rect.cell.getType() == "EMPTY":
                    self.edges.append(Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest)))
                elif rect.cell.getType() == "SOLID":

                    self.edges.append(Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest)))


        elif cornerStitch.orientation == 'h':
            print"stitchlist-h"
            for rect in cornerStitch.stitchList:
                origin = self.zeroDimensionList.index(rect.cell.x)
                # print"origin-",origin
                dest = self.zeroDimensionList.index(rect.getEast().cell.x)
                self.vertexMatrix[origin][dest] = rect.getWidth()
                if rect.cell.getType() == "EMPTY":
                    self.edges.append(Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest)))
                elif rect.cell.getType() == "SOLID":
                    self.edges.append(Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest)))
            #####draw graph
    """

    # print"stitchList=", cornerStitch.stitchList


    def setEdgesFromLayer(self, cornerStitch_h, cornerStitch_v):
        # self.vertexMatrixh=defaultdict(lambda: defaultdict(list))
        # self.vertexMatrixv = defaultdict(lambda: defaultdict(list))
        n1 = len(self.zeroDimensionListh)
        n2 = len(self.zeroDimensionListv)
        self.vertexMatrixh = [[[] for i in range(n1)] for j in range(n1)]
        self.vertexMatrixv = [[[] for i in range(n2)] for j in range(n2)]
        for rect in cornerStitch_v.stitchList:

            if rect.cell.type == "SOLID":
                origin = self.zeroDimensionListh.index(rect.cell.x)
                dest = self.zeroDimensionListh.index(rect.getEast().cell.x)
                id = rect.cell.id
                East = rect.getEast().cell.id
                West = rect.getWest().cell.id
                #print id,East,West,rect.cell.x,rect.cell.y
                e = Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest), "1", id, East, West)
                # print"e=", Edge.getEdgeWeight(e,origin,dest)
                # self.edgesv.append(e)
                self.edgesh.append(
                    Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest), "1", id, East=East,West=West))
                # self.vertexMatrixh[origin][dest].append((rect.getWidth()))
                self.vertexMatrixh[origin][dest].append(Edge.getEdgeWeight(e, origin, dest))

                # self.edgesh.append(Edge(origin, dest, constraint.constraint(rect.getWidth(), origin, dest)))#
            elif rect.cell.type == "EMPTY":
                origin = self.zeroDimensionListv.index(rect.cell.y)
                dest = self.zeroDimensionListv.index(rect.getNorth().cell.y)
                e = Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest), "0", None, None, None)
                # self.edgesv.append(e)
                self.edgesv.append(
                    Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest), "0", None, None, None))
                self.vertexMatrixv[origin][dest].append(Edge.getEdgeWeight(e, origin, dest))
                # self.edgesv.append(Edge(origin, dest, constraint.constraint( rect.getHeight(), origin, dest)))

        for rect in cornerStitch_h.stitchList:
            if rect.cell.type == "SOLID":
                origin = self.zeroDimensionListv.index(rect.cell.y)
                dest = self.zeroDimensionListv.index(rect.getNorth().cell.y)
                id = rect.cell.id
                North = rect.getNorth().cell.id
                South = rect.getSouth().cell.id

                # print id,North,South
                e = Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest), "1", id, North, South)
                # self.edgesh.append(e)
                self.edgesv.append(
                    Edge(origin, dest, constraint.constraint(1, 'minWidth', origin, dest), "1", id, North=North,
                         South=South))
                # self.vertexMatrixv[origin][dest] = rect.getHeight()
                self.vertexMatrixv[origin][dest].append(e.getEdgeWeight(origin, dest))
                # self.edgesv.append(Edge(origin, dest, constraint.constraint(rect.getHeight() , origin, dest)))#

            elif rect.cell.type == "EMPTY":
                origin = self.zeroDimensionListh.index(rect.cell.x)
                dest = self.zeroDimensionListh.index(rect.getEast().cell.x)
                e = Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest), "0", None, None, None)
                # self.edgesh.append(e)
                self.edgesh.append(
                    Edge(origin, dest, constraint.constraint(0, 'minWidth', origin, dest), "0", None, None, None))
                # self.vertexMatrixh[origin][dest] = rect.getWidth()
                self.vertexMatrixh[origin][dest].append(e.getEdgeWeight(origin, dest))
                ##'minWidth'

                # self.edgesh.append(Edge(origin, dest, constraint.constraint( rect.getWidth(), origin, dest)))
        # print "verh=",dict(self.vertexMatrixh)
        # print(dict.__repr__(self.vertexMatrixh))
        # print "verv=", self.vertexMatrixv
        dictList1 = []
        # print self.edgesh
        self.edgesh_new = copy.deepcopy(self.edgesh)
        # print self.edgesh_new
        for foo in self.edgesh_new:
            # print foo.getEdgeDict()
            dictList1.append(foo.getEdgeDict())
        # print dictList1

        ######
        d = defaultdict(list)
        for i in dictList1:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d[k].append(v)
        edge_labels1 = d
        # print d
        # print d.keys()
        # for u,v in d.keys():
        # print u,v

        nodes = [x for x in range(len(self.zeroDimensionListh))]
        # G2.add_nodes_from(nodes)
        ### adding missing edges for evaluation
        for i in range(len(nodes) - 1):
            if (nodes[i], nodes[i + 1]) not in d.keys():
                # d[nodes[i], nodes[i + 1]] = [1]
                self.edgesh_new.append(
                    Edge(nodes[i], nodes[i + 1], constraint.constraint(0, 'minWidth', nodes[i], nodes[i + 1]), "0",
                         None))
        dictList = []
        self.edgesv_new = copy.deepcopy(self.edgesv)
        for foo in self.edgesv_new:
            dictList.append(foo.getEdgeDict())
        d1 = defaultdict(list)
        for i in dictList:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d1[k].append(v)
        edge_labels = d1
        # print d1
        nodes_v = [x for x in range(len(self.zeroDimensionListv))]
        # G1.add_nodes_from(nodes)
        ### adding missing edges for evaluation
        for i in range(len(nodes_v) - 1):
            if (nodes_v[i], nodes_v[i + 1]) not in d1.keys():
                # d[nodes[i], nodes[i + 1]] = [1]
                self.edgesv_new.append(
                    Edge(nodes_v[i], nodes_v[i + 1], constraint.constraint(0, 'minWidth', nodes_v[i], nodes_v[i + 1]),
                         "0", None))
                # print "edge",self.edgesv_new

    '''
    def dimListFromLayer(self, cornerStitch):
        """
        generate the zeroDimensionList from a cornerStitch         
        """
        pointSet = Set()  # this is a set of zero dimensional line coordinates, (e.g. x0, x1, x2, etc.)
        if cornerStitch.orientation == 'v':  # if orientation is vertical, add all unique y values for cells
            for rect in cornerStitch.stitchList:
                pointSet.add(rect.cell.y)
            pointSet.add(cornerStitch.northBoundary.cell.y)

        elif cornerStitch.orientation == 'h':  # same for horizontal orientation
            for rect in cornerStitch.stitchList:
                pointSet.add(rect.cell.x)

            pointSet.add(cornerStitch.eastBoundary.cell.x)
        setToList = list(pointSet)
        setToList.sort()

        self.zeroDimensionList = setToList

        ####

        # print"ZDL=",len(setToList)
     '''
    '''####final
    def dimListFromLayer(self, cornerStitch_h,cornerStitch_v):
        """
        generate the zeroDimensionList from a cornerStitch         
        """
        pointSet = Set() #this is a set of zero dimensional line coordinates, (e.g. x0, x1, x2, etc.)
        #if cornerStitch.orientation == 'v':  # if orientation is vertical, add all unique y values for cells
        for rect in cornerStitch_v.stitchList:
                pointSet.add(rect.cell.y)

        pointSet.add(cornerStitch_v.northBoundary.cell.y)  # this won't be included in the normal list, so we do it here
        setToList = list(pointSet)
        setToList.sort()

        self.zeroDimensionListvy = setToList
        print"vy=", setToList
        pointSet = Set()
        for rect in cornerStitch_v.stitchList:
                pointSet.add(rect.cell.x)

        pointSet.add(cornerStitch_v.eastBoundary.cell.x)  # this won't be included in the normal list, so we do it here
        setToList = list(pointSet)
        setToList.sort()
        self.zeroDimensionListvx = setToList
        print"vx=", setToList
        pointSet = Set()
        #elif cornerStitch.orientation == 'h':  # same for horizontal orientation
        for rect in cornerStitch_h.stitchList:
                pointSet.add(rect.cell.x)
        pointSet.add(cornerStitch_h.eastBoundary.cell.x)
        setToList = list(pointSet)
        setToList.sort()
        self.zeroDimensionListhx = setToList  # setting the list of orientation values to an ordered list
        print"hx=", setToList


        pointSet = Set()
        for rect in cornerStitch_h.stitchList:
                pointSet.add(rect.cell.y)

        pointSet.add(cornerStitch_h.northBoundary.cell.y)  # this won't be included in the normal list, so we do it here
        setToList = list(pointSet)
        setToList.sort()

        self.zeroDimensionListhy = setToList
        print"hy=", setToList


    '''

    def dimListFromLayer(self, cornerStitch_h, cornerStitch_v):
        """
        generate the zeroDimensionList from a cornerStitch
        """

        pointSet_v = Set()  # this is a set of zero dimensional line coordinates, (e.g. x0, x1, x2, etc.)
        # if cornerStitch.orientation == 'v':  # if orientation is vertical, add all unique y values for cells
        for rect in cornerStitch_v.stitchList:
            pointSet_v.add(rect.cell.y)

        pointSet_v.add(
            cornerStitch_v.northBoundary.cell.y)  # this won't be included in the normal list, so we do it here
        for rect in cornerStitch_h.stitchList:
            pointSet_v.add(rect.cell.y)

        pointSet_v.add(cornerStitch_h.northBoundary.cell.y)
        setToList_v = list(pointSet_v)
        setToList_v.sort()
        # self.zeroDimensionListvy = setToList
        self.zeroDimensionListv = setToList_v
        # print self.zeroDimensionListv
        # print"vy=", setToList
        pointSet_h = Set()
        for rect in cornerStitch_v.stitchList:
            pointSet_h.add(rect.cell.x)
        pointSet_h.add(
            cornerStitch_v.eastBoundary.cell.x)  # this won't be included in the normal list, so we do it here
        for rect in cornerStitch_h.stitchList:
            pointSet_h.add(rect.cell.x)
        pointSet_h.add(cornerStitch_h.eastBoundary.cell.x)
        setToList_h = list(pointSet_h)
        setToList_h.sort()
        self.zeroDimensionListh = setToList_h
        # print self.zeroDimensionListh
        # print"vx=", setToList

    '''
    def toposort(self,graph):


        data = defaultdict(set)
        for x, y in graph.items():
            for z in y:
                data[z[0]].add(x)

        # Ignore self dependencies.
        for k, v in data.items():
            v.discard(k)
        # Find all items that don't depend on anything.
        extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
        # Add empty dependences where needed
        data.update({item: set() for item in extra_items_in_deps})
        while True:
            ordered = set(item for item, dep in data.items() if not dep)
            if not ordered:
                break
            yield ordered
            data = {item: (dep - ordered)
                    for item, dep in data.items()
                    if item not in ordered}
        assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())
    '''

    def cgToGraph_h(self, name):
        G2 = nx.MultiDiGraph()
        dictList1 = []
        # print self.edgesh
        for foo in self.edgesh:
            # print foo.getEdgeDict()
            dictList1.append(foo.getEdgeDict())
        # print dictList1

        ######
        d = defaultdict(list)
        for i in dictList1:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d[k].append(v)
        edge_labels1 = d
        # print d.keys()
        # for u,v in d.keys():
        # print u,v

        nodes = [x for x in range(len(self.zeroDimensionListh))]
        G2.add_nodes_from(nodes)
        '''
        ### adding missing edges for evaluation
        for i in range(len(nodes)-1):
            if (nodes[i],nodes[i+1]) not in d.keys():
                d[nodes[i],nodes[i+1]]=[1]
                #self.edgesh.append(Edge(nodes[i], nodes[i+1], constraint.constraint(0, 'minWidth', nodes[i], nodes[i+1])))
        '''
        # print nodes[i],nodes[i+1]
        ####
        # print G2.nodes()
        # print G2.edges()
        # print"label=", edge_labels1
        label = []
        edge_label = []
        for branch in edge_labels1:
            lst_branch = list(branch)
            data = []

            for internal_edge in edge_labels1[branch]:
                # print lst_branch[0], lst_branch[1]
                # print internal_edge
                # if (lst_branch[0], lst_branch[1], internal_edge) not in data:
                data.append((lst_branch[0], lst_branch[1], internal_edge))
                label.append({(lst_branch[0], lst_branch[
                    1]): internal_edge})  #####{(source,dest):[weight,type,id,East cell id,West cell id]}
                edge_label.append({(lst_branch[0], lst_branch[1]): internal_edge[0]})  ### {(source,dest):weight}
                '''
                if (lst_branch[0], lst_branch[1], {'route': internal_edge}) not in data:
                data.append((lst_branch[0], lst_branch[1], {'route': internal_edge}))
                label.append({(lst_branch[0], lst_branch[1]): internal_edge})
                '''
            # print data
            G2.add_weighted_edges_from(data)
        d = defaultdict(list)
        # print label
        for i in edge_label:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d[k].append(v)
        edge_labels1 = d
        self.drawGraph_h(name, G2, edge_labels1)
        #### New graph with missing edges
        G3 = nx.MultiDiGraph()
        dictList3 = []
        # print self.edgesh
        for foo in self.edgesh_new:
            # print foo.getEdgeDict()
            dictList3.append(foo.getEdgeDict())
        # print dictList1

        ######
        d3 = defaultdict(list)
        for i in dictList3:
            k, v = list(i.items())[0]
            d3[k].append(v)
        edge_labels3 = d3
        # print d.keys()
        # for u,v in d.keys():
        # print u,v

        nodes = [x for x in range(len(self.zeroDimensionListh))]
        G3.add_nodes_from(nodes)

        # print"label=", edge_labels1
        label3 = []
        label5 = []
        for branch in edge_labels3:
            lst_branch = list(branch)
            data = []

            for internal_edge in edge_labels3[branch]:
                # print lst_branch[0], lst_branch[1]
                # print internal_edge[0]
                # if (lst_branch[0], lst_branch[1], internal_edge) not in data:
                data.append((lst_branch[0], lst_branch[1], internal_edge))
                label3.append({(lst_branch[0], lst_branch[
                    1]): internal_edge})  #####{(source,dest):[weight,type,id,East cell id,West cell id]}
                label5.append({(lst_branch[0], lst_branch[1]): internal_edge[0]})  ######{(source,dest):weight}
                '''
                if (lst_branch[0], lst_branch[1], {'route': internal_edge}) not in data:
                data.append((lst_branch[0], lst_branch[1], {'route': internal_edge}))
                label.append({(lst_branch[0], lst_branch[1]): internal_edge})
                '''
            # print data
            G3.add_weighted_edges_from(data)
        #############################################################
        label4 = copy.deepcopy(label3)
        # print "l3",label3
        D = []
        # print label3
        for i in label4:
            # print i.values()[0][1]
            if i.values()[0][1] == "1":
                D.append(i)

        # print D, len(D)
        W_total = []
        for i in range(5):
            W = []
            for i in range(len(D)):
                # W.append(randint(2, 10))
                W.append(randint(2, 10))
            W_total.append(W)
        # print "W_T=",W_total

        NewD = []
        for i in range(len(D)):
            NewD.append(D[i].keys()[0])
        Space = []
        for i in label4:
            if i.values()[0][1] == "0":
                Space.append(i)
        # print Space
        ############################ Varying Spacing
        S_total = []
        for i in range(5):
            S = []
            for i in range(len(Space)):
                S.append(randint(1, 3))
            S_total.append(S)
        # print "S_T=", S_total
        NewS = []
        for i in range(len(Space)):
            NewS.append(Space[i].keys()[0])
        # print "NEWD=", NewS
        new_labelw = []
        for j in range(len(W_total)):
            labelnew = []
            for i in range(len(NewD)):
                newdict = {NewD[i]: W_total[j][i]}
                labelnew.append(newdict)
                # labelnew.extend(Space)
            new_labelw.append(labelnew)
        # print new_labelw
        new_labels = []
        for j in range(len(S_total)):
            labelnew = []
            for i in range(len(NewS)):
                newdict = {NewS[i]: S_total[j][i]}
                labelnew.append(newdict)
            new_labels.append(labelnew)

        # print new_labels
        new_label = []
        for i in range(len(new_labels)):
            new_labels[i].extend(new_labelw[i])
            new_label.append(new_labels[i])
        # new_label
        # print "l4=", label4

        for i in range(len(new_label)):
            #
            new_label[i].extend(label5)
            # print new_label[i]

        # print new_label
        ################################
        '''
        new_label=[]
        for j in range(len(W_total)):
            labelnew=[]
            for i in range(len(NewD)):
                newdict = {NewD[i]:W_total[j][i]}
                labelnew.append(newdict)
                labelnew.extend(Space)
            new_label.append(labelnew)
        '''
        # print len(new_label)
        # for i in new_label:
        # print i
        D_3 = []
        for j in range(len(new_label)):
            d[j] = defaultdict(list)
            # print d[j]
            # print"N=", new_label[j]
            for i in new_label[j]:
                # print i
                # print new_label[j]
                k, v = list(i.items())[
                    0]  # an alternative to the single-iterating inner loop from the previous solution

                # print k,v
                d[j][k].append(v)
            # print d[j]
            # print "d[j]",d[j]


            D_3.append(d[j])

        # print len(D_3),D_3
        ###############################################################
        d3 = defaultdict(list)
        for i in label3:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d3[k].append(v)
        edge_labels3 = d3
        # print len(edge_labels3)


        #### Storing edge data in (u,v,w) format in a file(begin)
        z = [(u, v, d['weight']) for u, v, d in G3.edges(data=True)]
        f1 = open(name, 'w')
        for i in z:
            # print i
            print >> f1, i
        ######## Storing edge data in (u,v,w) format in a file(end)

        ######## Finds all possible paths from start vertex to end vertex(begin)
        n = list(G3.nodes())
        self.FindingAllPaths_h(G3, n[0], n[-1])
        '''
        f2 = open("paths_h.txt", "rb")
        for line in f2.read().splitlines():  # considering each line in file
            self.paths_h.append(line)
        paths=[json.loads(y) for y in self.paths_h]
        '''
        paths = self.paths_h
        print paths
        #### (end)
        #### finding new location of each vertex in longest paths (begin)########
        '''
        l = []
        for path in paths:
            l.append(len(path))
        L = max(l)
        for path in paths:
            if (len(path)) == L:
                p = path
        longest_path = [p] ###finds the path which one has maximum nodes
        for j in range(len(paths)):
            if (not (set(paths[j]).issubset(set(p)))):
                if (paths[j] not in longest_path):
                    longest_path.append(paths[j])
        print "LONG=",longest_path ### Finds all unique paths so that all nodes are covered.
        '''

        ##############TESTING
        # NEWXLOCATION=[]
        loct = []
        for k in range(len(D_3)):
            new_Xlocation = []

            dist = {}
            distance = set()  ###stores (u,v,w)where u=parent,v=child,w=cumulative weight from source to child
            location = set()  ###No use
            position_k = {}  ## stores {node:location}
            for i in range(len(paths)):
                path = paths[i]
                # print path
                for j in range(len(path)):
                    node = path[j]
                    # print "node=",path[-1]
                    if j > 0:
                        pred = path[j - 1]
                    else:
                        pred = node
                    # print node, pred
                    if node == 0:
                        dist[node] = (0, pred)
                        # distance.append((pred,node,0))
                        distance.add((pred, node, 0))
                        # location.add((node,0))
                        key = node
                        position_k.setdefault(key, [])
                        position_k[key].append(0)
                    # elif node== path[-1]:

                    else:

                        pairs = (dist[pred][0] + max(D_3[k][(pred, node)]), pred)
                        # print  max(edge_labels1[(pred, node)])
                        dist[node] = pairs
                        # print dist[node][0]

                        distance.add((pred, node, pairs[0]))
                        # print pairs[0]
                        # if location[node]<pairs[0]:
                        location.add((node, pairs[0]))
                        key = node
                        position_k.setdefault(key, [])
                        position_k[key].append(pairs[0])
                        # print position_k
            loc_i = {}
            for key in position_k:
                loc_i[key] = max(position_k[key])
                # if key==n[-2]:
                # loc_i[key] = 19
                # elif key==n[-1]:
                # loc_i[key] = 20
                new_Xlocation.append(loc_i[key])
            loct.append(loc_i)

            self.NEWXLOCATION.append(new_Xlocation)
        f3 = open(name + "location_x.txt", 'wb')
        for i in loct:
            # print i
            print >> f3, i
        print"LOC=", loct, self.NEWXLOCATION
        Graph_pos_h = []
        for i in range(len(loct)):
            dist = {}
            for node in loct[i]:
                key = node

                dist.setdefault(key, [])
                dist[node].append(node)
                dist[node].append(loct[i][node])
            Graph_pos_h.append(dist)
        # print Graph_pos_h
        # print"LOC=",Graph_pos_h
        self.drawGraph_h_new(name, G3, D_3, Graph_pos_h)

        ######################### Handling special edges independently
        '''
        for i in range(len(self.zeroDimensionListh)):
            for j in range(len(self.zeroDimensionListh)):
                if (len(self.vertexMatrixh[i][j])>1):
                    for k in self.vertexMatrixh[i][j]:
                        if k[1]=='1':
                            print i,j
        '''

        special_edge_h = []  ### list of edges which are of type"1"  and in same nodes

        for i in range(len(self.edgesh_new) - 1):
            for j in range(len(self.edgesh_new) - 1):
                if j == i:
                    continue
                if self.edgesh_new[i].source == self.edgesh_new[j].source and self.edgesh_new[i].dest == \
                        self.edgesh_new[j].dest and self.edgesh_new[i].type == self.edgesh_new[j].type == '1':
                    if self.edgesh_new[i] not in special_edge_h:
                        special_edge_h.append(self.edgesh_new[i])
                    if self.edgesh_new[j] not in special_edge_h:
                        special_edge_h.append(self.edgesh_new[j])

                        # print special_edge_h
                        # for foo in special_edge_h:
                        # print "hfo", foo.getEdgeDict()
        #for foo in special_edge_h:
            #print "hfo", foo.getEdgeDict()
        ######## Removing all of those edges which have connected neighbor edges of type 1 incoming to source or outgoing of dest
        EAST = []
        WEST = []
        for edge in special_edge_h:
            EAST.append(edge.East)
            WEST.append(edge.West)
        #print EAST,WEST
        for edge in special_edge_h:
            # print "src",edge.source
            for ed in self.edgesh_new:
                # print "dest=",ed.dest
                if ed.dest == edge.source and ed.type == '1':
                    # print edge.source, edge.dest
                    # if edge.West == ed.id:
                    if edge.West  in WEST:
                        special_edge_h = [x for x in special_edge_h if x != edge]
                        # special_edge_v.remove(edge)
                elif ed.source == edge.dest and ed.type == '1':
                    # print edge.source, edge.dest
                    # if edge.East == ed.id:
                    if edge.East  in EAST:
                        special_edge_h = [x for x in special_edge_h if x != edge]
                        # special_edge_v.remove(edge)
                        # for foo in special_edge_h:
                        # print "foh", foo.getEdgeDict()
        #print "len=", len(special_edge_h)
        #for edge in special_edge_h:
            #print edge.source,edge.dest,edge.id,edge.type
        # self.special_edgeh = copy.deepcopy(special_edge_h)
        self.special_edgeh = copy.deepcopy(special_edge_h)
        for i in range(len(special_edge_h)):
            self.special_cell_id_h.append(special_edge_h[i].id)

        if len(special_edge_h) > 0:
            # W_max = []
            # OFFSET=[]


            for i in range(len(loct)):
                ######### Calculating offset values and determining new location of edge's source and dest node
                # for i in loct[i]:
                # print loct[i]
                special_location_x = []
                Wmax = []
                for edge in special_edge_h:
                    w = loct[i][edge.dest] - loct[i][edge.source]
                    # print w
                    Wmax.append(w)
                offset1 = []
                offset2 = []
                for j in range(len(Wmax)):
                    avg = (Wmax[j] - 2) / 2
                    offset_1 = randint(0, avg)
                    offset_2 = randint(0, avg)
                    offset1.append(offset_1)
                    offset2.append(offset_2)
                # print offset1, offset2
                # OFFSET.append([offset1, offset2])
                for j in range(len(special_edge_h)):
                    location = {}
                    key = special_edge_h[j].id
                    location.setdefault(key, [])
                    # print"id=",special_edge_h[j].id
                    # print loct[i]
                    location[key].append(loct[i][special_edge_h[j].source] + offset1[j])
                    location[key].append(loct[i][special_edge_h[j].dest] - offset2[j])
                    location[key].append(Wmax[j] - (offset1[j] + offset2[j]))
                    special_location_x.append(location)
                    # print'lo',special_location_x
                self.special_location_x.append(
                    special_location_x)  ######[[{special cell id_1:[x1,x2,width]},{special cell id_2:[x1,x2,width]}],[{special cell id_1:[x1,x2,width]},{special cell id_2:[x1,x2,width]},......]]
            print self.special_location_x

        '''

        ###############       Without optimization
        dist = {}
        distance =set()###stores (u,v,w)where u=parent,v=child,w=cumulative weight from source to child
        location=set()###No use
        position={}## stores {node:location}
        for i in range(len(paths)):
            path = paths[i]
            #print path
            for j in range(len(path)):
                node = path[j]
                if j > 0:
                    pred = path[j - 1]
                else:
                    pred = node
                #print node, pred
                if node == 0:
                    dist[node] = (0, pred)
                    # distance.append((pred,node,0))
                    distance.add((pred, node, 0))
                    #location.add((node,0))
                    key=node
                    position.setdefault(key,[])
                    position[key].append(0)
                else:

                    pairs = (dist[pred][0] + max(edge_labels3[(pred, node)]), pred)
                    #print  max(edge_labels1[(pred, node)])
                    dist[node] = pairs
                    #print dist[node][0]

                    distance.add((pred, node, pairs[0]))
                    #print pairs[0]
                    #if location[node]<pairs[0]:
                    location.add((node,pairs[0]))
                    key = node
                    position.setdefault(key, [])
                    position[key].append(pairs[0])
            #print position
        loc={}
        for key in position:
            loc[key]=max(position[key])
            self.newXlocation.append(loc[key])
        print"LOC=", loc,self.newXlocation
        dist={}
        for node in loc:
            key = node

            dist.setdefault(key, [])
            dist[node].append(node)
            dist[node].append(loc[node])
        self.drawGraph_h_new(name, G3, edge_labels3, dist)  ### Drawing HCG

        #print dist
        '''
        '''
        #####Final Plot to show locations of new position(No need)
        G = nx.DiGraph()
        keys = [(0, node) for node in G2.nodes()]
        nodelist = [node for node in G2.nodes()]
        zeros = np.zeros(len(nodelist))
        values = [loc[node] for node in loc]
        data = map(lambda x, y, z: (x, y, z), zeros, nodelist, values)
        G.add_weighted_edges_from(data)
        val = map(lambda x, y: (x, y), G2.nodes(), values)
        pos = nx.shell_layout(G)
        labels = dict(zip(keys, values))
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_labels(G, pos)
        nx.draw(G, pos, node_color='red', node_size=300, edge_color='black')
        plt.savefig(self.name1 + 'loc_h.png')
        plt.close()
        '''

        #### finding new location of each vertex in longest paths (end)########

    def FindingAllPaths_h(self, G, start, end):
        """
        This should call subroutines for edge and vertex reduction, to pare the constraint graph down to its
        minimum form
        """
        # f1 = open("paths_h.txt", 'w')
        visited = [False] * (len(G.nodes()))
        path = []

        self.printAllPaths_h(G, start, end, visited, path)

    def printAllPaths_h(self, G, start, end, visited, path):
        visited[start] = True
        path.append(start)

        # If current vertex is same as destination, then print
        # current path[]

        if start == end:
            saved_path = path[:]
            self.paths_h.append(saved_path)
            # for i in edge_labels1:
            # print >> f1, path



            # self.paths_h.append(path)
            # print "self.paths_h",self.paths_h

            # paths.append(path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex

            for i in G.neighbors(start):
                if visited[i] == False:
                    self.printAllPaths_h(G, i, end, visited, path)

        # Remove current vertex from path[] and mark it as unvisited

        path.pop()
        visited[start] = False

    def cgToGraph_v(self, name):
        G1 = nx.MultiDiGraph()
        dictList = []
        for foo in self.edgesv:
            dictList.append(foo.getEdgeDict())
        d = defaultdict(list)
        for i in dictList:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d[k].append(v)
        edge_labels = d
        nodes = [x for x in range(len(self.zeroDimensionListv))]
        G1.add_nodes_from(nodes)
        '''
        ### adding missing edges for evaluation
        for i in range(len(nodes)-1):
            if (nodes[i],nodes[i+1]) not in d.keys():
                d[nodes[i],nodes[i+1]]=[1]
                #self.edgesv.append(Edge(nodes[i], nodes[i+1], constraint.constraint(0, 'minWidth', nodes[i], nodes[i+1])))
        ######
        '''
        label = []
        edge_label = []
        for branch in edge_labels:
            lst_branch = list(branch)
            data = []
            for internal_edge in edge_labels[branch]:
                # if (lst_branch[0], lst_branch[1],  internal_edge) not in data:
                data.append((lst_branch[0], lst_branch[1], internal_edge))
                # data.append((lst_branch[0], lst_branch[1], {'route': internal_edge}))
                label.append({(lst_branch[0], lst_branch[1]): internal_edge})
                edge_label.append({(lst_branch[0], lst_branch[1]): internal_edge[0]})
            G1.add_weighted_edges_from(data)

        d = defaultdict(list)
        for i in edge_label:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d[k].append(v)
        edge_labels = d
        # print len(d)
        self.drawGraph_v(name, G1, edge_labels)
        G4 = nx.MultiDiGraph()
        dictList4 = []
        for foo in self.edgesv_new:
            dictList4.append(foo.getEdgeDict())
        d4 = defaultdict(list)
        for i in dictList4:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d4[k].append(v)
        edge_labels4 = d4
        # print edge_labels4
        nodes = [x for x in range(len(self.zeroDimensionListv))]
        G4.add_nodes_from(nodes)
        '''
        ### adding missing edges for evaluation
        for i in range(len(nodes)-1):
            if (nodes[i],nodes[i+1]) not in d.keys():
                d[nodes[i],nodes[i+1]]=[1]
                #self.edgesv.append(Edge(nodes[i], nodes[i+1], constraint.constraint(0, 'minWidth', nodes[i], nodes[i+1])))
        ######
        '''
        label4 = []
        label6 = []
        for branch in edge_labels4:
            lst_branch = list(branch)
            data = []
            for internal_edge in edge_labels4[branch]:
                # if (lst_branch[0], lst_branch[1],  internal_edge) not in data:
                data.append((lst_branch[0], lst_branch[1], internal_edge))
                # data.append((lst_branch[0], lst_branch[1], {'route': internal_edge}))
                label4.append({(lst_branch[0], lst_branch[1]): internal_edge})
                label6.append({(lst_branch[0], lst_branch[1]): internal_edge[0]})
            G4.add_weighted_edges_from(data)
        #############################################################
        '''(One output figure with variable Y)
        label_4 = copy.deepcopy(label4)
        D = []
        # print label3
        for i in label_4:
            if i.values()[0] == 2:
                D.append(i)

        # print D, len(D)
        W_total = []
        for i in range(10):
            W = []
            for i in range(len(D)):
                W.append(randint(2, 10))
            W_total.append(W)
        print W_total
        NewD = []
        for i in range(len(D)):
            NewD.append(D[i].keys()[0])
        labelnew = []

        for i in range(len(NewD)):
            newdict = {NewD[i]: W_total[0][i]}
            labelnew.append(newdict)

        Space = []
        for i in label4:
            if i.values()[0] == 1:
                Space.append(i)
        print Space
        labelnew.extend(Space)
        print "labelnew", labelnew
        d_3 = defaultdict(list)
        for i in labelnew:
            k, v = list(i.items())[
                0]  # an alternative to the single-iterating inner loop from the previous solution
            d_3[k].append(v)
        edge_labels_3 = d_3
        print len(edge_labels_3)
        '''

        ###############################################################
        ##############################           OPTIMIZATION
        label_4 = copy.deepcopy(label4)
        D = []
        # print label3
        for i in label_4:
            if i.values()[0][1] == "1":
                D.append(i)

        # print D, len(D)
        W_total = []
        for i in range(5):
            W = []
            for i in range(len(D)):
                W.append(randint(2, 10))
            W_total.append(W)
        # print "W_T",W_total

        NewD = []
        for i in range(len(D)):
            NewD.append(D[i].keys()[0])
        # print "NEWD=",NewD
        Space = []
        for i in label_4:
            if i.values()[0][1] == "0":
                Space.append(i)
        ################### Varying spacing
        S_total = []
        for i in range(5):
            S = []
            for i in range(len(Space)):
                S.append(randint(1, 4))
            S_total.append(S)
        # print "S_T=", S_total
        NewS = []
        for i in range(len(Space)):
            NewS.append(Space[i].keys()[0])

        new_labelw = []
        for j in range(len(W_total)):
            labelnew = []
            for i in range(len(NewD)):
                newdict = {NewD[i]: W_total[j][i]}
                labelnew.append(newdict)
                # labelnew.extend(Space)
            new_labelw.append(labelnew)
        # print new_labelw
        new_labels = []
        for j in range(len(S_total)):
            labelnew = []
            for i in range(len(NewS)):
                newdict = {NewS[i]: S_total[j][i]}
                labelnew.append(newdict)
            new_labels.append(labelnew)

        # print new_labels
        new_label = []
        for i in range(len(new_labels)):
            new_labels[i].extend(new_labelw[i])
            new_label.append(new_labels[i])
        # print new_label
        # print "l4=",label4

        for i in range(len(new_label)):
            #
            new_label[i].extend(label6)
            # print new_label[i]

        # print "new_label",new_label





        ###########################
        # print Space
        '''
        new_label = []
        for j in range(len(W_total)):
            labelnew = []
            for i in range(len(NewD)):
                newdict = {NewD[i]: W_total[j][i]}
                labelnew.append(newdict)
                labelnew.extend(Space)
            new_label.append(labelnew)
        '''
        # print len(new_label)
        # for i in new_label:
        # print i
        D_3 = []
        for j in range(len(new_label)):
            d[j] = defaultdict(list)
            # print d[j]
            # print"N=", new_label[j]
            for i in new_label[j]:
                # print i
                # print new_label[j]
                k, v = list(i.items())[
                    0]  # an alternative to the single-iterating inner loop from the previous solution
                # print k,v
                d[j][k].append(v)
            # print d[j]
            # print "d[j]", d[j]

            D_3.append(d[j])

        # print "V=",len(D_3), D_3

        ############################
        d4 = defaultdict(list)
        for i in label4:
            k, v = list(i.items())[0]  # an alternative to the single-iterating inner loop from the previous solution
            d4[k].append(v)
        edge_labels4 = d4
        # print len(d4)

        z = [(u, v, d['weight']) for u, v, d in G4.edges(data=True)]
        f1 = open(name, 'w')
        for i in z:
            print >> f1, i
        # A = nx.adjacency_matrix(G1)


        # self.drawGraph_v(name, G1, edge_labels)### Drawing VCG
        #### Finding all possible paths from start vertex to end vertex
        n = list(G4.nodes())
        self.FindingAllPaths_v(G4, n[0], n[-1])
        '''
        f = open("paths_v.txt", "rb")
        for line in f.read().splitlines():  # considering each line in file
            self.paths_v.append(line)
        paths = [json.loads(y) for y in self.paths_v]
        '''
        paths = self.paths_v
        print paths
        '''
        for node in G1.nodes():
            print [v for u,v in G1.edges(node)]
            tree = nx.dfs_tree(G1,node)
            print"tree=",tree.edges()
        '''
        '''
        dist = {}  # stores {v : (length, u)}
        for v in nx.topological_sort(G1):
            print  G1.pred[v]
            #us = [(dist[u][0] + data.get(weight, default_weight), u)for u, data in G1.pred[v].items()]
            print  G1.pred[v].items()
            # Use the best predecessor if there is one and its distance is non-negative, otherwise terminate.
            maxu = max(us, key=lambda x: x[0]) if us else (0, v)
            dist[v] = maxu if maxu[0] >= 0 else (0, v)
        u = None
        v = max(dist, key=lambda x: dist[x][0])
        path = []
        while u != v:
            path.append(v)
            u = v
            v = dist[v][1]
        path.reverse()

        '''
        #### finding new location of each vertex in longest paths (begin)########
        '''
        l = []
        for path in paths:
            l.append(len(path))
        L = max(l)
        for path in paths:
            if (len(path)) == L:
                p = path
        longest_path = [p]
        for j in range(len(paths)):
            if (not (set(paths[j]).issubset(set(p)))):
                if (paths[j] not in longest_path):
                    longest_path.append(paths[j])
        print "long=", longest_path
        '''
        '''
        ########### Without optimization
        dist = {}
        distance =set()
        position = {}  ## stores {node:location}
        for i in range(len(paths)):
            path=paths[i]
            #print path
            for j in range(len(path)):
                node=path[j]
                if j>0:
                    pred=path[j-1]
                else:
                    pred=node
                if node==0:
                    dist[node]=(0,pred)
                    distance.add((pred, node, 0))
                    key = node
                    position.setdefault(key, [])
                    position[key].append(0)
                else:
                    pairs = (dist[pred][0] + max(edge_labels4[(pred, node)]), pred)
                    dist[node]=pairs
                    distance.add((pred, node, pairs[0]))
                    key = node
                    position.setdefault(key, [])
                    position[key].append(pairs[0])
            #print position
        loc = {}
        for key in position:
            loc[key] = max(position[key])
            self.newYlocation.append(loc[key])
        print"LOC=", loc,self.newYlocation

        dist = {}
        for node in loc:
            key = node

            dist.setdefault(key, [])
            dist[node].append(node)
            dist[node].append(loc[node])
        #print dist

        #### finding new location of each vertex in longest paths (end)########
        #### redraw graph with new position
        #print loc
        self.drawGraph_v_new(name, G4, edge_labels4, dist)  ### Drawing VCG
        ####################################
        '''
        ##############TESTING optimization
        # NEWXLOCATION=[]
        loct = []
        for k in range(len(D_3)):
            new_Ylocation = []

            dist = {}
            distance = set()  ###stores (u,v,w)where u=parent,v=child,w=cumulative weight from source to child
            location = set()  ###No use
            position_k = {}  ## stores {node:location}
            for i in range(len(paths)):
                path = paths[i]
                # print path
                for j in range(len(path)):
                    node = path[j]
                    if j > 0:
                        pred = path[j - 1]
                    else:
                        pred = node
                    # print node, pred
                    if node == 0:
                        dist[node] = (0, pred)
                        # distance.append((pred,node,0))
                        distance.add((pred, node, 0))
                        # location.add((node,0))
                        key = node
                        position_k.setdefault(key, [])
                        position_k[key].append(0)
                    else:

                        pairs = (dist[pred][0] + max(D_3[k][(pred, node)]), pred)
                        # print  max(edge_labels1[(pred, node)])
                        dist[node] = pairs
                        # print dist[node][0]

                        distance.add((pred, node, pairs[0]))
                        # print pairs[0]
                        # if location[node]<pairs[0]:
                        location.add((node, pairs[0]))
                        key = node
                        position_k.setdefault(key, [])
                        position_k[key].append(pairs[0])
                        # print position
            loc_i = {}
            for key in position_k:
                loc_i[key] = max(position_k[key])
                new_Ylocation.append(loc_i[key])
            loct.append(loc_i)

            self.NEWYLOCATION.append(new_Ylocation)
        f4 = open(name + 'location_y.txt', 'w')
        for i in loct:
            # print i
            print >> f4, i
        print"LOC=", loct, self.NEWYLOCATION
        Graph_pos_v = []
        for i in range(len(loct)):
            dist = {}
            for node in loct[i]:
                key = node

                dist.setdefault(key, [])
                dist[node].append(node)
                dist[node].append(loct[i][node])
            Graph_pos_v.append(dist)
        # print Graph_pos_v

        self.drawGraph_v_new(name, G4, D_3, Graph_pos_v)

        #####################################################################################################################handling edge independently
        # for i in range(len(self.edgesv)):
        # print self.edgesv[i].id,self.edgesv[i].North,self.edgesv[i].South
        special_edge_v = []  ### list of edges which are of type"1"  and in between same nodes

        for i in range(len(self.edgesv_new)):
            for j in range(len(self.edgesv_new)):
                if j == i:
                    continue
                if self.edgesv_new[i].source == self.edgesv_new[j].source and self.edgesv_new[i].dest == \
                        self.edgesv_new[j].dest and self.edgesv_new[i].type == self.edgesv_new[j].type == '1':

                    if self.edgesv_new[i] not in special_edge_v:
                        special_edge_v.append(self.edgesv_new[i])
                    if self.edgesv_new[j] not in special_edge_v:
                        special_edge_v.append(self.edgesv_new[j])
        ######### Removing all edges which have connected type 1 edge neighbor incoming to source or outgoing of dest

        NORTH = []
        SOUTH = []
        for edge in special_edge_v:
            NORTH.append(edge.North)
            SOUTH.append(edge.South)
        for edge in special_edge_v:
            # print edge.id,edge.North,edge.South
            # print "src",edge.source
            for ed in self.edgesv_new:
                # print "dest=",ed.dest
                if ed.dest == edge.source and ed.type == '1':
                    # print edge.id,edge.North,edge.South
                    # print edge.source, edge.dest
                    if edge.South in SOUTH:
                        # print 1
                        special_edge_v = [x for x in special_edge_v if x != edge]
                        # special_edge_v.remove(edge)
                elif ed.source == edge.dest and ed.type == '1':
                    # print edge.source, edge.dest
                    if edge.North in NORTH:
                        special_edge_v = [x for x in special_edge_v if x != edge]
                        # special_edge_v.remove(edge)
        self.special_edgev = copy.deepcopy(special_edge_v)
        #print special_edge_v
        for i in range(len(special_edge_v)):
            self.special_cell_id_v.append(special_edge_v[i].id)

        if len(special_edge_v) > 0:
            ###### Calculating offsets and location of special edge's source node and destination node
            for i in range(len(loct)):
                special_location_y = []
                Wmax = []
                for edge in special_edge_v:
                    w = loct[i][edge.dest] - loct[i][edge.source]
                    Wmax.append(w)
                # print Wmax
                offset1 = []
                offset2 = []
                for j in range(len(Wmax)):
                    avg = (Wmax[j] - 2) / 2
                    offset_1 = randint(0, avg)
                    offset_2 = randint(0, avg)
                    offset1.append(offset_1)
                    offset2.append(offset_2)
                # print offset1, offset2

                for j in range(len(special_edge_v)):
                    location = {}
                    key = special_edge_v[j].id
                    location.setdefault(key, [])
                    # print"id=", special_edge_v[j].id
                    location[key].append(loct[i][special_edge_v[j].source] + offset1[j])
                    location[key].append(loct[i][special_edge_v[j].dest] - offset2[j])
                    location[key].append(Wmax[j] - (offset1[j] + offset2[j]))
                    special_location_y.append(location)
                    # print'lo', special_location_y
                self.special_location_y.append(
                    special_location_y)  ######[[{special cell id_1:[x1,x2,width]},{special cell id_2:[x1,x2,width]}],[{special cell id_1:[x1,x2,width]},{special cell id_2:[x1,x2,width]},......]]
            print self.special_location_y

        ###################################################################################################################












        '''
        G = nx.DiGraph()
        keys=[(0,node)for node in G1.nodes()]

        nodelist = [node for node in G1.nodes()]
        zeros = np.zeros(len(nodelist))
        values = [loc[node] for node in loc]
        print "values",values
        data=map(lambda x,y,z:(x,y,z),zeros,nodelist,values)
        G.add_weighted_edges_from(data)


        pos = nx.shell_layout(G)
        labels=dict(zip(keys, values))
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_labels(G, pos)

        nx.draw(G, pos, node_color='red', node_size=300, edge_color='black')
        plt.savefig(self.name2 + 'loc_v.png')
        plt.close()
        '''

        '''
            for node in path:
                print "node=",node
                pairs = [(dist[v][0] + max(edge_labels[(v, node)], v) for v in path.pred[node]]
                print pairs
                if pairs:
                    dist[node] = max(pairs, key=lambda x: x[0])
                else:
                    dist[node] = (0, node)
            print dist
        '''
        '''
        dist = {}  # stores [node, distance] pair
        distance={}
        for node in nx.topological_sort(G1):
            # pairs of dist,node for all incoming edges
            # pairs = [(dist[v][0] + 1, v) for v in G1.pred[node]]
            pairs = [(dist[v][0] + max(edge_labels[(v, node)]), v) for v in G1.pred[node]]
            #pairs=[(dist[v][0]+max(edge_labels[(v, node)],v) for v in path]
            print "node=", node, v
            print "pairs=", pairs
            if pairs:
                l=[]
                for j,k in pairs:
                    l.append(j)

                maxv=max(l)
                y= [item for item in pairs if item[0] == maxv]
                print "Y=",y
                dist[node] =max(pairs, key=lambda x: x[0])
                distance[node]= y

                #dist[node].append(x)
                print distance[node]
            else:
                dist[node] = (0, node)
                distance[node]=[(0, node)]
                print "1"
                print dist[0][0]
            print "dist=", dist
            print"distance=",distance
            print dist.items()
            #node, (length, _) = max(dist.items(), key=lambda x: x[1])
            #print node, (length, _)
        '''

        # """
        # print nx.algorithms.dag.dag_longest_path(G1)

    '''
    G = nx.Graph()

        it = np.nditer(self.vertexMatrixh, flags=['multi_index'])
        while not it.finished:
            if it[0] != 0:
                G.add_edges_from([it.multi_index], weight = it[0])
#               # print it[0]
            it.iternext()
        return G
    def cgToGraph2(self):
        G = nx.Graph()

        it = np.nditer(self.vertexMatrixv, flags=['multi_index'])
        while not it.finished:
            if it[0] != 0:
                G.add_edges_from([it.multi_index], weight=it[0])
                ## print it[0]
            it.iternext()
        return G
    '''
    '''
    def drawGraph(self):

        G1 = nx.DiGraph()

        it = np.nditer(self.vertexMatrix, flags=['multi_index'])
        while not it.finished:
            if it[0] != 0:
                G1.add_edges_from([it.multi_index], weight = it[0])
                print it[0]
            it.iternext()

        dictList = []
        print "checking edges"
        for foo in self.edges:
            dictList.append(foo.getEdgeDict())
            print foo.getEdgeDict()
        print dictList
            #print dir(foo.getEdgeDict())
        # edge_labels[(foo.source, foo.dest): foo.constraint.getConstraintVal()]
        #for foo in self.edges:
        #    dictList.append(foo.getEdgeDict())

        edge_labels = self.merge_dicts(dictList)
        print "checking edge labels"
        print edge_labels
        for foo in edge_labels:
            print foo
#        edge_labels = dict([((u, v,), d)
#                            for u, v, d in self.edges])

        edge_colors = ['black' for edge in G1.edges()]
        #edge_colors1 = ['black' for edge in G.edges()]
        #for edge in G.edges():
           # print"constraint=", edge.getConstraint()

        #, edge_cmap = plt.cm.Reds - goes with nx.draw if needed
        pos = nx.shell_layout(G1)
        nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(G1, pos)
        nx.draw(G1, pos, node_color='red', node_size=300, edge_color=edge_colors)
        #nx.draw(G, pos, node_color='red', node_size=300, edge_color=edge_colors)
        plt.savefig(self.name)
        #pylab.show()

   '''

    def FindingAllPaths_v(self, G, start, end):
        """
        This should call subroutines for edge and vertex reduction, to pare the constraint graph down to its
        minimum form
        """
        # f1 = open("paths_v.txt", 'w')
        visited = [False] * (len(G.nodes()))
        path = []
        self.printAllPaths_v(G, start, end, visited, path)

    def printAllPaths_v(self, G, start, end, visited, path):
        visited[start] = True
        path.append(start)
        # If current vertex is same as destination, then print
        # current path[]
        if start == end:
            saved_path = path[:]
            self.paths_v.append(saved_path)
            # print >> f1, path
        else:
            for i in G.neighbors(start):

                if visited[i] == False:
                    self.printAllPaths_v(G, i, end, visited, path)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[start] = False

    def drawGraph_h(self, name, G2, edge_labels1):

        # edge_labels1 = self.merge_dicts(dictList1)
        edge_colors1 = ['black' for edge in G2.edges()]
        pos = nx.shell_layout(G2)
        nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels1)
        nx.draw_networkx_labels(G2, pos)
        nx.draw(G2, pos, node_color='red', node_size=300, edge_color=edge_colors1)
        # nx.draw(G, pos, node_color='red', node_size=300, edge_color=edge_colors)
        # plt.show()
        plt.savefig(self.name1 + 'gh.png')
        plt.close()

    def drawGraph_h_new(self, name, G2, edge_labels1, loc):

        for i in range(len(loc)):
            # edge_labels1 = self.merge_dicts(dictList1)
            edge_colors1 = ['black' for edge in G2.edges()]
            pos = nx.shell_layout(G2)
            nx.draw_networkx_labels(G2, pos, labels=loc[i])
            nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels1[i])
            nx.draw(G2, pos, node_color='red', node_size=900, edge_color=edge_colors1)
            plt.savefig(self.name2 + '-' + str(i) + 'location_h.png')
            plt.close()
            # pylab.show()

    def drawGraph_v(self, name2, G1, edge_labels):

        #######

        edge_colors = ['black' for edge in G1.edges()]
        pos = nx.shell_layout(G1)
        nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(G1, pos)
        nx.draw(G1, pos, node_color='red', node_size=300, edge_color=edge_colors)
        plt.savefig(self.name2 + 'gv.png')
        plt.close()

        '''
        nlist = map(list, loc.items())
        pos = nx.circular_layout(loc)
        nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels)
        #nx.draw_networkx_labels(G1, pos)
        nx.draw(G1, pos, node_color='red', node_size=300, edge_color=edge_colors)
        plt.savefig(self.name2 + 'locv.png')
        '''
        # nx.draw(G, pos, node_color='red', node_size=300, edge_color=edge_colors)
        # app = Viewer(G1)
        # app.mainloop()


        # pylab.show()

    def drawGraph_v_new(self, name2, G1, edge_labels, loc):

        #######
        for i in range(len(loc)):
            edge_colors = ['black' for edge in G1.edges()]
            pos = nx.shell_layout(G1)

            nx.draw_networkx_labels(G1, pos, labels=loc[i])
            nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels[i])
            nx.draw(G1, pos, node_color='red', node_size=900, edge_color=edge_colors)
            plt.savefig(self.name2 + '-' + str(i) + 'location_v.png')
            plt.close()


class multiCG():
    """
    Same as a constraint graph class, except this allows for multiple edges between nodes. Necessary for
    inserting custom constraints. 
    """

    def __init__(self, sourceGraph):
        """
        given a source graph, copy vertices and all existing nodes into a multigraph
        """
        self.diGraph1 = nx.MultiDiGraph()
        self.diGraph1.add_nodes_from(sourceGraph.cgToGraph1().nodes(data=True))
        self.diGraph1.add_edges_from(sourceGraph.cgToGraph1().edges(data=True))
        self.diGraph2 = nx.MultiDiGraph()
        self.diGraph2.add_nodes_from(sourceGraph.cgToGraph2().nodes(data=True))
        self.diGraph2.add_edges_from(sourceGraph.cgToGraph2().edges(data=True))

    def addEdge(self, source, dest, constraint):
        self.diGraph.add_edge(source, dest, constraint, weight=constraint.getConstraintVal())

    def drawGraph1(self):
        G = self.diGraph1
        edge_Labels = dict([((u, v,), d['weight'])
                            for u, v, d in G.edges(data=True)])
        # for foo in list(edge_Labels):
        # print foo

        edge_colors = ['black' for edge in G.edges()]

        pos = nx.shell_layout(self.diGraph1)
        nx.draw_networkx_edge_labels(self.diGraph1, pos, edge_labels=edge_Labels)
        nx.draw_networkx_labels(self.diGraph1, pos)
        nx.draw(self.diGraph1, pos, node_color='white', node_size=300, edge_color=edge_colors, arrows=True)

        pylab.show()

    def drawGraph2(self):
        G = self.diGraph2
        edge_Labels = dict([((u, v,), d['weight'])
                            for u, v, d in G.edges(data=True)])
        # for foo in list(edge_Labels):
        # print foo

        edge_colors = ['black' for edge in G.edges()]

        pos = nx.shell_layout(self.diGraph2)
        nx.draw_networkx_edge_labels(self.diGraph2, pos, edge_labels=edge_Labels)
        nx.draw_networkx_labels(self.diGraph2, pos)
        nx.draw(self.diGraph2, pos, node_color='white', node_size=300, edge_color=edge_colors, arrows=True)

        pylab.show()

    def edgeReduce(self):
        """Eliminate redundant edges"""

    def vertexReduce(self):
        """Eliminate redundant vertices"""
        return


class Edge():
    def __init__(self, source, dest, constraint, type, id, East=None, West=None, North=None, South=None):
        self.source = source
        self.dest = dest
        self.constraint = constraint
        self.type = type
        self.id = id
        self.East = East
        self.West = West
        self.North = North
        self.South = South
        self.setEdgeDict()

    def getConstraint(self):
        return self.constraint

    def setEdgeDict(self):
        self.edgeDict = {(self.source, self.dest): [self.constraint.getConstraintVal(), self.type]}
        # self.edgeDict = {(self.source, self.dest): self.constraint.constraintval}

    def getEdgeDict(self):
        return self.edgeDict

    def getEdgeWeight(self, source, dest):
        return self.getEdgeDict()[(self.source, self.dest)]

    def printEdge(self):
        print "s: ", self.source, "d: ", self.dest, "con = ", self.constraint.printCon()
