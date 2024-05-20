# --------------------------------------------------------------------------
# Load results from file to generate heatmap
# Author: Laura Quiroga
# --------------------------------------------------------------------------


import matplotlib.pyplot as plt
import numpy as np

# Configure plot format (font)
font = {'family': 'Times New Roman', 'size':24}
plt.rc('font', **font)
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14

def show_hm(total_i):
  """
  Plot the evolution of the number of nodes in the infected compartment when varying the outburst source
  Display 10 time steps of the simulation
  """
  plt.figure(figsize=(20,20))
  matrix = np.asarray(total_i, dtype=float)
  # Create the reversed "hot" colormap
  reversed_hot_cmap = plt.cm.hot_r
  im = plt.imshow(matrix, cmap=reversed_hot_cmap, aspect='equal')
  #im = plt.imshow(matrix, cmap='hot', aspect='equal')

  cbar = plt.colorbar()
  cbar.set_label('Number of infected nodes', labelpad=20)
  plt.gca().set_aspect(len(total_i[0])/len(total_i))

  # Draw horizontal lines on the grid
  num_lines = len(total_i)-1 # Number of lines to draw

  for i in range(0, num_lines + 1):
      y = i +0.5
      plt.axhline(y=y, color='black', linewidth=0.1)

  plt.xlabel('Time step', labelpad=20)
  plt.ylabel('Initially infected device', labelpad=20)

  # Set custom ticks for the x-axis
  x_ticks = [x*100 for x in range(11)]  # Custom tick positions
  x_labels = [x for x in range(11)] # Custom tick labels
  plt.xticks(x_ticks, x_labels)

#   plt.title('Evolution of total infected nodes by initially infeted device')
  plt.show()

def show_hm_chosen_its(total_i, x_freq_ticks:int, x_range_ticks:int, from_x:int):
    """
    Plot the evolution of the number of nodes in the infected compartment when varying the outburst source
    Display only relevant time frames
    """
    plt.figure(figsize=(20,20))
    print(np.shape(total_i))
    to_x = from_x+(x_freq_ticks*(x_range_ticks-1))+1
    new_infected = [sliced[from_x:to_x] for sliced in total_i]
    print(np.shape(new_infected))
    results_to_display = new_infected
    matrix = np.asarray(results_to_display, dtype=float)
    # Create the reversed "hot" colormap
    reversed_hot_cmap = plt.cm.hot_r
    im = plt.imshow(matrix, cmap=reversed_hot_cmap, aspect='equal')
    #im = plt.imshow(matrix, cmap='hot', aspect='equal')

    cbar = plt.colorbar()
    cbar.set_label('Number of infected nodes', labelpad=20)
    plt.gca().set_aspect(len(results_to_display[0])/len(results_to_display))

    # Draw horizontal lines on the grid
    num_lines = len(results_to_display)-1 # Number of lines to draw

    for i in range(0, num_lines + 1):
        y = i +0.5
        plt.axhline(y=y, color='black', linewidth=0.1) # Configure line thickness

    plt.xlabel('Time step', labelpad=20)
    plt.ylabel('Initially infected device', labelpad=20)

    # Set custom ticks for the x-axis
    x_ticks = [x*x_freq_ticks for x in range(x_range_ticks)]  # Custom tick positions 
    ticks_per_step = 100/x_freq_ticks
    step_start = from_x/100
    x_labels_start_range = step_start*ticks_per_step
    x_labels = [(x+x_labels_start_range)/ticks_per_step for x in range(x_range_ticks)] # Custom tick labels
    plt.xticks(x_ticks, x_labels)

    # plt.title('Evolution of total infected nodes by initially infeted device')
    plt.show()


def show_hm_chosen_its_nodes(total_i, chosen_nodes, x_freq_ticks:int, x_range_ticks:int, from_x:int):
    """
    Plot the evolution of the number of nodes in the infected compartment when varying the outburst source
    Display only relevant time frames for the critical nodes
    """
    plt.figure(figsize=(20,20))
    print(np.shape(total_i))
    to_x = from_x+(x_freq_ticks*(x_range_ticks-1))+1
    nodes_of_interest = [total_i[node] for node in chosen_nodes]
    new_infected = [sliced[from_x:to_x] for sliced in nodes_of_interest]
    results_to_display = new_infected
    matrix = np.asarray(results_to_display, dtype=float)
    # Create the reversed "hot" colormap
    reversed_hot_cmap = plt.cm.hot_r
    im = plt.imshow(matrix, cmap=reversed_hot_cmap, aspect='equal')
    #im = plt.imshow(matrix, cmap='hot', aspect='equal')

    cbar = plt.colorbar()
    cbar.set_label('Number of infected nodes', labelpad=20)
    plt.gca().set_aspect(len(results_to_display[0])/len(results_to_display))

    # Draw horizontal lines on the grid
    num_lines = len(results_to_display)-1 # Number of lines to draw

    for i in range(0, num_lines + 1):
        y = i +0.5
        plt.axhline(y=y, color='black', linewidth=0.5)

    plt.xlabel('Time step', labelpad=20)
    plt.ylabel('Initially infected device', labelpad=20)

    # Set custom ticks for the y-axis
    y_ticks = [x for x in range(len(chosen_nodes))]
    y_labels = chosen_nodes
    plt.yticks(y_ticks, y_labels)

    # Set custom ticks for the x-axis
    x_ticks = [x*x_freq_ticks for x in range(x_range_ticks)]  # Custom tick positions (entero de (to_x-from_x)/100)
    ticks_per_step = 100/x_freq_ticks
    step_start = from_x/100
    x_labels_start_range = step_start*ticks_per_step
    x_labels = [(x+x_labels_start_range)/ticks_per_step for x in range(x_range_ticks)] # Custom tick labels (enteros de from_x/100, (to_x+1)/100)
    plt.xticks(x_ticks, x_labels)
    # plt.title('Evolution of total infected nodes by initially infeted device')
    plt.show()

def load_results(file_name):
    """
    Load model results from file
    """
    try:
        # Open the file
        with open(file_name, 'r') as file:
            # Read lines from the file
            lines = file.readlines()

            # Remove leading and trailing whitespace from each line
            lines = [line.strip() for line in lines]

            # Remove empty lines and lines containing only brackets
            lines = [line for line in lines if line and not line.isspace() and '[' in line and ']' in line]

            # Convert each line to a list using eval
            arrays = [eval(line) for line in lines]

            # Convert the list of lists to a numpy array
            data = np.concatenate(arrays)
            return data
    except FileNotFoundError as fnf:
        mess = str(fnf).split('] ', 1)[1]
        raise FileNotFoundError(mess)
    except Exception:
        raise Exception(f"Unable to parse the file {file_name}")
  
def load_top(file_name):
    """
    Load top critical nodes from file
    """
    try:
            # Open the file
            with open(file_name, 'r') as file:
                # Read lines from the file
                nodes = []
                for line in file:
                    # Find the index of ":" in the line
                    colon_index = line.find(":")
                    # Slice the line to ignore characters before ":"
                    if colon_index != -1:  # Check if ":" exists in the line
                        processed_line = line[colon_index + 1:].strip()  # Remove leading/trailing whitespace
                        critical_tuples = eval(processed_line) # convert line to a list using eval
                        critical_nodes = [pair[2] for pair in critical_tuples] # take only the critical nodes, exclude the iteration
                        nodes+=critical_nodes
                
                # take unique elements (count each critical node only once)
                nodes = set(nodes)
                top_nodes_ordered = sorted(list(nodes))
                return top_nodes_ordered

    except FileNotFoundError as fnf:
        mess = str(fnf).split('] ', 1)[1]
        raise FileNotFoundError(mess)
    except Exception:
        raise Exception(f"Unable to parse the file {file_name}")

# WLoad results
total_infected_from_file = load_results("Size/TCnResults_N1000_D05_a04_b01_d01_g06.txt")

# Show entire simulation results
show_hm(total_infected_from_file)

# Set up focused graphs
x_freq_ticks = 5 # Number of iterations between one x tick and the next
x_range_ticks = 4 # Number of ticks in the graph
from_x=300 # Starting iteration for display

# Show zoomed window of iterations
show_hm_chosen_its(total_infected_from_file, x_freq_ticks, x_range_ticks, from_x)

# Read top critical nodes from file
critical_nodes = load_top("Size/TCnTop_N1000_D05_a04_b01_d01_g06.txt")
print(f"Critical nodes: {critical_nodes}")
show_hm_chosen_its_nodes(total_infected_from_file, critical_nodes, x_freq_ticks, x_range_ticks, from_x)