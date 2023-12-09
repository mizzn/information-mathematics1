import sys
import heapq
from union_find import UnionFind
from collections import deque
INF = sys.maxsize

def prim(n, p, graph):
    ans = 0 # 重みの合計
    expanded = [False for i in range(n)] # ノードiが展開済みのときexpanded[i]はTrue
    
    expanded[0] = True # 0から出発
    que = [(w, to) for to, w in graph[0]] # 重み順にしたいから逆にする
    heapq.heapify(que)
    # print(que)

    while que: # queが空になるまで
        w, to = heapq.heappop(que) # 最小の重みと行き先を持ってくる

        # 取り出した行き先が展開済みだったら無視
        if expanded[to] == True:
            continue

        # 取り出した行き先が展開済みではないとき，行き先を展開済みにして重みを足す
        expanded[to] = True
        ans += w

        fr = to # 行き先を出発地にする
        for to, w in graph[fr]:
            heapq.heappush(que, (w, to)) # 次の行き先と重みを全部ヒープに入れる
            
    return ans

def kruskal(n, p, graph):
    ans = 0 
    unionfind = UnionFind(n)

    # パスを重み順にする
    paths = []
    for fr in range(n):
        for to, w in graph[fr]:
            paths.append((w, fr, to))
    paths.sort()
    # print(paths)
    # exit()

    for w, fr, to in paths:
        # ソートしたので小さい順に取り出される
        if unionfind.same(fr, to):
            # frとtoが繋がっているときは無視
            continue
        else:
            # frとtoが繋がっていないときは繋げて重みを足す
            unionfind.union(fr, to)
            ans += w

    return ans

def boruvka(n, p, graph):
    ans = 0
    unionfind = UnionFind(n)
    mins =[INF]*n # 連結成分の最小の辺を入れる

    num = n # 連結成分の数，最初はすべてのノードの数
    # debug = 0

    while num > 1: #連結成分が1のとき終了
        # debug += 1
        # print("path")
        # すべてのパスに対して
        for fr in range(n):
            for to, w in graph[fr]:
                # print(fr, to, w)
                # 連結成分の根
                fr_root = unionfind.find(fr) 
                to_root = unionfind.find(to)
                # print("根", fr_root, to_root)

                if fr_root != to_root: # 違うグループにいるとき
                    # 根それぞれについて
                    # 初期値もしくは今回の重みのほうが小さかったら更新
                    if mins[fr_root] == INF or mins[fr_root][2] > w: 
                        mins[fr_root] = [fr, to, w]

                    if mins[to_root] == INF or mins[to_root][2] > w:
                        mins[to_root] = [fr, to, w]

                    # print("mins[fr_root] = ", mins[fr_root])
                    # print("mins[to_root] = ", mins[to_root])

        # print("mins = ", mins)
        
        # print("node")
        # すべてのノードに対して
        for node in range(n):
            if mins[node] != INF: # 更新されていたら
                fr, to , w = mins[node]
                # print(fr, to, w)
                # 連結成分の根を取り出し
                fr_root = unionfind.find(fr) 
                to_root = unionfind.find(to)
                # print("根", fr_root, to_root)

                if fr_root != to_root:
                    # 違うグループのときは繋げて重みを足す
                    unionfind.union(fr_root, to_root)
                    ans += w
                    num -= 1
                    # print("fr_rootとto_rootを繋げる")
                    # print("ans = ", ans)
                    # print("num = ",num)

        # print("ans = ", ans)
        # print("num = ",num)
        
        mins =[INF]*n
        # if debug ==2:
        #     exit(1)

    return ans

# testmain
if __name__ == "__main__":
    # 入力を受け取ってグラフを作る
    INF = sys.maxsize
    n, p = map(int, input().split()) # n個のノード，p個のパス

    #　隣接グラフを作る
    graph = [[] for _ in range(n)]
    for _ in range(p):
        i, c, w = map(int, input().split())
        graph[i].append((c, w))
        graph[c].append((i, w)) # 無向グラフだから必要

    # print(graph)

    print(prim(n, p, graph))
    print(kruskal(n, p, graph))
    print(boruvka(n, p, graph))

    



"""test gragh
5 7
0 1 10
0 4 30
1 2 10
1 4 20
2 3 30
4 2 20
4 3 10
"""