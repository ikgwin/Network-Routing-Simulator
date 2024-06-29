#!/usr/bin/env python3

import sys
from heapq import heappush
from heapq import heappop

def read_network_config():

    network_nodes = {}  # stores the router initial config
    current_section = 'init'  # tracks current input section
    network_updates = []  # stores updates and initial link states

    for input_line in sys.stdin:

        # strip white space from each input line
        input_line = input_line.strip()  
        
        if input_line == 'LINKSTATE':
            # transition to link state in put
            current_section = 'linkstate'  
        elif input_line == 'UPDATE':
            # transition to updates input
            current_section = 'update'  
        
        elif input_line == 'END':
            break  # stop readin input

        else:
            
            if current_section == 'init':
                # initialise routers with no connections
                network_nodes[input_line] = {}  
            
            elif current_section in ['linkstate', 'update']:
                components = input_line.split()  # split line into components
                node1, node2 = components[0].split('-')
                link_cost = int(components[1])
                affected_routers = components[2].split(',') if len(components) > 2 else []
                network_updates.append((current_section, node1, node2, link_cost, affected_routers))
    
    # return both routers and their updates/actions
    return network_nodes, network_updates  

def modify_network_topology(network_nodes, node1, node2, link_cost):
    # check if link should get removed (cost -> -1)
    if link_cost == -1:
        # remove link from node1 to node2 if exists
        if node2 in network_nodes.get(node1,{}):
            del network_nodes[node1][node2]
        # remove link from node2 to node1 if exist
        if node1 in network_nodes.get(node2,{}):
            del network_nodes[node2][node1]
    else:
        # Ensure both nodes exist in the network
        if node1 not in network_nodes:
            network_nodes[node1] = {}
        if node2 not in network_nodes:
            network_nodes[node2] = {}

        # add / update link cost between node1 and node2
        network_nodes[node1][node2] = link_cost
        network_nodes[node2][node1] = link_cost

from heapq import heappush, heappop

def compute_dijkstra(network_nodes, start_node):

    # init distances from start_node to infinity, and to 0 for start_node itself
    shortest_distances={node: float('inf') for node in network_nodes}
    shortest_distances[start_node]=0

    # track paths
    previous_nodes = {node: None for node in network_nodes}  

    # priority queue to pick  node with smallest distance
    priority_queue=[(0,start_node)]  

    while priority_queue:

        # get node w smallest distance
        curr_dist, curr_node = heappop(priority_queue)

        if curr_dist > shortest_distances[curr_node]:
            # skip if found a shorter path 
            continue  

        # explore each neighbor and update paths an distances
        for neighbor, weight in network_nodes.get(curr_node,{}).items():
            # calc new distance to neighbor
            new_distance = curr_dist+weight  

            if new_distance < shortest_distances[neighbor]:
                # update if new distance is shorter
                shortest_distances[neighbor]=new_distance
                previous_nodes[neighbor]=curr_node
                # push new distance into priority queue
                heappush(priority_queue,(new_distance,neighbor))  

    # return both distances and paths info
    return shortest_distances, previous_nodes  

# printing the info
def display_routing_information(curr_router, network_nodes):
    # init data structures for LSDB and routing table
    link_state_database = set()
    routing_info = []

    # check if curr router exists in network or has no connections
    if curr_router not in network_nodes or not network_nodes[curr_router]:
        print(f"{curr_router} Neighbour Table:\n")
        print(f"{curr_router} LSDB:\n")
        print(f"{curr_router} Routing Table:\n")
        return

    # compute dijkstra to get distances n paths
    shortest_distances, path_predecessors = compute_dijkstra(network_nodes, curr_router)

    # get all link states for LSDB
    for node1 in network_nodes:
        for node2 in network_nodes[node1]:
            if node1 < node2:
                link_state_database.add(f"{node1}|{node2}|{network_nodes[node1][node2]}")

    # construct routing info data for easier printing
    for dest in sorted(network_nodes):
        if dest != curr_router and shortest_distances[dest] != float('inf'):
            hop_next = dest
            # Reverse trace to find the first hop in the path to the destination
            while path_predecessors[hop_next] != curr_router:
                hop_next = path_predecessors[hop_next]
            routing_info.append(f"{dest}|{hop_next}|{shortest_distances[dest]}")

    # output info
    print(f"{curr_router} Neighbour Table:")
    for neighbor in sorted(network_nodes[curr_router]):
        print(f"{neighbor}|{network_nodes[curr_router][neighbor]}")
    print()

    print(f"{curr_router} LSDB:")
    for link in sorted(link_state_database):
        print(link)
    print()

    print(f"{curr_router} Routing Table:")
    for route in routing_info:
        print(route)
    print()



def main():

    # read initial config and updates from network input
    routers, actions = read_network_config()
    
    # process each action retrieved from input
    for action in actions:
        state, router1, router2, cost, selected_routers = action
        
        # update network topology based on current action deets
        modify_network_topology(routers, router1, router2, cost)
        
        # check if current action requires displaying routing information
        if state == 'linkstate' or (state == 'update' and selected_routers):
            # print routing information for each router affected by current action
            for router in sorted(selected_routers):
                display_routing_information(router, routers)

if __name__ == "__main__":
    main()


    
