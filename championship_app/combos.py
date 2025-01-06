def create_round_robin_schedule(teams):
    """
    Δημιουργεί πρόγραμμα πρωταθλήματος με γύρους όπου κάθε αγωνιστική
    έχει τον μέγιστο αριθμό αγώνων και καμία ομάδα δεν παίζει πάνω από μία φορά.
    """
    if len(teams) % 2 != 0:
        teams.append("Ρεπό")  # Προσθήκη "Ρεπό" αν ο αριθμός των ομάδων είναι περιττός

    num_teams = len(teams)
    schedule = []

    for round_num in range(num_teams - 1):
        round_matches = []
        for i in range(num_teams // 2):
            match = (teams[i], teams[num_teams - 1 - i])
            round_matches.append(match)
        schedule.append(round_matches)
        # Περιστροφή των ομάδων για τον επόμενο γύρο
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return schedule


def schedule_champ(champion):
    
    teams = [t[0] for t in champion]
    # teams = [f"Ομάδα{i}" for i in range(1, 8)]  # 14 ομάδες

    schedule = create_round_robin_schedule(teams)
    full_schedule = []

    for round in schedule:
        round_match = []
        for g in round:
            round_match.append((g[0], g[1]))
        full_schedule.append(round_match)

    for round in schedule:
        round_match = []
        for g in round:
            round_match.append((g[1], g[0]))
        full_schedule.append(round_match)

    return full_schedule

    # print("\nΠρόγραμμα πρωταθλήματος:")
    #for round_num, round_matches in enumerate(schedule, start=1):
    #    print(f"\nΑγωνιστική {round_num}:")
    #    for match in round_matches:
    #        print(f"{match[0]} vs {match[1]}")


