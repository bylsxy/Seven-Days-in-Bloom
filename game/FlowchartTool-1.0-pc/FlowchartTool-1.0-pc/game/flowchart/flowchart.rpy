########## DEVIL SPIδεR'S FLOWCHART PLUGIN ##########
# This plugin is an implementation of a flowchart feature, commonly found in visual novels with many routes.
# It will often refer to flowchart's buttons representing different segments of a story as "nodes"
# Currently support features:
#   - Expanding flowchart - the flowchart becomes bigger with more progress being unlocked
#   - Conditional access to nodes - make some already visited nodes inaccessible from a flowchart under your own conditions
#   - On-screen flag adjustments - if you want the player to change some story variables within the flowchart screen itself

## Parameters ##
# There are numerous occasions where I list out a format for parameters. If the argument is in quotation marks in the format (like "this")
# the argument should also be in quotation marks

## Images ##
# There should be at least seven images located in game/flowchart/image:
# All images except crosshair.png have to be the same size - the size itself however doesn't matter
# ground.png - the base "frame" of the flowchart - this will appear as soon as the player is able to see the flowchart
# idle.png, hover.png, selected_idle.png, select_hover.png, insensitive.png - all the different states all the flowchart nodes can be in
# crosshair.png - should be the size of one node (look at gui.flow_hotspot_size for its resolution)
# Optionally, you can supply additional images (should be the same size as the imagemap) that can get added if you want an extending flowchart (see extra_lines dict)

### THIS PLUG-IN ASSUMES THE GAME CAN BE COMPLETED IN A SINGLE FILE - IF AN NON-TRUE ENDING THROWS THE PLAYER TO THE MAIN MENU, #
### THE FLOWCHART WILL NOT WORK AS INTENDED ###

## If you've downloaded the standalone archive, all parameters match the example demo and should be changed to fit the game##

##### STORY VARIABLES #####
# These are used to track progress within the game, do not change anything here #

init -3:
    default segment = "" # keeps track of the current segment
    default segments = [] # keeps track of visited segments in a save file
    default endings = [] # keeps track of completed endings in a save file
    default story_flags = {} # keeps track of special flags in a story (for example choices that have delayed effect on the story) - this is a python dict

    default flowchart_accessible = False # there are moments where you need to disable the flowchart


init python:
    # This is recommended to put at the beginning of a label - this will add the old label's name to the visited list and sets the current segment name
    # If there are more labels per node in your script, only put this to the first label
    def new_node(n=None):
        global segment, segments
        if segment not in segments:
            segments.append(segment)
        segment = n
    # This is a function that adds a completed ending - usually named after the label it's in - to the endings list. You can call len(endings) to track amount of endings
    def unlock_ending(n=None):
        global endings
        if n not in endings:
            endings.append(n)

    # Use this alongside unlock_ending to make the ending accessible from the flowchart
    def unlock_node(n=None):
        global segments
        if n not in segments:
            segments.append(n)


    ##### STORY NODES #####
    # This is where you fill out information for all nodes in your game
    # The format is: "label": [(x coordinate, y coordinate), "name", "description", "condition"],
    # Coordinates are for the imagemap's buttons to render correctly - they tell the upper-left corner of an imagebutton hotspot
    # condition is a string containing either a Python expression or True - if the expression evaluates to false, the node can't be selected from the menu.

    nodes = {

        "loop": [(450, 0), "Looping Point", "This is where you end up after you reach an ending.", "True"],
        "loop2": [(450, 100), "Choice Imminent", "In this segment, you have a branching point.", "True"],
        "apples": [(350, 200), "Apples Route", "Beginning of the apples route.", "True"],
        "apples2": [(350, 300), "Apples Route 2", "Apples route continues.", "True"],
        "apples3": [(350, 400), "Apples Route 3", "Apples route continues.", "True"],
        "red_apples": [(300, 500), "Red Apples Ending", "This is the red apples ending.", "story_flags['apple_kind'] == 'red'"],
        "green_apples": [(400, 500), "Green Apples Ending", "This is the green apples ending.", "story_flags['apple_kind'] == 'green'"],
        "oranges": [(550, 200), "Oranges Route", "Beginning of the oranges route.", "True"],
        "oranges2": [(550, 300), "Oranges Route 2", "Oranges route continues.", "True"],
        "oranges3": [(550, 400), "Oranges Ending", "Oranges route ending.", "True"],
        "secret1": [(650, 400), "Secret Route", "Beginning of the secret route.", "True"],
        "secret2": [(650, 500), "Secret Ending", "Secret ending.", "True"],

    }

    gui.flow_hotspot_size = (100, 100) # X and Y size of a node - if your hotspots are sized differently, change this

    ##### ON-SCREEN FLAG ADJUSTMENTS #####
    # There can be decisions in the story that you want to let players change directly in the flowchart. This dict allows such choices to appear in the flowchart.
    # The format of this dict is:
    # "label_name": ["Choice string", [("choice text", "choice action")...]],
    # Choice string is displayed before the buttons, and it creates the correct amount of buttons with choice text, performing a choice action
    flow_choices = {
        "apples": ["What kind of apples do you like?", [("Red", "SetDict(story_flags, 'apple_kind', 'red')"),("Green", "SetDict(story_flags, 'apple_kind', 'green')")]],
    }

    ##### EXPANDING FLOWCHARTS #####
    # You can split the flowchart into multiple parts that appear under specific conditions (hidden routes, spoiler prevention etc.)
    # The format for these is:
    # "image name": "Python expression",
    # where image name is the image filename found in game/flowchart/image

    extra_lines = {
        "hidden_1": "'secret1' in segments",
    }

## This is the actual screen displayed to the user

screen flowchart():

    tag menu

    default select_node = None
    use game_menu(_("Flowchart"), scroll="viewport"):
        vbox:
            align (0.5, 0.5)
            viewport:
                xalign 0.5
                xysize (1025, 625) # Change this to your flowchart's image size + 25 on each axis
                child_size (1000, 600) # Change this to your flowchart's image size
                mousewheel True
                scrollbars "vertical"
                edgescroll (150, 2000) # Optional
                draggable True
                xinitial 0.5
                for img, cnd in extra_lines.items():
                    if eval(cnd):
                        add "flowchart/image/" + img + ".png"
                imagemap:
                    auto "flowchart/image/%s.png"
                    for i in segments:
                        hotspot nodes[i][0] + gui.flow_hotspot_size:
                            action SetScreenVariable("select_node", i)
                            sensitive eval(nodes[i][3])
                add "flowchart/image/crosshair.png" xpos nodes[segment][0][0] ypos nodes[segment][0][1]

            if select_node:
                text nodes[select_node][1]
                text nodes[select_node][2]
                textbutton "Jump" action [SetVariable("segment", select_node), Start(select_node)]
                if flow_choices.get(select_node):
                    text flow_choices[select_node][0]
                    hbox:
                        for t in flow_choices[select_node][1]:
                            textbutton t[0] action eval(t[1])
