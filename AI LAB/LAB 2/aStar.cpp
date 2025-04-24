#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Node {
public:
    string value;
    int heuristic;
    int pathCost;
    int tillNow;
    Node* parent;
    vector<pair<Node*, int>> voisins;

    Node(string val, int h) : value(val), heuristic(h), pathCost(0), tillNow(0), parent(nullptr) {}
};

struct CompareNode {
    bool operator()(Node* a, Node* b) {
        return a->tillNow > b->tillNow;
    }
};

void AStarSearch(Node* source, Node* goal) {
    vector<Node*> explored;
    source->pathCost = 0;
    priority_queue<Node*, vector<Node*>, CompareNode> queue;
    vector<Node*> queueContents;

    queue.push(source);
    queueContents.push_back(source);

    vector<Node*> path;

    while (!queue.empty()) {
        path.clear();
        Node* current = queue.top();
        queue.pop();
        queueContents.erase(remove(queueContents.begin(), queueContents.end(), current), queueContents.end());

        cout<< " -> " << current->value;
        explored.push_back(current);

        for (Node* node = current; node != nullptr; node = node->parent) {
            path.push_back(node);
        }

        if (current->value == goal->value) {
            goal->parent = current->parent;
            goal->pathCost = current->pathCost;
            cout << endl << "Least cost solution found: " << current->value << endl;
            return;
        }

        for (auto& e : current->voisins) {
            Node* voisin = e.first;
            int cost = e.second;

            bool inQueue = find(queueContents.begin(), queueContents.end(), voisin) != queueContents.end();
            bool inExplored = find(explored.begin(), explored.end(), voisin) != explored.end();
            bool inPath = find(path.begin(), path.end(), voisin) != path.end();

            if ((inQueue || inExplored) && !inPath) {
                Node* n = new Node(*voisin);
                n->pathCost = current->pathCost + cost;
                n->tillNow = n->pathCost + n->heuristic;
                n->parent = current;
                queue.push(n);
                queueContents.push_back(n);
            } else if (!inPath) {
                voisin->pathCost = current->pathCost + cost;
                voisin->tillNow = voisin->pathCost + voisin->heuristic;
                voisin->parent = current;
                queue.push(voisin);
                queueContents.push_back(voisin);
            }
        }
    }
}

int main() {
    Node* n1 = new Node("Arad", 366);
    Node* n2 = new Node("Zerind", 374);
    Node* n3 = new Node("Oradea", 380);
    Node* n4 = new Node("Sibiu", 253);
    Node* n5 = new Node("Fagaras", 176);
    Node* n6 = new Node("Rimnicu Vilcea", 193);
    Node* n7 = new Node("Pitesti", 100);
    Node* n8 = new Node("Timisoara", 329);
    Node* n9 = new Node("Lugoj", 244);
    Node* n10 = new Node("Mehadia", 241);
    Node* n11 = new Node("Drobeta", 242);
    Node* n12 = new Node("Craiova", 160);
    Node* n13 = new Node("Bucharest", 0);
    Node* n14 = new Node("Giurgiu", 77);

    n1->voisins = {{n2, 75}, {n4, 140}, {n8, 118}};
    n2->voisins = {{n1, 75}, {n3, 71}};
    n3->voisins = {{n2, 71}, {n4, 151}};
    n4->voisins = {{n1, 140}, {n5, 99}, {n3, 151}, {n6, 80}};
    n5->voisins = {{n4, 99}, {n13, 211}};
    n6->voisins = {{n4, 80}, {n7, 97}, {n12, 146}};
    n7->voisins = {{n6, 97}, {n13, 101}, {n12, 138}};
    n8->voisins = {{n1, 118}, {n9, 111}};
    n9->voisins = {{n8, 111}, {n10, 70}};
    n10->voisins = {{n9, 70}, {n11, 75}};
    n11->voisins = {{n10, 75}, {n12, 120}};
    n12->voisins = {{n11, 120}, {n6, 146}, {n7, 138}};
    n13->voisins = {{n7, 101}, {n14, 90}, {n5, 211}};
    n14->voisins = {{n13, 90}};

    AStarSearch(n1, n13);

    return 0;
}