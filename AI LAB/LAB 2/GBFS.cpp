#include <iostream>
#include <queue>
#include <vector>
#include <unordered_map>
#include <unordered_set>

using namespace std;

struct Node {
    int state;
    int heuristic;
    Node* parent;
    Node(int s, int h, Node* p = nullptr) : state(s), heuristic(h), parent(p) {}
};

struct Compare {
    bool operator()(Node* a, Node* b) {
        return a->heuristic > b->heuristic;  // Min-heap based on heuristic
    }
};

class GBFS {
public:
    GBFS(int goal, unordered_map<int, int> heuristics, unordered_map<int, vector<int>> graph) 
        : goalState(goal), h(heuristics), adjList(graph) {}

    bool search(int start) {
        priority_queue<Node*, vector<Node*>, Compare> frontier;
        unordered_set<int> explored;  // Use unordered_set for O(1) lookups
        
        frontier.push(new Node(start, h[start]));  // Start node

        while (!frontier.empty()) {
            Node* current = frontier.top();
            frontier.pop();
            
            cout << "Visiting: " << current->state << endl;  // Debug Output
            
            if (current->state == goalState) {
                printPath(current);
                return true;
            }

            explored.insert(current->state);  // Mark as explored
            
            for (int neighbor : adjList[current->state]) {
                if (explored.find(neighbor) == explored.end()) {  // Only push unexplored nodes
                    frontier.push(new Node(neighbor, h[neighbor], current));
                }
            }
        }
        cout << "Goal not reachable." << endl;
        return false;
    }

private:
    int goalState;
    unordered_map<int, int> h;
    unordered_map<int, vector<int>> adjList;

    void printPath(Node* node) {
        if (!node) return;
        printPath(node->parent);
        cout << node->state << " ";
    }
};

int main() {
    unordered_map<int, int> heuristics = {
        {0, 5}, {1, 4}, {2, 3}, {3, 2}, {4, 1}, {5, 0}
    };

    unordered_map<int, vector<int>> graph = {
        {0, {1, 2}}, {1, {0, 3}}, {2, {0, 4}}, {3, {1, 5}}, {4, {2, 5}}, {5, {}}
    };

    GBFS gbfs(5, heuristics, graph);
    gbfs.search(0);

    return 0;
}
