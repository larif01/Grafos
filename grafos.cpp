#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>

using namespace std;

// Classe base para Grafos
class Grafo {
protected:
    bool direcionado;
    bool ponderado;
    vector<string> vertices;

public:
    Grafo(bool dir, bool pond) : direcionado(dir), ponderado(pond) {}

    virtual bool inserirVertice(string label) = 0;
    virtual bool removerVertice(int indice) = 0;
    virtual string labelVertice(int indice) = 0;
    virtual void imprimeGrafo() = 0;
    virtual bool inserirAresta(int origem, int destino, float peso = 1) = 0;
    virtual bool removerAresta(int origem, int destino) = 0;
    virtual bool existeAresta(int origem, int destino) = 0;
    virtual float pesoAresta(int origem, int destino) = 0;
    virtual vector<int> retornarVizinhos(int vertice) = 0;
};

// Classe para Grafo com Matriz de Adjacência
class GrafoMatriz : public Grafo {
private:
    vector<vector<float>> matriz;

public:
    GrafoMatriz(bool dir, bool pond) : Grafo(dir, pond) {}

    bool inserirVertice(string label) override {
        vertices.push_back(label);
        for (auto& row : matriz) {
            row.push_back(0); // Inicializa novas arestas com 0
        }
        matriz.push_back(vector<float>(vertices.size(), 0)); // Nova linha
        return true;
    }

    bool removerVertice(int indice) override {
        if (indice < 0 || indice >= vertices.size()) return false;

        vertices.erase(vertices.begin() + indice);
        matriz.erase(matriz.begin() + indice);
        for (auto& row : matriz) {
            row.erase(row.begin() + indice);
        }
        return true;
    }

    string labelVertice(int indice) override {
        if (indice < 0 || indice >= vertices.size()) throw out_of_range("Índice fora do intervalo.");
        return vertices[indice];
    }

    void imprimeGrafo() override {
        for (const auto& vertice : vertices) {
            cout << vertice << " ";
        }
        cout << endl;

        for (size_t i = 0; i < matriz.size(); ++i) {
            for (size_t j = 0; j < matriz[i].size(); ++j) {
                cout << matriz[i][j] << " ";
            }
            cout << endl;
        }
    }

    bool inserirAresta(int origem, int destino, float peso = 1) override {
        if (origem < 0 || origem >= vertices.size() || destino < 0 || destino >= vertices.size()) return false;
        matriz[origem][destino] = ponderado ? peso : 1;
        if (!direcionado) {
            matriz[destino][origem] = ponderado ? peso : 1;
        }
        return true;
    }

    bool removerAresta(int origem, int destino) override {
        if (origem < 0 || origem >= vertices.size() || destino < 0 || destino >= vertices.size()) return false;
        matriz[origem][destino] = 0;
        if (!direcionado) {
            matriz[destino][origem] = 0;
        }
        return true;
    }

    bool existeAresta(int origem, int destino) override {
        return matriz[origem][destino] != 0;
    }

    float pesoAresta(int origem, int destino) override {
        return matriz[origem][destino];
    }

    vector<int> retornarVizinhos(int vertice) override {
        vector<int> vizinhos;
        for (size_t i = 0; i < matriz[vertice].size(); ++i) {
            if (matriz[vertice][i] != 0) {
                vizinhos.push_back(i);
            }
        }
        return vizinhos;
    }
};

// Classe para Grafo com Lista de Adjacência
class Aresta {
public:
    int destino;
    float peso;

    Aresta(int dest, float p) : destino(dest), peso(p) {}
};

class GrafoLista : public Grafo {
private:
    vector<vector<Aresta>> lista;

public:
    GrafoLista(bool dir, bool pond) : Grafo(dir, pond) {}

    bool inserirVertice(string label) override {
        vertices.push_back(label);
        lista.push_back(vector<Aresta>());
        return true;
    }

    bool removerVertice(int indice) override {
        if (indice < 0 || indice >= vertices.size()) return false;

        vertices.erase(vertices.begin() + indice);
        lista.erase(lista.begin() + indice);

        for (auto& arestas : lista) {
            arestas.erase(remove_if(arestas.begin(), arestas.end(),
                [indice](Aresta& a) { return a.destino == indice; }), arestas.end());
        }
        return true;
    }

    string labelVertice(int indice) override {
        if (indice < 0 || indice >= vertices.size()) throw out_of_range("Índice fora do intervalo.");
        return vertices[indice];
    }

    void imprimeGrafo() override {
        for (size_t i = 0; i < vertices.size(); ++i) {
            cout << vertices[i] << ": ";
            for (const auto& aresta : lista[i]) {
                cout << "(" << aresta.destino << ", " << aresta.peso << ") ";
            }
            cout << endl;
        }
    }

    bool inserirAresta(int origem, int destino, float peso = 1) override {
        if (origem < 0 || origem >= vertices.size() || destino < 0 || destino >= vertices.size()) return false;
        lista[origem].emplace_back(destino, ponderado ? peso : 1);
        if (!direcionado) {
            lista[destino].emplace_back(origem, ponderado ? peso : 1);
        }
        return true;
    }

    bool removerAresta(int origem, int destino) override {
        if (origem < 0 || origem >= vertices.size() || destino < 0 || destino >= vertices.size()) return false;

        lista[origem].erase(remove_if(lista[origem].begin(), lista[origem].end(),
            [destino](Aresta& a) { return a.destino == destino; }), lista[origem].end());

        if (!direcionado) {
            lista[destino].erase(remove_if(lista[destino].begin(), lista[destino].end(),
                [origem](Aresta& a) { return a.destino == origem; }), lista[destino].end());
        }
        return true;
    }

    bool existeAresta(int origem, int destino) override {
        for (const auto& aresta : lista[origem]) {
            if (aresta.destino == destino) return true;
        }
        return false;
    }

    float pesoAresta(int origem, int destino) override {
        for (const auto& aresta : lista[origem]) {
            if (aresta.destino == destino) return aresta.peso;
        }
        return 0; // Aresta não existe
    }

    vector<int> retornarVizinhos(int vertice) override {
        vector<int> vizinhos;
        for (const auto& aresta : lista[vertice]) {
            vizinhos.push_back(aresta.destino);
        }
        return vizinhos;
    }
};

// Exemplo de uso
int main() {
    GrafoMatriz grafoM(true, false); // Grafo direcionado e não ponderado
    grafoM.inserirVertice("A");
    grafoM.inserirVertice("B");
    grafoM.inserirAresta(0, 1);
    grafoM.imprimeGrafo();

    GrafoLista grafoL(false, true); // Grafo não direcionado e ponderado
    grafoL.inserirVertice("C");
    grafoL.inserirVertice("D");
    grafoL.inserirAresta(0, 1, 2.5);
    grafoL.imprimeGrafo();

    return 0;
}
