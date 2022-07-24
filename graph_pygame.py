# coding: utf-8
# by Joao Bueno
from random import randrange, choice
from re import L, M
from turtle import home
from venv import create
from matplotlib.pyplot import sca, yscale
import pygame
import json
import numpy as np
 
FR = 30
SIZE = 900, 680
BGCOLOR = (255,255,255)
NODECOLOR = (255,0,0)
NODESIZE = 4,4
GRIDSPACING = 50
MAXTRIES = 1000
STARTINGNODES = 8
 
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.nodes_list = list()
        # record positions of each node, so that we can check for overlaps
        self.positions = dict()
 
    def add(self, node, pos):
        
            self.nodes.add(node)
            self.nodes_list.append(node)
            node.setpos((pos[0], pos[1]), self)
            
    def update(self):
        SCREEN.fill(BGCOLOR)
        for node in self.nodes:
            pygame.draw.rect(SCREEN, node.color, node.rect)
            for neighbor in node.neighbors:
                pygame.draw.line(SCREEN, NODECOLOR,
                    node.rect.center, neighbor.rect.center)
 
class Node(object):
    # Class variable, incremented with each
    # instance so that each node has a unique ID that
    # can be used as its hash:
    creation_counter = 0
    def __init__(self, color):
        self.id = self.__class__.creation_counter
        self.__class__.creation_counter += 1
        # We don't  set this attribute here, but by adding then here,
        # we indicate that it "exists" for readers of the code:
        self.rect = None
        self.color = color
        self.neighbors = set()
 
    def setpos(self, pos, graph = None):
        if self.rect and graph:
            # remove self from previous position in the graph:
            graph.positions.pop(self.rect.topleft, None)
        # self.rect = pygame.Rect(pos[0], pos[1],NODESIZE[0], NODESIZE[1])
        self.rect = pygame.Rect(pos[0], pos[1],NODESIZE[0], NODESIZE[1])
        self.pos = pos
        if graph:
            graph.positions[pos] = self
        # print('Set pos done')
    def  __hash__(self):
        return self.id
 

def get_cluster_data(fname= 'output/TSP_phase.json'):
    cluster_data = json.load(open(fname, 'r'))
    return cluster_data

def create_graph(location_list, color_list, correlate_list):
    # create new graph and populate nodes:
    graph = Graph()
    # locallist for adding neighbors:
    nodes = []
    for i in range(len(location_list)):
        node = Node(color_list[i])
        graph.add(node, location_list[i])

    nodes = graph.nodes_list
    n_nodes = len(location_list)
    for i in range(n_nodes):
        for j in range(n_nodes):
            if correlate_list[i][j] !=0:
                nodes[i].neighbors.add(nodes[j])
                nodes[j].neighbors.add(nodes[i])

        # randomly connect node with some other nodes
        # if nodes:
        #     for i in range(0, randrange(1,3)):
        #         neighbor = choice(nodes)
        #         # Without a special collection, or an "Edge" class,
        #         # in adirectional graphs, we should always upddate
        #         # neighbor set in both nodes:
        #         node.neighbors.add(neighbor)
        #         neighbor.neighbors.add(node)
        # nodes.append(node)
    return graph
 
def init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SIZE)
 
def quit():
    pygame.quit()

def scale(at_position, x_scale, y_scale, point_list):
    #Dùng để đánh lại các tọa độ khi zoom 

    return_point_list = []
    for point in point_list:
        dx_new = x_scale*(point[0]-at_position[0])
        dy_new = y_scale*(point[1] - at_position[1])
        return_point_list.append([at_position[0]+dx_new, at_position[1]+dy_new])
    
    return return_point_list

def transition(x_trans, y_trans, point_list):
    return list(np.array(point_list)+np.array([x_trans, y_trans]))

# Đổi từ tọa độ lat long về hệ tọa độ descartes
def convert_lat_long_to_descartes(location_list, x_low, x_high, y_low, y_high):

    # Lấy ra các điểm cực N,E,W,S
    n_pole, e_pole, w_pole, s_pole = [0, 10000], [0, 0], [10000, 0], [0, 0]
    for point in location_list:
        print('Cluster center: {}'.format(point))
        if point[0] < w_pole[0]: w_pole = point #update west pole
        if point[0] > e_pole[0]: e_pole = point #update east pole
        if point[1] < n_pole[1]: n_pole = point #update north pole
        if point[1] > s_pole[1]: s_pole = point #update south pole

    print('N_pole = {}\nS_pole = {}\nE_pole = {}\nW_pole = {}'.format(n_pole, s_pole, e_pole, w_pole))
    print('X trans = {}, y_trans = {}'.format(x_low - w_pole[0], y_low - n_pole[1]))
    print('X scale = {}, y scale = {}'.format((x_high-x_low)/(e_pole[0]-x_low), (y_high-y_low)/(n_pole[1]-y_low)))
    x_trans, y_trans = x_low - w_pole[0], y_low - n_pole[1]
    new_point_list = scale([x_low, y_low], (x_high-x_low)/(e_pole[0]-w_pole[0]), (y_high-y_low)/(s_pole[1]-n_pole[1]), transition(x_low - w_pole[0], y_low - n_pole[1], location_list))
    return new_point_list

def round(point_list):
    return np.round(point_list)

def create_button(rect, text):
    global SCREEN
    color_dark = (100,100,100)
    pygame.draw.rect(SCREEN, color_dark, rect)
    smallfont = pygame.font.SysFont('Corbel',16) 
    t = smallfont.render(text , True , (255,255,255))
    SCREEN.blit(t , (rect[0]+10, rect[1]+5))



def main():
    
    offset = [60, 60]
    x_low, y_low = offset
    x_high, y_high = np.array(SIZE) - np.array(offset)
    TSP_data = get_cluster_data()
    cluster_data = get_cluster_data('output/pre_TSP_phase.json')
    
    mapping_code_to_index = {}
    # Lấy ra các tâm cụm lưu vào mảng
    cluster_center_list = []
    color_list_no_child = []

    cluster_center_list_with_child = []
    color_list_with_child = []

    full_node_list = []

    # Danh sách các màu
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    for key1 in TSP_data:

        cluster_center_list.append([float(TSP_data[key1]['center']['lat']), float(TSP_data[key1]['center']['long'])])
        color_list_no_child.append(red)
        cluster_center_list_with_child.append(cluster_center_list[-1])
        color_list_with_child.append(red)
        full_node_list.append(cluster_center_list[-1])

        if len(cluster_data[key1]['child_cluster_list'])>1:
            for key2 in TSP_data[key1]["child_cluster_list"]:

                cluster_center_list_with_child.append([cluster_data[key1]["child_cluster_list"][key2]['center']['lat'], cluster_data[key1]["child_cluster_list"][key2]['center']['long']])
                color_list_with_child.append(blue)
                full_node_list.append(cluster_center_list_with_child[-1])
                # for key3 in 
    
    correlate_no_child = np.zeros((len(color_list_no_child), len(color_list_no_child)))
    correlate_with_child = np.zeros((len(color_list_with_child), len(color_list_with_child)))

    i = j = 0 #iter for loop
    for key1 in TSP_data:
        
        if len(cluster_data[key1]['child_cluster_list'])>1:
            for key2 in TSP_data[key1]["child_cluster_list"]:
                j +=1
                i+=1
                correlate_with_child[i-j][i] = 1
        i+=1
        j = 0


    graph_no_child = create_graph(convert_lat_long_to_descartes(cluster_center_list, 0+offset[0],SIZE[0]-offset[0], 0+offset[1], SIZE[1]-offset[1]), color_list_no_child, correlate_no_child)
    node_list_no_child = graph_no_child.nodes_list
    graph_with_child = create_graph(convert_lat_long_to_descartes(cluster_center_list_with_child, 0+offset[0],SIZE[0]-offset[0], 0+offset[1], SIZE[1]-offset[1]), color_list_with_child, correlate_with_child)
    node_list_with_child = graph_with_child.nodes_list
    # Putting the "pygame.quit" call in a try-finally clause
    # will guarrantee Pygame exits normally if later you
    # decide to use fullscreen graphics
    
    child_flag = 'with_child'
    if child_flag == 'with_child': 
        graph = graph_with_child
        node_list = node_list_with_child
    
    default_node_list = [] # Lưu trữ node list ban đầu, sử dụng khi ấn vào 'home'
    for node in node_list:
        default_node_list.append(node.pos)
    del node

    selected = None
    
    nodes_rect = []
    mapping_rect_to_node_id = {}
    for node in graph.nodes:
        nodes_rect.append(node.rect)
        # mapping_rect_to_node_id[nodes_rect[-1]] = node.id
    del node
    # Thiết lập các cờ
    home_flag = zoom_flag = drag_flag = cursor_to_node_flag = False
    
    # Lấy tọa độ của chuột khi drag
    mouse_down = np.zeros(2)
    mouse_up = np.zeros(2)
    try:
        init()
        
        
        while True:
            graph.update()
            pygame.event.pump()
            home_rect = pygame.Rect(10, 10, 80, 30)
            zoom_rect = pygame.Rect(110, 10, 80, 30)
            drag_rect = pygame.Rect(210, 10, 80, 30)
            home_btn = create_button(home_rect, 'Home')
            zoom_btn = create_button(zoom_rect, 'Zoom')
            drag_btn = create_button(drag_rect, 'Drag')
            tool_bar_rects = [home_rect, zoom_rect, drag_rect]
            
            # Đặt lại các cờ 
            cursor_to_node_flag = False
            
            # Exit the mainloop at any time the "ESC" key is pressed
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                break
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = event.pos
                    # round down x,y to multiples of NODESIZE
                    x = x_mouse % NODESIZE[0]
                    y = y_mouse % NODESIZE[1]
                    # pygame.draw.rect(SCREEN, (0,0,255), (x,y) + NODESIZE)
                    if (x,y) in graph.positions:
                        node = graph.positions[x,y]
                        if selected:
                            print(selected.id, node.id)
                            if selected is node:
                                selected = None
                                node.color = NODECOLOR
                            # elif selected not in node.neighbors:
                            #     selected.neighbors.add(node)
                            #     node.neighbors.add(selected)
                            # else:
                            #     selected.neighbors.remove(node)
                            #     node.neighbors.remove(selected)
                        else:
                            node.color = (0,0,0)
                            selected = node
                    
                    # Check click vào home btn
                    if tool_bar_rects[0].collidepoint(x_mouse, y_mouse):
                        home_flag = True
                        zoom_flag = drag_flag = 0
                        print('Home button clicked')
                    
                    # Check click vào zoom btn
                    if tool_bar_rects[1].collidepoint((x_mouse, y_mouse)):
                        zoom_flag = 1 - zoom_flag
                        home_flag = drag_flag = 0
                        print('Zoom button clicked')
                    
                    # Check click vào drag btn
                    if tool_bar_rects[2].collidepoint((x_mouse, y_mouse)):
                        drag_flag = 1 - drag_flag
                        zoom_flag = home_flag = 0
                        print('Drag button clicked')

                    if zoom_flag or drag_flag:
                        mouse_down[0] = x_mouse
                        mouse_down[1] = y_mouse
                    
                    # elif selected:
                    #     selected.setpos((x,y), graph)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    x_mouse, y_mouse = event.pos
                    mouse_up[0] = x_mouse
                    mouse_up[1] = y_mouse
                    
                    if zoom_flag: 
                        if mouse_up[0] - mouse_down[0] > 20 and mouse_up[1] - mouse_down[1] > 20:
                            # print('Mouse down = {}, mouse up = {}'.format(mouse_down, mouse_up))
                            x_trans, y_trans = - np.array(mouse_down)
                            x_scale, y_scale = (x_high - x_low)/(mouse_up[0] - mouse_down[0]), (y_high - y_low)/(mouse_up[1] - mouse_down[1])
                            # print('x_trans = {}, y_trans = {}\nx_scale = {}, y_scale = {}'.format(x_trans, y_trans, x_scale, y_scale))
                            for node in node_list:
                                x,y = node.pos
                                node.setpos(((x+x_trans)*x_scale + offset[0], (y+y_trans)*y_scale + offset[1]), graph)
                                print('Old pos = ({}, {}), New pos = ({}, {})'.format(x,y,(x+x_trans)*x_scale+ offset[0], (y+y_trans)*y_scale+ offset[1]))
                            del node_list
                            node_list = graph.nodes_list

                            nodes_rect = []
                            for node in graph.nodes:
                                nodes_rect.append(node.rect)
                    if home_flag:
                        
                        for i in range(len(default_node_list)):
                                x,y = default_node_list[i]
                                print('Old pos = {}, New pos = {}'.format(node_list[i].pos, (x,y)))
                                node_list[i].setpos((x,y), graph)

                        nodes_rect = []
                        for node in graph.nodes:
                            nodes_rect.append(node.rect)

                        home_flag = False

                    if drag_flag:
                        x_trans, y_trans = np.array(mouse_up) - np.array(mouse_down)
                        for node in node_list:
                            x,y = node.pos
                            node.setpos((x+x_trans, y+y_trans), graph)
                            print('Old pos = {}, New pos = {}'.format((x,y),(x+x_trans, y+y_trans)))
                        del node_list
                        node_list = graph.nodes_list

                        nodes_rect = []
                        for node in graph.nodes:
                            nodes_rect.append(node.rect)


                elif event.type == pygame.MOUSEMOTION:
                    # # x, y = event.pos
                    # # # round down x,y to multiples of NODESIZE
                    # # x -= x % NODESIZE[0]
                    # # y -= y % NODESIZE[1]
                    # # selected.setpos((x,y), graph)
                    # x, y = event.pos
                    # # round down x,y to multiples of NODESIZE
                    # x -= x % NODESIZE[0]
                    # y -= y % NODESIZE[1]
                    # # pygame.draw.rect(SCREEN, (0,0,255), (x,y) + NODESIZE)
                    x, y = event.pos
                    for rect in nodes_rect:
                        if rect.collidepoint((x,y)):
                            cursor_to_node_flag = True
                            break
                    for rect in tool_bar_rects:
                        if rect.collidepoint((x,y)):
                            cursor_to_node_flag = True
                    if cursor_to_node_flag:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
 
            pygame.display.flip()
            pygame.time.delay(FR)
    finally:
        quit()
 
# Pattern in Python to make the same module
# be reusable as  main program or importable module:
# if the builtin "__name__" variable is set to "__main__"
# this is the main module, and should perform some action
# (otherwise it is set to the module name)
if __name__ == "__main__":
    main()