import sys
import time
import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_questions():
    questions = []
    
    # Divisible by (your favorite style)
    for d in range(2, 11):
        questions.append({
            "text": f"Is your number divisible by {d}?",
            "func": lambda x, d=d: x % d == 0
        })
    
    # Contains digit
    for d in range(10):
        questions.append({
            "text": f"Does your number contain the digit {d}?",
            "func": lambda x, d=d: str(d) in str(x)
        })
    
    # Ends with digit
    for d in range(10):
        questions.append({
            "text": f"Does your number end with {d}?",
            "func": lambda x, d=d: x % 10 == d
        })
    
    # Bonus strong questions
    questions.append({
        "text": "Is your number a prime number?",
        "func": is_prime
    })
    
    questions.append({
        "text": "Is your number a perfect square?",
        "func": lambda x: int(math.sqrt(x)) ** 2 == x
    })
    
    questions.append({
        "text": "Is the sum of digits in your number even?",
        "func": lambda x: sum(int(d) for d in str(x)) % 2 == 0
    })
    
    return questions

def clear_screen():
    print("\033c", end="")  # Clear terminal

def print_header():
    print("\033[1;32m" + "="*60 + "\033[0m")
    print("\033[1;36m                  NUMBER-GUESSER\033[0m")
    print("\033[1;32m" + "="*60 + "\033[0m")
    print("   Hi Mayon! Think of any number between 0 and 100")
    print("   I'll guess it by asking smart yes/no questions\n")

def main():
    candidates = set(range(101))
    questions = generate_questions()
    question_history = []
    
    clear_screen()
    print_header()
    
    print("🤖 Starting Number-guesser...\n")
    time.sleep(1.2)
    
    while len(candidates) > 1:
        # Find the best question (most balanced split)
        best_question = None
        best_score = -1
        best_func = None
        
        for q in questions:
            yes_count = sum(1 for c in candidates if q["func"](c))
            no_count = len(candidates) - yes_count
            if yes_count == 0 or no_count == 0:
                continue
            score = min(yes_count, no_count)
            if score > best_score:
                best_score = score
                best_question = q["text"]
                best_func = q["func"]
        
        if best_question is None:
            # Fallback: ask one by one
            fallback = min(candidates)
            best_question = f"Is your number {fallback}?"
            best_func = None
        
        print(f"\033[1;33mQ: {best_question}\033[0m")
        while True:
            ans = input("\033[1;37mYour answer (yes/no): \033[0m").strip().lower()
            if ans in ["yes", "y"]:
                answer = True
                break
            elif ans in ["no", "n"]:
                answer = False
                break
            else:
                print("Please type 'yes' or 'no'")
        
        question_history.append((best_question, "Yes" if answer else "No"))
        
        # Filter candidates
        new_candidates = set()
        for c in candidates:
            if best_func is None:  # fallback case
                if (answer and c == fallback) or (not answer and c != fallback):
                    new_candidates.add(c)
            else:
                if (answer and best_func(c)) or (not answer and not best_func(c)):
                    new_candidates.add(c)
        candidates = new_candidates
        
        print(f"\033[1;32m→ Remaining possibilities: {len(candidates)}\033[0m\n")
        time.sleep(0.4)
    
    # Result
    if len(candidates) == 1:
        guessed = next(iter(candidates))
        print("\033[1;35m" + "═"*60 + "\033[0m")
        print(f"\033[1;32m🎉 I GOT IT! Your number is \033[1;37m{guessed}\033[0m")
        print("\033[1;35m" + "═"*60 + "\033[0m")
    else:
        print("Something went wrong... no number left!")
    
    # Show summary
    print("\nQuick summary of questions I asked:")
    for q, a in question_history[-8:]:  # last 8 only
        print(f"   • {q} → {a}")
    
    print("\nThanks for playing, Mayon! 🎮")
    input("\nPress Enter to play again or Ctrl+C to exit...")

if __name__ == "__main__":
    try:
        while True:
            main()
            print("\n" + "-"*60)
    except KeyboardInterrupt:
        print("\n\n👋 Bye Mayon! See you next time in Nagpur.")
        sys.exit(0)
