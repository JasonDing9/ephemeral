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
"""
output = together.Complete.create(
  prompt = f"[INST] {prompt} [/INST]", 
  model = "codellama/CodeLlama-34b-Instruct-hf", 
  max_tokens = 13500,
  temperature = 0.7,
  top_k = 50,
  top_p = 0.7,
  repetition_penalty = 1,
  stop = ["[INST]"],
  safety_model = "",
)

# print generated text
print(output['output']['choices'][0]['text'])