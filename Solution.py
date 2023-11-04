from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

        #the bandwidth map in the format {time:[(bandwidth left,ID), ...], ...}
        self.band_map = {}

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}


        return (paths, bandwidths, priorities)
    
    #New Stuff
    #other


def modified_bfs_path(self,graph,isp, list_clients):
    paths = {}
    graph_size = len(graph)
    priors = [-1]*graph_size
    search_queue = []
    heapq.heappush(search_queue, (0,isp))
    while search_queue:
        node = heapq.heappop(search_queue)
        for neighbor in graph[node[1]]:
            if(priors[neighbor] == -1 and neighbor != isp):
                priors[neighbor] = node[1]
                heapq.heappush(search_queue,(node[0] + 1, neighbor))

    for client in list_clients:
        path = []
        current_node = client
        while(current_node != -1):
            path.append(current_node)
            current_node = priors[current_node]
        path = path[::-1]
        paths[client] = path

        return paths

def output_paths(self):
    paths, bandwidths, priorities = {}, {}, {}

    bw = 500
    node_bandwidths = self.info["bandwidths"]
    size = len(node_bandwidths)
    for key, val in node_bandwidths.items():
        if node_bandwidths[key] < bw:
            node_bandwidths[key] = bw
    tol = 500
    node_tols = self.info["alphas"]
    for key, val in node_tols.items():
        if node_tols[key] < tol:
            node_tols[key] = tol
    paths = self.modified_bfs_path(self.graph,self.isp, self.info["list_clients"])

    return paths,node_bandwidths, priorities
    
