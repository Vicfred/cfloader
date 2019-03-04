from codeforces import Methods

if __name__ == "__main__":
    programmers = ["Vicfred", "rng_58", "iwiwi"]
    users = Methods.user_info(programmers)
    for user in users:
        print(user)
