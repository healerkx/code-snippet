

p [1,2,3,1, 2, 3, 92].inject{|s, i| s^i}


python_one_line = <<PYTHON_CODE
print reduce(lambda x, y: x ^ y,  [2, 7, 2, 1, 1, 3, 3])
PYTHON_CODE