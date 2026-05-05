Date: 2026/04/08, 1pm
**Goal**
Adding a background image and block texture

**Implementation**
Technical Plan/Credit:Raylib reference, lab04 code, project01 code
Content Credit:
https://opengameart.org/content/paper-textures-seamless
https://opengameart.org/content/seamless-sky-backgrounds

Commit Message: feat(drawing):Add background and block texture
Next TODO:

- Improve enemies
- Level loading

Date: 2026/04/08, 14:00
**Goal**
Improving enemy AI to chase the player
**Implementation**
Technical Plan/Credit:Raylib reference, https://www.davepagurek.com/blog/enemy-ai/
Content Credit:

Commit Message: feat(enemies): add basic enemy AI

Next TODO:

- Level Loading improvements
- Player and enemy animations

Date: 2026/04/08, 14:30
**Goal**
Load the level from an external file
**Implementation**
Technical Plan/Credit: https://www.w3schools.com/python/python_file_open.asp
Content Credit: Some AI was used as a consultant and debugger

Commit Message: feat(QoL): load levels from files

Next TODO:

- Level Loading improvements
- Player and enemy animations

Date 2026/04/15, 13:30
**Goal**
Refactor game to separate the components from a single file
**Implementation**
Technical Plan/Credit: I'm going to be following the same structure as in my midterm game
Content Credit: Inspiration from this class
Commit Message: Refactor the game structure

Date 2026/04/20, 00-30
**Goal**
Look into Falling sand rules and have a basic implementation
Finish the refactor and implement it.
**Implementation**
Technical Plan/Credit:
Content Credit: https://jason.today/falling-sand

Commit Message: Feature: Basic falling sand simulation and refactor

Next TODO:

- Do not simulate sand that hasn't been interacted with, propagate interactions to neighbours
- Possibly divide sand into smaller or bigger particles?

Date 2026/04/20, 14-30
**Goal**
Have the falling sand collide with the player
**Implementation**
Technical Plan/Credit: AABB implementation for tiles currently in the project, some debugging with the help of AI was done for finetuning the ground toggling.

Content Credit:

Commit Message: Improved Falling sand

Next TODO:

- Rock Throwing
- Do not simulate sand that hasn't been interacted with, propagate interactions to neighbours

Date 2026/04/20, 16-00
**Goal**
Throw rocks to make sand clumps fall
**Implementation**
Technical Plan/Credit: Class material for the rock trajectory, AI with the recursive nature of toggling the sand grains active
Content Credit:

Commit Message: Feature: Throwable rocks, falling clumps of sand

Next TODO:

- Sand damage to both the player and enemies when falling
- Start bringing assets

Date 2026/04/22, 17-00
**Goal**
Refine the sand clump falling
**Implementation**
Just a regular while loop with a stack

Commit Message: Bugfix: Sand, added extra materials

Next TODO:

- Sand Damage
- Bring MORE assets

Date 2026/04/22, 12-45
**Goal**
Add Sand crushing to both player and enemies, add mineable block type
**Implementation**
Technical Plan/Credit: Just coding with some debugging help from AI
Commit Message: Feature: Sand Crushing, mineable block type

Next TODO:

- Gems
- Level One Design
- Add assets

Date 2026/04/28, 04-00
**Goal**
Add a preliminary level one, along with a mining ability, adjust tile size and the camera positon.
**Implementation**
Technical Plan/Credit: Google sheets was used to create the levels, inspired by Edgar's approach
Commit Message: Level one, mining ability, minor adjustments.

Next TODO:

- Gems
- Dynamite
- Add assets

Date 2026/04/28, 12-45
**Goal**
Add most important assets with animations, fix enemy behaviour, expand level 1
**Implementation**
Technical Plan/Credit: Coolors color picker was used to pick some colors, gemini and chatGPT image generation was used to generate the basic assets which were then edited with GIMP.
Commit Message: Added player and enemy assets, expanded level 1, fixed enemy behaviour.

Next TODO:

- Gems
- Dynamite
- Slight enemy fix

Date 2026/04/29 12-45
**Goal**
Change enemy sprite, further fix enemy interactions with sand, subdivide sand particles
**Implementation**
Technical plan: Just my hard own thinking :), reused the sand step code from the player
Enemy sprite available at https://opengameart.org/content/super-dead-gunner-new-enemy-grenademortar-guy

Commit Message: Enemy update, sand refining.

Next TODO:

- Gems
- Dynamite
- Level 2 implementation
- Bring extra assets
- Dialogues/menus,etc.

Date 2026/05/01 16-00
**Goal**
Clean up unused materials, add the assets

**Implementation**
Gems from https://opengameart.org/content/32x32-pixel-gems
Dynamite from https://tumas81.itch.io/minerman-adventure
Final Background generated with gemini
Egg sprite manually traced over from the picture
Tent Sprite from https://www.dreamstime.com/camping-tent-pixel-art-bit-tourist-isolated-pixelated-vector-illustration-image277660178
traced over

Commit Message: Added all the necessary assets, removed unused ones
Next TODO:
Add gameplay changes with these assets
Implement menus, gameover state, pause
Implement SFX

Date 2026/05/01 22-00
**Goal**
Add the final proposed features for the game
**Implementation**
Changed gems to be their own class
Small changes to stone with the help of AI to fix some movement bugs
Lowered the tile size and reworked the levels 
Implemented dynamite that destroys mineable, sand, kills the player and enemies when it explodes

Commit Message
Added dynamite,gems, and lowered the tile size.

Next TODO:
Implement menus, gameover state, pause
Implement SFX
Make level 2


**Goal**
Add the final proposed features for the game
**Implementation**
Finished level 2
Made dynamites be chainable
Added the egg collectable that advances the game
Improved the enemy pathfinding
refactored the sand_game to be instantiable to a specific level
made it so you can now mine sand with the picaxe
added the menus and transitions between levels

Commit Message
Finished level 2, various feature improvements
Next TODO:
Implement pause, and a reset button
Implement SFX
add introduction to the game

**Goal**
Add all the necessary menus and missing assets to the game
**Implementation**
Gimp and Gemini image generation for the title screen 
Added pause and reset level function
Added a small introduction to the game

Commit Message:
FINAL COMMIT: Added a small introduction, pause and reset.
Next TODO:
Implement SFX

**Goal**
Added the GDD and the game trailer link.
**Implementation**
Davinci Resolve for editing the game trailer
Added extra images meant to be used with the Game Design Document
Fixed the win screen text layout

Commit Message:
Added the GDD and the game trailer link, fixed text.

Unfinished TODO:
Implement SFX
Add music to the game