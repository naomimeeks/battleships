# Battleships Project
## Guidance on how to play the game
**Objective**  
The goal of the game is to sink all of your opponents’ ships before they sink yours.  
Each player is given a hidden fleet of ships placed randomly on their grid. By taking turns to attack tiles on enemy boards, players must locate and destroy all ship segments.  
The last remaining player with any ships left on their board is declared the winner.
  
**1 vs Computer** – Player battles against an AI opponent with three difficulty options:  
 - **Easy** – random tile selection  
 - **Medium** – targets adjacent tiles after a hit  
 - **Hard** – uses a probability heatmap to predict ship positions

**Multiplayer** – Up to **4 human players** take turns on the same device
  
**Rules**    
 - Each player is given a square grid (9x9) with **3 randomly placed ships** of different sizes (2, 3, and 4 tiles)  
 - Players take turns clicking on their opponents' boards to guess where ships are hidden  
 - A **hit** is shown with a **broken ship image** and plays an **explosion sound**  
 - A **miss** is shown with a **splash image** and plays a **water droplet sound**  
- Each player has **3 lives**, shown as **heart icons** beside their board  
 - A life is lost **each time a full ship is destroyed**  
 - When all 3 ships are sunk, the player is eliminated from the game
 - Turns automatically skip players who have been eliminated  
 - The last remaining player with ships on the board is declared the **winner**  
 - In previous versions, scoring awarded **3 points per hit**, but this version uses visual indicators and player elimination instead of numerical scores  
   
## App controls and walkthrough
**Controls**  
**Mouser clicks-** used to place ships, selecting squares of the othe player's board, click through the menus  
**Keyboard-** used to input player names, (if selected) to select squares to sink ships and place ships  
  
**Walkthrough**
1. **Launch the game**  
   The game opens to a hand-drawn intro screen with three options:  
    - **Play**: starts a new game  
    - **Settings**: opens the settings menu  
    - **Quit**: exits the game  

2. **Settings Menu** (optional)  
   Selecting **Settings** opens a simple screen with:  
    - **Toggle Sound**: turns game audio on or off  
    - **Theme: Light**: placeholder for future GUI customization  
   The **Back** button in the top right returns you to the intro screen  

3. **Select Game Mode**  
   Clicking **Play** brings up the **Game Mode Selection** screen, with four options:  
    - **1 vs Computer**  
    - **1v1**  
    - **1v1v1**  
    - **1v1v1v1**  
   Player names are automatically generated (e.g., "Player 1") and AI is assigned if "1 vs Computer" is selected  

4. **Gameplay Screen**  
   - Each player is shown a square grid with ships randomly placed  
   - The number of boards and layout adjusts dynamically to fit all players  
   - The current player’s board is highlighted in yellow  
   - **Click** on another player’s grid to attack a square  
   - If the square contains a ship:  
     - A **broken ship image** is displayed  
     - An **explosion sound** is played  
   - If the square is empty:  
     - A **water splash image** is shown  
     - A **splash sound** is played  
   - Lives are displayed as heart icons beside each board  
   - **Each heart disappears** when a full ship is sunk, visually tracking remaining lives

5. **Turns and Elimination**  
   - Turns rotate automatically  
   - Eliminated players (all ships destroyed) are skipped  
   - The game continues until one player remains  

6. **Winner Screen**  
   When a player wins, a final screen appears showing:  
    - The winner’s name  
    - A **Main Menu** button to return to the intro screen  

## Updates
Since the initial version of the project, which was a text-based terminal game, the application has undergone a complete transformation.  
Below is a summary of the key changes and enhancements made:

**From Text to GUI**

 - Replaced command-line interface with a **fully interactive graphical UI** using Pygame  
 - Added **mouse-based controls** instead of typed input  
 - Introduced **custom images** for ships, water, hits, and background  
 - Included **sound effects** for hits, misses, victory, and defeat  

**Gameplay Enhancements**

 - Added support for multiplayer:  
   - **1v1**  
   - **1v1v1**  
   - **1v1v1v1**  

 - Added **1 vs Computer** mode with **Easy AI**  
 - Boards **dynamically reposition** based on the number of players  

**Logic and Mechanics Improvements**

 - Removed manual input errors by using **grid-based interaction**  
 - Improved **turn handling** — automatically skips eliminated players  
 - Integrated a **winner detection screen** with visual and audio feedback  

**UI & Settings**

 - Created **intro and settings menus**  
 - Players can **toggle sound** on/off  
 - Placeholder added for **theme switching**  
 - Players are now **automatically named** (e.g., "Player 1") to speed up setup  

**Visual Polish**

 - Added **themed grid backdrops** depending on the number of players  
 - Lives are represented using **heart icons** beside each board  
 - Ships and attacks use **high-quality sprite images**  

## GUI design
The visual design of the Battleships game adheres closely to the **Golden Rules of User Interface Design**, ensuring a clear, engaging, and user-friendly experience.

 - **Consistency**  
   - The entire interface follows a cohesive **hand-drawn notebook theme**, from the background grid to buttons and fonts.  
   - Button placement is consistent across screens (e.g., "Back" always appears in the upper-right corner).  
   - Visual elements like grids, ships, and hearts are uniformly styled and scaled.

 - **Feedback**  
   - Players receive immediate visual and audio feedback after each action:  
     - Hits show a broken ship image and play an explosion sound.  
     - Misses display a water image and play a splash sound.  
     - Turn indicators and highlighted active boards provide clear visual cues.

 - **Simplicity**  
   - The interface avoids unnecessary complexity — only essential elements are shown per screen.  
   - Navigation is intuitive, with a minimal set of clearly labeled buttons like "Play", "Quit", and "Settings".  
   - Game states (Intro, Menu, Game, Winner) are cleanly separated and visually distinct.

 - **User-Friendly Layout**  
   - Large, clickable buttons are easy to interact with.  
   - Player boards are evenly spaced and dynamically positioned depending on the number of players.  
   - The use of visual elements like hearts for lives, text for turns, and central alignment of messages ensures readability.

Overall, the GUI is visually distinctive, functionally intuitive, and supports a smooth user experience throughout the game.

## AI tools
- Approximately 40–50% of this project was supported through AI-assisted development  
 - The core structure, including the core classes (`Board`, `Square`, `Button`, `AI classes`), game flow, and screen transitions, was designed and implemented by us
   
 - AI assistance was used primarily for:  
   - Debugging issues in game logic and turn order  
   - Helping resolve bugs with event handling, such as click detection and player elimination  
   - Offering suggestions for GUI implementation, including use of Pygame image scaling, blitting, and font rendering  
   - Improving efficiency in repetitive sections of code (e.g., drawing grids, checking ship status)  
   - Assisting in writing documentation, including structuring the README and formatting Markdown

## Evaluation & Recommendations
The enhanced Battleships game aimed to improve user experience through a polished GUI, intuitive interactions, and expanded gameplay features. Below is an evaluation of how well our project aligns with the specified GUI options and overall goals from the brief.

**What We Achieved:**
**GUI Design & Usability**
- The interface is consistent, visually engaging, and user-friendly — following the Golden Rules of UI Design (e.g., consistent layout, feedback, simplicity).
- We used hand-drawn visuals and clean typography to support clarity and visual appeal.

**Option 5: Quit and Restart Functionality**
- A clear **Settings menu** includes options to **restart** the game or return to the **main menu** at any time.

**Option 6: Final Score Logic (Adapted)**
- Instead of a numerical score, players "lose lives" visually through disappearing heart icons.
- This encourages strategic gameplay and still tracks progress meaningfully.
- We adapted scoring into a visual elimination mechanic to better suit multiplayer dynamics.

**Option 7: Multimedia Components**
- The game uses **custom sounds** (explosions, splashes, trumpets) and **images** (ships, water, hearts) for immersive feedback.
- Each interaction gives the player both visual and audio cues.

**Option 8: Option for More Than Two Players**
- Fully supports **1 to 4 players**, dynamically laying out boards for all participants.
- Also includes **AI player modes** with three difficulty levels.

---

**What We Chose Not to Include (and Why):**
**Option 1: Adjust Number of Rows and Columns**
- We intentionally fixed the board size to 9x9 for balance, simplicity, and compatibility with the UI layout.
- Dynamic resizing would require full redesign of the grid layout and ship placement logic — deemed unnecessary for the gameplay scope.

**Option 2: Input Method Selection**
- All input is **mouse-based** for consistency and clarity.
- Adding keyboard input would not improve gameplay meaningfully and could create confusion or conflicts with mouse actions.

**Option 3: GUI Customisation Options**
- While players cannot customise colors or styles, the theme is intentionally unified and consistent.
- Aesthetic options were deprioritized in favour of polish, gameplay clarity, and simplicity.

**Option 4: Display Current Time and Points**
- Since scoring was visual (heart lives) and time-tracking was not central to gameplay, this feature was not implemented.
- The turn-based nature of the game made a timer unnecessary.

**Summary:**
We chose features that directly improve player experience and engagement while avoiding over-complication. The game is polished, consistent, and supports dynamic multiplayer gameplay with strategic depth through AI and lives tracking. Future updates could explore optional themes or more in-depth stat tracking if user demand calls for it.

