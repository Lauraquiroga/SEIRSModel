# SEIRS-NIMFA Model for Infectious Disease Dynamics


This project is a Python implementation for a SEIRS-NIMFA compartmental epideiologic model that describes the evolution of a malware infection in an IoT network. This is an individual-based model that is described by the following flow diagram:

![image](https://github.com/Lauraquiroga/SEIRSModel/assets/60222757/9ee43e87-6c97-4d49-8347-b7c2caed4a1e)   
The SEIRS-NIMFA flow diagram for a device i

Here x<sub>i</sub>(t), w<sub>i</sub>(t), y<sub>i</sub>(t), and z<sub>i</sub>(t) represent the probability of the device i being at each of the compartments, S, E, I, R, repectively, at time t, and b<sub>i</sub>(t), α<sub>i</sub>, σ<sub>i</sub>, and ɣ<sub>i</sub> represent the transition rates between the compartments for each of the devices (although these are homogeneous for all the network in the implementation). 

## Folder Structure

├── SEIRSModel/ # Root directory    
│ ├── assets/ # Folder containing images, diagrams, or other assets   
│ ├── data/ # Folder containing sample initial configurations     
│ │ ├── results/ # Folder where results of the simulation are dynamically saved     
│ ├── interface/ # Folder containing Python files for the GUI     
│ ├── model/ # Folder containing Python files for the logic of the simulation     
│ │ ├── network.py # Network class: IoT device network construction     
│ │ ├── seirs_model.py # NIMFA SEIRS model for a homogeneous network with constant parameters     
│ │ └── states.py # Enumeration for the states definition     
│ ├── .gitignore # Gitignore file     
│ ├── README.md # Project README file     
│ └── requirements.txt # Dependencies specification file  

## Running the Project

Follow these steps to run the SEIRSModel project:
1. **Clone the project**
   ```bash
   git clone https://github.com/Lauraquiroga/SEIRSModel.git
   cd SEIRSModel
   ```
2. **Install Dependencies**    
   ```bash
   pip install -r requirements.txt
   ```
   Ensure that you have Python installed on your system.    
3. **Configure**
   
   Modify or add initial configuration files for your scenarios. These might be found in the data folder.
   
4. **Run the GUI**
   ```bash
   python interface_seirs.py     
   ```
   Follow the steps indicated in the GUI according to your requirements.
     
5. **View Results**

   Visualize and save the graphs of the results through the GUI if needed.    
   Explore the results in the data/results folder. The simulation dynamically saves output files there.
