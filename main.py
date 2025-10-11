# main.py
import os
import glob
from leitor_arquivos import ler_arquivo  # mantém leitor

def find_file(base_name):
    if os.path.exists(base_name):
        return base_name
    for ext in ['.txt', '.dat', '.edges']:
        candidate = base_name + ext
        if os.path.exists(candidate):
            return candidate
    matches = [f for f in os.listdir('.') if f.lower().startswith(base_name.lower())]
    if matches:
        return matches[0]
    gl = glob.glob(base_name + '*')
    if gl:
        return gl[0]
    return None

if __name__ == "__main__":
    arquivos_base = ["espacoaereo", "slides", "slides_modificado"]

    for base in arquivos_base:
        caminho = find_file(base)
        if not caminho:
            print(f"\n❌ Arquivo não encontrado para base '{base}'. Diretório atual: {os.getcwd()}")
            print("Arquivos na pasta:", os.listdir('.'))
            continue

        print(f"\n--- Testando arquivo: {caminho} ---")
        grafo = ler_arquivo(caminho, representacao="lista")  # ou "matriz"

        if not grafo:
            print("Erro ao criar o grafo.")
            continue

        print("Número de vértices:", len(grafo.vertices))

        # Origem fixa em 0 
        ordem_bfs = grafo.bfs(0) if len(grafo.vertices) > 0 else []
        ordem_dfs = grafo.dfs(0) if len(grafo.vertices) > 0 else []
        print("BFS (primeiros 20):", ordem_bfs[:20])
        print("DFS (primeiros 20):", ordem_dfs[:20])

        if grafo.ponderado:
            distancias, caminhos = grafo.dijkstra(0)
            print("Dijkstra (distâncias, primeiros 10):", distancias[:10], "...")
            if 5 < len(grafo.vertices):
                print("Caminho até 5:", caminhos.get(5, []))

