define e = Character("Eileen")


label start:

    scene bg room
    show eileen
    e "Welcome to the beginning of the script"
    e "This is that part of the story outside the flowchart - you can't access the screen!"
    $ _game_menu_screen = "flowchart"
label loop:
    $ flowchart_accessible = True
    $ segment = "loop"
    if endings != []:
        $ ends = len(endings)
        e "You've seen [ends] endings."
        if ends >= 4:
            e "You have seen all endings! Congratulations!"
            return
        e "To make yourself familiar with it as a user, feel free to jump to various points in this demo to access all four endings faster!"
    else:
        e "Now we're in the story proper."
        e "Now you can access the flowchart screen."
        e "I would recommend frequently checking the flowchart screen in the game menu - it will change as you progress through the demo!"
        extend " To make this a bit easier, I made it so you can access it just with pressing Escape or clicking your right mouse button."
label loop2:
    $ new_node("loop2")
    e "You have completed the first node, so it should appear in the flowchart."
    menu:
        e "Now tell me... what do you like?"

        "Apples":
            "{i}You said you like apples.{/i}"
            jump apples

        "Oranges":
            "{i}You said you like oranges.{/i}"
            jump oranges
    return
label apples:
    $ new_node("apples")
    e "Oh? You like apples?"
    e "Interesting."
    e "Tell me..."
    menu:
        e "Red apples or green apples?"

        "Red Apples":
            $ story_flags["apple_kind"] = "red" # this adds the "apple_kind": "red" key-value pair to the story_flags dict
            "{i}You said you prefer red apples.{/i}"

        "Green Apples":
            $ story_flags["apple_kind"] = "green" # this adds the "apple_kind": "green" key-value pair to the story_flags dict
            "{i}You said you prefer green apples.{/i}"
    e "Interesting choice."
label apples2:
    $ new_node("apples2")
    e "The plot hasn't branched off yet despite the previous choice about red or green apples."
    e "I would recommend checking the flowchart menu to see the segment above this one. There should be something at the bottom of the screen if you do so."
    e "The branching point will come soon, don't worry."
label apples3:
    $ new_node("apples3")
    e "The point is approaching... now!"
    if story_flags["apple_kind"] == "red":
        jump red_apples
    if story_flags["apple_kind"] == "green":
        jump green_apples

label red_apples:
    $ new_node("red_apples")
    e "You have achieved the red apples ending."
    $ unlock_node("red_apples")
    $ unlock_ending("red_apples")
    jump loop

label green_apples:
    $ new_node("green_apples")
    e "You have achieved the green apples ending."
    $ unlock_node("green_apples")
    $ unlock_ending("green_apples")
    jump loop

label oranges:
    $ new_node("oranges")
    e "Oh? You like oranges?"
    e "Good choice."
    e "I like oranges too."
label oranges2:
    $ new_node("oranges2")
    e "I feel like there's something bound to happen, but I'm not sure..."
    if "green_apples" in endings:
        menu:
            e "Do you feel it too?"
            "Yes":
                e "Right..."
                jump secret1
            "No":
                pass
    e "Nevermind..."
label oranges3:
    $ new_node("oranges3")
    e "You have achieved the oranges ending."
    $ unlock_node("oranges3")
    $ unlock_ending("oranges")
    jump loop

label secret1:
    $ new_node("secret1")
    e "Wait... do you remember the time you said you liked green apples?"
    e "I feel that too!"
label secret2:
    $ new_node("secret2")
    e "Can we really remember other choices and their consequences?"
    "You have unlocked the secret ending."
    $ unlock_node("secret2")
    $ unlock_ending("secret")
    jump loop
