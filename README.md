# HappyHero

A fun 2D endless-runner platformer game with a twist, built using Python and [Pygame Community Edition (pygame-ce)](https://pyga.me/docs/index.html).

## Features

- **Dynamic Gameplay & Controls:** Smooth player animations, jumping/double-jumping mechanics, and progressively increasing difficulty as your run goes on.
- **Varied Obstacles & Power-Ups:** Randomized enemy spawn logic alongside collectible power-ups (such as score multipliers, extra lives, and invincibility).
- **Complete Game Loop & UI:** Includes animated transition screens, a life counter, a pause menu, a settings menu, and a game over screen.
- **Persistent Top 10 Leaderboard:** Automatically tracks and saves high scores locally in `leaderboards.txt`.
- **Custom Visuals & Audio:** Features custom character, enemy, and environment sprites (`graphics/`), custom typography (`fonts/`), and integrated sound effects and background music (`sounds/`).

## Getting Started

### Prerequisites
- Python 3.8+ installed on your machine

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd happyhero
   ```

2. **Create a virtual environment:**  
   *(Use `python3` instead of `python` if you are on macOS/Linux)*
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python main.py
   ```

## Project Structure

```text
happyhero/
├── fonts/            # Custom font files used in menus and HUD
├── graphics/         # Player, enemy, power-up, and background sprites
├── sounds/           # Background music and sound effects
├── leaderboards.txt  # Local storage for top 10 high scores
├── main.py           # Main game loop and logic
├── requirements.txt  # Python dependencies (pygame-ce)
└── LICENSE           # MIT License
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
