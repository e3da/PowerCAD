'''
@author: Peter N. Tucker, Quang
'''
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
from powercad.design.library_structures import Device
from powercad.spice_export.components import *
from powercad.sym_layout.plot import plot_layout
from pprint import pprint #sxm test; delete later
from numpy import add

#from
class Module_SPICE_lumped_graph():
    def __init__(self, name, sym_layout, solution_index, template_graph=None):
        """
        Creates a lumped graph to hold SPICE information based on a symbolic layout solution or template graph
        
        Keyword Arguments:
            sym_layout     -- symbolic layout object containing layout solutions
            solution_index -- index of layout in solutions of sym_layout
            template_graph -- lumped graph from which the SPICE graph will be based on
            
        Returns:
            spice_lumped_graph
        """
        self.name = name.replace(' ','')
        self.gate_nodes = []
        self.sym_layout = sym_layout
        self.sym_layout.gen_solution_layout(solution_index)
        if template_graph is None:
            template_graph = self.sym_layout.lumped_graph
        
        # ensure every node has a type
        self._check_node_types(template_graph)
        
        # create graph
        self.spice_graph = nx.Graph()
        
        # get nodes and edges from template_graph
        nbunch = template_graph.nodes(data=True)
        ebunch = template_graph.edges(data=True)
        
        # ensure every node begins with a letter for SPICE
        nbunch[:] = [('N{}'.format(node[0]),node[1]) for node in nbunch]
        ebunch[:] = [('N{}'.format(edge[0]),'N{}'.format(edge[1]),edge[2]) for edge in ebunch]
        print nbunch
        print ebunch
    def _check_node_types(self, graph):
        """
        Ensures that each node has a 'type'
        
        Keyword Arguments:
            graph -- networkx graph
        """
        for node,node_attrib in graph.nodes_iter(data=True):
            try:
                node_attrib['type']  # check that node has a 'type'
            except KeyError:         # if not, give it a 'type' of 'node'
                node_attrib['type'] = 'node'
                        
        return graph
class Module_SPICE_netlist_graph_v2():
    def __init__(self, name, sym_layout, solution_index, template_graph=None):
        """
        Creates a graph to hold SPICE information based on a symbolic layout solution or template graph
        
        Keyword Arguments:
            sym_layout     -- symbolic layout object containing layout solutions
            solution_index -- index of layout in solutions of sym_layout
            template_graph -- lumped graph from which the SPICE graph will be based on
            
        Returns:
            spice_graph
        """
        
        self.name = name.replace(' ','')
        self.gate_nodes = []
        
        # load solution
        self.sym_layout = sym_layout
        self.sym_layout.gen_solution_layout(solution_index)
        if template_graph is None:
            template_graph = self.sym_layout.lumped_graph
        
        # ensure every node has a type
        self._check_node_types(template_graph)
        
        # create graph
        self.spice_graph = nx.Graph()
        
        # get nodes and edges from template_graph
        nbunch = template_graph.nodes(data=True)
        ebunch = template_graph.edges(data=True)
        
        # ensure every node begins with a letter for SPICE
        nbunch[:] = [('N{}'.format(node[0]),node[1]) for node in nbunch]
        ebunch[:] = [('N{}'.format(edge[0]),'N{}'.format(edge[1]),edge[2]) for edge in ebunch]
        
        # add nodes to spice_graph
        self.spice_graph.add_nodes_from(nbunch)
        
        # prepare spice_node dictionaries to map between networkx nodes and SPICE nodes/components
        self.spice_node = {}
        self.spice_node_count = 1 # node 0 is a special node reserved for ground
        self.spice_name = {}
        self.spice_name_count = 1
        self.type={'Lead':1,'device':1,'mos':1,'body':1}
        self.node_type={'d':1,'g':1,'s':1}
        # create pi or L models from each edge in template_graph
        for edge in ebunch:
            if self.spice_graph.node[edge[0]]['type']=='lead':
                self._build_wire_L_model(edge,edge[0],edge[1])
            elif self.spice_graph.node[edge[1]]['type']=='lead':
                self._build_wire_L_model(edge,edge[1],edge[0])
            else:
                self._build_wire_pi_model(edge)
                
        # create devices
        self.device_models = {} # {'device_name': '(device_model_name, model)', ...}
        for device in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='device']:
            # find model, if it doesn't exist, add it to the device dictionary
            device_name = device[1]['obj'].tech.device_tech.name
            if device_name in self.device_models:
                model_name = self.device_models[device_name][0]
            else:
                # get Verilog-A model
                model = device[1]['obj'].tech.device_tech.device_model
                # check Verilog-A file for module
                try:
                    model_name = ((re.search('(?<=module) \w+', model)).group(0)).strip()
                except AttributeError:
                    raise DeviceError(DeviceError.NO_VA_MODULE, device[1]['obj'].tech.device_tech.name)
                # add to device dictionary
                self.device_models[device_name] = (model_name, model)
            
            # determine device type and create device
            if device[1]['obj'].tech.device_tech.device_type == Device.DIODE:
                self._create_diode(device[0], model_name)
            elif device[1]['obj'].tech.device_tech.device_type == Device.TRANSISTOR:
                self._create_mosfet(device[0], model_name)
            else:
                raise DeviceError(DeviceError.UNKNOWN_DEVICE, device[1]['obj'].tech.device_tech.name)

        # create gate leads
        self._create_gate_leads()

            
    def _check_node_types(self, graph):
        """
        Ensures that each node has a 'type'
        
        Keyword Arguments:
            graph -- networkx graph
        """
        for node,node_attrib in graph.nodes_iter(data=True):
            try:
                node_attrib['type']  # check that node has a 'type'
            except KeyError:         # if not, give it a 'type' of 'node'
                node_attrib['type'] = 'node'
                        
        return graph
    
    def get_SPICE_node(self, nx_node):
        """
        Return a unique SPICE node for the networkx node.
            The defined networkx nodes in spice_graph contain spatial information,
            but nodes in SPICE must be a non-negative integer between 0-9999.
            This function maps between the two node spaces
            
        Keyword Arguments:
            nx_node -- networkx node name
            
        Returns:
            spice node equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if self.spice_node.get(nx_node) is None:
            self.spice_node[nx_node] = str(self.spice_node_count).zfill(4)
            self.spice_node_count += 1
            # check that node count is less than or equal to 9999
            if self.spice_node_count > 9999:
                raise SpiceNodeError('Node count too high')
        
        # return respective SPICE node
        return self.spice_node[nx_node]
    def get_SPICE_node_old(self, nx_node):
        """
        Return a unique SPICE node for the networkx node.
            The defined networkx nodes in spice_graph contain spatial information,
            but nodes in SPICE must be a non-negative integer between 0-9999.
            This function maps between the two node spaces
            
        Keyword Arguments:
            nx_node -- networkx node name
            
        Returns:
            spice node equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if self.spice_node.get(nx_node) is None:
            self.spice_node[nx_node] = str(self.spice_node_count).zfill(4)
            self.spice_node_count += 1
            # check that node count is less than or equal to 9999
            if self.spice_node_count > 9999:
                raise SpiceNodeError('Node count too high')
        
        # return respective SPICE node
        return self.spice_node[nx_node]
    def get_SPICE_component(self, nx_node,type):
        """
        Return a unique SPICE component name for the networkx node.
            First, the user need to define a list of prefixes with initial count:
            e.g: {'yellow':1}
            depends on the count, and the prefix, a unique name will be created
            
        Keyword Arguments:
            nx_node -- networkx node name
            prefix: given prefixes for unique names
        Returns:
            spice name equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if type!=None:
            if self.spice_name.get(nx_node) is None:
                self.spice_name[nx_node] = type+str(self.type[type])
                self.type[type] += 1
                # check that node name is less than 7 characters
                if self.type[type] > 999999:
                    raise SpiceNameError('Name count too high')
        else:
            self.get_SPICE_component_old(nx_node)       
        # return respective SPICE node
        return self.spice_name[nx_node]    
        
    def get_SPICE_component_old(self, nx_node):
        """
        Return a unique SPICE component name for the networkx node.
            The defined networkx node names in spice_graph contain spatial information,
            but component names in SPICE must be an alphanumeric identifier less than
            seven characters long. This function maps between the two name spaces
            
        Keyword Arguments:
            nx_node -- networkx node name
            
        Returns:
            spice name equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if self.spice_name.get(nx_node) is None:
            self.spice_name[nx_node] = str(self.spice_name_count).zfill(7)
            self.spice_name_count += 1
            # check that node name is less than 7 characters
            if self.spice_name_count > 999999:
                raise SpiceNameError('Name count too high')
        
        # return respective SPICE node
        return self.spice_name[nx_node]
    
    
    def get_NX_node(self, spice_node):
        """
        Return the networkx node name for the given SPICE node.
            The defined networkx nodes in spice_graph contain spatial information,
            but nodes in SPICE must be a non-negative integer between 0-9999.
            This function maps between the two node spaces
            
        Keyword Arguments:
            spice_node -- SPICE node number
            
        Returns:
            networkx node equivalent of spice_node
        """
        for nx_node, spice_node_num in self.spice_node.iteritems():
            if spice_node == spice_node_num:
                return nx_node
    
    
    def _build_wire_pi_model(self, edge):
        """
        Builds a pi wire delay model
        
        Keyword Arguments:
            edge  -- edge of template_graph to be converted to pi model in spice_graph
        """
        # get nodes on either side
        node_1 = edge[0]
        node_2 = edge[1]
        
        # add intermediate node
        interm_node = '{}{}'.format(node_1,node_2)
        self.spice_graph.add_node(interm_node, attr_dict={'type':'node'})
        group_name = interm_node
        
        # check for devices on either side
        #    in the event of a device, create a new node for connections
        #    and connect to device
        if self.spice_graph.node[node_1]['type']=='device':
            new_node_1 = '{}{}'.format(node_1,interm_node)
            self.spice_graph.add_node(new_node_1, attr_dict={'type':'node'})
            self.spice_graph.add_edge(node_1,new_node_1, attr_dict={'type':edge[2]['type']})
            node_1 = new_node_1
        if self.spice_graph.node[node_2]['type']=='device':
            new_node_2 = '{}{}'.format(interm_node,node_2)
            self.spice_graph.add_node(new_node_2, attr_dict={'type':'node'})
            self.spice_graph.add_edge(new_node_2,node_2, attr_dict={'type':edge[2]['type']})
            node_2 = new_node_2

        # add resistance node
        res = ((1.0/edge[2]['res'])*1e-3)
        spice_res = Resistor(self.get_SPICE_component(group_name,None),
                             self.get_SPICE_node(node_1),
                             self.get_SPICE_node(interm_node),
                             res)
        self.spice_graph.add_node('R{}'.format(group_name), attr_dict={'type':'res','component':spice_res})
        self.spice_graph.add_edge(node_1,'R{}'.format(group_name,None))
        self.spice_graph.add_edge('R{}'.format(group_name),interm_node)
        
        # add inductance node
        ind = ((1.0/edge[2]['ind'])*1e-9)
        spice_ind = Inductor(self.get_SPICE_component(group_name,None),
                             self.get_SPICE_node(interm_node),
                             self.get_SPICE_node(node_2),
                             ind)
        self.spice_graph.add_node('L{}'.format(group_name), attr_dict={'type':'ind','component':spice_ind})
        self.spice_graph.add_edge(interm_node,'L{}'.format(group_name))
        self.spice_graph.add_edge('L{}'.format(group_name),node_2)
        
        # add two capacitance nodes
        cap = ((1.0/float(edge[2]['cap']))*1e-12)
        # create two imaginary nodes for the body (for visual purposes)
        self.spice_graph.add_node('B{}_1'.format(group_name), attr_dict={'type':'body'})
        self.spice_graph.add_node('B{}_2'.format(group_name), attr_dict={'type':'body'})
        # create capacitor nodes
        spice_cap1 = Capacitor(self.get_SPICE_component('1'+group_name,None),
                               self.get_SPICE_node(node_1),
                               self.get_SPICE_node('body'),
                               cap/2.0)
        self.spice_graph.add_node('C{}_1'.format(group_name), attr_dict={'type':'cap','component':spice_cap1})
        self.spice_graph.add_edge(node_1,'C{}_1'.format(group_name))
        self.spice_graph.add_edge('C{}_1'.format(group_name),'B{}_1'.format(group_name))
        spice_cap2 = Capacitor(self.get_SPICE_component('2'+group_name,None),
                               self.get_SPICE_node(node_2),
                               self.get_SPICE_node('body'),
                               cap/2.0)
        self.spice_graph.add_node('C{}_2'.format(group_name), attr_dict={'type':'cap','component':spice_cap2})
        self.spice_graph.add_edge(node_2,'C{}_2'.format(group_name))
        self.spice_graph.add_edge('C{}_2'.format(group_name),'B{}_2'.format(group_name))
    
    
    def _build_wire_L_model(self, edge, lead, non_lead):
        """
        Builds an L wire delay model
        
        Keyword Arguments:
            edge     -- edge of template_graph to be converted to L model in spice_graph
            lead     -- lead node
            non_lead -- non-lead node
        """
        # add intermediate node
        interm_node = '{}{}'.format(edge[0],edge[1])
        self.spice_graph.add_node(interm_node, attr_dict={'type':'node'})
        group_name = interm_node
        
        # check for device on non_lead side
        #    in the event of a device, create a new node for connections
        #    and connect to device
        if self.spice_graph.node[non_lead]['type']=='device':
            new_non_lead = '{}{}'.format(non_lead,interm_node)
            self.spice_graph.add_node(new_non_lead, attr_dict={'type':'node'})
            self.spice_graph.add_edge(non_lead,new_non_lead, attr_dict={'type':edge[2]['type']})
            non_lead = new_non_lead
        
        # add resistance node
        res = ((1.0/edge[2]['res'])*1e-3)
        spice_res = Resistor(self.get_SPICE_component(group_name,None),
                             self.get_SPICE_node(lead),
                             self.get_SPICE_node(interm_node),
                             res)
        self.spice_graph.add_node('R{}'.format(group_name), attr_dict={'type':'res','component':spice_res})
        self.spice_graph.add_edge(lead,'R{}'.format(group_name))
        self.spice_graph.add_edge('R{}'.format(group_name),interm_node)
        
        # add inductance node
        ind = ((1.0/edge[2]['ind'])*1e-9)
        spice_ind = Inductor(self.get_SPICE_component(group_name,None),
                             self.get_SPICE_node(interm_node),
                             self.get_SPICE_node(non_lead),
                             ind)
        self.spice_graph.add_node('L{}'.format(group_name), attr_dict={'type':'ind','component':spice_ind})
        self.spice_graph.add_edge(interm_node,'L{}'.format(group_name))
        self.spice_graph.add_edge('L{}'.format(group_name),non_lead)
        
        # add single capacitance node on non_lead side
        cap = ((1.0/float(edge[2]['cap']))*1e-12)
        # create imaginary node for the body (for visual purposes)
        self.spice_graph.add_node('B{}'.format(group_name), attr_dict={'type':'body'})
        # create capacitance node
        spice_cap = Capacitor(self.get_SPICE_component(group_name,'body'),
                              self.get_SPICE_node(non_lead),
                              self.get_SPICE_node('body'),
                              cap)
        self.spice_graph.add_node('C{}'.format(group_name), attr_dict={'type':'cap','component':spice_cap})
        self.spice_graph.add_edge(non_lead,'C{}'.format(group_name))
        self.spice_graph.add_edge('C{}'.format(group_name),'B{}'.format(group_name))

            
    def _create_diode(self, node, model_name):
        """
        Creates a diode model
        
        Keyword Arguments:
            node -- diode node
        """
        # determine diode terminals
        anode = []
        cathode = []
        for edge in self.spice_graph.edges(node, data=True):
            if edge[2]['type'] == 'trace':
                anode.append([an for an in edge if an != node][0])
            elif edge[2]['type'] == 'bw power':
                cathode.append([ca for ca in edge if ca != node][0])
        
        # check terminal connections
        namespace = locals()
        for terminal in [anode,cathode]:
            num_connect = len(terminal)
            # check that all terminals have been assigned
            if num_connect == 0:
                raise TerminalError('Diode', node, [name for name in namespace if namespace[name] is terminal][0])
            # check for multiple connections connected to terminal
            if num_connect > 1:
                # if so, create shorts to connect all traces/bondwires to first node
                for connect in range(1,num_connect):
                    short = Short(self.get_SPICE_node(terminal[connect]),
                                         self.get_SPICE_node(terminal[0]))
                    self.spice_graph.add_node('R{}_short'.format(terminal[connect]), attr_dict={'type':'short','component':short})
                    self.spice_graph.add_edge(terminal[connect],'R{}_short'.format(terminal[connect]))
                    self.spice_graph.add_edge('R{}_short'.format(terminal[connect]),terminal[0])
        
        # create diode
        type=self.spice_graph.node[node][type]
        self.spice_graph.node[node]['component'] = Diode(self.get_SPICE_component(node,type),
                                                         self.get_SPICE_node(anode[0]),
                                                         self.get_SPICE_node(cathode[0]),
                                                         model_name)
    
    
    def _create_mosfet(self, node, model_name):
        """
        Creates a mosfet model
        
        Keyword Arguments:
            node -- mosfet node
        """
        # determine mosfet terminals
        drain = []
        gate = []
        source = []
        for edge in self.spice_graph.edges(node, data=True):
            #print 'mosfet edge:'
            #print edge
            if edge[2]['type'] == 'trace':
                drain.append([dr for dr in edge if dr != node][0])
            elif edge[2]['type'] == 'bw signal':
                gate.append([gt for gt in edge if gt != node][0])
                self.gate_nodes.append([gt for gt in edge if gt != node][0])
            elif edge[2]['type'] == 'bw power':
                source.append([src for src in edge if src != node][0])
        type='mos'
       # print type +str(self.type['mos'])
       # print drain
       # print gate
       # print source    
        # check terminal connections
        
        namespace = locals()
        for terminal in [drain,gate,source]:
            num_connect = len(terminal)
            # check that all terminals have been assigned
            if num_connect == 0:
                raise TerminalError('MOSFET', node, [name for name in namespace if namespace[name] is terminal][0])
            # check for multiple connections connected to terminal
            elif num_connect > 1:
                # if so, create shorts to connect all traces/bondwires to first node
                for connect in range(1,num_connect):
                    short = Short('R{}_short'.format(terminal[connect]), 
                                  self.get_SPICE_node(terminal[connect]),
                                  self.get_SPICE_node(terminal[0]))
                    self.spice_graph.add_node('R{}_short'.format(terminal[connect]), attr_dict={'type':'short','component':short})
                    self.spice_graph.add_edge(terminal[connect],'R{}_short'.format(terminal[connect]))
                    self.spice_graph.add_edge('R{}_short'.format(terminal[connect]),terminal[0])
        
        # create mosfet
        
        self.spice_graph.node[node]['component'] = Mosfet(self.get_SPICE_component(node,type),
                                                          self.get_SPICE_node(drain[0]),
                                                          self.get_SPICE_node(gate[0]),
                                                          self.get_SPICE_node(source[0]),
                                                          model_name)
    
    
    def _create_gate_leads(self):
        '''
        Add gate leads for export
        '''
        node_type = nx.get_node_attributes(self.spice_graph, 'type')
        coordinates = nx.get_node_attributes(self.spice_graph, 'point')
        self.gate_trace_endpts = []

        # Iterate through device gate paths to find gate trace endpoints
        for gate in self.gate_nodes:
            count = 0
            current_node = gate
            prev_nodes = []
            prev_nodes.append(gate)
            
            while count < 8:        # Move along path from device gate node to gate trace
                current_node = self._get_next_gate_path_node(current_node, prev_nodes)
                prev_nodes.append(current_node)
                count += 1
            
            # Check if node is an endpoint on the gate trace
            if nx.degree(self.spice_graph, current_node) < 5:
                self.gate_trace_endpts.append(current_node)
        
        # Check number of gate trace endpoints found
        if len(self.gate_trace_endpts) > 4:
            raise Exception('Too many gate trace endpoints found!')
            
        # Determine paths representing gate traces
        possible_gate_trace_paths = []
        for start_pt in self.gate_trace_endpts:
            temp_path = []
            
            for end_pt in [pt for pt in self.gate_trace_endpts if pt != start_pt]:
                temp_path = list(nx.all_shortest_paths(self.spice_graph, start_pt, end_pt))[0]  # Path from start_pt to end_pt
            
                for node in temp_path:
                    if node_type[node] == 'device' or node_type[node] == 'cap':   # Ensure device or capacitor is not present
                        temp_path = []
                        break
                
                if temp_path != []:
                    possible_gate_trace_paths.append(temp_path)
        
        # Eliminate duplicate reversed paths - should be left with 0-2 gate trace paths
        for path in possible_gate_trace_paths:
            for other_path in [other_path for other_path in possible_gate_trace_paths if other_path != path]:
                if path == list(reversed(other_path)):
                    possible_gate_trace_paths.remove(other_path)
        
        gate_trace_paths = possible_gate_trace_paths
        
        # Check if 0-2 gate traces found
        if len(gate_trace_paths) > 2:
            raise Exception('More than two gate traces found!')

        # Add gate leads to graph
        self.gate_leads = []
        for path in gate_trace_paths:
            
            # Add gate lead node
            self.spice_graph.add_node('G'+path[0], attr_dict={'type':'lead', 'point':coordinates[path[0]]})
            
            # Connect gate lead to gate trace endpoint with a short
            short = Short('G'+path[0]+'_short',
                          self.get_SPICE_node('G'+path[0]), 
                          self.get_SPICE_node(path[0]))
            self.spice_graph.add_node('G'+path[0]+'_short', attr_dict={'type':'short', 'component':short})
            self.spice_graph.add_edge('G'+path[0], 'G'+path[0]+'_short') 
            self.spice_graph.add_edge('G'+path[0]+'_short', path[0]) 
            
            
            self.gate_leads.append('G'+path[0])
        
        # --- testing ---
        #print 'GATE LEADS:', (' '.join(self.get_SPICE_node(gate_lead) for gate_lead in self.gate_leads))
        
        #print '\nGate Trace Paths:'
        #for path in gate_trace_paths:
        #    print (' '.join(self.get_SPICE_node(node) for node in path))
        #print '\n'
         
                
    def _get_next_gate_path_node(self, current_node, prev_nodes):
        '''
        Helper function for _create_gate_leads()
        Used to iterate through nodes from device gate node to a node on the gate trace
        
        Keyword Arguments:
            current_node -- it's pretty self-explanatory
            prev_nodes -- list of nodes already iterated through on path
            
        Returns:
            next_node -- next node on path
        '''
        node_type = nx.get_node_attributes(self.spice_graph, 'type')
        next_node = None
        
        # Determine next node from neighbors of current node
        for neighbor in [neighbor for neighbor in nx.all_neighbors(self.spice_graph, current_node) if node_type[neighbor] != 'device' and node_type[neighbor] != 'cap']:  

            if neighbor not in prev_nodes:  # Make sure it doesn't go backwards
                next_node = neighbor
                break
        
        if next_node == None:
            raise Exception('Next node not found!')

        return next_node

        
    def write_SPICE_subcircuit(self, directory):
        """
        Writes H-SPICE subcircuit out to [self.name].inc in the directory specified
        
        Keyword Arguments:
            directory  -- file directory to write file to
            
        Returns:
            SPICE file path
        """
        
        # write each device Verilog-A file to local directory
        for model in self.device_models.itervalues():
            full_path = os.path.join(directory, '{}.va'.format(model[0]))
            model_file = open(full_path, 'w')
            model_file.write(model[1])
            model_file.close()
        
        # find leads of module
        lead_list = ''
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            lead_list += ' ' + self.get_SPICE_node(lead[0])
        lead_list += ' ' + self.get_SPICE_node('body')
        
        # prepare netlist file
        full_path = os.path.join(directory, '{}.inc'.format(self.name))
        spice_file = open(full_path, 'w')
        
        # write module name
        spice_file.write('*{}\n'.format(self.name))
        
        # include each device model
        spice_file.write('\n*** Device Models ***\n')
        for model in self.device_models.itervalues():
            spice_file.write('.hdl "{}.va"\n'.format(model[0]))
            
        # write subcircuit start line with list of lead nodes
        spice_file.write('\n\n.SUBCKT {}{}\n'.format(self.name, lead_list))
        
        # write SPICE line for each node that has a component
        spice_file.write('\n*** {} Components ***\n'.format(self.name))  
        for node in self.spice_graph.nodes(data=True):            
            if node[1].get('component') is not None:
                spice_file.write(node[1]['component'].SPICE +'\n')
                
        # end subcircuit file
        spice_file.write('\n.ENDS {}'.format(self.name))
        spice_file.close()
        
        # save layout image to clarify lead names
        self.draw_layout()        
        plt.savefig(os.path.join(directory, '{}_lead_layout.png'.format(self.name)))
        '''
        # testing
        print 'names'
        for key,val in self.spice_name.items(): print '{}: {}'.format(key,val)
        print '\n\nnodes'
        for key,val in self.spice_node.items(): print '{}: {}'.format(key,val)
        '''
        return full_path
    
    def write_SPICE_reduced_subcircuit(self, directory):
        '''sxm063 Apr 2016 - This function is used to write a spice netlist similar to the one defined in write_SPICE_subcircuit()
        except that it reduces series and parallel components to their equivalents. '''
        
        
        # write each device Verilog-A file to local directory
        for model in self.device_models.itervalues():
            full_path = os.path.join(directory, '{}.va'.format(model[0]))
            model_file = open(full_path, 'w')
            model_file.write(model[1])
            model_file.close()
        
        # find leads of module
        lead_list = ''
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            lead_list += ' ' + self.get_SPICE_node(lead[0])
        lead_list += ' ' + self.get_SPICE_node('body')
        
        # prepare netlist file
        full_path = os.path.join(directory, '{}.inc'.format(self.name))
        spice_file = open(full_path, 'w')
        
        # write module name
        spice_file.write('*{}\n'.format(self.name))
        
        # include each device model
        spice_file.write('\n*** Device Models ***\n')
        for model in self.device_models.itervalues():
            spice_file.write('.hdl "{}.va"\n'.format(model[0]))
            
        # write subcircuit start line with list of lead nodes
        spice_file.write('\n\n.SUBCKT {}{}\n'.format(self.name, lead_list))
        
        # write SPICE line for each node that has a component
        spice_file.write('\n*** {} Components ***\n'.format(self.name))  
        
        # sxm - 
        a=[]
        #print self.spice_graph.nodes
        for node in self.spice_graph.nodes(data=True):       
            sub_a=[]
            if node[1].get('component') is not None:
                #print node[1]['component']
                sub_a.append(node[1]['component'].SPICE[:8])
                sub_a.append(node[1]['component'].SPICE[9:13])
                sub_a.append(node[1]['component'].SPICE[14:18])
                sub_a.append(node[1]['component'].SPICE[19:])
                a.append(sub_a)
        print a
        print "---------------"
        #print a[0]
                
        # sxm - add  capacitances that are in parallel
        for i in range(0,len(a)):
            if (a[i][0][:1]=="C" and len(a[i])==4): # for each line in the spice network 
                for j in range(i+1,len(a)): # for all other lines below the line being compared
                    #print j
                    if (a[j][0][:1]=="C" and len(a[j])==4): # check if both components are capacitors
                        if ((a[i][1]==a[j][1] and a[i][2]==a[j][2]) or (a[i][2]==a[j][1] and a[i][1]==a[j][2])): # check if the two devices are in parallel by checking node commonality (node 1&2 of component1 = node 1&2 of component2 OR node 1&2 of component1 = node 2&1 of component2)
                            #print i,j
                            #print a[i]
                            #print a[j]
                            #print a[i][3]+a[j][3]
                            #update the first row
                            a[i].insert(3, add(float(a[i][3]), float(a[j][3]))) # insert equivalent capacitor value at appropriate location of the line                                
                            #print "line " + i + ":" + a[i]
                            a[i].pop(4) # remove old capacitor value
                            #mark the second row for removal
                            a[j].insert(4, "remove") # remove the 2nd of the two capacitor lines (since it is already accounted for in the equivalent value)
                            #print "Equivalent:"
                            #print a[i]
                            #print a[j]                           
                            #j-=1 # since one line was removed, all lines will move up by one. Therefore, decrement j so as not to miss a line in the comparison.
                            #print i,j 
        print "\n Old"
        for items in a:
            print items
        
        # remove the lines that have been accounted for (i.e. that lines marked with the word "remove")
        print "\n -------------"
        print "\n To be removed"        
        count=0
        print "initial count ", count
        for i in range(0,len(a)-1):
            print "items removed (count) =", count, " i=", i, " index=", i-count, " len(a[i-count])=", len(a[i-count])            
            if len(a[i-count])>4:
                print i-count, a[i-count] 
                a.pop(i-count)
                count = count + 1 
                print "number of items removed (count) = ", count
            
                
        print "\n New"
        for items in a:
            print items
            
        # write netlist lines
        for spice_line in a:
            #spice_file.write(str(spice_line) +'\n')    
            #spice_file.write(spice_line.SPICE + '\n')
            spice_file.write("{name} {N1} {N2} {value}".format(name=spice_line[0], N1=spice_line[1], N2=spice_line[2], value=spice_line[3]) + '\n')            
        
        # end subcircuit file
        spice_file.write('\n.ENDS {}'.format(self.name))
        spice_file.close()
        
        # save layout image to clarify lead names
        self.draw_layout()        
        plt.savefig(os.path.join(directory, '{}_lead_layout.png'.format(self.name)))
                    
        #self.draw_graph() #sxm063 testing; this code outputs the network-x nodes map as an image; delete this line after testing
        #plt.savefig(os.path.join(directory, '{}_nx_nodes.png'.format(self.name)))
        
        '''
        #create reduced netlist graph
        self.reduced_netlist_graph = nx.Graph()
        #add nodes to graph:
        #spice_node_list=[]
        self.reduced_netlist_graph.add_nodes_from('{}'.format(spice_line[0]) for spice_line in a)
        plt.close()
        ax = plt.subplot('111', adjustable='box', aspect=1.0)
        ax.set_axis_off()
        pos = nx.spring_layout(self.reduced_netlist_graph,scale=50)
        nx.draw_networkx_nodes(self.reduced_netlist_graph, pos, node_size=100, node_color='blue', node_shape='o', alpha=0.7)
        nx.draw_networkx_edges(self.reduced_netlist_graph, pos, edge_color='black')
        nx.draw_networkx_labels(self.reduced_netlist_graph, pos, font_size=7, font_weight=3)
        plt.show()
        plt.savefig(os.path.join(directory, '{}_reduced_netlist_graph.png'.format(self.name)))
        '''
        return full_path                                  

    def draw_layout(self):
        """ Draws symbolic layout and labels lead nodes for connecting into circuit """
        plt.close()
        ax = plt.subplot('111', adjustable='box', aspect=1.0)
        ax.set_axis_off()
        fig = plot_layout(self.sym_layout, ax = ax, new_window=False)
        # label leads
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            pos = lead[1]['point']
            name = lead[0]
            fig.text(pos[0], pos[1], self.get_SPICE_node(name),
                    horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='yellow', alpha=0.8))
        # add body label
        fig.text(0,0,'body: {}'.format(self.get_SPICE_node('body')),horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='yellow', alpha=0.8))
        
        # show plot
        plt.title(self.name)
        plt.show()
        
        
        
    def draw_graph(self):
        """ Draws networkx graph of spice_graph """   
        
        # sxm testing 2016 Mar 31 ------- this section added for testing purposes only; to be deleted after testing ---------     
        plt.close() #sxm test
        ax = plt.subplot('111', adjustable='box', aspect=1.0) #sxm test
        ax.set_axis_off() #sxm test
        # sxm test block-----------------------------------------------------------------------------------------------------
        
        pos = nx.spring_layout(self.spice_graph,scale=50) #sxm test; original scale=50
        nx.draw_networkx_nodes(self.spice_graph, pos, node_size=100, node_color='blue', node_shape='o', alpha=0.7) #sxm test; original node_size=400
        nx.draw_networkx_edges(self.spice_graph, pos, edge_color='black')
        nx.draw_networkx_labels(self.spice_graph, pos, font_size=7, font_weight=3) #sxm test; original font_size=10, weight=2
        plt.show()
               
# ------------------------------------------------------------------------------------------------------
# old version old version old version old version old version old version old version old version old version old version 

class Module_SPICE_netlist_graph():
    def __init__(self, name, sym_layout, solution_index, template_graph=None):
        """
        Creates a graph to hold SPICE information based on a symbolic layout solution or template graph
        
        Keyword Arguments:
            sym_layout     -- symbolic layout object containing layout solutions
            solution_index -- index of layout in solutions of sym_layout
            template_graph -- lumped graph from which the SPICE graph will be based on
            
        Returns:
            spice_graph
        """
        
        self.name = name.replace(' ','')
        self.gate_nodes = []
        
        # load solution
        self.sym_layout = sym_layout
        self.sym_layout.gen_solution_layout(solution_index)
        if template_graph is None:
            template_graph = self.sym_layout.lumped_graph
        
        # ensure every node has a type
        self._check_node_types(template_graph)
        
        # create graph
        self.spice_graph = nx.Graph()
        
        # get nodes and edges from template_graph
        nbunch = template_graph.nodes(data=True)
        ebunch = template_graph.edges(data=True)
        
        # ensure every node begins with a letter for SPICE
        nbunch[:] = [('N{}'.format(node[0]),node[1]) for node in nbunch]
        ebunch[:] = [('N{}'.format(edge[0]),'N{}'.format(edge[1]),edge[2]) for edge in ebunch]
        
        # add nodes to spice_graph
        self.spice_graph.add_nodes_from(nbunch)
        
        # prepare spice_node dictionaries to map between networkx nodes and SPICE nodes/components
        self.spice_node = {}
        self.spice_node_count = 1 # node 0 is a special node reserved for ground
        self.spice_name = {}
        self.spice_name_count = 1
        
        # create pi or L models from each edge in template_graph
        for edge in ebunch:
            if self.spice_graph.node[edge[0]]['type']=='lead':
                self._build_wire_L_model(edge,edge[0],edge[1])
            elif self.spice_graph.node[edge[1]]['type']=='lead':
                self._build_wire_L_model(edge,edge[1],edge[0])
            else:
                self._build_wire_pi_model(edge)
                
        # create devices
        self.device_models = {} # {'device_name': '(device_model_name, model)', ...}
        for device in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='device']:
            # find model, if it doesn't exist, add it to the device dictionary
            device_name = device[1]['obj'].tech.device_tech.name
            if device_name in self.device_models:
                model_name = self.device_models[device_name][0]
            else:
                # get Verilog-A model
                model = device[1]['obj'].tech.device_tech.device_model
                # check Verilog-A file for module
                try:
                    model_name = ((re.search('(?<=module) \w+', model)).group(0)).strip()
                except AttributeError:
                    raise DeviceError(DeviceError.NO_VA_MODULE, device[1]['obj'].tech.device_tech.name)
                # add to device dictionary
                self.device_models[device_name] = (model_name, model)
            
            # determine device type and create device
            if device[1]['obj'].tech.device_tech.device_type == Device.DIODE:
                self._create_diode(device[0], model_name)
            elif device[1]['obj'].tech.device_tech.device_type == Device.TRANSISTOR:
                self._create_mosfet(device[0], model_name)
            else:
                raise DeviceError(DeviceError.UNKNOWN_DEVICE, device[1]['obj'].tech.device_tech.name)

        # create gate leads
        self._create_gate_leads()

            
    def _check_node_types(self, graph):
        """
        Ensures that each node has a 'type'
        
        Keyword Arguments:
            graph -- networkx graph
        """
        for node,node_attrib in graph.nodes_iter(data=True):
            try:
                node_attrib['type']  # check that node has a 'type'
            except KeyError:         # if not, give it a 'type' of 'node'
                node_attrib['type'] = 'node'
                        
        return graph
    
    
    def get_SPICE_node(self, nx_node):
        """
        Return a unique SPICE node for the networkx node.
            The defined networkx nodes in spice_graph contain spatial information,
            but nodes in SPICE must be a non-negative integer between 0-9999.
            This function maps between the two node spaces
            
        Keyword Arguments:
            nx_node -- networkx node name
            
        Returns:
            spice node equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if self.spice_node.get(nx_node) is None:
            self.spice_node[nx_node] = str(self.spice_node_count).zfill(4)
            self.spice_node_count += 1
            # check that node count is less than or equal to 9999
            if self.spice_node_count > 9999:
                raise SpiceNodeError('Node count too high')
        
        # return respective SPICE node
        return self.spice_node[nx_node]
        
        
    def get_SPICE_component(self, nx_node):
        """
        Return a unique SPICE component name for the networkx node.
            The defined networkx node names in spice_graph contain spatial information,
            but component names in SPICE must be an alphanumeric identifier less than
            seven characters long. This function maps between the two name spaces
            
        Keyword Arguments:
            nx_node -- networkx node name
            
        Returns:
            spice name equivalent of nx_node
        """
        # if it is not already in the dictionary, add it
        if self.spice_name.get(nx_node) is None:
            self.spice_name[nx_node] = str(self.spice_name_count).zfill(7)
            self.spice_name_count += 1
            # check that node name is less than 7 characters
            if self.spice_name_count > 999999:
                raise SpiceNameError('Name count too high')
        
        # return respective SPICE node
        return self.spice_name[nx_node]
    
    
    def get_NX_node(self, spice_node):
        """
        Return the networkx node name for the given SPICE node.
            The defined networkx nodes in spice_graph contain spatial information,
            but nodes in SPICE must be a non-negative integer between 0-9999.
            This function maps between the two node spaces
            
        Keyword Arguments:
            spice_node -- SPICE node number
            
        Returns:
            networkx node equivalent of spice_node
        """
        for nx_node, spice_node_num in self.spice_node.iteritems():
            if spice_node == spice_node_num:
                return nx_node
    
    
    def _build_wire_pi_model(self, edge):
        """
        Builds a pi wire delay model
        
        Keyword Arguments:
            edge  -- edge of template_graph to be converted to pi model in spice_graph
        """
        # get nodes on either side
        node_1 = edge[0]
        node_2 = edge[1]
        
        # add intermediate node
        interm_node = '{}{}'.format(node_1,node_2)
        self.spice_graph.add_node(interm_node, attr_dict={'type':'node'})
        group_name = interm_node
        
        # check for devices on either side
        #    in the event of a device, create a new node for connections
        #    and connect to device
        if self.spice_graph.node[node_1]['type']=='device':
            new_node_1 = '{}{}'.format(node_1,interm_node)
            self.spice_graph.add_node(new_node_1, attr_dict={'type':'node'})
            self.spice_graph.add_edge(node_1,new_node_1, attr_dict={'type':edge[2]['type']})
            node_1 = new_node_1
        if self.spice_graph.node[node_2]['type']=='device':
            new_node_2 = '{}{}'.format(interm_node,node_2)
            self.spice_graph.add_node(new_node_2, attr_dict={'type':'node'})
            self.spice_graph.add_edge(new_node_2,node_2, attr_dict={'type':edge[2]['type']})
            node_2 = new_node_2

        # add resistance node
        res = ((1.0/edge[2]['res'])*1e-3)
        spice_res = Resistor(self.get_SPICE_component(group_name),
                             self.get_SPICE_node(node_1),
                             self.get_SPICE_node(interm_node),
                             res)
        self.spice_graph.add_node('R{}'.format(group_name), attr_dict={'type':'res','component':spice_res})
        self.spice_graph.add_edge(node_1,'R{}'.format(group_name))
        self.spice_graph.add_edge('R{}'.format(group_name),interm_node)
        
        # add inductance node
        ind = ((1.0/edge[2]['ind'])*1e-9)
        spice_ind = Inductor(self.get_SPICE_component(group_name),
                             self.get_SPICE_node(interm_node),
                             self.get_SPICE_node(node_2),
                             ind)
        self.spice_graph.add_node('L{}'.format(group_name), attr_dict={'type':'ind','component':spice_ind})
        self.spice_graph.add_edge(interm_node,'L{}'.format(group_name))
        self.spice_graph.add_edge('L{}'.format(group_name),node_2)
        
        # add two capacitance nodes
        cap = ((1.0/float(edge[2]['cap']))*1e-12)
        # create two imaginary nodes for the body (for visual purposes)
        self.spice_graph.add_node('B{}_1'.format(group_name), attr_dict={'type':'body'})
        self.spice_graph.add_node('B{}_2'.format(group_name), attr_dict={'type':'body'})
        # create capacitor nodes
        spice_cap1 = Capacitor(self.get_SPICE_component('1'+group_name),
                               self.get_SPICE_node(node_1),
                               self.get_SPICE_node('body'),
                               cap/2.0)
        self.spice_graph.add_node('C{}_1'.format(group_name), attr_dict={'type':'cap','component':spice_cap1})
        self.spice_graph.add_edge(node_1,'C{}_1'.format(group_name))
        self.spice_graph.add_edge('C{}_1'.format(group_name),'B{}_1'.format(group_name))
        spice_cap2 = Capacitor(self.get_SPICE_component('2'+group_name),
                               self.get_SPICE_node(node_2),
                               self.get_SPICE_node('body'),
                               cap/2.0)
        self.spice_graph.add_node('C{}_2'.format(group_name), attr_dict={'type':'cap','component':spice_cap2})
        self.spice_graph.add_edge(node_2,'C{}_2'.format(group_name))
        self.spice_graph.add_edge('C{}_2'.format(group_name),'B{}_2'.format(group_name))
    
    
    def _build_wire_L_model(self, edge, lead, non_lead):
        """
        Builds an L wire delay model
        
        Keyword Arguments:
            edge     -- edge of template_graph to be converted to L model in spice_graph
            lead     -- lead node
            non_lead -- non-lead node
        """
        # add intermediate node
        interm_node = '{}{}'.format(edge[0],edge[1])
        self.spice_graph.add_node(interm_node, attr_dict={'type':'node'})
        group_name = interm_node
        
        # check for device on non_lead side
        #    in the event of a device, create a new node for connections
        #    and connect to device
        if self.spice_graph.node[non_lead]['type']=='device':
            new_non_lead = '{}{}'.format(non_lead,interm_node)
            self.spice_graph.add_node(new_non_lead, attr_dict={'type':'node'})
            self.spice_graph.add_edge(non_lead,new_non_lead, attr_dict={'type':edge[2]['type']})
            non_lead = new_non_lead
        
        # add resistance node
        res = ((1.0/edge[2]['res'])*1e-3)
        spice_res = Resistor(self.get_SPICE_component(group_name),
                             self.get_SPICE_node(lead),
                             self.get_SPICE_node(interm_node),
                             res)
        self.spice_graph.add_node('R{}'.format(group_name), attr_dict={'type':'res','component':spice_res})
        self.spice_graph.add_edge(lead,'R{}'.format(group_name))
        self.spice_graph.add_edge('R{}'.format(group_name),interm_node)
        
        # add inductance node
        ind = ((1.0/edge[2]['ind'])*1e-9)
        spice_ind = Inductor(self.get_SPICE_component(group_name),
                             self.get_SPICE_node(interm_node),
                             self.get_SPICE_node(non_lead),
                             ind)
        self.spice_graph.add_node('L{}'.format(group_name), attr_dict={'type':'ind','component':spice_ind})
        self.spice_graph.add_edge(interm_node,'L{}'.format(group_name))
        self.spice_graph.add_edge('L{}'.format(group_name),non_lead)
        
        # add single capacitance node on non_lead side
        cap = ((1.0/float(edge[2]['cap']))*1e-12)
        # create imaginary node for the body (for visual purposes)
        self.spice_graph.add_node('B{}'.format(group_name), attr_dict={'type':'body'})
        # create capacitance node
        spice_cap = Capacitor(self.get_SPICE_component(group_name),
                              self.get_SPICE_node(non_lead),
                              self.get_SPICE_node('body'),
                              cap)
        self.spice_graph.add_node('C{}'.format(group_name), attr_dict={'type':'cap','component':spice_cap})
        self.spice_graph.add_edge(non_lead,'C{}'.format(group_name))
        self.spice_graph.add_edge('C{}'.format(group_name),'B{}'.format(group_name))

            
    def _create_diode(self, node, model_name):
        """
        Creates a diode model
        
        Keyword Arguments:
            node -- diode node
        """
        # determine diode terminals
        anode = []
        cathode = []
        for edge in self.spice_graph.edges(node, data=True):
            if edge[2]['type'] == 'trace':
                anode.append([an for an in edge if an != node][0])
            elif edge[2]['type'] == 'bw power':
                cathode.append([ca for ca in edge if ca != node][0])
        
        # check terminal connections
        namespace = locals()
        for terminal in [anode,cathode]:
            num_connect = len(terminal)
            # check that all terminals have been assigned
            if num_connect == 0:
                raise TerminalError('Diode', node, [name for name in namespace if namespace[name] is terminal][0])
            # check for multiple connections connected to terminal
            if num_connect > 1:
                # if so, create shorts to connect all traces/bondwires to first node
                for connect in range(1,num_connect):
                    short = Short(self.get_SPICE_node(terminal[connect]),
                                         self.get_SPICE_node(terminal[0]))
                    self.spice_graph.add_node('R{}_short'.format(terminal[connect]), attr_dict={'type':'short','component':short})
                    self.spice_graph.add_edge(terminal[connect],'R{}_short'.format(terminal[connect]))
                    self.spice_graph.add_edge('R{}_short'.format(terminal[connect]),terminal[0])
        
        # create diode
        self.spice_graph.node[node]['component'] = Diode(self.get_SPICE_component(node),
                                                         self.get_SPICE_node(anode[0]),
                                                         self.get_SPICE_node(cathode[0]),
                                                         model_name)
    
    
    def _create_mosfet(self, node, model_name):
        """
        Creates a mosfet model
        
        Keyword Arguments:
            node -- mosfet node
        """
        # determine mosfet terminals
        drain = []
        gate = []
        source = []
        for edge in self.spice_graph.edges(node, data=True):
            if edge[2]['type'] == 'trace':
                drain.append([dr for dr in edge if dr != node][0])
            elif edge[2]['type'] == 'bw signal':
                gate.append([gt for gt in edge if gt != node][0])
                self.gate_nodes.append([gt for gt in edge if gt != node][0])
            elif edge[2]['type'] == 'bw power':
                source.append([src for src in edge if src != node][0])
            
        # check terminal connections
        namespace = locals()
        for terminal in [drain,gate,source]:
            num_connect = len(terminal)
            # check that all terminals have been assigned
            if num_connect == 0:
                raise TerminalError('MOSFET', node, [name for name in namespace if namespace[name] is terminal][0])
            # check for multiple connections connected to terminal
            elif num_connect > 1:
                # if so, create shorts to connect all traces/bondwires to first node
                for connect in range(1,num_connect):
                    short = Short('R{}_short'.format(terminal[connect]), 
                                  self.get_SPICE_node(terminal[connect]),
                                  self.get_SPICE_node(terminal[0]))
                    self.spice_graph.add_node('R{}_short'.format(terminal[connect]), attr_dict={'type':'short','component':short})
                    self.spice_graph.add_edge(terminal[connect],'R{}_short'.format(terminal[connect]))
                    self.spice_graph.add_edge('R{}_short'.format(terminal[connect]),terminal[0])
        
        # create mosfet
        self.spice_graph.node[node]['component'] = Mosfet(self.get_SPICE_component(node),
                                                          self.get_SPICE_node(drain[0]),
                                                          self.get_SPICE_node(gate[0]),
                                                          self.get_SPICE_node(source[0]),
                                                          model_name)
    
    
    def _create_gate_leads(self):
        '''
        Add gate leads for export
        '''
        node_type = nx.get_node_attributes(self.spice_graph, 'type')
        coordinates = nx.get_node_attributes(self.spice_graph, 'point')
        self.gate_trace_endpts = []

        # Iterate through device gate paths to find gate trace endpoints
        for gate in self.gate_nodes:
            count = 0
            current_node = gate
            prev_nodes = []
            prev_nodes.append(gate)
            
            while count < 8:        # Move along path from device gate node to gate trace
                current_node = self._get_next_gate_path_node(current_node, prev_nodes)
                prev_nodes.append(current_node)
                count += 1
            
            # Check if node is an endpoint on the gate trace
            if nx.degree(self.spice_graph, current_node) < 5:
                self.gate_trace_endpts.append(current_node)
        
        # Check number of gate trace endpoints found
        if len(self.gate_trace_endpts) > 4:
            raise Exception('Too many gate trace endpoints found!')
            
        # Determine paths representing gate traces
        possible_gate_trace_paths = []
        for start_pt in self.gate_trace_endpts:
            temp_path = []
            
            for end_pt in [pt for pt in self.gate_trace_endpts if pt != start_pt]:
                temp_path = list(nx.all_shortest_paths(self.spice_graph, start_pt, end_pt))[0]  # Path from start_pt to end_pt
            
                for node in temp_path:
                    if node_type[node] == 'device' or node_type[node] == 'cap':   # Ensure device or capacitor is not present
                        temp_path = []
                        break
                
                if temp_path != []:
                    possible_gate_trace_paths.append(temp_path)
        
        # Eliminate duplicate reversed paths - should be left with 0-2 gate trace paths
        for path in possible_gate_trace_paths:
            for other_path in [other_path for other_path in possible_gate_trace_paths if other_path != path]:
                if path == list(reversed(other_path)):
                    possible_gate_trace_paths.remove(other_path)
        
        gate_trace_paths = possible_gate_trace_paths
        
        # Check if 0-2 gate traces found
        if len(gate_trace_paths) > 2:
            raise Exception('More than two gate traces found!')

        # Add gate leads to graph
        self.gate_leads = []
        for path in gate_trace_paths:
            
            # Add gate lead node
            self.spice_graph.add_node('G'+path[0], attr_dict={'type':'lead', 'point':coordinates[path[0]]})
            
            # Connect gate lead to gate trace endpoint with a short
            short = Short('G'+path[0]+'_short',
                          self.get_SPICE_node('G'+path[0]), 
                          self.get_SPICE_node(path[0]))
            self.spice_graph.add_node('G'+path[0]+'_short', attr_dict={'type':'short', 'component':short})
            self.spice_graph.add_edge('G'+path[0], 'G'+path[0]+'_short') 
            self.spice_graph.add_edge('G'+path[0]+'_short', path[0]) 
            
            
            self.gate_leads.append('G'+path[0])
        
        # --- testing ---
        #print 'GATE LEADS:', (' '.join(self.get_SPICE_node(gate_lead) for gate_lead in self.gate_leads))
        
        #print '\nGate Trace Paths:'
        #for path in gate_trace_paths:
        #    print (' '.join(self.get_SPICE_node(node) for node in path))
        #print '\n'
         
                
    def _get_next_gate_path_node(self, current_node, prev_nodes):
        '''
        Helper function for _create_gate_leads()
        Used to iterate through nodes from device gate node to a node on the gate trace
        
        Keyword Arguments:
            current_node -- it's pretty self-explanatory
            prev_nodes -- list of nodes already iterated through on path
            
        Returns:
            next_node -- next node on path
        '''
        node_type = nx.get_node_attributes(self.spice_graph, 'type')
        next_node = None
        
        # Determine next node from neighbors of current node
        for neighbor in [neighbor for neighbor in nx.all_neighbors(self.spice_graph, current_node) if node_type[neighbor] != 'device' and node_type[neighbor] != 'cap']:  

            if neighbor not in prev_nodes:  # Make sure it doesn't go backwards
                next_node = neighbor
                break
        
        if next_node == None:
            raise Exception('Next node not found!')

        return next_node

        
    def write_SPICE_subcircuit(self, directory):
        """
        Writes H-SPICE subcircuit out to [self.name].inc in the directory specified
        
        Keyword Arguments:
            directory  -- file directory to write file to
            
        Returns:
            SPICE file path
        """
        
        # write each device Verilog-A file to local directory
        for model in self.device_models.itervalues():
            full_path = os.path.join(directory, '{}.va'.format(model[0]))
            model_file = open(full_path, 'w')
            model_file.write(model[1])
            model_file.close()
        
        # find leads of module
        lead_list = ''
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            lead_list += ' ' + self.get_SPICE_node(lead[0])
        lead_list += ' ' + self.get_SPICE_node('body')
        
        # prepare netlist file
        full_path = os.path.join(directory, '{}.inc'.format(self.name))
        spice_file = open(full_path, 'w')
        
        # write module name
        spice_file.write('*{}\n'.format(self.name))
        
        # include each device model
        spice_file.write('\n*** Device Models ***\n')
        for model in self.device_models.itervalues():
            spice_file.write('.hdl "{}.va"\n'.format(model[0]))
            
        # write subcircuit start line with list of lead nodes
        spice_file.write('\n\n.SUBCKT {}{}\n'.format(self.name, lead_list))
        
        # write SPICE line for each node that has a component
        spice_file.write('\n*** {} Components ***\n'.format(self.name))  
        for node in self.spice_graph.nodes(data=True):            
            if node[1].get('component') is not None:
                spice_file.write(node[1]['component'].SPICE +'\n')
                
        # end subcircuit file
        spice_file.write('\n.ENDS {}'.format(self.name))
        spice_file.close()
        
        # save layout image to clarify lead names
        self.draw_layout()        
        plt.savefig(os.path.join(directory, '{}_lead_layout.png'.format(self.name)))
        '''
        # testing
        print 'names'
        for key,val in self.spice_name.items(): print '{}: {}'.format(key,val)
        print '\n\nnodes'
        for key,val in self.spice_node.items(): print '{}: {}'.format(key,val)
        '''
        return full_path
    
    def write_SPICE_reduced_subcircuit(self, directory):
        '''sxm063 Apr 2016 - This function is used to write a spice netlist similar to the one defined in write_SPICE_subcircuit()
        except that it reduces series and parallel components to their equivalents. '''
        
        
        # write each device Verilog-A file to local directory
        for model in self.device_models.itervalues():
            full_path = os.path.join(directory, '{}.va'.format(model[0]))
            model_file = open(full_path, 'w')
            model_file.write(model[1])
            model_file.close()
        
        # find leads of module
        lead_list = ''
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            lead_list += ' ' + self.get_SPICE_node(lead[0])
        lead_list += ' ' + self.get_SPICE_node('body')
        
        # prepare netlist file
        full_path = os.path.join(directory, '{}.inc'.format(self.name))
        spice_file = open(full_path, 'w')
        
        # write module name
        spice_file.write('*{}\n'.format(self.name))
        
        # include each device model
        spice_file.write('\n*** Device Models ***\n')
        for model in self.device_models.itervalues():
            spice_file.write('.hdl "{}.va"\n'.format(model[0]))
            
        # write subcircuit start line with list of lead nodes
        spice_file.write('\n\n.SUBCKT {}{}\n'.format(self.name, lead_list))
        
        # write SPICE line for each node that has a component
        spice_file.write('\n*** {} Components ***\n'.format(self.name))  
        
        # sxm - 
        a=[]
        #print self.spice_graph.nodes
        for node in self.spice_graph.nodes(data=True):       
            sub_a=[]
            if node[1].get('component') is not None:
                print node[1]['component']
                sub_a.append(node[1]['component'].SPICE[:8])      # name
                sub_a.append(node[1]['component'].SPICE[9:13])    # node1  
                sub_a.append(node[1]['component'].SPICE[14:18])   # node2
                sub_a.append(node[1]['component'].SPICE[19:])     #value  
                a.append(sub_a)
        #print a
        #print "---------------"
        #print a[0]
                
        # sxm - add  capacitances that are in parallel
        for i in range(0,len(a)):
            if (a[i][0][:1]=="C" and len(a[i])==4): # for each line in the spice network 
                for j in range(i+1,len(a)): # for all other lines below the line being compared
                    #print j
                    if (a[j][0][:1]=="C" and len(a[j])==4): # check if both components are capacitors
                        if ((a[i][1]==a[j][1] and a[i][2]==a[j][2]) or (a[i][2]==a[j][1] and a[i][1]==a[j][2])): # check if the two devices are in parallel by checking node commonality (node 1&2 of component1 = node 1&2 of component2 OR node 1&2 of component1 = node 2&1 of component2)
                            #print i,j
                            #print a[i]
                            #print a[j]
                            #print a[i][3]+a[j][3]
                            #update the first row
                            a[i].insert(3, add(float(a[i][3]), float(a[j][3]))) # insert equivalent capacitor value at appropriate location of the line                                
                            #print "line " + i + ":" + a[i]
                            a[i].pop(4) # remove old capacitor value
                            #mark the second row for removal
                            a[j].insert(4, "remove") # remove the 2nd of the two capacitor lines (since it is already accounted for in the equivalent value)
                            #print "Equivalent:"
                            #print a[i]
                            #print a[j]                           
                            #j-=1 # since one line was removed, all lines will move up by one. Therefore, decrement j so as not to miss a line in the comparison.
                            #print i,j 
        #print "\n Old"
        for items in a:
            print items
        
        # remove the lines that have been accounted for (i.e. that lines marked with the word "remove")
        #print "\n -------------"
        #print "\n To be removed"        
        count=0
        #print "initial count ", count
        for i in range(0,len(a)-1):
            #print "items removed (count) =", count, " i=", i, " index=", i-count, " len(a[i-count])=", len(a[i-count])            
            if len(a[i-count])>4:
                #print i-count, a[i-count] 
                a.pop(i-count)
                count = count + 1 
                #print "number of items removed (count) = ", count
            
                
        #print "\n New"
        #for items in a:
           # print items
            
        # write netlist lines
        for spice_line in a:
            #spice_file.write(str(spice_line) +'\n')    
            #spice_file.write(spice_line.SPICE + '\n')
            spice_file.write("{name} {N1} {N2} {value}".format(name=spice_line[0], N1=spice_line[1], N2=spice_line[2], value=spice_line[3]) + '\n')            
        
        # end subcircuit file
        spice_file.write('\n.ENDS {}'.format(self.name))
        spice_file.close()
        
        # save layout image to clarify lead names
        self.draw_layout()        
        plt.savefig(os.path.join(directory, '{}_lead_layout.png'.format(self.name)))
                    
        #self.draw_graph() #sxm063 testing; this code outputs the network-x nodes map as an image; delete this line after testing
        #plt.savefig(os.path.join(directory, '{}_nx_nodes.png'.format(self.name)))
        
        '''
        #create reduced netlist graph
        self.reduced_netlist_graph = nx.Graph()
        #add nodes to graph:
        #spice_node_list=[]
        self.reduced_netlist_graph.add_nodes_from('{}'.format(spice_line[0]) for spice_line in a)
        plt.close()
        ax = plt.subplot('111', adjustable='box', aspect=1.0)
        ax.set_axis_off()
        pos = nx.spring_layout(self.reduced_netlist_graph,scale=50)
        nx.draw_networkx_nodes(self.reduced_netlist_graph, pos, node_size=100, node_color='blue', node_shape='o', alpha=0.7)
        nx.draw_networkx_edges(self.reduced_netlist_graph, pos, edge_color='black')
        nx.draw_networkx_labels(self.reduced_netlist_graph, pos, font_size=7, font_weight=3)
        plt.show()
        plt.savefig(os.path.join(directory, '{}_reduced_netlist_graph.png'.format(self.name)))
        '''
        return full_path                                  

    def draw_layout(self):
        """ Draws symbolic layout and labels lead nodes for connecting into circuit """
        plt.close()
        ax = plt.subplot('111', adjustable='box', aspect=1.0)
        ax.set_axis_off()
        fig = plot_layout(self.sym_layout, ax = ax, new_window=False)
        # label leads
        for lead in [node for node in self.spice_graph.nodes(data=True) if node[1]['type']=='lead']:
            pos = lead[1]['point']
            name = lead[0]
            fig.text(pos[0], pos[1], self.get_SPICE_node(name),
                    horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='yellow', alpha=0.8))
        # add body label
        fig.text(0,0,'body: {}'.format(self.get_SPICE_node('body')),horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='yellow', alpha=0.8))
        
        # show plot
        plt.title(self.name)
        plt.show()
        
        
        
    def draw_graph(self):
        """ Draws networkx graph of spice_graph """   
        
        # sxm testing 2016 Mar 31 ------- this section added for testing purposes only; to be deleted after testing ---------     
        plt.close() #sxm test
        ax = plt.subplot('111', adjustable='box', aspect=1.0) #sxm test
        ax.set_axis_off() #sxm test
        # sxm test block-----------------------------------------------------------------------------------------------------
        
        pos = nx.spring_layout(self.spice_graph,scale=50) #sxm test; original scale=50
        nx.draw_networkx_nodes(self.spice_graph, pos, node_size=100, node_color='blue', node_shape='o', alpha=0.7) #sxm test; original node_size=400
        nx.draw_networkx_edges(self.spice_graph, pos, edge_color='black')
        nx.draw_networkx_labels(self.spice_graph, pos, font_size=7, font_weight=3) #sxm test; original font_size=10, weight=2
        plt.show()
           

# unit-testing
if __name__ == '__main__':
    
    import pickle
    from test_functions import *

    test_graph = None
#    test_graph = build_test_graph();
#    test_graph = build_diode_test_graph()
#    test_graph = build_diode_test_graph_2()
#    test_graph = build_mosfet_test_graph()
#    test_graph = build_mosfet_test_graph_2()
  
    def load_symbolic_layout(filename):
        f = open(filename, 'r')
        sym_layout = pickle.load(f)
        f.close()
        return sym_layout
    
    sym_layout = load_symbolic_layout("../../../export_data/symlayout.p")     
    
    spice_graph = Module_SPICE_netlist_graph('Module_2', sym_layout, 10, test_graph)
    spice_graph.write_SPICE_subcircuit('C:\Users\qmle\Desktop\Thermal\BIN') 
    
    spice_graph.draw_layout()

#    spice_graph.draw_graph()
