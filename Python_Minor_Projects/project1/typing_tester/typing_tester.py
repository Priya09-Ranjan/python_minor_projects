import time
import random

# Sample sentences for typing test
sentences = [
    "Python is an amazing and beginner friendly programming language.",
    "Artificial intelligence and machine learning are changing the world.",
    "Consistency and daily practice are the keys to becoming a good developer.",
    "Git and GitHub help developers manage and share their code easily."
]

def show_bubble_animation():
    """Terminal bubble floating animation."""
    print("\n" + " " * 15 + "🫧 CONGRATULATIONS! 🫧")
    
    # Simple ASCII bubble frames moving up
    bubble_frames = [
        "       .       o        O        .       ",
        "     o    .        O        .        o   ",
        "  .     O      .        o       O        ",
        "     (o)     (O)     ( o )    ( O )      ",
        "  🫧    🫧     🫧      🫧     🫧     "
    ]
    
    for frame in bubble_frames:
        print(frame)
        time.sleep(0.3)  # Small delay for animation effect
    print("\n")

def run_typing_test():
    # Loop for playing again and again
    while True:
        print("=" * 50)
        print("         WELCOME TO TYPING SPEED TESTER         ")
        print("=" * 50)
        
        target_sentence = random.choice(sentences)
        
        print("\nType the following sentence as fast and accurately as you can:\n")
        print(f'"{target_sentence}"\n')
        
        input("Press ENTER when you are ready to start...")
        print("\nSTART TYPING NOW!\n")
        
        start_time = time.time()
        user_input = input("> ")
        end_time = time.time()
        
        time_taken = round(end_time - start_time, 2)
        words_typed = len(user_input.split())
        wpm = round((words_typed / time_taken) * 60) if time_taken > 0 else 0
        
        target_words = target_sentence.split()
        typed_words = user_input.split()
        
        correct_words = 0
        for w1, w2 in zip(target_words, typed_words):
            if w1 == w2:
                correct_words += 1
                
        accuracy = round((correct_words / len(target_words)) * 100, 2) if len(target_words) > 0 else 0
        
        # Trigger the Bubble Animation
        show_bubble_animation()
        
        # Display Results
        print("=" * 35)
        print("           YOUR RESULTS           ")
        print("=" * 35)
        print(f"Time Taken  : {time_taken} seconds")
        print(f"Typing Speed: {wpm} Words Per Minute (WPM)")
        print(f"Accuracy    : {accuracy}%")
        print("=" * 35)
        
        # Ask user if they want to play again (Looping mechanism)
        print("\n" + "-" * 35)
        choice = input("Do you want to try again? (y/n): ").strip().lower()
        print("-" * 35 + "\n")
        
        if choice != 'y':
            print("Thanks for playing! Happy Coding! 👋")
            break

if __name__ == "__main__":
    run_typing_test()
