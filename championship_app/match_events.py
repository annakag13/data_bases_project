import random

"""
a = [ 
    ( 1, "keep" ),
    ( 17, "keep" ),
    ( 2, "def" ),
    ( 3, "def" ),
    ( 4, "half" ),
    ( 5, "fw" ),
    ( 6, 'fw' ),
    ( 7, "half" ),
    ( 8, "fw" ),
    ( 9, 'fw' )
]
b = [
    ( 11, "keep" ),
    ( 41, "keep" ),
    ( 12, "def" ),
    ( 13, "def" ),
    ( 24, "half" ),
    ( 35, "fw" ),
    ( 36, "fw" ),
    ( 23, "def" ),
    ( 44, "half" ),
    ( 45, "fw" ),
    ( 46, "fw" )
]
"""

max_noch = 3    # number of changes
basikoi = 10
max_yellow = 5
red_pc = 10      # red-card percentage (int 0-100)
owngoal_pc = 10

def participation_and_cards(list):
    keeper = []
    other = []
    participation = []
    cards = []
    have_yellow = []

    noch = random.randint(0, max_noch)

    has_red_card = False
    if random.randint(0,100) < red_pc:
        has_red_card = True
    
    for (id, pos) in list:
        if pos == "τερματοφύλακας":
            keeper.append(id)
        else:
            other.append(id)
    random.shuffle(keeper)
    random.shuffle(other)

    play_all_match = other[0 : (basikoi - noch)]

    play_all_match.append(keeper[0])

    changes = other[(basikoi-noch) : ((basikoi-noch) + noch*2)]

    # print(play_all_match, other, changes, noch)

    for plr in play_all_match:
        if has_red_card and plr == play_all_match[0]:
            red_card_min = random.randint(5,85)

            participation.append(
                (plr, 0, red_card_min )
            )
            cards.append(
                (plr, 2, red_card_min)
            )
        else:
            participation.append(
                (plr, 0, 90)
            )
    for i in range(0, noch):
        min = random.randint(40, 85)
        participation.append(
            ( changes[i] , 0, min )
        )
        participation.append(
            ( changes[i + noch], min, 90)
        )
    
    for i in range(0, random.randint(0, max_yellow)):
        (id, min_in, min_o) = participation[random.randint(0, len(participation)-1)]
        if not id in have_yellow:
            have_yellow.append(id)
            cards.append(
                (id, 1, random.randint(min_in, min_o))
            )

    return {
        "keep": keeper,
        "other": other,
        "part_tbl": participation,
        "cards": cards
    }

def rand_int_in_range(start, end, excluded):
    randMin = random.randint(start, end)
    while randMin in excluded:
        randMin = random.randint(start, end)
    return randMin
    

def goal_achivers(home_participation, guest_participation, goalsHome, goalsGuest):
    goals = []
    goalMinutes = []
    for i in range(0, goalsHome):
        is_own_goal = False
        if random.randint(0,100) < owngoal_pc:
            is_own_goal = True
        
        if is_own_goal:
            (id, min_in, min_out) = guest_participation[random.randint(0, len(guest_participation)-1)]
            minute = rand_int_in_range(min_in, min_out, goalMinutes)
            goals.append(
                (id, 2, minute)
            )
            goalMinutes.append(minute)
        else:
            (id, min_in, min_out) = home_participation[random.randint(0, len(home_participation)-1)]
            minute = rand_int_in_range(min_in, min_out, goalMinutes)
            goals.append(
                (id, 1, minute)
            )
            goalMinutes.append(minute)

    for i in range(0, goalsGuest):
        is_own_goal = False
        if random.randint(0,100) < owngoal_pc:
            is_own_goal = True
        
        if is_own_goal:
            (id, min_in, min_out) = home_participation[random.randint(0, len(home_participation)-1)]
            minute = rand_int_in_range(min_in, min_out, goalMinutes)
            goals.append(
                (id, 2, minute)
            )
            goalMinutes.append(minute)

        else:
            (id, min_in, min_out) = guest_participation[random.randint(0, len(guest_participation)-1)]
            minute = rand_int_in_range(min_in, min_out, goalMinutes)
            goals.append(
                (id, 1, minute)
            )
            goalMinutes.append(minute)
    return goals

# print(participation_and_cards(a))

# part_a = participation_and_cards(a)
# part_b = participation_and_cards(b)

# print(part_a)
# print(part_b)
# print(goal_achivers(part_a["part_tbl"], part_b["part_tbl"], 5, 4) )
