import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import threading
import time as pytime

def plot_progression_with_controls(Uh_history, X, Y, plot_type='3d'):
    fig = plt.figure(figsize=(8, 4))
    vmax = 40
    zlim = vmax  # Set z-axis limit to a fixed maximum value
    
    ax = None
    cbar = None
    if plot_type == '3d':
        ax = fig.add_subplot(1, 1, 1, projection='3d')
    elif plot_type == 'height':
        ax = fig.add_subplot(1, 1, 1)

    # Set initial plot
    current_index = 0  # Integer to track the current iteration
    playing = [False]  # Mutable flag to control play/stop

    # Function to calculate statistics
    def calculate_stats(Uh):
        mean = np.mean(Uh)
        min_val = np.min(Uh)
        max_val = np.max(Uh)
        std_dev = np.std(Uh)
        return mean, min_val, max_val, std_dev

    # Initialize plot and stats
    time, Uh = Uh_history[current_index]
    mean, min_val, max_val, std_dev = calculate_stats(Uh)
    if plot_type == '3d':
        surf = ax.plot_surface(X, Y, Uh, cmap='hot', vmin=0, vmax=vmax)
        ax.set_zlim(0, zlim)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Température')
        ax.set_title(f'Distribution 3D de la température à t = {time:.2f} s')
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    elif plot_type == 'height':
        cp = ax.contourf(X, Y, Uh, levels=50, cmap='hot', vmin=0, vmax=vmax)
        cbar = fig.colorbar(cp, ax=ax)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_title(f'Distribution 2D de la température à t = {time:.2f} s')

    # Display statistics in French
    stats_text = fig.text(
        0.05, 0.85,
        f'Moyenne : {mean:.2f}°C\nMin : {min_val:.2f}°C\nMax : {max_val:.2f}°C\nÉcart-type : {std_dev:.2f}°C',
        color='blue', fontsize=10, verticalalignment='top', horizontalalignment='left'
    )

    # Function to update the plot
    def update_plot():
        nonlocal stats_text
        time, Uh = Uh_history[current_index]
        ax.clear()  # Clear the previous plot
        if plot_type == '3d':
            surf = ax.plot_surface(X, Y, Uh, cmap='hot', vmin=0, vmax=vmax)
            ax.set_zlim(0, zlim)  # Keep z-axis limit fixed
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_zlabel('Température')
            ax.set_title(f'Distribution 3D de la température à t = {time:.2f} s')
            cbar.update_normal(surf)
        elif plot_type == 'height':
            cp = ax.contourf(X, Y, Uh, levels=50, cmap='hot', vmin=0, vmax=vmax)
            cbar.update_normal(cp)
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_title(f'Distribution 2D de la température à t = {time:.2f} s')
        
        # Update statistics
        mean, min_val, max_val, std_dev = calculate_stats(Uh)
        stats_text.set_text(
            f'Moyenne : {mean:.2f}°C\nMin : {min_val:.2f}°C\nMax : {max_val:.2f}°C\nÉcart-type : {std_dev:.2f}°C'
        )
        plt.draw()

    # Button to go to the next iteration
    def next(event):
        nonlocal current_index
        if current_index < len(Uh_history) - 1:
            current_index += 1
            update_plot()

    # Button to go to the previous iteration
    def prev(event):
        nonlocal current_index
        if current_index > 0:
            current_index -= 1
            update_plot()

    # Function to play through the iterations
    def play():
        nonlocal current_index
        while playing[0]:
            if current_index < len(Uh_history) - 1:
                current_index += 1
            else:
                current_index = 0  # Loop back to start
            update_plot()
            pytime.sleep(0.2)  # Pause between frames

    # Button to play/stop the animation
    def play_stop(event):
        if not playing[0]:
            playing[0] = True
            thread = threading.Thread(target=play)
            thread.start()
        else:
            playing[0] = False

    # Adding buttons to the figure
    axprev = plt.axes([0.6, 0.01, 0.1, 0.075])
    axnext = plt.axes([0.71, 0.01, 0.1, 0.075])
    axplay = plt.axes([0.82, 0.01, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(prev)
    bplay = Button(axplay, 'Play/Stop')
    bplay.on_clicked(play_stop)

    plt.show()
