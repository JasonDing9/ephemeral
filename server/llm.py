import together
import os
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

def parse_correction(correction):
    return f"{correction} Can you please fix it?"

def parse_diagram(diagram, caption, topic, load=None):
    lines = diagram.split('\n')
    lines = [x.strip() for x in lines]

    layout = ""
    entity_bounds = { }
    entity_relatonships = [ ]

    if load is not None:
        layout = load["layout"]
        entity_bounds = load["entity_bounds"]
        entity_relatonships = load["entity_relationships"]

    entity_index = -100000
    relationship_index = -100000
    location_index = -100000

    save_values = []
    
    for i, line in enumerate(lines):
        if line.startswith("Diagram Layout:"):
            layout = lines[i+1]
        if line.startswith("Required Entities:"):
            entity_index = i
        if line.startswith("Entity Relationships:"):
            relationship_index = i
            save_values.append("entity_bounds")
        if line.startswith("Entity Locations"):
            location_index = i
            save_values.append("entity_relationships")

    if entity_index > -1:
        x = relationship_index

        if x < 0:
            x = location_index

            if x < 0:
                x = len(lines)

        for line in lines[entity_index+1:x]:
            if len(line.strip()) == 0:
                continue

            if "image" in line:
                words = line.split(" image ")

                id = line.split("(")[1]
                value = words[0]
                type = "image"
                
            elif "text" in line:
                words = line.split(" text label ")

                id = line.split("(")[1]
                value = words[0].replace("\"", "")
                type = "text"

            id = id.replace("(", "").replace(")", "")
            entity_bounds[id] = {
                "id": id,
                "type": type,
                "value": value,
                "bounds": []
            }
    
    if relationship_index > -1:
        x = location_index

        if x < 0:
            x = len(lines)

        for line in lines[relationship_index+1:x]:
            ids = line.split(" ")

            passed = len(line.strip()) > 0
            count = 0
            for i, word in enumerate(ids):
                if word.startswith("T") or word.startswith("I"):
                    if not (word in entity_bounds):
                        passed = False
                        break
                    count += 1

            if count < 2:
                passed = False

            if not passed:
                print("Failed to parse relationship: ", line)
                continue
            entity_relatonships.append(line)

    if location_index > -1:
        for line in lines[location_index+1:]:
            words = line.split(" is located at ")

            try:
                id = words[0]
                words[1] = words[1][:words[1].index("]")]
                value = words[1].replace("[", "").replace("]", "").replace(", ", ",")
            except:
                print("Failed to parse location: ", line)
                continue

            if not (id in entity_bounds):
                print("Failed to parse location: ", line)
                continue

            bounds = value.split(",")
            bounds = [int(x.strip()) for x in bounds]

            entity_bounds[id]["bounds"] = bounds

        bad_ids = []
        for id in entity_bounds:
            if len(entity_bounds[id]["bounds"]) == 0:
                bad_ids.append(id)

        for id in bad_ids:
            del entity_bounds[id]

    r = {
        "caption": caption,
        "topic": topic,
        "layout": layout,
        "entity_bounds": entity_bounds,
        "entity_relationships": list(set(entity_relatonships))
    }

    return r

DIAGRAM_PROMPT_engineering = """Given a caption of a diagram and topic, generate the diagram layout, and then a list of required entities that would be needed to create the described diagram. Then generate a list of the relationships between the entities (i.e. which ones are connected or labeling each other). Finally, generate the location of each entity.
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
"""

AUDITOR_PROMPT_engineering = """Given a caption and a layout of a diagram, you should determine if something is wrong in the diagram based on the caption. You should explain your answer. Think step-by-step as to why the diagram is correct or not.
The diagram will be described in terms of entities in the diagram, the relationships between the entities, and the location of each entity.
An entity can be an image or text. Entity locations will be in [x, y, width, height] format, where 0,0 is the top left corner and 100,100 is max image size.

Here are some rules the diagrams should follow:
All numbers should be positive, no negative numbers.
Entities should not be outside the bounds [0, 0, 100, 100].
The x coordinate + the width of an entity should not exceed 100.
The y coordinate + the height of an entity should not exceed 100.
Entities of the same type should not overlap.

Here are some examples:
Caption:
A diagram showing a simple electrical circuit schematic with a battery, a switch, and two light bulbs.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery schematic image (I0)
light bulb schematic image (I1)
light bulb schematic image (I2)
"simple electrical circuit" text label (T0)
Entity Relationships:
I2 connects to I0
I1 connects to I2
I0 connects to I1
T0 labels I0
Entity Locations:
I0 is located at [10, 40, 20, 20]
I1 is located at [40, 10, 20, 20]
I2 is located at [70, 40, 20, 20]
T0 is located at [10, 70, 80, 10]
What is wrong with this diagram?
The switch is missing from the circuit in this diagram.

Caption:
A diagram showing the cross-section of a cable with different components, including rubber insulator and copper conductor.
Topic:
engineering
Diagram Layout:
abstract
Required Entities:
cross-section of cable image (I0)
rubber insulator image (I1)
copper conductor image (I2)
"rubber insulator" text label (T0)
"copper conductor" text label (T1)
Entity Relationships:
T1 labels I2
T0 labels I1
Entity Locations:
I0 is located at [0, 0, 100, 100]
I1 is located at [20, 40, 20, 20]
I2 is located at [60, 40, 20, 20]
T0 is located at [20, 65, 20, 10]
T1 is located at [60, 65, 25, 10]
What is wrong with this diagram?
The copper conductor should be inside of the rubber insulator. The rubber insulator should be a bit bigger.

Caption:
A diagram showing a simple electronic circuit schematic with a battery and a resistor.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery schematic image (I0)
resistor schematic image (I1)
"battery" text label (T0)
"resistor" text label (T1)
Entity Relationships:
T1 labels I1
I0 connects to I1
T0 labels I0
Entity Locations:
I0 is located at [10, 40, 20, 20]
I1 is located at [60, 40, 20, 20]
T0 is located at [10, 65, 20, 10]
T1 is located at [60, 65, 20, 10]
What is wrong with this diagram?
There should a connection from I1 to I0 as well.

Caption:
A diagram showing a circuit with two light bulbs and a battery connect in parallel. There is also a schematic diagram of the circuit.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
light bulb image (I0)
light bulb image (I1)
battery image (I2)
circuit schematic image (I3)
Entity Relationships:
I2 connects to I0
I0 connects to I2
I1 connects to I2
I2 connects to I1
Entity Locations:
I0 is located at [10, 20, 20, 30]
I1 is located at [10, 60, 20, 30]
I2 is located at [40, 40, 20, 20]
I3 is located at [70, 40, 20, 20]
What is wrong with this diagram?
The light bulbs should also be connected to each other. The image of a circuit schematic should actually have 3 entities that have the same connections as the actual circuit.

Caption:
A diagram showing a simple circuit schematic with a battery, light bulb, and a switch all connected in series.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
battery image (I0)
light bulb image (I1)
switch image (I2)
"simple circuit schematic" text label (T0)
Entity Relationships:
I2 connects to I0
I1 connects to I2
I0 connects to I1
Entity Locations:
I0 is located at [10, 40, 20, 20]
I1 is located at [40, 40, 20, 20]
I2 is located at [70, 40, 20, 20]
T0 is located at [10, 10, 80, 10]
What is wrong with this diagram?
The components of the circuit should form a loop rather than straight line.

Caption:
A diagram showing a simple circuit with two light bulbs and a battery. The light bulbs are connected parallel with the battery.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
light bulb image (I0)
light bulb image (I1)
battery image (I2)
Entity Relationships:
I0 connects to I2
I1 connects to I2
Entity Locations:
I0 is located at [10, 30, 20, 30]
I1 is located at [70, 30, 20, 30]
I2 is located at [40, 50, 20, 30]
What is wrong with this diagram?
The battery should connect to both light bulbs and the light bulbs should connect to each other.

Caption:
A diagram showing two circuits. The first is a open circuit with a light bulb connected to battery but the battery doesn't have a connection to the light bulb. The second is a closed circuit with a light bulb connected to a battery and the battery returns the connection.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
light bulb image (I0)
battery image (I1)
light bulb image (I2)
battery image (I3)
"open circuit" text label (T0)
"closed circuit" text label (T1)
Entity Relationships:
I2 connects to I3
I1 connects to I0
I3 connects to I2
Entity Locations:
I0 is located at [10, 20, 15, 25]
I1 is located at [10, 60, 15, 25]
I2 is located at [60, 20, 15, 25]
I3 is located at [60, 60, 15, 25]
T0 is located at [30, 30, 20, 10]
T1 is located at [80, 70, 20, 10]
What is wrong with this diagram?
The open and closed circuit text labels should be above each circuit, not besides them.

Caption:
A diagram showing a electrical circuit schematic. It has a 12V battery connected to a 1k resistor, a light bulb, and another 1k resistor.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
"12v" text label (T0)
"1k" text label (T1)
"1k" text label (T2)
battery schematic image (I0)
resistor schematic image (I1)
light bulb schematic image (I2)
resistor schematic image (I3)
Entity Relationships:
I3 connects to I0
I1 connects to I2
I2 connects to I3
T1 labels I1
I0 connects to I1
T0 labels I0
T2 labels I3
Entity Locations:
T0 is located at [2, 40, 8, 7]
T1 is located at [20, 10, 8, 7]
T2 is located at [80, 10, 8, 7]
I0 is located at [10, 50, 15, 10]
I1 is located at [30, 20, 10, 10]
I2 is located at [50, 50, 10, 10]
I3 is located at [70, 20, 10, 10]
What is wrong with this diagram?
The light bulb schematic and the resistor schematic should swap places to make the diagram flow smoother.

Caption:
A diagram showing the structure of an electric circuit with a light bulb, a switch, and a battery.
Topic:
engineering
Diagram Layout:
circular
Required Entities:
light bulb image (I0)
battery image (I1)
"electric circuit" text label (T0)
Entity Relationships:
T0 labels I0 and I1
I0 connects to I1
I1 connects to I0
Entity Locations:
I0 is located at [10, 30, 20, 40]
I1 is located at [70, 30, 20, 40]
T0 is located at [40, 50, 20, 10]
What is wrong with this diagram?
The switch is missing from the circuit in this diagram.
"""

diagram_prompt = f"{DIAGRAM_PROMPT_engineering}\nCaption:\nA diagram showing a client creates audio, and then the audio is  sent to a LLM. The LLM also gets data fromthe corpus using a RAG. Then the LLM decides an action to take, and then the agent will automatically do the action.\nTopic:\nengineering\n"

output = together.Complete.create(
  prompt = f"[INST] {diagram_prompt} [/INST]", 
  model = "codellama/CodeLlama-34b-Instruct-hf", 
  max_tokens = 10000,
  temperature = 0.7,
  top_k = 50,
  top_p = 0.7,
  repetition_penalty = 1,
  stop = ["[INST]"],
  safety_model = "",
)

# print generated text
print(output['output']['choices'][0]['text'])