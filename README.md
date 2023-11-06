# patmag
Minigame for TTRPG wizard player

```python
from patmag import pattern, board

p = pattern.Pattern(height=2, width=3)
p.set_contents("-f-ses") # first row blank-fire-blank, second row sun-earth-sun

b = board.Board() # 9x9

b.write(p, 2, 3) # write pattern to board with offset of 2 rows and 3 cols

b.save("/foo/bar/smiting_fire.ptn") # save pattern or board definition to .ptn file

b.visualize("/foo/bar/smiting_fire.png") # create pretty visualization of pattern or board

b.contains(p) # True
```