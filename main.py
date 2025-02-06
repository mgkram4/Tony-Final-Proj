import random

from flask import Flask, jsonify, render_template
from sklearn import svm

app = Flask(__name__)


def move_to_beat(move):
  if move == 1:
    return 2
  elif move == 2:
    return 3
  else:
    return 1

history = [1, 2, 3, 1, 1, 2, 3, 2, 1, 2, 3, 3, 2, 3, 1, 2, 2, 1, 3, 2, 1, 3]


input_p1 = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
]
output_p1 = [2, 3, 1, 1]
model = svm.SVC()
model.fit(input_p1, output_p1)

def getPlayer1():
  data_record = [history[-18], history[-17], history[-16], history[-15], history[-14], history[-13],
           history[-12], history[-11], history[-10], history[-9], history[-8], history[-7],
           history[-6], history[-5], history[-4], history[-3], history[-2], history[-1]]
  prediction = model.predict([data_record])[0]
  return move_to_beat(prediction)

history_p2 = [1, 2, 3, 1]

input_p2 = [
  [1, 1, 1, 1],
  [2, 2, 2, 2],
  [3, 3, 3, 3],
  [1, 2, 3, 1]
]
output_p2 = [2, 3, 1, 1]
model2 = svm.SVC()
model2.fit(input_p2, output_p2)

def getPlayer2():
  data_record = [history_p2[-4], history_p2[-3], history_p2[-2], history_p2[-1]]
  prediction = model2.predict([data_record])[0]
  return move_to_beat(prediction)

wins_player1 = 0
wins_player2 = 0
total_ties = 0

# Add these global variables to store results
game_results = []
current_round = 0

@app.route('/')
def index():
    return render_template('index.html', results=game_results)

@app.route('/simulate', methods=['POST'])
def simulate():
    global current_round, game_results
    
    # Reset stats for this round
    wins_player1 = 0
    wins_player2 = 0
    total_ties = 0
    
    # Run 50 games
    for i in range(1000):
        player1 = getPlayer1()
        player2 = getPlayer2()
        
        if player1 == 1 and player2 == 1:
            wins_player2 += 1
        elif player1 == 1 and player2 == 2:
            wins_player1 += 1
        elif player1 == 1 and player2 == 3:
            wins_player1 += 1
        elif player1 == 2 and player2 == 1:
            wins_player2 += 1
        elif player1 == 2 and player2 == 2:
            wins_player2 += 1
        elif player1 == 2 and player2 == 3:
            wins_player1 += 1
        elif player1 == 3 and player2 == 1:
            total_ties += 1
        
        # Update models as before
        history.append(player2)
        input_p1.append([history[-19], history[-18], history[-17], history[-16], history[-15], history[-14],
                 history[-13], history[-12], history[-11], history[-10], history[-9], history[-8],
                 history[-7], history[-6], history[-5], history[-4], history[-3], history[-2]])
        output_p1.append(history_p2[-1])
        model.fit(input_p1, output_p1)
        
        history_p2.append(player1)
        input_p2.append([history_p2[-5], history_p2[-4], history_p2[-3], history_p2[-2]])
        output_p2.append(history_p2[-1])
        model2.fit(input_p2, output_p2)
    
    current_round += 1
    round_results = {
        'round': current_round,
        'player1_wins': wins_player1,
        'player2_wins': wins_player2,
        'ties': total_ties
    }
    game_results.append(round_results)
    
    return jsonify(round_results)

if __name__ == '__main__':
    app.run(debug=True)