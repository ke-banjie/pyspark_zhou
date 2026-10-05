import pandas as pd

a = [1, 2, 3]

myvar = pd.Series(a)

print(myvar)
print(myvar[1])

#-------------------
print('-'*30)

sites = {1: "Google", 2: "Runoob", 3: "Wiki"}

myvar = pd.Series(sites)

print(myvar)