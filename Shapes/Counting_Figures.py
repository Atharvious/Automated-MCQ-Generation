import math
import matplotlib.pyplot as plt
import random
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString,Point
import os
import pandas as pd
from itertools import combinations
from sys import argv, exit
op_folder = "output"
if os.path.exists(op_folder):
    pass
else:
    os.mkdir(op_folder)
def isBetween(c,line):
    ls = LineString(list(line))
    point = Point(c)
    return point.distance(ls) < 2e-14

def collinear(p0, p1, p2):
    poly = Polygon([p0,p1,p2])
    area = poly.area
    return area < 2e-14

def area(p1,p2,p3):
    poly = Polygon([p1,p2,p3])
    area = poly.area
    return area

def is_connected(p1,p2,lines):
    for line in lines:
        if isBetween(p1,line) and isBetween(p2,line):
            return True
    return False



def num_triangles(points,lines):
    tri_triplets = []
    areas = []
    num_triangles = 0
    point_triplets = [x for x in combinations(points, 3)]
    for index,triplet in enumerate(point_triplets):
        p1 = triplet[0]
        p2 = triplet[1]
        p3 = triplet[2]
        if is_connected(p1,p2,lines) and is_connected(p2,p3,lines) and is_connected(p3,p1,lines):
            if not collinear(p1,p2,p3):
                num_triangles += 1
                tri_triplets.append(triplet)
                area_p = area(p1,p2,p3)
                areas.append(area_p)
    return num_triangles, tri_triplets,areas

def add_lines(points, lines = None):
    if lines is None:
        lines = []
    points_copy = points[:]
    points_copy.append(points_copy[0])
    for index,point in enumerate(points):
        line = (point, points_copy[index + 1])
        if line not in lines:
            lines.append(line)
    return lines

def add_points(points, point_container = None):
    if point_container is None:
        point_container = []
    for point in points:
        if point not in point_container:
            point_container.append(point)
    return point_container

class Poly:
    def __init__(self, vertices):
        self.vertices = vertices[:]
        self.path = vertices[:]
        self.path.append(self.path[0])
        self.edges = self.store_edges()
        self.mids = []


    def find_midpoints(self):
        for index,point in enumerate(self.vertices):
            midx = (get_x(point)+get_x(self.path[index+1]))/2
            midy = (get_y(point)+get_y(self.path[index+1]))/2
            self.mids.append((midx,midy))
        return self.mids

    def store_edges(self):
        edges = []
        for index,point in enumerate(self.vertices):
            edge= (point, self.path[index+1])
            edges.append(edge)
        return edges

def get_x(vertex):
    return vertex[0]

def get_y(vertex):
    return vertex[1]

def find_mid(line):
    p1 = line[0]
    p2 = line[1]
    return ((get_x(p1)+get_x(p2))/2,(get_y(p1)+get_y(p2))/2)


def deg_to_rad(deg_angle):
    return deg_angle*(math.pi/180)


def find_point(origin, d,angle):
    angle = math.pi/2 - math.radians(angle)
    (ox, oy) = origin
    return(ox + math.cos(angle) * d,oy + math.sin(angle) * d)

def generate_random_points(num_of_points = 1):
    points = []
    while len(points) < num_of_points:
        random.seed()
        point_x = random.randint(1,50)
        random.seed()
        point_y = random.randint(1,50)
        point = (point_x,point_y)
        if point not in points:
            points.append(point)
    return points

def man_triangle():
    i = 0
    while i == 0:
        points = generate_random_points(3)
        polygon = Polygon(points)
        if polygon.area > 20:
            i = 1
            x,y = polygon.exterior.xy
            pt = []
            for index in range(len(x)-1):
                pt.append((x[index],y[index]))
    return pt


def prop_tri():
    random.seed()
    cx = random.random()
    random.seed()
    cy = random.random()
    random.seed()
    a = random.randint(5,9)
    random.seed()
    com_angle = random.randint(80,85)
    random.seed()
    #iso_eq_flag = random.randint(0,1)
    random.seed()
    rot = random.randint(15,20)
    #if iso_eq_flag == 1:
     #   com_angle = 60
    com_angle += rot
    points = [(cx,cy)]
    p1 = find_point((cx,cy),a,com_angle)
    points.append(p1)
    com_angle += 180 - 2*com_angle
    p2 = find_point(p1,a,com_angle)
    points.append(p2)
    return points

def man_rect():
    random.seed()
    cx = random.random()
    random.seed()
    cy = random.random()
    random.seed()
    l = random.randint(5,9)
    random.seed()
    b = random.randint(4,8)
    random.seed()
    a = random.randint(0,90)
    random.seed()
    rec_sq_flag = random.randint(0,1)
    if rec_sq_flag == 1:
        b = l
        a = 0
    random.seed()
    angle_flag = random.randint(0,5)
    if angle_flag >3:
        a = 0
    points = [(cx,cy)]
    p1 = find_point((cx,cy),l,a)
    points.append(p1)
    a += 90
    p2 = find_point(p1,b,a)
    points.append(p2)
    a += 90
    p3 = find_point(p2,l,a)
    points.append(p3)
    return points

def plot_points(points):
    path = points[:]
    path.append(path[0])
    x,y = zip(*path)
    plt.plot(x,y,'r')

def combine_shapes(points_list,all_points,iteration):

    alphabets = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
    annotations = alphabets[:len(all_points)]
    sol_dict = dict(zip(annotations,all_points))
    plt.figure()
    plt.axis("off")
    for points in points_list:
        plot_points(points)
    #plot_just_points(points_list)
    save_dir = "output\\{}".format(iteration+1)
    if os.path.exists(save_dir):
        pass
    else:
        os.mkdir(save_dir)
    plt.savefig("output\\{}\\Question.png".format(iteration + 1))
    for label,point in sol_dict.items():
        plt.annotate(label,point,(point[0],point[1]*1.04),c = "#000000",size = 20)
    plt.savefig("output\\{}\\Solution.png".format(iteration + 1))
    #img = cv2.imread("output\\{}\\Solution.png".format(iteration + 1),0)
    #img = standardize_image(img)
    #cv2.imwrite("output\\{}\\Solution.png".format(iteration + 1),img)
    return sol_dict



def intricacies(poly_object):
    vertices = poly_object.vertices
    mids = poly_object.find_midpoints()
    random.seed()
    v_index = random.randint(0,len(vertices)-1)
    alt_vindex = v_index + 2
    if alt_vindex >= len(vertices):
        alt_vindex -= len(vertices)
    alt_verts = [vertices[v_index], vertices[alt_vindex]]
    random.seed()
    index = random.randint(0,len(mids)-1)
    alt_index = index + 2
    if alt_index >= len(mids):
        alt_index -= len(mids)
    alt_mids = [mids[index],mids[alt_index]]
    return alt_verts, alt_mids


def make_mids(poly_object,tri_rec_f= 0, override = 0):
    mids = poly_object.find_midpoints()
    if override == 0:
        if tri_rec_f == 0:
            random.seed()
            rand_no = random.randint(3,len(mids))
        else:
            random.seed()
            rand_no = random.randint(2,len(mids))
    else:
        rand_no = len(mids)
    random.seed()
    selected_points = random.sample(mids,rand_no)
    return selected_points

def line_intersection(line1, line2):
    ls1 = LineString(list(line1))
    ls2 = LineString(list(line2))
    int_point = ls1.intersection(ls2)
    if int_point.geom_type == "Point":
        return (int_point.x,int_point.y)
    else:
        return None

def get_all_intersects(tot_lines,tot_points):
    new_points = tot_points[:]
    line_pairs = combinations(tot_lines,2)
    for line_pair in line_pairs:
        interpoint = line_intersection(line_pair[0],line_pair[1])
        if interpoint is not None and interpoint not in new_points:
            new_points.append(interpoint)
    return new_points

def round_points(points):
    rounded_points = []
    points_copy = []
    for index,point in enumerate(points):
        x = round(point[0],2)
        y = round(point[1],2)
        new_point = (x,y)
        if new_point not in rounded_points:
            rounded_points.append((x,y))
            points_copy.append((point[0],point[1]))
    return points_copy

def is_part(line1,line2):
    ls1 = LineString(list(line1))
    ls2 = LineString(list(line2))
    int_point = ls1.intersection(ls2)
    if int_point.geom_type != "Point":
        if int_point.length > 2e-14:
            return True
    else:
        return False

def length(line):
    ls = LineString(list(line))
    return ls.length

def reduce_lines(all_lines):
    reduced_lines = all_lines[:]
    line_pairs = combinations(reduced_lines,2)
    for line1,line2 in line_pairs:
        if is_part(line1,line2):
            d1 = length(line1)
            d2 = length(line2)
            if d1>d2:
                if line2 in reduced_lines:
                    reduced_lines.remove(line2)
            else:
                if line1 in reduced_lines:
                    reduced_lines.remove(line1)
    return reduced_lines


def get_label(point, solution_dictionary):
    for label,points in solution_dictionary.items():
        if points == point:
            if label is not None:
                return label
    return "-"
"""!!------------------Algorithm---------------------------!!
1 - make outer shape
2 - add the lines to lines container
3 - add the points to point container
4 - make the mids
5 - add the mid lines
6 - add the mid points
7 - make mids of mids
8 - add lines
9 - add points
10- add vetex-mid lines
11 - check if the vm lines interset with any of the present lines.
                if yes, add intersect point to the point container
12 - for all triplets in points, see if they are all connected.
            if they are, then they form a triangle."""





def save_figs(iterations):
    quest_dict = {
            "Question": [],
            "Option1" : [],
            "Option2" : [],
            "Option3" : [],
            "Option4" : [],
            "Answer"  : [],
            "Solution" : [],
            }

    for number in range(iterations):
        random.seed()
        line_tri = random.randint(0,2)
        made_shapes = []
        all_lines = []
        all_points = []
        random.seed()
        shape_flag = random.randint(0,1)
        if shape_flag == 0:
            edge_points = man_rect()
        elif shape_flag == 1:
            edge_points = prop_tri()
        all_lines = add_lines(edge_points)
        all_points = add_points(edge_points)
        made_shapes.append(edge_points)

        mid_points = make_mids(Poly(edge_points),shape_flag)
        all_lines = add_lines(mid_points,all_lines)
        all_points= add_points(mid_points,all_points)
        made_shapes.append(mid_points)

        op_verts,op_mids = intricacies(Poly(edge_points))
        all_lines = add_lines(op_verts,all_lines)
        all_lines = add_lines(op_mids, all_lines)
        made_shapes.append(op_verts)
        made_shapes.append(op_mids)

        tot_mids = Poly(edge_points).find_midpoints()
        mid_of_mids = make_mids(Poly(tot_mids),shape_flag)
        all_lines = add_lines(mid_of_mids,all_lines)
        all_points= add_points(mid_of_mids,all_points)
        made_shapes.append(mid_of_mids)


        all_points = get_all_intersects(all_lines,all_points)
        c_points = round_points(all_points)
        solution_dictionary = combine_shapes(made_shapes, c_points,number)
        if line_tri == 0:
            quest_dict["Question"].append("Find the number of triangles in the given figure:")
            n_t, triangle_pts,areas = num_triangles(c_points, all_lines)
            answer = n_t
            triangle_labels = []
            for triplet in triangle_pts:
                p1 = triplet[0]
                label1 = get_label(p1,solution_dictionary)
                p2 = triplet[1]
                label2 = get_label(p2,solution_dictionary)
                p3 = triplet[2]
                label3 = get_label(p3,solution_dictionary)
                triangle_string = "{}{}{}".format(label1,label2,label3)
                triangle_labels.append(triangle_string)
            sol_string = "The triangles in the given figure are : {}".format(",".join(triangle_labels))


        elif line_tri == 1:
            quest_dict["Question"].append("Find the number of straight lines in the given figure:")
            reduced_lines = reduce_lines(all_lines)
            no_lines = len(reduced_lines)
            answer = no_lines
            line_labels = []
            for line in reduced_lines:
                p1 = line[0]
                label1 = get_label(p1,solution_dictionary)
                p2 = line[1]
                label2 = get_label(p2,solution_dictionary)
                line_string = "{}{}".format(label1,label2)
                line_labels.append(line_string)
            sol_string = "The lines in the given figure are: {}".format(",".join(line_labels))
        
        elif line_tri == 2:
            quest_dict["Question"].append("Find the number of straight lines and triangles in the given figure:")
            reduced_lines = reduce_lines(all_lines)
            no_lines = len(reduced_lines)
            no_tri,triangle_pts,areas = num_triangles(c_points,all_lines)
            answer = "{} Triangles, {} Lines".format(no_tri,no_lines)
            line_labels = []
            for line in reduced_lines:
                p1 = line[0]
                label1 = get_label(p1,solution_dictionary)
                p2 = line[1]
                label2 = get_label(p2,solution_dictionary)
                line_string = "{}{}".format(label1,label2)
                line_labels.append(line_string)
            triangle_labels = []
            for triplet in triangle_pts:
                p1 = triplet[0]
                label1 = get_label(p1,solution_dictionary)
                p2 = triplet[1]
                label2 = get_label(p2,solution_dictionary)
                p3 = triplet[2]
                label3 = get_label(p3,solution_dictionary)
                triangle_string = "{}{}{}".format(label1,label2,label3)
                triangle_labels.append(triangle_string)
            sol_string = "The triangles are {}. The stright lines are {}".format(",".join(triangle_labels),",".join(line_labels))
            opt_list = ["Option1","Option2","Option3","Option4"]
            random.seed()
            right_op = random.choice(opt_list)
            quest_dict[right_op].append(answer)
            quest_dict["Answer"].append(right_op)
            rem_list = opt_list[:]
            rem_list.remove(right_op)
            wrong_answers = []
            for rem_op in rem_list:
                i = 0
                while i == 0:
                    random.seed()
                    offset = random.randint(2,6)
                    wr_lines = random.randint(no_lines - offset, no_lines + offset)
                    random.seed()
                    offset = random.randint(2,6)
                    wr_triangles = random.randint(no_tri - offset, no_tri + offset)
                    wr_ans = "{} Triangles, {} Lines".format(wr_triangles, wr_lines)
                    if wr_lines != no_lines or wr_triangles != no_tri:
                        if wr_ans not in wrong_answers:
                            quest_dict[rem_op].append(wr_ans)
                            wrong_answers.append(wr_ans)
                            i = 1


        quest_dict["Solution"].append(sol_string)

        print("Run - {} \t Answer - {}".format(number + 1, answer))

        if line_tri <2:
            opt_list = ["Option1","Option2","Option3","Option4"]
            random.seed()
            right_op = random.choice(opt_list)
            quest_dict[right_op].append(answer)
            quest_dict["Answer"].append(right_op)
            rem_list = opt_list[:]
            rem_list.remove(right_op)
            wrong_answers = []
            for rem_op in rem_list:
                i = 0
                while i == 0:
                    random.seed()
                    op_set = random.randint(0,1)
                    random.seed()
                    offset = random.randint(2,5)
                    if op_set == 0:
                        wrong_ans = answer - offset
                    else:
                        wrong_ans = answer + offset
                    if wrong_ans > 0 and wrong_ans not in wrong_answers:
                        quest_dict[rem_op].append(wrong_ans)
                        wrong_answers.append(wrong_ans)
                        i = 1
    df = pd.DataFrame(quest_dict)
    df.to_csv("Questions.csv")




def main():
    if len(argv) < 2:
        print("Please enter number of questions for file %s" % argv[0])
        exit(1)
    num_questions = argv[1]
    save_figs(int(num_questions))
    
    
if __name__ == "__main__":
    main()


     
