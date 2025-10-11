from collections import deque
import heapq
from typing import List, Tuple, Dict

def busca_em_largura(grafo, origem: int) -> List[int]:
    """Busca em Largura (BFS) - retorna ordem de visitação"""
    if origem < 0 or origem >= len(grafo.vertices):
        return []
    
    visitados = [False] * len(grafo.vertices)
    fila = deque([origem])
    visitados[origem] = True
    ordem_visita = []
    
    while fila:
        vertice = fila.popleft()
        ordem_visita.append(vertice)
        
        for vizinho in grafo.retornar_vizinhos(vertice):
            if not visitados[vizinho]:
                visitados[vizinho] = True
                fila.append(vizinho)
    
    return ordem_visita

def busca_em_profundidade(grafo, origem: int) -> List[int]:
    """Busca em Profundidade (DFS) - retorna ordem de visitação"""
    if origem < 0 or origem >= len(grafo.vertices):
        return []
    
    visitados = [False] * len(grafo.vertices)
    ordem_visita = []
    
    def dfs_recursiva(v):
        visitados[v] = True
        ordem_visita.append(v)
        
        for vizinho in grafo.retornar_vizinhos(v):
            if not visitados[vizinho]:
                dfs_recursiva(vizinho)
    
    dfs_recursiva(origem)
    return ordem_visita

def dijkstra(grafo, origem: int) -> Tuple[List[float], Dict[int, List[int]]]:
    """
    Algoritmo de Dijkstra - retorna (distancias, caminhos)
    """
    #print(grafo.peso_aresta, 5, 3)

    if origem < 0 or origem >= len(grafo.vertices) or not grafo.ponderado:
        return [], {}
    
    n = len(grafo.vertices)
    distancias = [float('inf')] * n
    predecessores = [-1] * n
    visitados = [False] * n
    
    distancias[origem] = 0
    fila_prioridade = [(0, origem)]
    
    while fila_prioridade:
        dist_atual, vertice_atual = heapq.heappop(fila_prioridade)  # CORRIGIDO AQUI!
        
        if visitados[vertice_atual]:
            continue
            
        visitados[vertice_atual] = True
        
        for vizinho in grafo.retornar_vizinhos(vertice_atual):
            peso = grafo.peso_aresta(vertice_atual, vizinho)
            if peso is None:
                continue
                
            nova_distancia = dist_atual + peso
            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = vertice_atual
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
    
    # Construir caminhos completos
    caminhos = {}
    for i in range(n):
        if distancias[i] == float('inf'):
            caminhos[i] = []
            continue
            
        caminho = []
        atual = i
        while atual != -1:
            caminho.append(atual)
            atual = predecessores[atual]
        caminhos[i] = list(reversed(caminho))
    
    return distancias, caminhos