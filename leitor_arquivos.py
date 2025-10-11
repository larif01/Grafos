# leitor_arquivos.py
from grafo_matriz import GrafoMatriz
from grafo_lista import GrafoLista

def ler_arquivo(caminho: str, representacao: str = "lista"):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas_brutas = f.readlines()
    except FileNotFoundError:
        print(f"❌ Arquivo {caminho} não encontrado!")
        return None
    except Exception as e:
        print(f"❌ Erro ao abrir {caminho}: {e}")
        return None

    linhas = []
    for l in linhas_brutas:
        l = l.strip()
        if not l or l.startswith("#") or l.startswith("//"):
            continue
        linhas.append(l)

    if not linhas:
        print(f"⚠️ Arquivo {caminho} está vazio (após filtrar comentários).")
        return None

    header = linhas[0].split()
    if len(header) < 4:
        print(f"❌ Formato do header inválido em {caminho}: {linhas[0]!r}")
        return None

    try:
        V, A, D, P = map(int, header[:4])
    except ValueError:
        print(f"❌ Header não numérico em {caminho}: {linhas[0]!r}")
        return None

    grafo = GrafoMatriz(bool(D), bool(P)) if representacao.lower()=="matriz" else GrafoLista(bool(D), bool(P))
    for i in range(V):
        grafo.inserir_vertice(str(i))

    arestas_raw = []
    for linha in linhas[:]:
        partes = linha.split()
        if len(partes) < 2:
            continue
        try:
            u, v = int(partes[0]), int(partes[1])
        except ValueError:
            continue
        peso = 1.0
        if P == 1 and len(partes) >= 3:
            try:
                peso = float(partes[2])
            except ValueError:
                peso = 1.0
        arestas_raw.append((u, v, peso))

    if not arestas_raw:
        print(f"⚠️ Arquivo {caminho} não contém arestas válidas.")
        return grafo

    todos_idx = [x for (u, v, _) in arestas_raw for x in (u, v)]
    contem_zero = any(idx == 0 for idx in todos_idx)
    contem_V = any(idx == V for idx in todos_idx)
    one_based = (not contem_zero) and contem_V

    if one_based:
        arestas = [(u-1, v-1, w) for (u, v, w) in arestas_raw]
        print(f"ℹ️ {caminho}: índices 1-based detectados → normalizado para 0-based.")
    else:
        arestas = arestas_raw

    rejeitadas = 0
    inseridas = 0
    for (u, v, w) in arestas:
        if u < 0 or v < 0 or u >= V or v >= V:
            rejeitadas += 1
            continue
        if grafo.inserir_aresta(u, v, w):
            inseridas += 1
        else:
            rejeitadas += 1

    print(f"ℹ️ {caminho}: vértices={V}, arestas_lidas={len(arestas_raw)}, arestas_inseridas={inseridas}, rejeitadas={rejeitadas}")
    return grafo
