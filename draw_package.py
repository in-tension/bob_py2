#!/usr/bin/env python
# coding: utf-8

import brutils as br

import drawSvg as draw
import os



red = '#bc4b51'
dred = '#89373B'
ddred = '#67292D'
orange = '#F4A259'
dorange = '#C88549'
ddorange = '#865931'
yellow = '#f4e285'
dyellow = '#C8B96D'
ddyellow = '#867C49'
green = '#739356'
dgreen = '#5A7243'
ddgreen = '#3F512F'
aqua = '#5b8e7d'
daqua = '#4B7567'
ddaqua = '#324E45'




reds = [red, dred, ddred]
oranges = [orange, dorange, ddorange]
yellows = [yellow, dyellow, ddyellow]
greens = [green, dgreen, ddgreen]
aquas = [aqua, daqua, ddaqua]




def add_rounded_rect(d_obj,bx,by,w,h, **kwargs) :
    rad=20

    draw_horiz = w - 2*rad
    draw_vert = h - 2*rad

    rr = draw.Path(**kwargs)

    rr.M(bx,by-rad)
    rr.v(-draw_vert)
    rr.a(rad,rad,0,0,0,rad,-rad)
    rr.h(draw_horiz)
    rr.a(rad,rad,0,0,0,rad,rad)
    rr.v(draw_vert)
    rr.a(rad,rad,0,0,0,-rad,rad)
    rr.h(-draw_horiz)
    rr.a(rad,rad,0,0,0,-rad,-rad)

    d_obj.append(rr)





def add_rounded_rect2(d_obj,cx,cy,w,h, **kwargs) :
    rad=20

    bx = cx - w/2
    by = cy - h/2

    draw_horiz = w - 2*rad
    draw_vert = h - 2*rad

    rr = draw.Path(**kwargs)

    rr.M(bx,by-rad)
    rr.v(-draw_vert)
    rr.a(rad,rad,0,0,0,rad,-rad)
    rr.h(draw_horiz)
    rr.a(rad,rad,0,0,0,rad,rad)
    rr.v(draw_vert)
    rr.a(rad,rad,0,0,0,-rad,rad)
    rr.h(-draw_horiz)
    rr.a(rad,rad,0,0,0,-rad,-rad)

    d_obj.append(rr)





def add_oval_text(d_obj, text, cx, cy, xr, yr,  **kwargs) :
    """(cx,cy) -> oval center
    | xr and yr -> oval x-radius and y-radius"""

    x1 = cx-xr
    x2 = cx+xr
    y1 = cy
    y2 = cy

    oval = draw.Path(**kwargs)
    oval.M(x1,y1)
    oval.A(xr,yr,0,0,0,x2,y2)
    oval.A(xr,yr,0,0,0,x1,y1)

    d_obj.append(oval)
    d_obj.append(draw.Text(text,18,cx,cy,text_anchor="middle",fill=kwargs['stroke'], font_family='arial'))





def draw_class(d, class_name, class_struct_dict, start_y, drawing_width) :

    PADDING = 10
    COL_NUM = 3
    OVAL_HEIGHT = 60

    FONTSIZE=14
    TEXT_PADDING=3
    FONTSIZE_BIG = 18

    RAD = 20



    usable_width = drawing_width - (COL_NUM+1)*PADDING
    col_width = usable_width/COL_NUM
    xr = col_width/2
    yr = OVAL_HEIGHT/2




    cx1 = -(col_width + PADDING)
    cx2 = 0
    cx3 = col_width + PADDING
    col_xs = [cx1, cx2, cx3]

    colors = [oranges, yellows, greens]

    top_cy = start_y -(PADDING + yr)

    br.dprint(len(class_struct_dict), 'len(class_struct_dict)')
    br.dprint(len(col_xs), 'len(col_xs)')

    for i in range(len(class_struct_dict)) :
        d.append(draw.Lines(cx2, top_cy, col_xs[i],
                            top_cy - (OVAL_HEIGHT/2 + 2*PADDING),
                            stroke=colors[i][1], stroke_width=4))

    add_oval_text(d, class_name, cx2, top_cy, xr, yr, fill=red, stroke=dred, stroke_width=2 )

    line_height = FONTSIZE + TEXT_PADDING


    startx = cx2
    starty = top_cy - yr

    end_y = 0

    i = -1
    for group_name, group in class_struct_dict.items() :
        i += 1

        cur_by = top_cy - (OVAL_HEIGHT/2 + PADDING)
        bx = col_xs[i] - col_width/2

        line_cnt = len(group)

        height = line_height*line_cnt + RAD*2

        poss_end_y = cur_by - height

        if abs(poss_end_y) > abs(end_y) : end_y = poss_end_y

        add_rounded_rect(d, bx, cur_by, col_width, height, fill=colors[i][0], stroke=colors[i][1], stroke_width=2)

        cur_by -= RAD + 5
        text_bx = bx + PADDING

        d.append(draw.Text(group_name, FONTSIZE_BIG, text_bx, cur_by, fill=colors[i][2], font_family='arial'))

        text_bx += PADDING

        cur_by -= line_height + TEXT_PADDING

        for line in group :
            d.append(draw.Text(line, FONTSIZE, text_bx, cur_by, font_family='arial'))
            cur_by -= line_height



    return end_y


def draw_package(package_dict) :
    DRAWING_WIDTH = 800
    DRAWING_HEIGHT = 500*len(package_dict)

    origin =(-DRAWING_WIDTH/2, -DRAWING_HEIGHT)

    d = draw.Drawing(DRAWING_WIDTH, DRAWING_HEIGHT, origin=origin, style="background-color:#ffffff")

    start_y = 0
    for class_name, class_dict in package_dict.items() :
        end_y = draw_class(d, class_name, class_dict, start_y, DRAWING_WIDTH)
        start_y = end_y - 20

#     display(d)
    return d





# from butts import bob_package_dict
# from make_package_struct_dict import package_dict as bob_py_package_dict
import make_package_struct_dict as mpsd
import imp
imp.reload(mpsd)
bob_py_package_dict = mpsd.package_dict
print(bob_py_package_dict)

d = draw_package(bob_py_package_dict)
# cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/bob_idk'
d.saveSvg(os.path.join('.','example.svg'))
