# coding: utf-8
# by Joao Bueno
import codecs
from random import randrange, choice
from re import L, M
from turtle import home
from venv import create
from matplotlib.pyplot import sca, yscale
import pygame
import json
import numpy as np
import pyautogui

FR = 30
# SIZE = 1000, 720
BGCOLOR = (255,255,255)
NODECOLOR = (255,0,0)
NODESIZE = 4,4
GRIDSPACING = 50
MAXTRIES = 1000
STARTINGNODES = 8
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
grey = (100,100,100)
white = (255,255,255)
orange = (255, 88, 0)
yellow = (255,255,0)

width, height = pyautogui.size()
if int((height-100)/3) * 4 <width - 150:
    height = height-100
    width = int(height/3) * 4
SIZE = width, height

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
    
    def change_color_by_type(self, type, color):
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i].type == type:
                self.nodes_list[i].color = color

    def update(self):
        SCREEN.fill(BGCOLOR)
        # seperate into many layer filter by node type

        for i in range(len(self.nodes_list)):
            if self.nodes_list[i].type == 'Customer':
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)
                for neighbor in self.nodes_list[i].neighbors:
                    if self.nodes_list[i].color == white or neighbor.color == white: c = white
                    else: c = self.nodes_list[i].color
                    pygame.draw.line(SCREEN, c,
                        self.nodes_list[i].rect.center, neighbor.rect.center)
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)
        
        for i in range(len(self.nodes_list)):
            if (self.nodes_list)[i].type == 'Depot':
                for neighbor in self.nodes_list[i].neighbors:
                    if self.nodes_list[i].color == white or neighbor.color == white: c = white
                    else: c = self.nodes_list[i].color
                    pygame.draw.line(SCREEN, c,
                        self.nodes_list[i].rect.center, neighbor.rect.center)
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)
        
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i].type == 'Cluster child':
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)
                for neighbor in self.nodes_list[i].neighbors:
                    if self.nodes_list[i].color == white or neighbor.color == white: c = white
                    else: c = self.nodes_list[i].color
                    pygame.draw.line(SCREEN, c,
                        self.nodes_list[i].rect.center, neighbor.rect.center)
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)

        for i in range(len(self.nodes_list)):
            if self.nodes_list[i].type == 'Cluster parent':
                for neighbor in self.nodes_list[i].neighbors:
                    if self.nodes_list[i].color == white or neighbor.color == white: c = white
                    else: c = self.nodes_list[i].color
                    pygame.draw.line(SCREEN, c,
                        self.nodes_list[i].rect.center, neighbor.rect.center)
                pygame.draw.rect(SCREEN, self.nodes_list[i].color, self.nodes_list[i].rect)

 
class Node(object):
    # Class variable, incremented with each
    # instance so that each node has a unique ID that
    # can be used as its hash:
    creation_counter = 0
    def __init__(self, color, default_pos, node_id, type, parent_id, n_child, size_rect = NODESIZE):
        self.id = self.__class__.creation_counter
        self.__class__.creation_counter += 1
        # We don't  set this attribute here, but by adding then here,
        # we indicate that it "exists" for readers of the code:
        self.rect = None
        self.color = color
        self.neighbors = set()
        self.size_rect = size_rect
        self.default_pos = [default_pos[0], default_pos[1]]
        self.node_id = node_id
        self.type = type
        self.parent_id = parent_id
        self.n_child = n_child

    def setpos(self, pos, graph = None):
        if self.rect and graph:
            # remove self from previous position in the graph:
            graph.positions.pop(self.rect.topleft, None)
        # self.rect = pygame.Rect(pos[0], pos[1],NODESIZE[0], NODESIZE[1])
        self.rect = pygame.Rect(pos[0], pos[1], self.size_rect[0], self.size_rect[1])
        self.pos = pos
        if graph:
            graph.positions[pos] = self
        # print('Set pos done')
    def  __hash__(self):
        return self.id

    def get_info(self):
        a = []
        a.append('Id: {}'.format(self.node_id))
        a.append('Type: {}'.format(self.type))
        a.append('Parent id: {}'.format(self.parent_id))
        a.append('No. child: {}'.format(self.n_child))
        return str('\n'.join(a))


def get_cluster_data(fname= 'output/TSP_phase_with_Kmeans.json'):
    cluster_data = json.load(open(fname, 'r'))
    return cluster_data

def create_graph(location_list, color_list, correlate_list, id_list, type_list, parent_id_list, n_child_list):
    # create new graph and populate nodes:
    graph = Graph()
    # locallist for adding neighbors:
    nodes = []
    for i in range(len(location_list)):
        node = Node(color_list[i], location_list[i], id_list[i], type_list[i], parent_id_list[i], n_child_list[i])
        graph.add(node, location_list[i])

    nodes = graph.nodes_list
    n_nodes = len(location_list)
    for i in range(n_nodes):
        for j in range(n_nodes):
            if correlate_list[i][j] !=0:
                nodes[i].neighbors.add(nodes[j])
                # nodes[j].neighbors.add(nodes[i])

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
        # print('Cluster center: {}'.format(point))
        if point[0] < w_pole[0]: w_pole = point #update west pole
        if point[0] > e_pole[0]: e_pole = point #update east pole
        if point[1] < n_pole[1]: n_pole = point #update north pole
        if point[1] > s_pole[1]: s_pole = point #update south pole

    # print('N_pole = {}\nS_pole = {}\nE_pole = {}\nW_pole = {}'.format(n_pole, s_pole, e_pole, w_pole))
    # print('X trans = {}, y_trans = {}'.format(x_low - w_pole[0], y_low - n_pole[1]))
    # print('X scale = {}, y scale = {}'.format((x_high-x_low)/(e_pole[0]-x_low), (y_high-y_low)/(n_pole[1]-y_low)))
    x_trans, y_trans = x_low - w_pole[0], y_low - n_pole[1]
    new_point_list = scale([x_low, y_low], (x_high-x_low)/(e_pole[0]-w_pole[0]), (y_high-y_low)/(s_pole[1]-n_pole[1]), transition(x_low - w_pole[0], y_low - n_pole[1], location_list))
    return new_point_list

def round(point_list):
    return np.round(point_list)

def create_button(rect, text, font_color = (0,0,0), text_color = (255,255,255), size = 50):
    global SCREEN
    color_dark = (100,100,100)
    pygame.draw.rect(SCREEN, font_color, rect)
    smallfont = pygame.font.SysFont('Corbel',size) 

    y = 0
    text = text.split('\n')
    for line in text:

        t = smallfont.render(line , True , text_color)
        word_width, word_height = t.get_size()
        SCREEN.blit(t , (rect[0]+10, rect[1]+5+y))
        y += word_height  # Start on new row.
 


def main():

    offset = [90, 90]
    x_low, y_low = offset
    x_high, y_high = np.array(SIZE) - np.array(offset)
    TSP_data = get_cluster_data()
    cluster_data = get_cluster_data('output/pre_TSP_phase.json')
    market_data = json.load(codecs.open('input/market.json', 'r', 'utf-8-sig'))['market']
    depot_data = json.load(codecs.open('input/depot.json', 'r', 'utf-8-sig'))['depot']

    mapping_code_to_index = {}
    # Lấy ra các tâm cụm lưu vào mảng
    cluster_center_list = []
    color_list_no_child = []

    cluster_center_list_with_child = []
    color_list_with_child = []

    full_node_list = []
    color_list_full_node = []

    id_with_child = []
    type_with_child = []
    parent_id_with_child = []
    n_child_with_child = []

    id_all_node = []
    type_all_node = []
    parent_id_all_node = []
    n_child_all_node = []

    # Danh sách các màu
    

    for key1 in TSP_data:

        cluster_center_list.append([float(TSP_data[key1]['center']['lat']), float(TSP_data[key1]['center']['long'])])
        color_list_no_child.append(red)
        cluster_center_list_with_child.append(cluster_center_list[-1])
        color_list_with_child.append(red)
        id_with_child.append(key1)
        type_with_child.append('Cluster parent')
        parent_id_with_child.append(None)
        n_child_with_child.append(len(TSP_data[key1]["child_cluster_list"]))

        full_node_list.append(cluster_center_list[-1])
        color_list_full_node.append(red)
        id_all_node.append(key1)
        type_all_node.append('Cluster parent')
        parent_id_all_node.append(None)
        n_child_all_node.append(len(TSP_data[key1]["child_cluster_list"]))

        
        for key2 in TSP_data[key1]["child_cluster_list"]:
            if len(cluster_data[key1]['child_cluster_list'])>1:
                # print('key1 = {}, key2 = {}'.format(key1, key2))
                cluster_center_list_with_child.append([cluster_data[key1]["child_cluster_list"][key2]['center']['lat'], cluster_data[key1]["child_cluster_list"][key2]['center']['long']])
                color_list_with_child.append(blue)
                id_with_child.append(key2)
                type_with_child.append('Cluster child')
                parent_id_with_child.append(key1)
                n_child_with_child.append(len(cluster_data[key1]["child_cluster_list"][key2]["node_list"]))

                full_node_list.append(cluster_center_list_with_child[-1])
                color_list_full_node.append(blue)
                id_all_node.append(key2)
                type_all_node.append('Cluster child')
                parent_id_all_node.append(key1)
                n_child_all_node.append(len(cluster_data[key1]["child_cluster_list"][key2]["node_list"]))

            route = TSP_data[key1]["child_cluster_list"][key2]['route'].split(' -> ')[:-1]
            # print(route)
            full_node_list.append([depot_data[route[0][1:]]['location']['lat'], depot_data[route[0][1:]]['location']['long']])
            color_list_full_node.append(orange)
            id_all_node.append(route[0][1:])
            type_all_node.append('Depot')
            parent_id_all_node.append(key2)
            n_child_all_node.append(0)

            for i in range(1, len(route)):
                full_node_list.append([market_data[route[i][1:]]['location']['lat'], market_data[route[i][1:]]['location']['long']])
                color_list_full_node.append(green)
                id_all_node.append(route[i][1:])
                type_all_node.append('Customer')
                parent_id_all_node.append(key1)
                n_child_all_node.append(0)
    
    correlate_no_child = np.zeros((len(color_list_no_child), len(color_list_no_child)))
    correlate_with_child = np.zeros((len(color_list_with_child), len(color_list_with_child)))
    correlate_all_node = np.zeros((len(color_list_full_node), len(color_list_full_node)))

    i = j = 0 #iter for loop

    for key1 in TSP_data:

        if len(cluster_data[key1]['child_cluster_list'])>1:
            for key2 in TSP_data[key1]["child_cluster_list"]:
                j +=1
                i+=1
                correlate_with_child[i-j][i] = 1
        i+=1
        j = 0

    start_parent, start_child, start_depot = 0, 0, 0
    for i in range(len(color_list_full_node)):
        if color_list_full_node[i] == red:
            start_parent = i
            start_child = i
        if color_list_full_node[i] == blue:
            start_child = i
            correlate_all_node[start_parent][start_child] = 1
        if color_list_full_node[i] == orange:
            start_depot = i
            correlate_all_node[start_child][start_depot] = 1

        if color_list_full_node[i] == green: 
            correlate_all_node[i][i-1] = 1

    graph_with_child = create_graph(convert_lat_long_to_descartes(cluster_center_list_with_child, 0+offset[0],SIZE[0]-offset[0], 0+offset[1], SIZE[1]-offset[1]), color_list_with_child, correlate_with_child, id_with_child, type_with_child, parent_id_with_child, n_child_with_child)
    node_list_with_child = graph_with_child.nodes_list

    graph_all_node = create_graph(convert_lat_long_to_descartes(full_node_list, 0+offset[0],SIZE[0]-offset[0], 0+offset[1], SIZE[1]-offset[1]), color_list_full_node, correlate_all_node, id_all_node, type_all_node, parent_id_all_node, n_child_all_node)
    node_list_all = graph_all_node.nodes_list
    # Putting the "pygame.quit" call in a try-finally clause
    # will guarrantee Pygame exits normally if later you
    # decide to use fullscreen graphics
    nodes_rect_with_child = []
    for node in graph_with_child.nodes:
        nodes_rect_with_child.append(node.rect)
    
    nodes_rect_all = []
    for node in graph_all_node.nodes:
        nodes_rect_all.append(node.rect)

    # Lưu lại các default 
    default_node_list_with_child = []
    for node in node_list_with_child:
        default_node_list_with_child.append(node.pos)
    del node

    default_node_list_all = []
    for node in node_list_all:
        default_node_list_all.append(node.pos)
    del node

    # mapping các node tâm cụm cha và con ở cây đầy đủ với các node cha và con ở cây giản lược
    mapping = {}
    cnt = 0
    for i in range(len(color_list_full_node)):
        if color_list_full_node[i] in [red, blue]:
            mapping[i] = cnt
            cnt+=1

    graph = graph_all_node
    node_list = node_list_all
    nodes_rect = nodes_rect_all
    
    default_node_list = default_node_list_all # Lưu trữ node list ban đầu, sử dụng khi ấn vào 'home'


    # Thiết lập các cờ
    home_flag = zoom_flag = drag_flag = cursor_to_node_flag = update_scaler_flag = full_graph_flag = click_to_center_flag = show_text_flag = False
    
    # Lấy tọa độ của chuột khi drag
    mouse_down = np.zeros(2)
    mouse_up = np.zeros(2)
    w_btn, h_btn = 160, 60
    x_zoom_scaler, y_zoom_scaler = 1, 1
    try:
        init()


        while True:
            graph.update()
            pygame.event.pump()
            home_rect = pygame.Rect(10, 10, w_btn, h_btn)
            zoom_rect = pygame.Rect(10+w_btn+20, 10, w_btn, h_btn)
            drag_rect = pygame.Rect(10+2*w_btn+40, 10, w_btn, h_btn)
            tool_bar_rects = [home_rect, zoom_rect, drag_rect]
            
            # Vẽ khung của map để dễ nhìn
            create_button(pygame.Rect(offset[0]-5, offset[1]-5, SIZE[0] - 2 * (offset[0] - 5), 5), '', grey, size=35) # Top
            create_button(pygame.Rect(offset[0]-5, offset[1]-5, 5, SIZE[1] - 2 * (offset[1] - 5)), '', grey, size=35) # Left
            create_button(pygame.Rect(offset[0]-5, SIZE[1]-offset[1], SIZE[0] - 2 * (offset[0] - 5), 5), '', grey, size=35) # Down
            create_button(pygame.Rect(SIZE[0]-offset[0], offset[1]-5, 5, SIZE[1] - 2 * (offset[1] - 5)), '', grey, size=35) # Right

            create_button(pygame.Rect(0, 0, SIZE[0], offset[1]-5), '', BGCOLOR) # BG top
            create_button(pygame.Rect(0, 0, offset[0]-5, SIZE[1]), '', BGCOLOR) # BG left
            create_button(pygame.Rect(0, SIZE[1]-offset[1] + 5, SIZE[0], offset[1] - 5), '', BGCOLOR) # BG down
            create_button(pygame.Rect(SIZE[0] - offset[0] +5, 0, offset[0] - 5, SIZE[1]), '', BGCOLOR) # BG right

            home_btn = create_button(home_rect, 'Home', black, white)
            zoom_btn = create_button(zoom_rect, 'Zoom', black, white)
            drag_btn = create_button(drag_rect, 'Drag', black, white)

            
            # Đặt lại các cờ 
            cursor_to_node_flag = False
            click_to_center_flag = False

            # Exit the mainloop at any time the "ESC" key is pressed
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = event.pos                    
                    for i in range(len(nodes_rect)):
                        if nodes_rect[i].collidepoint((x_mouse, y_mouse)) and (node_list[i].color == red or node_list[i].color == blue):
                            location_focus = node_list[i].pos
                            print('Clicked rect: {}'.format(nodes_rect[i]))
                            print('Clicked point: {}'.format(location_focus))
                            click_to_center_flag = True
                            break
                    
                    if click_to_center_flag:
                        # Nếu click vào tâm cụm thì ta sẽ zoom map to ra và tâm cụm nằm giữa console
                        center_console = [SIZE[0]/2, SIZE[1]/2]
                        x_trans, y_trans = - np.array(location_focus)
                        x_scale, y_scale = 3/x_zoom_scaler, 4/y_zoom_scaler
                        cnt = 0
                        for node in graph.nodes_list:
                            x,y = node.pos
                            node.setpos(((x+x_trans)*x_scale + center_console[0], (y+y_trans)*y_scale + center_console[1]), graph)
                            if x==location_focus[0] and y == location_focus[1]: 
                                print('Check old pos: {}, new pos: {}'.format((x,y), node.pos))
                            cnt+=1
                        
                        x_zoom_scaler*=x_scale
                        y_zoom_scaler*=y_scale
                        update_scaler_flag = True

                        nodes_rect = []
                        for node in graph.nodes_list:
                            nodes_rect.append(node.rect)

                    # Check click vào home btn
                    if tool_bar_rects[0].collidepoint(x_mouse, y_mouse):
                        home_flag = True
                        zoom_flag = drag_flag = 0
                        # print('Home button clicked')

                    # Check click vào zoom btn
                    if tool_bar_rects[1].collidepoint((x_mouse, y_mouse)):
                        zoom_flag = 1 - zoom_flag
                        home_flag = drag_flag = 0
                        # print('Zoom button clicked')

                    # Check click vào drag btn
                    if tool_bar_rects[2].collidepoint((x_mouse, y_mouse)):
                        drag_flag = 1 - drag_flag
                        zoom_flag = home_flag = 0
                        # print('Drag button clicked')

                    if zoom_flag:
                        mouse_down[0] = x_mouse
                        mouse_down[1] = y_mouse
                        create_button(zoom_rect, 'Zoom', blue, white)
                    else: create_button(zoom_rect, 'Zoom', black, white)

                    if drag_flag:
                        mouse_down[0] = x_mouse
                        mouse_down[1] = y_mouse
                        create_button(drag_rect, 'Drag', blue, white)
                    else: create_button(drag_rect, 'Drag', black, white)

                    if home_flag: create_button(home_rect, 'Home', blue, white)
                    else: create_button(home_rect, 'Home', black, white)
                    

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
                            x_zoom_scaler*=x_scale
                            y_zoom_scaler*=y_scale
                            update_scaler_flag = True
                            # print('x_trans = {}, y_trans = {}\nx_scale = {}, y_scale = {}'.format(x_trans, y_trans, x_scale, y_scale))
                            
                            for node in node_list:
                                x,y = node.pos
                                node.setpos(((x+x_trans)*x_scale + offset[0], (y+y_trans)*y_scale + offset[1]), graph)
                                # print('Old pos = ({}, {}), New pos = ({}, {})'.format(x,y,(x+x_trans)*x_scale+ offset[0], (y+y_trans)*y_scale+ offset[1]))
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

                        x_zoom_scaler = y_zoom_scaler = 1
                        update_scaler_flag = True

                    if drag_flag:
                        x_trans, y_trans = np.array(mouse_up) - np.array(mouse_down)
                        for node in node_list:
                            x,y = node.pos
                            node.setpos((x+x_trans, y+y_trans), graph)
                            # print('Old pos = {}, New pos = {}'.format((x,y),(x+x_trans, y+y_trans)))
                        del node_list
                        node_list = graph.nodes_list

                        nodes_rect = []
                        for node in graph.nodes:
                            nodes_rect.append(node.rect)


                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos

                    for i in range(len(nodes_rect)):
                        if nodes_rect[i].collidepoint((x,y)) and (node_list[i].color == red or node_list[i].color == blue):
                            # check_out_flag = True
                            cursor_to_node_flag = True
                            show_text_flag = True
                            index = i
                            break
                    for rect in tool_bar_rects:
                        if rect.collidepoint((x,y)):
                            cursor_to_node_flag = True
                            show_text_flag = False

                    if cursor_to_node_flag:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else: 
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        show_text_flag = False
            if show_text_flag: 
                create_button(pygame.Rect(x-10, y+25, 150, 80), node_list[index].get_info(), yellow, black, size=16)
            
            if update_scaler_flag:
                # print('x_zoom_scaler = {}, y_zoom_scaler = {}'.format(x_zoom_scaler, y_zoom_scaler))
                update_scaler_flag = False
            
            # Cập nhật lại kích thước điểm 
            size_rect = (x_zoom_scaler - 15)/6
            for node in node_list:
                if node.type == 'Cluster parent': adding = 1
                if node.type == 'Cluster child' or node.type == 'Depot': adding = 0.8
                if node.type == 'Customer': adding = 0.6
                node.rect = pygame.Rect(node.pos[0], node.pos[1], np.max(np.array([4, int(size_rect*adding)])), np.max(np.array([4, int(size_rect*adding)])))

            nodes_rect = []
            for node in graph.nodes:
                nodes_rect.append(node.rect)
            
            if x_zoom_scaler>2 and y_zoom_scaler>2:
                graph.change_color_by_type('Customer', green)
                graph.change_color_by_type('Depot', orange)
            
            else: 
                graph.change_color_by_type('Customer', BGCOLOR)
                graph.change_color_by_type('Depot', BGCOLOR)
            
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