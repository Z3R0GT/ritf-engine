    
#COPY
label start:
    #Only need this function
    $ list_to_start()
    #Here end the game
    return


define textsize = 35
define g = Character (_("Guide"), color="#FFFFFF", what_size=textsize)

#Chapter normal (if you see a jump, so is a moddificade chapter)
label chapter_1_start_mod:
    $ renpy.pause(2)

    "{i}Welcome to the world of dragons, and thank you for playing my game, Rose's in The Flames.{/i}"

    g "Greetings, how are you?"

    g "My name is Guide, and I will remain your guide throughout the dragon world. I will be there to help you move throughout the dragon world as you progress as a player."

    g "I bet you're probably wondering why we're speaking in the dark."

    $ renpy.pause(2)

    e "Error! {w=2} User profile not found!"

    $ renpy.pause(1)

    e "Name not found! {w=2} Unknown gender!"

    $ renpy.pause(1)

    g "That was error, don't listen to him. He doesn't know what he's saying, but for once I agree with him, we need to set up a few basic things before you can play the game."

    g "Now, before we dive into the story, what is your gender?"

    #here must be the jump
    jump other_can

    return

#chapter normal
label chapter_2_start:
    "I" "yes, there we go"

    "I" "this test is funcionaly Bv"




