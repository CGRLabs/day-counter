# How many whole days the world has been through, on the action bar.
#
# The day is the world's clock divided by the length of a day: Horizon's clock
# counts up, so this is the day the world is on, the same number as
# /time query day.
#
# When the Day Tally native mod is installed it draws the day itself, in the
# corner, and sets #day_tally here; this line then stands down, so the day is
# not shown twice.
execute store result score $day daycounter run time query time
scoreboard players operation $day daycounter /= #ticks_per_day daycounter
scoreboard players add $day daycounter 0
execute unless score #day_tally daycounter matches 1 run title @a actionbar [{"text":"DAY ","color":"white"},{"score":{"name":"$day","objective":"daycounter"}}]
