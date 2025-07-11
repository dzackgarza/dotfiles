def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def main():
    print("Hello from main.py")
    n = 10  # Example: Calculate the 10th Fibonacci number
    result = fibonacci(n)
    print(f"The {n}th Fibonacci number is: {result}")

if __name__ == "__main__":
    main()
