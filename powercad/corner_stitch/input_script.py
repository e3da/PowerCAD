# intermediate input conversion file. Author @ Imam Al Razi (5-29-2019)

import re
from powercad.cons_aware_en.cons_engine import *
import pandas as pd
import constraint
from CornerStitch import *
from PySide import QtCore, QtGui
import sys
from powercad.project_builder.proj_dialogs import ConsDialog
from powercad.design.parts import *
from powercad.cons_aware_en.cons_engine import New_layout_engine
class ConstraintWindow(QtGui.QMainWindow):
    # A fake window to call the constraint dialog object
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        self.cons_df = None

class RoutingPath():
    def __init__(self,name=None,type=None,layout_component_id=None):
        '''

        :param name: routing path name: trace,bonding wire pads,vias etc.
        :param type: power:0, signal:1
        :param layout_component_id: 1,2,3.... id in the layout information
        '''
        self.name = name
        self.type = type
        self.layout_component_id = layout_component_id

    def printRoutingPath(self):

        print "Name: ", self.name
        if self.type==0:
            print "Type:  power trace"
        else:
            print "Type:  signal trace"
        print "ID in layout: ", self.layout_component_id



def read_input_script(input_file=None):

    with open(input_file,'rb') as fp:
        lines = fp.readlines()
    Definition=[]  # saves lines corresponding to definition in the input script
    layout_info=[] # saves lines corresponding to layout_info in the input script
    for i in range(1,len(lines)):
        line=lines[i]
        if len(line)!=2:
            L = line.strip('\r\n')
            d_out = re.sub("\t", ". ", L)
            d_out = re.sub("\s", ",", d_out)
            line = d_out.rstrip(',')
            line = line.split(',')
            Definition.append(line)
        else:
            part2=i
            break

    for i in range(part2+2,len(lines)):
        line=lines[i]
        L = line.strip('\r\n')
        d_out = re.sub("\t", ". ", L)
        d_out = re.sub("\s", ",", d_out)
        line = d_out.rstrip(',')
        line = line.split(',')
        layout_info.append(line)
    #print part2, Definition
    #print layout_info
    for i in layout_info:
        print len(i),i


    return Definition,layout_info

def gather_part_route_info(Definition=None,layout_info=None):
    all_parts_info = {}  # saves a list of parts corresponding to name of each part as its key
    info_files = {}  # saves each part technology info file name
    for i in Definition:
        key = i[0]
        all_parts_info.setdefault(key, [])
        info_files[key] = i[1]

    # updates type list according to definition input

    for i in Definition:

        if i[0] not in constraint.constraint.all_component_types:
            c=constraint.constraint()
            constraint.constraint.add_component_type(c,i[0])
    all_components_list =  constraint.constraint.all_component_types  # set of all components considered so far




    all_route_info = {}
    for j in range(1, len(layout_info)):
        if layout_info[j][1][0] == 'T':
            key = 'trace'
            all_route_info.setdefault(key, [])
        elif layout_info[j][1][0] == 'B':
            key = 'bonding wire pad'
            all_route_info.setdefault(key, [])
        elif layout_info[j][1][0] == 'V':
            key = 'via'
            all_route_info.setdefault(key, [])


    for j in range (1,len(layout_info)):

        #updates routing path components
        if layout_info[j][1][0]=='T' and layout_info[j][2]=='power':
            element=RoutingPath(name='trace',type=0,layout_component_id=layout_info[j][1])
            all_route_info['trace'].append(element)
        elif layout_info[j][1][0]=='T' and layout_info[j][2]=='signal':
            element = RoutingPath(name='trace', type=1, layout_component_id=layout_info[j][1])
            all_route_info['trace'].append(element)
        elif layout_info[j][1][0]=='B' and layout_info[j][2]=='signal':
            element = RoutingPath(name='bonding wire pad', type=1, layout_component_id=layout_info[j][1])
            all_route_info['bonding wire pad'].append(element)
        elif layout_info[j][1][0]=='B' and layout_info[j][2]=='power':
            element = RoutingPath(name='bonding wire pad', type=0, layout_component_id=layout_info[j][1])
            all_route_info['bonding wire pad'].append(element)

        elif layout_info[j][1][0] == 'D' and layout_info[j][2] in all_components_list and len(layout_info[j])<6:
            element = Part(name= layout_info[j][2],info_file=info_files[layout_info[j][2]], layout_component_id=layout_info[j][1])
            element.load_part()
            all_parts_info[layout_info[j][2]].append(element)
        elif layout_info[j][1][0] == 'L' and layout_info[j][2] == 'power_lead' and layout_info[j][2] in all_components_list and len(layout_info[j])<6:
            element = Part(name=layout_info[j][2], info_file=info_files[layout_info[j][2]], layout_component_id=layout_info[j][1])
            element.load_part()
            all_parts_info[layout_info[j][2]].append(element)
        elif layout_info[j][1][0] == 'L' and layout_info[j][2] == 'signal_lead' and layout_info[j][2] in all_components_list and len(layout_info[j])<6:
            element = Part(name=layout_info[j][2], info_file=info_files[layout_info[j][2]], layout_component_id=layout_info[j][1])
            element.load_part()
            all_parts_info[layout_info[j][2]].append(element)
        elif layout_info[j][1][0] == 'D' and layout_info[j][2] in all_components_list and len(layout_info[j])==6 and layout_info[j][5][0]=='R':
            element = Part(info_file=info_files[layout_info[j][2]],layout_component_id=layout_info[j][1])
            element.load_part()
            #print element.footprint
            if layout_info[j][5].strip('R')=='90':
                name=layout_info[j][2]+'_'+'90'
                element.name=name
                element.rotate_angle=1
                element.rotate_90()
            elif layout_info[j][5].strip('R')=='180':
                name = layout_info[j][2] + '_' + '180'
                element.name = name
                element.rotate_angle = 2
                element.rotate_180()
            elif layout_info[j][5].strip('R')=='270':
                name = layout_info[j][2] + '_' + '270'
                element.name = name
                element.rotate_angle = 3
                element.rotate_270()
            #print element.footprint
            all_parts_info[layout_info[j][2]].append(element)
        elif layout_info[j][1][0] == 'L' and layout_info[j][2] == 'power_lead' and layout_info[j][2] in all_components_list and len(layout_info[j])==6 and layout_info[j][5][0]=='R':
            element = Part( info_file=info_files[layout_info[j][2]], layout_component_id=layout_info[j][1])
            element.load_part()

            if layout_info[j][5].strip('R')=='90':
                name = layout_info[j][2] + '_' + '90'
                element.name = name
                element.rotate_angle=1
                element.rotate_90()
            elif layout_info[j][5].strip('R')=='180':
                name = layout_info[j][2] + '_' + '180'
                element.name = name
                element.rotate_angle = 2
                element.rotate_180()
            elif layout_info[j][5].strip('R')=='270':
                name = layout_info[j][2] + '_' + '270'
                element.name = name
                element.rotate_angle = 3
                element.rotate_270()
            all_parts_info[layout_info[j][2]].append(element)
        elif layout_info[j][1][0] == 'L' and layout_info[j][2] == 'signal_lead' and layout_info[j][2] in all_components_list and len(layout_info[j])==6 and layout_info[j][5][0]=='R':
            element = Part( info_file=info_files[layout_info[j][2]], layout_component_id=layout_info[j][1])
            element.load_part()
            if layout_info[j][5].strip('R')=='90':
                name = layout_info[j][2] + '_' + '90'
                element.name = name
                element.rotate_angle=1
                element.rotate_90()
            elif layout_info[j][5].strip('R')=='180':
                name = layout_info[j][2] + '_' + '180'
                element.name = name
                element.rotate_angle = 2
                element.rotate_180()
            elif layout_info[j][5].strip('R')=='270':
                name = layout_info[j][2] + '_' + '270'
                element.name = name
                element.rotate_angle = 3
                element.rotate_270()
            all_parts_info[layout_info[j][2]].append(element)

        else:
            name=layout_info[j][1][0]+'_'+layout_info[j][2]
            c=constraint.constraint()
            constraint.constraint.add_component_type(c,name)
            element=  RoutingPath(name=name, type=1, layout_component_id=layout_info[j][1])
            key=name
            all_route_info.setdefault(key,[])
            all_route_info[key].append(element)



    for key,comp in all_parts_info.items():
        for element in comp:
            if element.rotate_angle in [1,2,3]:
                c = constraint.constraint()
                name=element.name
                constraint.constraint.add_component_type(c, name)

    all_components_type_mapped_dict = constraint.constraint.component_to_component_type



    print all_parts_info, info_files
    print all_route_info
    print "map",all_components_type_mapped_dict



    #all_parts_info= {'MOS': [M1, M2], 'power_lead': [L1,L2,,,]}
    #info_files={'MOS':file1,'power_lead':file2}
    #all_route_info={'trace': [T1,t2,...],'bonding wire pad':[B1,B2...]}
    #all_components_type_mapped_dict={'MOS': 'Type_5', 'signal_lead': 'Type_4', 'power_lead': 'Type_3', 'EMPTY': 'EMPTY', 'signal_trace': 'Type_2','power_trace': 'Type_1', 'MOS_90': 'Type_6'}
    return all_parts_info,info_files,all_route_info,all_components_type_mapped_dict


def gather_layout_info(layout_info=None,all_parts_info=None,all_route_info=None,all_components_mapped_type_dict=None):
    size = [float(i) for i in layout_info[0]]  # extracts layout size (1st line of the layout_info)
    cs_info = []  # list of rectanges to be used as cornerstitch input information



    component_to_cs_type = {}
    # all_components=['EMPTY','power_trace','signal_trace','signal_lead', 'power_lead', 'MOS', 'IGBT', 'Diode','bonding wire pad','via']

    all_components_type_mapped_dict=all_components_mapped_type_dict # dict to map component type and cs type
    all_components_list= all_components_type_mapped_dict.keys()


    print all_components_list #all_components_list=['MOS', 'signal_lead', 'power_lead', 'EMPTY', 'signal_trace', 'power_trace', 'MOS_90']
    print all_components_type_mapped_dict



    all_component_type_names = ["EMPTY"]
    all_components = []
    for j in range(1, len(layout_info)):
        for k, v in all_parts_info.items():
            for element in v:
                if element.layout_component_id == layout_info[j][1]:
                    if element not in all_components:
                        all_components.append(element)
                    if element.name not in all_component_type_names:
                        all_component_type_names.append(element.name)
        for k, v in all_route_info.items():
            for element in v:

                if element.layout_component_id == layout_info[j][1]:
                    if element not in all_components:
                        all_components.append(element)
                    if element.type == 0 and element.name == 'trace':
                        type_name = 'power_trace'
                    elif element.type == 1 and element.name == 'trace':
                        type_name = 'signal_trace'
                if type_name not in all_component_type_names:
                    all_component_type_names.append(type_name)


    print all_component_type_names #['EMPTY', 'power_trace', 'signal_trace', 'MOS_90', 'MOS', 'power_lead', 'signal_lead']



    for i in range(len(all_component_type_names)):
        #print all_component_type_names[i]
            component_to_cs_type[all_component_type_names[i]] = all_components_type_mapped_dict[all_component_type_names[i]]

    print"CS", component_to_cs_type #{'MOS': 'Type_5', 'signal_lead': 'Type_4', 'power_lead': 'Type_3', 'EMPTY': 'EMPTY', 'signal_trace': 'Type_2', 'power_trace': 'Type_1', 'MOS_90': 'Type_6'}


    for k, v in all_parts_info.items():
        for comp in v:
            comp.cs_type = component_to_cs_type[comp.name]


            print comp.cs_type



    for j in range(1, len(layout_info)):
        for k, v in all_parts_info.items():
            for element in v:
                if element.layout_component_id == layout_info[j][1]:
                    type = component_to_cs_type[element.name]
                    x = float(layout_info[j][3])
                    y = float(layout_info[j][4])
                    width = element.footprint[0]
                    height = element.footprint[1]
                    name = layout_info[j][1]
                    Schar = '/'
                    Echar = '/'
                    rect_info = [type, x, y, width, height, name, Schar, Echar]
                    cs_info.append(rect_info)

        for k, v in all_route_info.items():
            for element in v:
                if element.layout_component_id == layout_info[j][1]:
                    if element.type == 0 and element.name == 'trace':
                        type_name = 'power_trace'
                    elif element.type == 1 and element.name == 'trace':
                        type_name = 'signal_trace'
                    type = component_to_cs_type[type_name]
                    x = float(layout_info[j][3])
                    y = float(layout_info[j][4])
                    width = float(layout_info[j][5])
                    height = float(layout_info[j][6])
                    name = layout_info[j][1]
                    Schar = '/'
                    Echar = '/'
                    rect_info = [type, x, y, width, height, name, Schar, Echar]
                    cs_info.append(rect_info)
                else:
                    continue

    print cs_info

    return size,cs_info,component_to_cs_type,all_components

def update_constraint_table(all_components=None,component_to_cs_type=None):


    #init_constraint=constraint.constraint()
    #init_constraint.update_constraints(all_components=all_components, component_to_cs_type=component_to_cs_type)

    #Types=init_constraint.Type

    Types_init=component_to_cs_type.values()
    print Types_init
    Types = [0 for i in range(len(Types_init))]
    for i in Types_init:
        if i=='EMPTY':
            Types[0]=i
        else:
            t=i.strip('Type_')
            ind=int(t)
            Types[ind]=i


    #print Types

    all_rows = []
    r1 = ['Min Dimensions']
    r1_c=[]
    for i in range(len(Types)):
        for k,v in component_to_cs_type.items():
            if v==Types[i]:
                r1_c.append(k)
    r1+=r1_c
    all_rows.append(r1)
    print r1

    r2 = ['Min Width']
    r2_c=[0 for i in range(len(Types))]
    for i in range(len(Types)):
        if Types[i]=='EMPTY':
            r2_c[i]=1.0
        else:
            for k,v in component_to_cs_type.items():

                if v==Types[i]:
                    for comp in all_components:
                        if k==comp.name:
                            #print "H",k,v,comp.footprint
                            if r2_c[i]==0:
                                r2_c[i]=comp.footprint[0]
                                break
    for i in range(len(r2_c)):
        if r2_c[i]==0:
            r2_c[i]=2.0




    r2+=r2_c
    all_rows.append(r2)

    print r2


    r3 = ['Min Height']
    r3_c = [0 for i in range(len(Types))]
    for i in range(len(Types)):
        if Types[i]=='EMPTY':
            r3_c[i]=1.0
        else:
            for k, v in component_to_cs_type.items():
                if v == Types[i]:
                    for comp in all_components:
                        if k == comp.name:
                            if r3_c[i] == 0:
                                r3_c[i] = comp.footprint[1]
                                break
    for i in range(len(r3_c)):
        if r3_c[i]==0:
            r3_c[i]=2.0

    r3 += r3_c
    all_rows.append(r3)
    print r3

    r4 = ['Min Extension']
    r4_c = [0 for i in range(len(Types))]
    for i in range(len(Types)):
        if Types[i]=='EMPTY':
            r4_c[i]=1.0
        else:
            for k, v in component_to_cs_type.items():
                if v == Types[i]:
                    for comp in all_components:
                        if k == comp.name:
                            if r4_c[i] == 0:
                                val = max(comp.footprint)
                                r4_c[i] = val
                                break
    for i in range(len(r4_c)):
        if r4_c[i]==0:
            r4_c[i]=2.0


    r4 += r4_c
    all_rows.append(r4)
    print r4

    r5 = ['Min Spacing']
    r5_c = []
    for i in range(len(Types)):
        for k, v in component_to_cs_type.items():
            if v == Types[i]:
                r5_c.append(k)
    r5 += r5_c
    all_rows.append(r5)
    print r5

    space_rows=[]
    print Types
    for i in range(len(Types)):
        for k,v in component_to_cs_type.items():

            if v==Types[i]:

                row=[k]
                for j in range(len(Types)):
                    row.append(2.0)
                space_rows.append(row)
                all_rows.append(row)
    print space_rows

    r6 = ['Min Enclosure']
    r6_c = []
    for i in range(len(Types)):
        for k, v in component_to_cs_type.items():
            if v == Types[i]:
                r6_c.append(k)
    r6 += r6_c
    all_rows.append(r6)
    print r6
    enclosure_rows=[]
    for i in range(len(Types)):
        for k,v in component_to_cs_type.items():
            if v==Types[i]:
                row=[k]

                for j in range(len(Types)):
                    row.append(1.0)
                enclosure_rows.append(row)
                all_rows.append(row)
    print enclosure_rows
    df = pd.DataFrame(all_rows)

    df.to_csv('out.csv', sep=',', header=None, index=None)
    return df,Types


def show_constraint_table(cons_df=None):

    app = QtGui.QApplication(sys.argv)
    main_window = ConstraintWindow()
    dialog = ConsDialog(parent=main_window, cons_df=cons_df)
    dialog.show()
    dialog.exec_()
    return main_window.cons_df
    #print "parent consdf",main_window.cons_df


def convert_rectangle(cs_info):

    input_rects=[]
    for rect in cs_info:
        type=rect[0]
        x=rect[1]
        y=rect[2]
        width=rect[3]
        height=rect[4]
        name=rect[5]
        Schar=rect[6]
        Echar=rect[7]
        input_rects.append(Rectangle(type, x, y, width, height, name, Schar=Schar, Echar=Echar))

    return input_rects

def plot_layout(fig=None,size=None):
    fig2, ax2 = plt.subplots()
    Names = fig.keys()
    Names.sort()
    for k, p in fig.items():

        if k[0] == 'T':
            x = p.get_x()
            y = p.get_y()
            ax2.text(x + 0.1, y + 0.1, k)
            ax2.add_patch(p)

    for k, p in fig.items():

        if k[0] != 'T':
            x = p.get_x()
            y = p.get_y()
            ax2.text(x + 0.1, y + 0.1, k, weight='bold')
            ax2.add_patch(p)
    ax2.set_xlim(0, size[0])
    ax2.set_ylim(0, size[1])
    plt.show()



def mode_zero(cons_df,Htree,Vtree): # evaluates mode 0(minimum sized layouts)

    CG1 = CS_to_CG(0)
    CG1.getConstraints(cons_df)
    #ledge_width=float(cons_df.iat[10,2])
    #ledge_height=float(cons_df.iat[10,2])

    #self.cons_df.to_csv('out_2.csv', sep=',', header=None, index=None)
    Evaluated_X, Evaluated_Y = CG1.evaluation(Htree=Htree, Vtree=Vtree, N=None, W=None, H=None, XLoc=None, YLoc=None,seed=None,individual=None)

    print "X",Evaluated_X
    print "Y",Evaluated_Y
    return Evaluated_X, Evaluated_Y

def plot_solution(Patches=None):
    for i in range(len(Patches)):
        fig, ax1 = plt.subplots()
        for k, v in Patches[i].items():
            for p in v:
                ax1.add_patch(p)
            ax1.set_xlim(0, k[0])
            ax1.set_ylim(0, k[1])

        ax1.set_aspect('equal')
        plt.savefig('C:\Users\qmle\Desktop\New_Layout_Engine\New_design_flow\\'+str(i)+'.png')

def test_file(input_script=None):
    if input_script==None:
        input_file = "C:\Users\ialrazi\Desktop\REU_Data_collection_input\h-bridge.txt"  # input script location
    else:
        input_file=input_script

    definition, layout_info = read_input_script(input_file)
    all_parts_info, info_files, all_route_info, all_components_mapped_type_dict = gather_part_route_info(Definition=definition, layout_info=layout_info)

    size, cs_info, component_to_cs_type, all_components = gather_layout_info(layout_info, all_parts_info,all_route_info,all_components_mapped_type_dict)
    print size
    print len(cs_info), cs_info
    print component_to_cs_type

    df, Types = update_constraint_table(all_components, component_to_cs_type)

    cons_df = show_constraint_table(df)
    input_rects = convert_rectangle(cs_info)

    # init_data,Htree,Vtree=create_cornerstitch(input_rects, size)
    # mode_zero(cons_df,Htree,Vtree)
    engine = New_layout_engine()
    engine.cons_df = cons_df
    engine.create_cornerstitch(input_rects, size)
    engine.Types = Types

    engine.all_components = all_components

    Patches, cs_sym_data = engine.generate_solutions(level=0, num_layouts=1, W=None, H=None, fixed_x_location=None,fixed_y_location=None, seed=None, individual=None)
    print Patches
    plot_solution(Patches)
    return all_components,cs_sym_data


if __name__ == '__main__':
    file = os.path.abspath("C:\Users\qmle\Desktop\New_Layout_Engine\New_design_flow\Halfbridge1.txt")
    component_list,layout_info=test_file(input_script=file)
    print "outside"
    print len(component_list),component_list
    print len(layout_info),layout_info
