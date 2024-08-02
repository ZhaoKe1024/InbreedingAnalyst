#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/8/1 14:13
# @Author: ZhaoKe
# @File : pyechart_test.py
# @Software: PyCharm
import random

from pyecharts import options as opts
from pyecharts.charts import Graph

from inbreed_lib.analyzer.data_example import get_instant_1
from inbreed_lib.analyzer.commonAncestors import FamilyAnalyzer

lg = get_instant_1()
analyzer = FamilyAnalyzer(familyGraph=lg)

# vertices = analyzer.familyGraph.vertex_list
graph = analyzer.familyGraph.edge_list
# print("点集", [item.index for item in analyzer.familyGraph.vertex_list])
# print("边集", analyzer.familyGraph.edge_list)
# print("深度", analyzer.Depth)
print("-----------------------")
# analyzer.calc_path_prob(16, 17, 0)
# print(analyzer.calc_inbreed_coef(2))
# print(analyzer.calc_inbreed_coef(9))
# print(analyzer.calc_inbreed_coef(26))
# print(analyzer.calc_kinship_corr(24, 25))
# print("---------------------------")
# for iten in analyzer.relagraph_ancestors_inbreed:
#     print(iten)
vertices = list(range(27))
# graph = [[10, 0], [10, 2], [12, 3], [12, 5], [18, 10], [18, 13], [13, 3], [13, 5], [19, 12], [19, 14], [14, 6], [14, 7],
#          [21, 16], [21, 17], [16, 9], [16, 12], [9, 0], [9, 1], [17, 10], [17, 11], [11, 3], [11, 4], [24, 21],
#          [24, 22], [22, 18], [22, 19], [25, 21], [25, 23], [23, 18], [23, 19]]
print("点集:", vertices)
print("边集:", graph)
depths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
depth_cnt, cur = [0] * 6, 0
cur_depth = depths[0]
for j in range(27):
    if depths[j] == cur_depth:
        depth_cnt[cur] += 1
    else:
        cur_depth = depths[j]
        cur += 1
        depth_cnt[cur] += 1
print(depth_cnt)
max_cnt = max(depth_cnt)
steps = [4*int(max_cnt/item) for item in depth_cnt]

xy = []
print(len(vertices), len(graph), len(depths))
cur_depth, depth_pos = depths[0], 0
cur_step = 0
top_m = 4
for j in range(27):
    if depths[j] == cur_depth:
        top_m += steps[depth_pos]
    else:
        cur_depth = depths[j]
        top_m = 4
        depth_pos += 1
    xy.append([depths[j]*8, top_m+random.randint(0, 2)])
# vertices = [1, 2, 3, 4, 5, 6]
# graph = [[1, 4], [2, 4], [2, 5], [3, 5], [4, 6], [5, 6]]

# xy = [[0, 5], [0, 8], [0, 11], [2, 7], [2, 9], [4, 8]]
# x left margin,  y: top margin
nodes_data = [opts.GraphNode(x=xy[j][0], y=xy[j][1], name="{}".format(vertices[j]), symbol_size=20) for j in
              range(len(vertices))]
#     [
#     opts.GraphNode(name="结点1", symbol_size=10),
#     opts.GraphNode(name="结点2", symbol_size=20),
#     opts.GraphNode(name="结点3", symbol_size=30),
#     opts.GraphNode(name="结点4", symbol_size=40),
#     opts.GraphNode(name="结点5", symbol_size=50),
#     opts.GraphNode(name="结点6", symbol_size=60),
# ]
links_data = []
for item in graph:
    links_data.append(opts.GraphLink(source="{}".format(item[0]), target="{}".format(item[1]), value=2))
#     [
#     opts.GraphLink(source="结点1", target="结点2", value=2),
#     opts.GraphLink(source="结点2", target="结点3", value=3),
#     opts.GraphLink(source="结点3", target="结点4", value=4),
#     opts.GraphLink(source="结点4", target="结点5", value=5),
#     opts.GraphLink(source="结点5", target="结点6", value=6),
#     opts.GraphLink(source="结点6", target="结点1", value=7),
# ]
c = (
    Graph()
    .add(
        "",
        nodes_data,
        links_data,
        repulsion=4000,
        edge_label=opts.LabelOpts(
            is_show=True, position="middle", formatter="{b}:{c}"
        ),
        edge_symbol=["none", "arrow"],
        layout="none"
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
    )
    .render("graph_with_edge_options.html")
)
