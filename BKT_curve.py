import matplotlib.pyplot as plt

def simulate_bkt_mixed(start_knowledge, win_games, loss_games, p_T_win=0.1, p_T_loss=-0.05):
    knowledge_history = [start_knowledge]
    p_L = start_knowledge / 100.0

    # First N wins
    p_T = p_T_win
    for i in range(win_games + loss_games):
        
        if i > win_games:
            p_T = p_T_loss
        
        new_p_L = p_L + (1 - p_L) * p_T  # Gain toward 1
        new_p_L = max(0, min(1, new_p_L))
        knowledge_history.append(round(new_p_L * 100, 2))
        p_L = new_p_L

    return knowledge_history

# Simulation parameters
n_win_games = 25
n_loss_games = 25
knowledge = simulate_bkt_mixed(start_knowledge=0, win_games=n_win_games, loss_games=n_loss_games)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(range(len(knowledge)), knowledge, label="Player Knowledge", linewidth=2)
plt.axvline(x=n_win_games, color='gray', linestyle='--', label='Start of Losing Streak')
plt.title(f"Knowledge Progression: {n_win_games} Wins Followed by {n_loss_games} Losses")
plt.xlabel("Game Number")
plt.ylabel("Knowledge (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
