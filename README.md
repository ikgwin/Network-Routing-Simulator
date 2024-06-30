# Network-Routing-Simulator
*University project*

This Python script simulates network routing using Dijkstra's algorithm and manages network topology updates based on input configurations. It supports two modes of operation: initial network setup (LINKSTATE) and dynamic updates (UPDATE).

Features
Network Configuration: Read initial network topology and updates from standard input.
Routing Calculation: Uses Dijkstra's algorithm to compute shortest paths and routing tables for each router.
Dynamic Updates: Handles dynamic updates to network topology (additions and removals of links).
Output: Displays neighbor tables, Link State Database (LSDB), and routing tables for each affected router.
Usage
Input Format:

Use LINKSTATE to specify initial network configuration.
Use UPDATE to provide dynamic updates to the network.
Use END to terminate input.
Execution:

Run the script and provide input through standard input (e.g., from a file or command line).
bash
Copy code
python3 routing_simulator.py < input_data.txt
Output:
Neighbor tables, LSDB, and routing tables will be displayed for each affected router based on the input actions.
Example
Assume input_data.txt contains:

css
Copy code
LINKSTATE
A
B
A-B 1
B
C
B-C 2
END
Running the script will generate output showing the network topology and routing tables.
