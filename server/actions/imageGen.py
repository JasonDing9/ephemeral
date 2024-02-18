import together
import base64
import os
import json
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

def create_summary_image():
    log = open("actions/central-log.txt", "r")
    central_log = "".join(log.readlines())
    
    description_gen_prompt = f"""
Given the following conversation, give a description of a memorable image that summarizes the conversation and a funny and wholehearted caption. For the description of the image, do not include humans or proper nouns, keep it within one or two sentences, and be as descriptive and creative as possible. Please just return a JSON response. Put each possible suggestion in an array, and make sure all arguments in the JSON response is in quotations.
    
Example #1:
Conversation:
Ayushi said: Hey Parth, I was thinking about our upcoming trip to the mountains. Have you checked the weather forecast?
Parth said: Not yet, but I can do that now. Hopefully, it'll be clear skies and perfect hiking weather.
Ayushi said: I hope so too. I can't wait to explore the trails and enjoy the scenic views. Oh, but speaking of hiking, do you think we should bring bear spray, just in case?
Parth said: That's a good point. I've heard there have been bear sightings in the area recently. But then again, I'm not sure if it's necessary since we'll be sticking to well-traveled paths.
Ayushi said: Yeah, you're right. It's probably better to be safe than sorry though. Maybe we should ask someone who's been there recently for their advice.
Parth said: That's a good idea. We could also check online forums or hiking groups for any recent updates on bear activity in the area.
Ayushi said: Definitely. I'll start looking into it tonight. But in the meantime, should we pack the bear spray just in case?
Parth said: Hmm, it's a tough call. Let's think about it some more and decide before we leave.
Ayushi said: Agreed. We don't want to carry unnecessary weight, but we also want to be prepared for any situation. Well, I guess we'll figure it out soon.
Parth said: Yeah, we'll figure it out together. I'm sure it'll be an amazing trip regardless.
Ayushi said: Absolutely. I can't wait!

JSON Response:
{{
    "description": "In a cozy cabin nestled among towering pine trees, a backpack sits by the door, stuffed to the brim with hiking gear and essentials. Through the window, the silhouette of snow-capped mountains can be seen against a vibrant sunset sky, while a signpost nearby points towards various trails disappearing into the wilderness.", 
    "caption": "Packed for adventure, debating bear spray - because nothing says 'bonding experience' like contemplating wildlife encounters with your hiking buddy! 🐻🎒 #MountainAdventures"
}}

Example #2:
Conversation:
Jason said: Hi Arvind, how's it going?
Arvind said: Hey Jason, all good here. How about you?
Jason said: Can't complain. Just trying to keep up with this project. Speaking of which, did you get a chance to look over the latest report?
Arvind said: Yeah, I did. It's looking solid for the most part, but there are a few sections where I think we could use more data.
Jason said: Agreed. I'll reach out to the team and see if we can gather some additional information. By the way, do you know when the next group meeting is scheduled?
Arvind said: Not sure, I haven't seen an update on that. Maybe it's in the calendar, let me check.
Jason said: Alright, let me know what you find. I'm just wondering because I have a conflicting appointment around that time, and I'm not sure if I should prioritize the meeting or reschedule my other commitment.
Arvind said: Hmm, tough call. It depends on how critical our presence is in the meeting. Maybe we can touch base with the project lead and get some clarity on what's expected from us.
Jason said: That sounds like a plan. I'll shoot them an email and see if they can provide some guidance. Thanks, Arvind.
Arvind said: No problem, Jason. Let me know what they say, and we can figure out the best course of action together.
Jason said: Will do. Talk to you soon!
Arvind said: Take care!

JSON Response:
{{
    "description": "A vibrant and bustling office scene with desks filled with papers, computers, and scattered coffee cups. In the center, a calendar hangs on the wall, its pages flipping rapidly as if caught in a whirlwind, while a clock on the wall ticks away, emphasizing the urgency of the conversation.", 
    "caption": "In the chaotic dance of deadlines and meetings, we're just trying to find our rhythm! 🕺💼 #OfficeTango"
}}
    
=======
Conversation:
{central_log}
    """
    
    success = False
    description_json_result = None
    image_description = None
    caption = None
    for i in range(3):
        try:
            output = together.Complete.create(
                prompt = f"[INST] {description_gen_prompt} [/INST]",
                model = "meta-llama/Llama-2-70b-chat-hf", 
                max_tokens = 1500,
                temperature = 0.7,
                top_k = 50,
                top_p = 0.7,
                repetition_penalty = 1,
                stop = ["[INST]"],
                safety_model = "",
            )

            # print generated text
            response = output['output']['choices'][0]['text']
            if response.find("{") == -1 or response.find("}") == -1:
                raise Exception("Sorry, no JSON object to be found")
            description_json_result = response[response.find("{"):response.find("}")+1]
            print(description_json_result)
            
            description_json_result = json.loads(description_json_result)
            image_description = description_json_result["description"]
            caption = description_json_result["caption"]
            success = True
        except:
            print("An error occured. Retrying...")
            pass
        
        if success:
            break
        
    # generate image 
    response = together.Image.create(
        prompt=image_description,
        model="stabilityai/stable-diffusion-2-1",
        height=512,
        width=512
    )

    # save the first image
    image = response["output"]["choices"][0]
    with open("image.png", "wb") as f:
        f.write(base64.b64decode(image["image_base64"]))
        
        
    # Open the image
    image = Image.open("image.png")

    # Get image width and height
    width, height = image.size

    # Create a new image with extended height
    extended_height = height + 100  # Adjust as needed
    extended_image = Image.new("RGB", (width, extended_height), color="white")

    # Paste the original image onto the extended image
    extended_image.paste(image, (0, 0))

    # Add text to the white box
    draw = ImageDraw.Draw(extended_image)
    font = ImageFont.truetype("actions/seguiemj.ttf", 20)  # You can specify the font and size
    
    words = caption.split()
    lines = []
    line = []
    max_width = 0
    for word in words:
        left, top, right, bottom = draw.textbbox((256, height + 15), " ".join(line + [word]), font=font, align="center")
        text_width = right - left
        if text_width <= 480:
            line.append(word)
            max_width = max(max_width, text_width)
        else:
            lines.append(line)
            line = [word]
    if line != []:
        lines.append(line)
        
    caption = "\n".join([" ".join(line) for line in lines])
    
    text_position = ((width - max_width) // 2, height + 15)  # Adjust position as needed
    draw.text(text_position, caption, fill="black", font=font, align="center")

    # Save or display the extended image
    extended_image.save("image.png")
    extended_image.show()
    
    b64string = None
    with open("image.png", "rb") as image:
        b64string = base64.b64encode(image.read())
        
    response = json.loads('{"bytes": "' + b64string.hex() + '"}')
    response["action"] = "end"
    # print(response)
    return json.dumps(response)