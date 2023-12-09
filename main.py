import time
import numpy as np
import networkx as nx
import random
from algorithms import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sims = 10 # シミュレーション数
    node_size_min = 10 # ノードの大きさ
    node_size_max = 500
    node_diff = 10 # 刻み
    path_p = 0.3 # パスができる確率

    # 実行時間をためておく配列
    prim_list = np.zeros((sims, int(node_size_max / node_size_min)))
    kruskal_list = np.zeros((sims, int(node_size_max / node_size_min)))
    boruvka_list = np.zeros((sims, int(node_size_max / node_size_min)))

    for sim in range(sims):
        print(str(sim)+"回目のシミュレーション")
        start_sim = time.time() 

        for node_size in range(node_size_min, node_size_max+1, node_diff):
            # print(node_size)
            
            
            # ランダムツリーを生成
            g = nx.random_graphs.fast_gnp_random_graph(node_size, path_p, sim, directed = True)
            g = g.to_undirected()
            path_num = len(list(g.edges)) # パスの数を取得
            # 0以上1未満の実数を重複なしで生成
            random.seed(sim)
            ws = random.sample([random.random() for _ in range(1000000)], path_num)
            wi = 0
            # print(ws)
            # 重みをツリーに追加
            for edge in g.edges():
                g.edges[edge]['w'] = ws[wi]
                wi += 1

            # 入力に合う形にする
            graph = [[] for _ in range(node_size)] # 入力用グラフ
            for fr, to, w in g.edges(data=True):
                # print(fr, to, w['w'])
                graph[fr].append((to, w['w']))
                graph[to].append((fr, w['w']))

            # print(graph)

            # print("prim")
            start = time.time() 
            prim(node_size, path_num, graph)
            end = time.time()
            t = end - start
            prim_list[sim][int(node_size/node_size_min)-1] = t

            # print("kruskal")
            start = time.time() 
            kruskal(node_size, path_num, graph)
            end = time.time()
            t = end - start
            kruskal_list[sim][int(node_size/node_size_min)-1] = t

            # print("boruvka")
            start = time.time() 
            boruvka(node_size, path_num, graph)
            end = time.time()
            t = end - start
            boruvka_list[sim][int(node_size/node_size_min)-1] = t

        end_sim = time.time()
        sim_time = end_sim - start_sim
        print(sim_time)     

    prim_mean = np.mean(prim_list, axis=0)
    kruskal_mean = np.mean(kruskal_list, axis=0)
    boruvka_mean = np.mean(boruvka_list, axis=0)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xlabel("nodes", size=18, weight="light")
    ax.set_ylabel("time", size=18, weight="light")
    # plt.ylim(0, 0.8)

    x = np.arange(node_size_min, node_size_max+1, node_diff)
    ax.plot(x,prim_mean, label='prim')
    ax.plot(x,kruskal_mean, label='kruskal')
    ax.plot(x,boruvka_mean, label='boruvka')

    ax.legend()

    plt.savefig("result.png")
    plt.show()