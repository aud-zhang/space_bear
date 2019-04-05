# Space Bear

## By: Kiana Mills, Jeanette Lin, Mallika Varkhedi, Audrey Zhang

### Install and Run
  1. Install pygame
  2. Ensure that Python 2.7 is in use
  3. Download files and run the code.py file

### How to Play
  1. Use the *right* and *left* arrow keys to move the player left and right
  2. Use the *up* arrow key to jump
  3. To fire bullets, use the *space bar*

### Objectives
Pass all the levels before all the lives are lost and get a high score by collecting as many stars as possible. The player
begins with 5 lives on each run of the game. The player should jump from cloud to cloud collecting stars in order to reach the
final pink cloud in each level. Throughout the level, the player should avoid hitting the floor or the enemy, as this bumps
them back to the beginning of the level and causes them to lose 50 points as well as a life. The enemies can be removed by
shooting them with bullets in order to clear the path forward. There are also diamonds in various locations that give the
player a boost when collected by increasing their size for a short period of time, allowing them to reach the end of the level
more quickly. The player wins the game when they reach the final platform in the last level.
  
## Features
  1. Enemy
    * can be killed by a bullet (+50 points)
    * player loses a life if collision with enemy and starts over
  2. Star
    * +50 points when collected
    * appears over random platforms on each run of the game (2/3 randomization based on the number of the platforms)
  3. Diamond
    * increases the player's size by 8%
    * may be stationary on platform or moving throughout the level
  4. Sound Effects
    * self-created sound effects
  5. Images
    * self-created images
