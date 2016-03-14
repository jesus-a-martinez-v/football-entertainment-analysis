def total_goals_scored(ft):
    """
    Takes the final time score and adds each component to obtain the total goals scored in the match.
    """
    goals = ft.split("-")
    return int(goals[0]) + int(goals[1])


def goal_difference(ft):
    """
    Takes the final time score and obtains the goal difference of the match.
    """
    goals = ft.split("-")
    return abs(int(goals[0]) - int(goals[1]))
