# Algorithm-Analysis-Project2
# Description

This is a project used to analyse Dijkstra's algorithm.

gui.py is the main user friendly interface, it doesn't depend on the other scripts present in this repository.

## draw_test.py
You can play around draw_test.py to generate random graphs with given size and edge creation probability by changing these variables at top
```python
NODE_COUNT = 100
EDGE_PROBABILITY = 0.2
```

## Remove 20 nodes limit on GUI

To remove the 20 nodes limit on the GUI, convert this part of the code in gui.py at line 181 from

```python
n_input_box = tk.Entry(main_frame, text="", validate='all', validatecommand=(vcmd, '%P'), width=5, justify="left")
# n_input_box = tk.Entry(main_frame, text="", width=5, justify="left")
```

to

```python
#n_input_box = tk.Entry(main_frame, text="", validate='all', validatecommand=(vcmd, '%P'), width=5, justify="left")
n_input_box = tk.Entry(main_frame, text="", width=5, justify="left")
```

## Extra
benchmark.py is used to test the average running time of algorithm with different node counts.
