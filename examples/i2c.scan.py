from machine import I2C
i2c = I2C(0)
print(i2c.scan())