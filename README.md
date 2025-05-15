# Battleships Project
## Guidance on how to play the game
**Objective**  
Need to talk to Iyanu about how the points system works and write this here  
Sink all your opponents ships before they sink yours  
  
**Game modes**  
**1vs Computer-** individual player battles an AI opponent with different difficulties, easy, medium and hard  
**Multiplayer-** two or more (write how many at the end here) players battle at the same computer  
  
**Rules**    
 - Each player has a square grid (size depending on player's choice at the start of the game) of ships with varying sizes  
 - Players take turns clicking on the opponent's grid  
 - Hits are marked with a broken ship image and explosion sound  
 - Misses are marked with a splash image and water sound  
 - The first player to sink all the opponent's ships wins  
 - Each successful hit scores **3 points**
   
## App controls and walkthrough
**Controls**  
**Mouser clicks-** used to place ships, selecting squares of the othe player's board, click through the menus  
**Keyboard-** used to input player names, (if selected) to select squares to sink ships and place ships  
  
**Walkthrough**
1. Launch game
2. 

The start button takes you to the initial screen...Once start is pressed  
The settings button takes you to where you can select different difficulties and board sizes, also different GUI designs  
Then there's multiplayer modes or 1v1 or vs computer  

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
