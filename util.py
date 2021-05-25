def get_frame_order(frame1, frame2):
    """Gets the turn order for the current turn of the game.
    Turn order is determined by the speeds of the current pokemon on the field.
    With the exception of the effects from certian moves, items, or abilities,
    the faster pokemon always switches or attacks before the slower pokemon.
    Switching to a different pokemon always occurs before a pokemon attacks (unless the opposing pokemon uses the move Pursuit)."""
    if frame1.attack_name == "Pursuit" and frame2.switch_choice:
        return [frame1, frame2]
    elif frame2.attack_name == "Pursuit" and frame1.switch_choice:
        return [frame1, frame2]

    if frame1.switch_choice and frame2.attack:
        return [frame1, frame2]
    elif frame2.switch_choice and frame1.attack:
        return [frame2, frame1]

    priority_p1 = check_priority(frame1)
    priority_p2 = check_priority(frame2)

    if priority_p1 == priority_p2:
        return check_speed(frame1, frame2)
    elif priority_p1 > priority_p2:
        return [frame1, frame2]
    else:
        return [frame2, frame1]


def check_speed(frame1, frame2):
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1_speed = calc_speed(frame1.attacking_team, frame1.weather)
    p2_speed = calc_speed(frame2.attacking_team, frame2.weather)

    if p1_speed > p2_speed:
        return [frame1, frame2]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [frame2, frame1]


def check_priority(f):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""

    if f.terrain.current_terrain == "Psychic Terrain" and f.target.grounded == True:
        return 0
    if (
        f.terrain.current_terrain == "Grassy Terrain"
        and f.attack.name == "Grassy Glide"
    ):
        return 1

    try:
        return priority_moves[f.attack.name]
    except Exception:
        return 0


def roll_paralysis(user, i=None):
    """Rolls to determine if a paralyzed pokemon can successfully use an attack. 25% that pokemon won't be able to move due to paralysis."""
    if i == None or i < 1 or i > 4:
        i = random.randint(1, 4)

    if i == 1:
        print(f"{user.name} is paralyzed and can't move.")
        return True
    return False


def roll_frozen(user, i=None):
    """Rolls to determine if a frozen pokemon thaws out during it's attack. Frozen pokemon are not able to attack. 20% chance to thaw out.
    The pokemon can use it's attack on the turn that it thaws out."""
    if i == None or i < 1 or i > 5:
        i = random.randint(1, 5)

    if i == 1:
        print(f"{user.name} thawed out!")
        user.cure_status()
        return False
    return True


def roll_confusion(user, i=None):
    """Rolls to determine if a confused pokemon can successfully use an attack. 33% chance they will hit themselves in confusion."""
    if i == None or i < 1 or i > 2:
        i = random.randint(1, 2)

    if i == 1:
        # TODO: Implement confusion damage.
        print(f"{user.name} hit its self in confusion!")
        return True
    return False


def check_can_attack(f):
    """Checks to make sure if an attacker is able to use a move based on any present status conditions.
    Calls functions that require a roll for an attack to be successful (like paralysis or confusion)."""
    if f.user.status[0] == "Paralyzed":
        if roll_paralyzed(user):
            pass

    if f.user.status[0] == "Asleep" and f.attack_name != "Sleep Talk":
        print(f"{frame.user.name} is asleep.")
        pass

    if f.user.status[0] == "Frozen":
        if roll_frozen(f.user):
            pass

    if "Confusion" in f.user.v_status:
        if roll_confusion(f.user):
            pass

    if "Flinched" in f.user.v_status:
        print(f"{f.user.name} flinched!")
        pass

    if check_immunity(f):
        print(f"It had no effect.")
        pass

    f.can_attack = True


def check_immunity(f):
    """Returns boolean if current attack isn't able to land due to target being immune to the attack's type."""
    if (
        (f.attack.type == "Poison" and "Steel" in f.target.typing)
        or (f.attack.type == "Dragon" and "Fairy" in f.target.typing)
        or (
            (f.attack.type == "Normal" or f.attack.type == "Fighting")
            and "Ghost" in f.target.typing
        )
        or (f.attack.type == "Ghost" and "Normal" in f.target.typing)
        or (f.attack.type == "Electric" and "Ground" in f.target.typing)
        or (f.attack.type == "Psychic" and "Dark" in f.target.typing)
    ):
        return True
    return False


def check_attack_lands(f, i=None):
    """Calculates required accuracy for an attack to land based on the accuracy of the attack,
    accuracy of user, evasion of target, and any additional modifiers. Rolls i in range 0 to 100.
    If i is less than or equal to required accuracy, attack hits and function returns True."""
    additional_modifier = 1

    # TODO: The accuracy minus evasion is probably wrong.
    a = (
        f.attack.accuracy
        * (
            100
            - (
                f.user.calc_modified_stat("accuracy")
                - f.target.calc_modified_stat("evasion")
            )
        )
        * additional_modifier
    )

    if i is None or i < 0 or i > 100:
        i = random.randint(0, 100)

    if i <= a:
        f.attack_lands = True
        return
    print(f"{f.user.name}s attack missed!")


def apply_non_damaging_move(frame):
    if frame.attack_name == "Stealth Rocks":
        set_stealth_rocks(frame)

    if frame.attack_name == "Defog":
        activate_defog(frame)


def apply_post_attack_effects(frame):
    """Applies post attack effects (lowering or raising stats, applying a status, etc) to the user/target of the given frame."""
    post_attack.apply_stat_alt_attack(frame.user, frame.target, frame.attack)
    post_attack.apply_status_inflicting_attack(frame.user, frame.target, frame.attack)
    post_attack.apply_v_status_inflicting_attack(frame.user, frame.target, frame.attack)


def apply_end_of_turn_effects(frame_order):
    """Applies end of turn events (recoil, leftovers healing, etc) to the user of the given frame."""
    for frame in frame_order:
        frame.user.decrement_statuses()
        if frame.attack_name:
            frame.attack.decrement_pp()

    if (
        frame_order[0].weather.current_weather == "Sandstorm"
        or frame_order[0].weather.current_weather == "Hail"
    ):
        for frame in frame_order:
            weather.apply_weather_damage(frame.weather, frame.user)

    if frame_order[0].terrain.current_terrain == "Grassy Terrain":
        for fram in frame_order:
            if frame.user == True:
                terrain.heal_from_grassy_terrain(frame.terrain, frame.user)

    for frame in frame_order:
        if frame.user.item == "Leftovers":
            apply_leftovers(frame.user)

    for frame in frame_order:
        if frame.user.status[0] == "Burned":
            apply_burn(frame.user)

    for frame in frame_order:
        if frame.user.status[0] == "Badly Poisoned":
            apply_bad_poison(frame.user)

    # TODO: Recoil damage.
    # for frame in frame_order:
    #     apply_recoil(frame.user)