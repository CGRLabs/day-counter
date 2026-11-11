# How many whole days the world has been through, on the action bar.
#
# The day is the world's clock divided by the length of a day: Horizon's clock
# counts up, so this is the day the world is on, the same number as
# /time query day.
execute store result score $day daycounter run time query time
scoreboard players operation $day daycounter /= #ticks_per_day daycounter
scoreboard players add $day daycounter 0
title @a actionbar [{"text":"DAY ","color":"white"},{"score":{"name":"$day","objective":"daycounter"}}]
