import math

# plot a sinusoidal curve around 80 degrees F / 25.56 C
# 
# 90 F = 32.2222222222 C 
# 85 F = 29.4444444444 C
# 80 F = 26.6666666667 C
# 75 F = 23.8888888889 C
# 70 F = 21.1111111111 C

def f2c(t):
	return (t-32.0)*(5.0/9.0)

def c2f(t):
	return (t*9.0/5.0)+32.0

print f2c(72)

TARGET_TEMPERATURE=26.67
LOWER_CONTROL_LIMIT=23.88
UPPER_CONTROL_LIMIT=29.44
LOWER_ALERT_LIMIT=19.00
UPPER_ALERT_LIMIT=31.00


for i in range(0,628,1):
	print TARGET_TEMPERATURE+(UPPER_ALERT_LIMIT-LOWER_ALERT_LIMIT)*math.sin(i)


# vim: ts=4
