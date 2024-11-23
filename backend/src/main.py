def main():
    print("Hello from backend!")


def is_prime(n: int):
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


if __name__ == "__main__":
    print(is_prime(7))
    main()
