import PIL
from PIL import Image
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk
from collections import defaultdict
from heapq import *
import networkx as nx
import random

global img, imagebox, start_selector, end_selector, var1, var2, pos, edgelist, iterator, delay_entry

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen, mins = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path += (v1,)
            if v1 == t: return cost, path

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None


def generate_graph(n, p):
    global edgelist
    G = nx.gnp_random_graph(n, p, directed=True)
    edgelist = []

    # gives all nodes weights
    for i in G.edges:
        G[i[0]][i[1]]["weight"] = 1 + random.randint(0, 20)
        edgelist.append((i[0], i[1], G[i[0]][i[1]]["weight"]))

    print("Generated graph of size", n)
    print("All edges and their weights (node1, node2, weight):")
    for i in edgelist:
        print(i[0], "to", i[1], "weight:", i[2])

    return G


def draw(G, new_positions=True):
    global img, start_selector, end_selector, var1, var2, pos
    if new_positions:
        pos = nx.spring_layout(G)
    plt.clf()

    # plot draws here
    nx.draw(G, pos, node_color='lightblue', with_labels=True, node_size=500)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))

    # update option menus
    update_menu(start_selector, G.nodes, var1)
    update_menu(end_selector, G.nodes, var2)
    refresh_image()


def highlight(G, nodes, edges, highlight_edges=True, highlight_nodes=True):
    global pos
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color='r')
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r')
    refresh_image()


def step_by_step(G, edges):
    global iterator
    highlight(G, (edges[iterator][0], edges[iterator][1]), [edges[iterator]])
    iterator = iterator + 1


def draw_path(G, start, end, canvas):
    global edgelist, pos, iterator, delay_entry
    if not start.isdigit() or not end.isdigit():
        print("Invalid input(s)")
        return False
    draw(G, new_positions=False)  # empty the canvas first, keep positions
    if not start.isdigit() and not end.isdigit():
        start = 0
        end = 0

    dijkstra_out = dijkstra(edgelist, int(start), int(end))
    if dijkstra_out[1] is None:
        print("No available path from", start, "to", end)
    elif int(start) == int(end):
        print("No movement from", start, "to", end, "since they are the same node")
        highlight(G, (int(start), int(end)), None, highlight_edges=False)
    else:
        node_path = dijkstra_out[1]
        edge_path = list(zip(node_path, node_path[1:]))
        iterator = 0
        print("Edges for the shortest path:")
        print(edge_path)
        for i in range(0, len(edge_path)):
            canvas.after(int(delay_entry.get()) + i * int(delay_entry.get()), step_by_step, G, edge_path)


def refresh_image():
    global img, imagebox
    img = plt.gcf()
    plt.savefig("step.png")
    plotimage = Image.open("step.png")
    plotimage.thumbnail((300, 400), PIL.Image.ANTIALIAS)
    img = ImageTk.PhotoImage(plotimage)
    imagebox.config(image=img)
    imagebox.image = img


def callbackn(N):
    if (str.isdigit(N) and 0 < int(N) < 20) or N == "":
        return True
    else:
        return False


def callbackp(P):
    if (str.isdigit(P) and 0 <= int(P) <= 100) or P == "":
        return True
    else:
        return False


def callbacks(S):
    if (str.isdigit(S) and 0 <= int(S) <= 10000) or S == "":
        return True
    else:
        return False


def zoom():
    plt.imread('step.png')
    plt.show()


def update_menu(option_menu, new_list, var):
    m = option_menu.children['menu']
    m.delete(0, tk.END)
    for val in new_list:
        m.add_command(label=val, command=lambda v=var, l=val: v.set(l))
    var.set(new_list[0])


root = tk.Tk()
root.title("Graph path gen")

#                   #
#   USER FRAME      #
#                   #
userframe = tk.Frame(root)

#                   #
#   LAUNCH FRAME    #
#                   #
launchframe = tk.Frame(userframe)

#                  #
#   INPUT FRAME    #
#                  #
main_frame = tk.Frame(launchframe)
vcmd = main_frame.register(callbackn)
vcmdp = main_frame.register(callbackp)
vcmds = main_frame.register(callbacks)

# Node count input is limited between 0 and 20
# use the commented line for n_input_box to ignore this
n_label = tk.Label(main_frame, text="Node count (0<N<20):")
n_input_box = tk.Entry(main_frame, text="", validate='all', validatecommand=(vcmd, '%P'), width=5, justify="left")
# n_input_box = tk.Entry(main_frame, text="", width=5, justify="left")
n_input_box.insert(0, "5")
p_label = tk.Label(main_frame, text="Edge probability (%):")
p_input_box = tk.Entry(main_frame, text="", validate='all', validatecommand=(vcmdp, '%P'), width=5)
p_input_box.insert(0, "50")

generate_button = tk.Button(main_frame, text="Generate graph",
                            command=lambda: draw(
                                generate_graph(int(n_input_box.get()), float(int(p_input_box.get()) / 100))))
err_msg = tk.Label(main_frame, text="")

n_label.grid(row=1, column=0)
n_input_box.grid(row=1, column=1)
p_label.grid(row=2, column=0)
p_input_box.grid(row=2, column=1)
generate_button.grid(row=3, column=1)
err_msg.grid(row=4, column=0)

main_frame.grid(row=1, columnspan=2)

start_node_in = tk.IntVar(launchframe)
start_node_in.set("1")

end_node_in = tk.IntVar(launchframe)
end_node_in.set("2")

lisst = [0]
var1 = tk.StringVar()
var1.set(lisst[0])
start_selector = tk.OptionMenu(launchframe, var1, *lisst)

lisst2 = [0]
var2 = tk.StringVar()
var2.set(lisst[0])
end_selector = tk.OptionMenu(launchframe, var2, *lisst2)

tk.Label(launchframe, text="Starting node:").grid(row=2, column=0)
tk.Label(launchframe, text="Ending node:").grid(row=2, column=1)
start_selector.grid(row=3, column=0)
end_selector.grid(row=3, column=1)
buttonframe = tk.Frame(userframe)
launchframe.pack()
tk.Label(buttonframe, text="Step delay in milliseconds\n(delay between path highlighting)").pack()
delay_entry = tk.Entry(buttonframe, text="", validate='all', validatecommand=(vcmds, '%P'), width=5, justify="left")
delay_entry.insert(0, "1000")
delay_entry.pack()
find_path_button = tk.Button(buttonframe, text="Find shortest path",
                             command=lambda: draw_path(G, var1.get(), var2.get(), imgframe)).pack()
buttonframe.pack()

#                   #
#   IMAGE FRAME     #
#                   #

# Initially, create a random graph for visualisation
# and draw the image
G = generate_graph(10, 0.5)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='lightblue', with_labels=True, node_size=500)
plt.savefig("step.png")
plotimage = Image.open("step.png")
img = ImageTk.PhotoImage(plotimage)
imgframe = tk.Frame(root, width=400, height=300)
imagebox = tk.Label(imgframe)
draw(G)
imagebox.image = img  # keep img as reference to avoid a certain bug

imagebox.pack(expand=1)
tk.Button(imgframe, text="Click to zoom in", command=lambda: zoom()).pack()
imgframe.pack_propagate(False)

imgframe.grid(row=0, column=0)
userframe.grid(row=0, column=1)
root.mainloop()
