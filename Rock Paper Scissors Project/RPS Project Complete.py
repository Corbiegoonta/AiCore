from IPython.display import clear_output
import time
import statistics
import cv2
from keras.models import load_model
import numpy as np
import random



def rockpaperscissors():
    def visual():
        model = load_model(r"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Rock Paper Scissors Project\converted_keras\keras_model.h5", compile=False)
        cap = cv2.VideoCapture(0)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        choice_list = ["nothing", "rock", "paper", "scissors"]
        choice_number = []
        start_time = time.time()
        end_time = time.time()
        final_time = end_time - start_time
        while final_time < 10.0: 
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            cv2.imshow('frame', frame)
            # Press q to close the window
            if prediction[0][0] == max(prediction[0]):
               choice_number.append(0)
            elif prediction[0][1] == max(prediction[0]):
                choice_number.append(1)
            elif prediction[0][2] == max(prediction[0]):
                choice_number.append(2)
            elif prediction[0][3] == max(prediction[0]):
                choice_number.append(3)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            final_choice = statistics.mode(choice_number)
            end_time = time.time()
            final_time = end_time - start_time
            
        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        print(choice_list[final_choice])
        return choice_list[final_choice]
        
    def player1_choose():
        ready_check = True
        while ready_check is True:
            try:
                ready = (input("Press s to make your choice\n")).lower()
                if ready == "s":
                    print("Player 1 choose Rock, Paper or Scissors: ")
                    choice = visual()
                    if choice == "rock" or choice == "paper" or choice == "scissors":
                        ready_check = False
                    else:
                        print("Sorry the camera didn't get that. Please try again. Please choose Rock, Paper or Scissors.")
                else:
                    print("This is an invalid input.")
            except Exception as e:
                print(e)
                print("This is an invalid input. Please input a string.")

        player1 = None

        if choice == "rock":
            player1 = choice
        elif choice == "paper":
            player1 = choice
        elif choice == "scissors":
            player1 = choice

        return (player1).title()

    def player2_choose():
        ready_check = True
        while ready_check is True:
            try:
                ready = (input("Press s to make your choice\n")).lower()
                if ready == "s":
                    print("Player 2 choose Rock, Paper or Scissors: ")
                    choice = visual()
                    if choice == "rock" or choice == "paper" or choice == "scissors":
                        ready_check = False
                    else:
                        print("Sorry the camera didn't get that. Please try again. Please choose Rock, Paper or Scissors.")
                else:
                    print("This is an invalid input.")
            except Exception:
                print("This is an invalid input. Please input a string.")
        
        player2 = None

        if choice == "rock":
            player2 = choice
            
        elif choice == "paper":
            player2 = choice
            
        elif choice == "scissors":
            player2 = choice
            
        return (player2).title()

    def outcome(choice1, choice2):
        if choice1 == "Rock" and choice2 == "Scissors":
            print(f"Player 1 wins round {round_counter + 1}!")
            return 1
        elif choice1 == "Paper" and choice2 == "Scissors":
            print(f"Player 2 wins round {round_counter + 1}!")
            return 2
        elif choice1 == "Scissors" and choice2 == "Rock":
            print(f"Player 2 wins round {round_counter + 1}!")
            return 2
        elif choice1 == "Paper" and choice2 == "Rock":
            print(f"Player 1 wins round {round_counter + 1}!")
            return 1
        elif choice1 == "Rock" and choice2 == "Paper":
            print(f"Player 2 wins round {round_counter + 1}!")
            return 2
        elif choice1 == "Scissors" and choice2 == "Paper":
            print(f"Player 1 wins round {round_counter + 1}!")
            return 1
        elif choice1 == choice2:
            print("It's a draw!")
            return 0
        
    def computer():
        computer_choices = ["Rock", "Paper", "Scissors"]
        return random.choice(computer_choices)
    
    def clear():
        clear_output(wait=True)

    clear()
    game_on = True
    while game_on is True:
        print("Welcome to the Rock, Paper, Scissors game!")
        checks = True
        game_type_check = True
        round_check = True
        while checks is True:
            try:
                while game_type_check is True:
                    game_type = int(input("Do you want to play Singleplayer or Multiplayer mode? (Input 1 for Singleplayer , 2 for Multiplayer)\n"))
                    if game_type == 1 or game_type == 2:
                        game_type_check = False
                        while round_check is True:
                            number_of_rounds = int(input("How many rounds do you want to play this game?\n"))
                            if number_of_rounds % 2 == 0:
                                print("Sorry this is an invaid input. Please input an odd integer number.")
                            else:
                                round_check = False
                                checks = False
                    else:
                        print("This input is invaild. Please choose either 1 or 2.")
            except Exception:
                print("Sorry this is an invaid input. Please input an integer number.")
        

        player1_score = 0

        player2_score = 0

        
        round_on = True
        round_counter = 0
        while round_on is True:
            if game_type == 1:
                opponent = computer()
            else:
                opponent = player2_choose()

            player1_choice = player1_choose()
            print(f"Player 1 chooses: {player1_choice}")

            print(f"Player 2 chooses: {opponent}")

            winner = outcome(player1_choice, opponent)
            
            if winner == 1:
                player1_score += 1
                round_counter += 1
            elif winner == 2:
                player2_score += 1
                round_counter += 1

            print(f"The score is {player1_score} : {player2_score}")
            
            print(round_counter, number_of_rounds)
            
            if round_counter == number_of_rounds and player1_score != player2_score:
                print(f"Game over! The final score is {player1_score} : {player2_score}.")
                if player1_score > player2_score:
                    print("Player 1 won the game!")
                else:
                    print("Player 2 won the game!")
                play_again_type_check = True
                play_again_check = True
                while play_again_check is True:
                    try:
                        play_again = (input("Do you want to play again? (Yes/No)\n")).lower()
                        if play_again == "yes" or play_again == "no":
                            play_again_check = False
                            round_on = False
                        else:
                            print("That is an invaild input. Please choose Yes or No.")
                    except Exception:
                        print("That is an invaild input. Please choose the string Yes or No.")
                if play_again == "no":
                    game_on = False
                    round_on = False
                    print("Thank you for playing Roack, Paper, Scissors.")

rockpaperscissors()
