  # WormLang - Interpreter written in Python

---

# WormLang Interpreter

WormLang is a lightweight and versatile programming language designed to facilitate basic arithmetic, logical operations, conditional statements, loops, functions, recursion, lambda expressions, print statements, and more. The WormLang interpreter allows you to execute `.worm` files that follow the syntax defined for this language.

## Features

- **Arithmetic Operations**: Supports addition, subtraction, multiplication, division, and modulus.
- **Logical Operations**: Includes AND, OR, and NOT operations.
- **Control Structures**: IF statements and FOR loops for flow control.
- **Functions**: Define and invoke single-line functions with support for recursion.
- **Lambda Expressions**: Anonymous functions executed with given parameters.
- **I/O Operations**: Print to the console and read from `.worm` files.

## Installation

To use the WormLang interpreter, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wormlang.git
   ```
2. Navigate to the project directory:
   ```bash
   cd wormlang
   ```
3. Run the interpreter on a `.worm` file:
   ```bash
   python Main.py path/to/yourfile.worm
   ```

## Basic Syntax

Here are some basic examples to get you started with WormLang:

### Arithmetic Operations
```worm
LET add(x, y) : x + y END
LET subtract(x, y) : x - y END
LET multiply(x, y) : x * y END
LET divide(x, y) : x / y END
LET modulo(x, y) : x % y END

PRINT( add(1, 2) )        # Output: 3
PRINT( subtract(5, 3) )   # Output: 2
PRINT( multiply(3, 4) )   # Output: 12
PRINT( divide(10, 2) )    # Output: 5
PRINT( modulo(10, 3) )    # Output: 1
```

### Logical Operations
```worm
LET and(x, y) : x AND y END
LET or(x, y) : x OR y END
LET not(x) : NOT x END

PRINT( and(TRUE, FALSE) )  # Output: FALSE
PRINT( or(TRUE, FALSE) )   # Output: TRUE
PRINT( not(TRUE) )         # Output: FALSE
```

### Conditional Statements
```worm
IF x == 5 THEN
    PRINT("x is 5")
ELSE
    PRINT("x is not 5")
END
```

### Loops
```worm
FOR i = 1 TO 5 DO
    PRINT(i)
END
```

### Functions
```worm
LET factorial(n) : IF n == 0 THEN 1 ELSE n * factorial(n - 1) END

PRINT( factorial(5) )  # Output: 120
```

### Lambda Expressions
Lambda expressions in WormLang are declared and then executed by providing values in parentheses:

```worm
LAMBDA (x) : x * x END (5)  # Output: 25
LAMBDA (x) : x + 5 END (10) # Output: 15
```

## Running WormLang Files

To run a `.worm` file, use the following command:
```bash
python Main.py your_script.worm
```

## Credits

Created by Amit Bar Kama & Lenny Medina as a final project for Programming Languages course
