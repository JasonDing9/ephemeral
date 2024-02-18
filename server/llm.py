import together
import os
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

prompt = """Given a caption of a diagram and topic, generate the diagram layout, and then a list of required entities that would be needed to create the described diagram. Then generate a list of the relationships between the entities (i.e. which ones are connected or labeling each other). Finally, generate the location of each entity.
An entity can be an image or text. Entity locations should be generated in [x, y, width, height] format, where 0,0 is the top left corner and 100,100 is max image size.

Think step-by-step, break each caption into parts and generate the required entities, relationships, and locations for each part.

Here are some rules to follow:
All numbers should be positive, do not generate negative numbers.
Please always generate a list of entities, even if the list is empty.
Entities should not be outside the bounds [0, 0, 100, 100].
The x coordinate + the width of an entity should not exceed 100.
The y coordinate + the height of an entity should not exceed 100.
Entities of the same type should not overlap.

Here are some examples:

Caption:
A diagram showing two simple circuits with a battery and three lights. One circuit has a switch to control the flow of electricity. Both circuits are connects in series.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery image (I0)
"battery" text label (T0)
"switch" text label (T1)
switch image (I1)
light bulb image (I2)
light bulb image (I3)
light bulb image (I4)
battery image (I5)
light bulb image (I6)
light bulb image (I7)
light bulb image (I8)
Entity Relationships:
I6 connects to I7
T1 labels I1
I0 connects to I1
I3 connects to I4
I5 connects to I6
I7 connects to I8
I8 connects to I5
I4 connects to I0
I2 connects to I3
T0 labels I0
I1 connects to I2
Entity Locations:
I0 is located at [0, 62, 7, 20]
T0 is located at [10, 69, 11, 7]
T1 is located at [10, 9, 10, 6]
I1 is located at [9, 17, 16, 14]
I2 is located at [27, 3, 14, 27]
I3 is located at [27, 35, 15, 26]
I4 is located at [26, 65, 15, 27]
I5 is located at [58, 33, 9, 28]
I6 is located at [73, 7, 7, 20]
I7 is located at [88, 43, 10, 12]
I8 is located at [74, 56, 7, 20]

Caption:
A diagram showing two circuits. In both a circuits, there are two light bulbs connected to a battery. The first circuit is in series and the second one is in parallel.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery image (I0)
light bulb image (I1)
light bulb image (I2)
light bulb image (I3)
light bulb image (I4)
battery image (I5)
Entity Relationships:
I4 connects to I5
I0 connects to I1
I4 connects to I3
I3 connects to I4
I5 connects to I4
I1 connects to I2
Entity Locations:
I0 is located at [17, 18, 22, 13]
I1 is located at [13, 46, 13, 27]
I2 is located at [28, 47, 14, 24]
I3 is located at [66, 71, 16, 25]
I4 is located at [68, 30, 14, 26]
I5 is located at [64, 3, 21, 12]

Caption:
A diagram showing a simple electric circuit with a battery, a light bulb, and a switch.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
light bulb image (I0)
battery image (I1)
switch image (I2)
"simple electric circuit" text label (T0)
Entity Relationships:
I1 connects to I2
I0 connects to I1
I2 connects to I0
Entity Locations:
I0 is located at [18, 22, 17, 26]
I1 is located at [30, 74, 40, 12]
I2 is located at [66, 38, 10, 9]
T0 is located at [5, 5, 90, 7]

Caption:
A diagram showing a simple circuit with a battery and three light bulbs. The lights and battery are connected in series.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery image (I0)
light bulb image (I1)
light bulb image (I2)
light bulb image (I3)
Entity Relationships:
I1 connects to I2
I2 connects to I3
I0 connects to I1
I3 connects to I0
Entity Locations:
I0 is located at [10, 37, 12, 37]
I1 is located at [44, 61, 14, 29]
I2 is located at [77, 37, 14, 29]
I3 is located at [43, 3, 14, 28]

Caption:
A diagram showing a circuit schematic. The 10V better is connected to a 1 ohm resistor directly. Then the 1 ohm resistor is connected to a 25 ohm resistor and 30 ohm resistor in parallel. Those resistors are connected to a 50 ohm and 55 ohm resistor respectively. Then the parallel circuit comes back together and connects to the battery. Both sides of the parallel circuit are connected via a 1 ohm resistor.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
"10v" text label (T0)
"1 ohm" text label (T1)
"25 ohm" text label (T2)
"50 ohm" text label (T3)
"1 ohm" text label (T4)
"30 ohm" text label (T5)
"55 ohm" text label (T6)
battery schematic image (I0)
resistor schematic image (I1)
resistor schematic image (I2)
resistor schematic image (I3)
resistor schematic image (I4)
resistor schematic image (I5)
resistor schematic image (I6)
Entity Relationships:
T0 labels I0
T2 labels I2
T6 labels I6
T5 labels I5
T1 labels I1
T4 labels I4
T3 labels I3
Entity Locations:
T0 is located at [1, 40, 9, 8]
T1 is located at [26, 11, 8, 9]
T2 is located at [53, 26, 9, 8]
T3 is located at [38, 72, 10, 7]
T4 is located at [62, 58, 8, 7]
T5 is located at [90, 27, 9, 8]
T6 is located at [89, 71, 9, 8]
I0 is located at [8, 48, 9, 7]
I1 is located at [25, 2, 12, 9]
I2 is located at [48, 21, 5, 17]
I3 is located at [48, 66, 6, 18]
I4 is located at [62, 46, 12, 9]
I5 is located at [83, 21, 6, 19]
I6 is located at [83, 64, 6, 20]

Caption:
A diagram showing a circuit with a 6V battery being connected to 2 light bulbs on opposite sides and then a switch in between them. The switch then connects to both light bulbs.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery image (I0)
switch image (I1)
light bulb on image (I2)
light bulb off image (I3)
"6v" text label (T0)
Entity Relationships:
T0 labels I0
I2 connects to I1
I0 connects to I1
I3 connects to I1
I0 connects to I2
I0 connects to I3
Entity Locations:
I0 is located at [9, 40, 11, 21]
I1 is located at [30, 37, 66, 26]
I2 is located at [66, 0, 10, 20]
I3 is located at [66, 75, 10, 21]
T0 is located at [12, 35, 6, 5]

Caption:
A diagram showing the components of a slipper spring. It includes a spring hanger, a spring bolt and locknut, a two rebound clips, a slipper, and a centre bolt.
Topic:
engineering
Diagram Layout:
abstract
Required Entities:
spring hanger image (I0)
spring bolt and locknut image (I1)
rebound clip image (I2)
rebound clip image (I3)
slipper image (I4)
"spring hanger" text label (T0)
"spring bolt & locknut" text label (T1)
"rebound clip" text label (T2)
"slipper" text label (T3)
"centre bolt" text label (T4)
centre bolt image (I5)
"eye/slipper spring components" text label (T5)
Entity Relationships:
T0 labels I0
T3 labels I4
T2 labels I2
T4 labels I5
T2 labels I3
T1 labels I1
Entity Locations:
I0 is located at [6, 18, 8, 24]
I1 is located at [7, 29, 4, 11]
I2 is located at [22, 56, 5, 18]
I3 is located at [65, 49, 6, 16]
I4 is located at [81, 17, 16, 16]
T0 is located at [16, 6, 15, 8]
T1 is located at [2, 72, 20, 7]
T2 is located at [75, 77, 13, 8]
T3 is located at [67, 2, 7, 6]
T4 is located at [42, 91, 11, 6]
I5 is located at [45, 64, 3, 15]
T5 is located at [61, 91, 33, 8]

Caption:
A diagram showing a simple electronic circuit with a lamp and a battery.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
lamp image (I0)
battery image (I1)
"lamp" text label (T0)
"battery" text label (T1)
Entity Relationships:
T1 labels I1
I0 connects to I1
I1 connects to I0
T0 labels I0
Entity Locations:
I0 is located at [32, 12, 28, 38]
I1 is located at [27, 65, 31, 22]
T0 is located at [31, 2, 14, 7]
T1 is located at [28, 90, 21, 7]

Caption:
A diagram showing the flow of energy through various processes, including energy conversion, storage, and distribution. Each process is represented as a block. It also shows the sun as an energy source going into the energy conversion, and energy use as a light bulb and electric utility as powerlines coming out of the energy distribution.
Topic:
engineering
Diagram Layout:
tree
Required Entities:
sun image (I0)
metal plate image (I1)
block image (I2)
block image (I3)
light bulb image (I4)
block image (I5)
powerline image (I6)
"energy source" text label (T0)
"energy conversion" text label (T1)
"energy storage" text label (T2)
"energy inversion & conditioning" text label (T3)
"energy use" text label (T4)
"energy distribution" text label (T5)
"electric utility" text label (T6)
Entity Relationships:
I3 has an arrow to I2
T0 labels I0
I6 has an arrow to I5
I2 has an arrow to I3
T2 labels I2
I2 has an arrow to I5
I5 has an arrow to I6
T6 labels I6
I0 has an arrow to I1
I1 has an arrow to I2
T5 labels I5
I5 has an arrow to I4
T1 labels I1
T4 labels I4
T3 labels I3
Entity Locations:
I0 is located at [0, 2, 11, 20]
I1 is located at [9, 38, 20, 17]
I2 is located at [44, 28, 12, 35]
I3 is located at [43, 78, 16, 20]
I4 is located at [70, 2, 12, 20]
I5 is located at [72, 37, 10, 18]
I6 is located at [69, 71, 18, 28]
T0 is located at [1, 26, 10, 11]
T1 is located at [10, 57, 15, 11]
T2 is located at [30, 83, 12, 14]
T3 is located at [43, 11, 16, 18]
T4 is located at [83, 8, 11, 12]
T5 is located at [82, 39, 17, 14]
T6 is located at [87, 78, 10, 15]

Caption:
A diagram showing a battery with a light bulb connected to it.
Topic:
engineering
Diagram Layout:
circular"""
output = together.Complete.create(
  prompt = f"[INST] {prompt} [/INST]", 
  model = "codellama/CodeLlama-7b-Instruct-hf", 
  max_tokens = 12000,
  temperature = 0.7,
  top_k = 50,
  top_p = 0.7,
  repetition_penalty = 1,
  stop = ["[INST]"],
  safety_model = "",
)

# print generated text
print(output['output']['choices'][0]['text'])