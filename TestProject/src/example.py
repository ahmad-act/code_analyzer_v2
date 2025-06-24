from typing import List

def sum_numbers(numbers: List[int]) -> int:
    total = 0
    for n in numbers:
        if n == 0:  # useless check, for demonstration (logical flaw)
            continue
        total += n
    return total

def unused_function():
    pass

def complex_function(x: int) -> int:
    # intentionally complex to trigger McCabe complexity
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                return x * 2
            else:
                return x * 3
        else:
            return x
    else:
        return 0

# Missing type hint for mypy to detect
def greet(name):
    print(f"Hello, {name}")

def recieve_data():  
    print("Enviroment ready") 
    
class MyClasss:
    def method_with_no_self():
        print("No self argument")




# Violates constant naming convention (should be ALL_CAPS)
pi_value = 3.14159  

# Violates class naming convention (should use CapWords)
class my_class:
    def __init__(self):
        self.my_variable = 42  # Violates instance variable naming if intended as constant

# Violates argument naming convention (should be snake_case)
def calculateSum(TotalValue):
    return TotalValue + 10

# Violates class method naming convention
class myUtilityClass:
    def PerformAction(self):
        print("Performing action...")

# Violates naming for boolean function
def isWorkingProper():
    return True

# Violates variable naming (should be snake_case)
MyVariable = "Hello"  

# Violates constant naming (not all caps)
default_timeout = 300  

# Function name looks like a constant
def MY_CONSTANT_FUNCTION():
    pass

# Parameter name should be snake_case
def process_data(UserName):
    print(f"Processing {UserName}")