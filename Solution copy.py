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

        #First set up the priority queue
        pque = self.innit_pqueue

        #For every client, run the path finding function
        while len(pque) > 0:
            #pop a client
            cl = heapq.heappop(pque)

            #find the best path for that client and then add it to the map
            paths[cl] = self.find_path(cl)


        return (paths, bandwidths, priorities)
    
    def innit_pqueue(self):
        """
        Innit the priority queue; queue up every node as a touple (tolerance,ID).

        Returns a priority queue of touples as described above.
        """
        #create a list and heapify it
        pqueue = []
        heapq.heapify(pqueue)

        #client list:
        c_list = self.info["list_clients"]

        #tolerances (aka alphas)
        alphas = self.info["alphas"]

        #now for every node, queue it and it's tolerance as a touple
        for c in c_list:

            #tolerance of this client
            tol = alphas.get(c)

            #queue it
            heapq.heappush(pqueue,(tol,c))
        
        return pqueue #return the pqueue

    def find_path(self,client):
        """
        Starting at the isp, find the best path to client while considering the bandwidth map.

        Returns a list that represents a path from isp to client.
        """
        #path for this node
        path = []

        #visited list
        visited = []

        #the current time tick (starts at -1 because we start at the isp which needs to be 0)
        time = -1

        #a list that for every node in the graph starts as null but is switched to the node that found it
        prev = self.set_prev()

        #append and then popleft should work like a normal queue?
        #the queue, starting with the isp node
        queue = deque(self.isp)

        #while the queue is not empty
        while len(queue) > 0:
            #increment time
            time += 1
            node = queue.popleft()
            visited.append(node)
            #find neighbors
            neighbors = self.graph[node]

            #this is where it differs from bfs, when looking for neighbors we need to check the bandwidth map
            for next in neighbors:
                #check for if the tick has any bandwidth modifications
                time_band = self.band_map.get(time + 1,-1)

                #check to see if that node is in the list for that time
                in_list = self.check_within_band_list(self.band_map[time + 1],next)

                #for each neighbor check visisted, then make sure the bandwidth for this tick isn't 0 before queueing
                if visited.count(next) == 0 and time_band != -1 and in_list == True:
                    #check that node's bandwidth for this time tick
                    if self.check_within_band_list == True:
                        queue.append(next)
                    
                elif visited.count(next) == 0 and time_band != -1 and in_list == False:
                    if self.check_within_band_list == True:
                        queue.append(next)

                elif visited.count(next) == 0 and time_band == -1:
                    if self.check_within_band_list == True:
                        queue.append(next)                    

        path = self.construct_path(prev,client)
        #before returning, update the bandwidth map
        self.update_b_map(path)

        return path
    
    def construct_path(self,prev,node):
        """
        Takes a prev list and uses that to construct a path.

        Returns a list representing a path.
        """
        path = []
        p = node
        #starting at the node, go backwards until the isp is found.
        while p != self.isp:
            path.append(p)
            if prev[p] != None:
                p = prev[p]
        path.append(self.isp)
        #remember to reverse the path
        path.reverse()
        return path
    
    def set_prev(self):
        """
        Innits the prev list.

        Returns a list n long with nulls.
        """
        prev = []

        for node in self.info["list_clients"]:
            prev.append(None)

        return prev
    
    def update_b_map(self,path):
        """
        Updates the bandwidth map with the latest path's modifications.

        This function assumes the path is in the right order (not reversed).

        Returns nothing.
        """
        #for every node in the path, place that node and the time (index) into the map/update the one already in there
        for index, node in enumerate(path):
            #skipping the first tick (all of the nodes start at the isp)
            if index != 0:
                #if this is the first entry for this time tick, we have to create the int -> list pair
                if self.band_map.get(index,-1) == -1:
                    #the bandwidth - 1
                    band = self.info["bandwidths"][node] - 1
                    #creating the int -> list pair with the (bandwidth,node) touple.
                    self.band_map[index] = [(band,node)]

                #if the time tick exists but this node is new, append the node to the list
                elif self.band_map.get(index,-1) != -1 and not(self.band_map[index].__contains__(node)):

                    #the bandwidth - 1
                    band = self.info["bandwidths"][node] - 1

                    #append (bandwidth, ID) to the list stored at index
                    self.band_map[index].append((band,node))
                
                #else, the index must exist as a key and the node must be in the corrsponding list
                else:
                    #update the list
                    for pair in self.band_map[index]:
                        #if this is the node
                        if pair[1] == node:
                            #subtract 1 from the bandwidth
                            pair[0] -= 1
        return
    
    def check_within_band_list(self,list,node):
        """
        Checks to see if a node is in the list for a given time tick in the bandwidth map.

        Returns bool.
        """
        #for every touple in the list, check index 1 (ID)
        for tups in list:
            if tups[1] == node:
                return True
            
        return False
    
    def grab_from_band(self,list,node):
        for tups in list:
            if tups[1] == node:
                if tups[0] > 0:
                    return True
            
        return False


    
