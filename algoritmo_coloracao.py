# algoritmo_coloracao.py
import time
from typing import List, Tuple, Set, List as TList
from heapq import heappush, heappop
from leitor_arquivos import ler_arquivo

# ========================================================
# Helpers gerais
# ========================================================
# 1) Vizinhança NÃO-DIRECIONADA (para coloração)
# 2) Adjacência e lista de arestas NÃO-DIRECIONADAS com pesos (para AGM)

def build_undirected_adj(grafo) -> TList[Set[int]]:
    n = len(grafo.vertices)
    adj: TList[Set[int]] = [set() for _ in range(n)]
    for u in range(n):
        for v in grafo.retornar_vizinhos(u):
            if u == v:
                continue
            adj[u].add(v)
            adj[v].add(u)
    return adj


def _peso_undirected(grafo, u: int, v: int):
    """Peso da aresta não-direcionada {u,v}. Em grafos direcionados, usa min(u->v, v->u).
    Em grafos não ponderados retorna 1.0. Se não existir em nenhum sentido, retorna None."""
    w1 = grafo.peso_aresta(u, v)
    w2 = grafo.peso_aresta(v, u)
    if w1 is None and w2 is None:
        return None
    if not grafo.ponderado:
        return 1.0
    if w1 is None:
        return float(w2)
    if w2 is None:
        return float(w1)
    return float(min(w1, w2))


def adj_undirected_weighted(grafo):
    n = len(grafo.vertices)
    adj = [[] for _ in range(n)]
    for u in range(n):
        for v in grafo.retornar_vizinhos(u):
            if u == v:
                continue
            w = _peso_undirected(grafo, u, v)
            if w is None:
                continue
            adj[u].append((v, w))
            adj[v].append((u, w))
    # dedup por menor peso
    for u in range(n):
        best = {}
        for v, w in adj[u]:
            if v not in best or w < best[v]:
                best[v] = w
        adj[u] = [(v, best[v]) for v in best]
    return adj


def edge_list_undirected(grafo):
    n = len(grafo.vertices)
    edges = []
    seen = set()
    for u in range(n):
        for v in grafo.retornar_vizinhos(u):
            if u == v:
                continue
            a, b = (u, v) if u < v else (v, u)
            if (a, b) in seen:
                continue
            w = _peso_undirected(grafo, a, b)
            if w is None:
                continue
            seen.add((a, b))
            edges.append((w, a, b))
    return edges


def is_valid_coloring_adj(adj: TList[Set[int]], coloracao: TList[int]) -> bool:
    for v, cor_v in enumerate(coloracao):
        for w in adj[v]:
            if coloracao[w] == cor_v:
                return False
    return True

# ========================================================
# Coloração
# ========================================================

def backtrack_coloracao(adj: TList[Set[int]], coloracao: TList[int], v: int, k: int) -> bool:
    n = len(adj)
    if v == n:
        return is_valid_coloring_adj(adj, coloracao)
    proibidas = { coloracao[u] for u in adj[v] if coloracao[u] != -1 }
    for cor in range(k):
        if cor in proibidas:
            continue
        coloracao[v] = cor
        if backtrack_coloracao(adj, coloracao, v + 1, k):
            return True
        coloracao[v] = -1
    return False


def forca_bruta_coloracao(grafo):
    n = len(grafo.vertices)
    if n == 0:
        return [], 0
    adj = build_undirected_adj(grafo)
    if all(len(adj[v]) == 0 for v in range(n)):
        return [0]*n, 1
    for k in range(2, n + 1):
        coloracao = [-1] * n
        if backtrack_coloracao(adj, coloracao, 0, k):
            return coloracao, k
    return [-1] * n, n


def greedy_by_order(adj: TList[Set[int]], ordem: TList[int]) -> Tuple[TList[int], int]:
    n = len(adj)
    cor = [-1] * n
    for v in ordem:
        proibidas = { cor[u] for u in adj[v] if cor[u] != -1 }
        c = 0
        while c in proibidas:
            c += 1
        cor[v] = c
    k = max(cor) + 1 if max(cor) >= 0 else 0
    return cor, k


def heuristica_welsh_powell(grafo):
    adj = build_undirected_adj(grafo)
    graus = [(v, len(adj[v])) for v in range(len(adj))]
    ordem = [v for v, _ in sorted(graus, key=lambda x: -x[1])]
    return greedy_by_order(adj, ordem)


def heuristica_dsat(grafo):
    adj = build_undirected_adj(grafo)
    n = len(adj)
    cor = [-1] * n
    dsat = [0] * n
    grau = [len(adj[v]) for v in range(n)]

    def recomputa_dsat(v: int):
        viz_cores = { cor[u] for u in adj[v] if cor[u] != -1 }
        dsat[v] = len(viz_cores)

    for _ in range(n):
        cand = [(dsat[v], grau[v], v) for v in range(n) if cor[v] == -1]
        if not cand:
            break
        _, _, u = max(cand)
        proibidas = { cor[x] for x in adj[u] if cor[x] != -1 }
        c = 0
        while c in proibidas:
            c += 1
        cor[u] = c
        for w in adj[u]:
            if cor[w] == -1:
                recomputa_dsat(w)
    k = max(cor) + 1 if max(cor) >= 0 else 0
    return cor, k


def heuristica_simples(grafo):
    adj = build_undirected_adj(grafo)
    ordem = list(range(len(adj)))
    return greedy_by_order(adj, ordem)


def testar_coloracao(nome_arquivo):
    grafo = ler_arquivo(nome_arquivo, representacao="lista")
    if grafo is None:
        print(f"❌ Arquivo '{nome_arquivo}' não pôde ser carregado.")
        return
    print(f"\n--- Testando: {nome_arquivo} ---")
    print("Número de vértices:", len(grafo.vertices))
    for nome, func in [
        ("Força Bruta", forca_bruta_coloracao),
        ("Welsh-Powell", heuristica_welsh_powell),
        ("DSATUR", heuristica_dsat),
        ("Heurística Simples", heuristica_simples)
    ]:
        if nome == "Força Bruta" and len(grafo.vertices) > 12:
            print(f"{nome}: ignorado (grafo muito grande)")
            continue
        ini = time.time()
        coloracao, num_cores = func(grafo)
        fim = time.time()
        adj = build_undirected_adj(grafo)
        valido = is_valid_coloring_adj(adj, coloracao)
        if not valido:
            print(f"⚠️ {nome}: coloração inválida!")
        elif num_cores <= 1 and any(len(a) > 0 for a in adj):
            print(f"⚠️ {nome}: cores insuficientes (1), havia arestas!")
        else:
            print(f"{nome}: {num_cores} cores válidas em {fim - ini:.4f}s")
        if len(grafo.vertices) <= 10:
            print("Vértices e cores:", list(enumerate(coloracao)))

# ========================================================
# Árvores Geradoras Mínimas (AGM): Prim e Kruskal 
# ========================================================

def prim(grafo):
    """Prim (E log V) com heap; retorna FLORESTA mínima se o grafo for desconexo."""
    n = len(grafo.vertices)
    if n == 0:
        print("❌ Grafo vazio.")
        return [], 0.0
    adj = adj_undirected_weighted(grafo)
    visitado = [False] * n
    mst = []
    total = 0.0
    for s in range(n):
        if visitado[s]:
            continue
        visitado[s] = True
        heap = []
        for v, w in adj[s]:
            heappush(heap, (w, s, v))
        while heap:
            w, u, v = heappop(heap)
            if visitado[v]:
                continue
            visitado[v] = True
            mst.append((u, v, w))
            total += w
            for x, wx in adj[v]:
                if not visitado[x]:
                    heappush(heap, (wx, v, x))
    print(f"🌲 Prim: {len(mst)} arestas, soma = {total:.2f}")
    return mst, total


def kruskal(grafo):
    """Kruskal com Union-Find; retorna FLORESTA mínima se desconexo."""
    n = len(grafo.vertices)
    if n == 0:
        print("❌ Grafo vazio.")
        return [], 0.0
    edges = edge_list_undirected(grafo)
    edges.sort(key=lambda x: x[0])
    parent = list(range(n))
    rank = [0] * n
    def find(a):
        if parent[a] != a:
            parent[a] = find(parent[a])
        return parent[a]
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True
    mst = []
    total = 0.0
    for w, u, v in edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
    print(f"🌲 Kruskal: {len(mst)} arestas, soma = {total:.2f}")
    return mst, total

# ========================================================
# Execução principal (testes)
# ========================================================
if __name__ == "__main__":
    arquivos_teste = [
        "espacoaereo.txt",
        "grafo_direcionado_Ponderado_Direcionado.txt",
        "grafo_grande_completo.txt",
        "grafo_ponderado_Ponderado_NDirecionado.txt",
        "grafo_simples_NPonderadoNDirecionado.txt",
        "slides.txt",
        "slides_modificado.txt",
        "r250-66-65.txt",
        "k5.txt",
        "k33.txt",
        "r1000-234-234.txt"
    ]

    print("\n" + "="*70)
    print("🔹 TESTES DE COLORAÇÃO DE GRAFOS")
    print("="*70)

    for nome in arquivos_teste:
        grafo = ler_arquivo(nome, representacao="lista")
        if grafo is None:
            print(f"\n❌ Arquivo '{nome}' não pôde ser carregado.")
            continue

        print(f"Arquivo: {nome}")
        print(f"   ├─ Número de vértices: {len(grafo.vertices)}")
        print(f"   ├─ Iniciando algoritmos de coloração...")
        print("   └──────────────────────────────────────────────")

        for nome_alg, func in [
            ("Força Bruta", forca_bruta_coloracao),
            ("Welsh-Powell", heuristica_welsh_powell),
            ("DSATUR", heuristica_dsat),
            ("Heurística Simples", heuristica_simples)
        ]:
            if nome_alg == "Força Bruta" and len(grafo.vertices) > 12:
                print(f"      ⚙️  {nome_alg:<20} → ignorado (grafo muito grande)")
                continue

            ini = time.time()
            coloracao, num_cores = func(grafo)
            fim = time.time()
            tempo = fim - ini
            adj = build_undirected_adj(grafo)
            valido = is_valid_coloring_adj(adj, coloracao)

            if not valido:
                status = "⚠️  Coloração inválida"
            elif num_cores <= 1 and any(len(a) > 0 for a in adj):
                status = "⚠️  Cores insuficientes"
            else:
                status = "✅ Válida"

            print(f"      ▶ {nome_alg:<20} | Cores: {num_cores:<2} | Tempo: {tempo:>7.4f}s | {status}")

            # Exibe as cores se o grafo for pequeno
            if len(grafo.vertices) <= 10:
                cores_fmt = ', '.join(f"v{v}:{c}" for v, c in enumerate(coloracao))
                print(f"        └─ Cores por vértice: {cores_fmt}" + "\n")

    # ========================================================
    # Testes de Árvores Geradoras Mínimas
    # ========================================================

    print("\n" + "="*70)
    print("🌳 TESTES DE ÁRVORE GERADORA MÍNIMA (AGM)")
    print("="*70)

    gnames = [
        "grafo_ponderado_Ponderado_NDirecionado.txt",
        "grafo_direcionado_Ponderado_Direcionado.txt",
        "grafo_simples_NPonderadoNDirecionado.txt",
        "slides.txt",
        "slides_modificado.txt",
        "500vertices50%Arestas.txt",
        "500vertices100%Arestas.txt",
        "1000vertices25%Arestas.txt"
    ]

    for fname in gnames:
        g = ler_arquivo(fname, representacao="lista")
        if g is None:
            print(f"\n❌ Não foi possível carregar {fname}")
            continue

        print(f"Arquivo: {fname}")
        print("   ├─ Executando Prim e Kruskal...")
        print("   └──────────────────────────────────────────────")

        t0 = time.time()
        mst1, s1 = prim(g)
        t1 = time.time()
        tempo_prim = t1 - t0

        t0 = time.time()
        mst2, s2 = kruskal(g)
        t1 = time.time()
        tempo_kruskal = t1 - t0

        print(f"      🌲 Prim:     {len(mst1):>3} arestas | Peso total: {s1:>8.2f} | Tempo: {tempo_prim:>7.4f}s")
        print(f"      🌿 Kruskal:  {len(mst2):>3} arestas | Peso total: {s2:>8.2f} | Tempo: {tempo_kruskal:>7.4f}s" + "\n")

    print("\n" + "="*70)
    print("✅ Fim dos testes.")
    print("="*70)
