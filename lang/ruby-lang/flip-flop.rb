
############################################################
# 5 6 7 8 Should be the Result.
# If branch would be true when i == 5, then it would be true always, till i == 8.
# When i == 9, it would be false.
(1..9).each{|i| p i  if i % 5 == 0 .. i % 8 == 0 }

