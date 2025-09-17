from flask import Flask, render_template, request, jsonify
import os
import re
from parser import Parser
from poteq import Poteq

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def finalcalc(blob):
    PREFLOP = {}
    FLOP = {}
    TURN = {}
    RIVER = {}

    parser = Parser(blob)
    preflop = parser.PREFLOP()
    flop = parser.FLOP()
    turn = parser.TURN()
    river = parser.RIVER()
    
    if not preflop and not flop:
        return 'Didnt play Hand'
    else:
        if preflop:
            for bets in preflop:
                q = r'raise.+'
                numvill = preflop[bets][2]
                pot_odds = float(preflop[bets][0]) * 100 / float(preflop[bets][1])
                if re.match(q, bets):
                    numvill = preflop[bets][3]
                    pot_odds = float(preflop[bets][0]) * 100 / (float(preflop[bets][2]) - float(preflop[bets][1]) + float(preflop[bets][0]))

                poteq = Poteq(numvill, [], blob)
                PREFLOP[bets] = (round(poteq.poteq(), 2), round(pot_odds, 2))

        if flop:
            for bets in flop:
                q = r'raise.+'
                numvill = flop[bets][2]
                pot_odds = float(flop[bets][0]) * 100 / float(flop[bets][1])
                if re.match(q, bets):
                    numvill = flop[bets][3]
                    pot_odds = float(flop[bets][0]) * 100 / (float(flop[bets][2]) - float(flop[bets][1]) + float(flop[bets][0]))
                poteq = Poteq(numvill, parser.Comm_cards['FLOP'], blob)
                FLOP[bets] = (round(poteq.poteq(), 2), round(pot_odds, 2))

        if turn:
            for bets in turn:
                q = r'raise.+'
                numvill = turn[bets][2]
                pot_odds = float(turn[bets][0]) * 100 / float(turn[bets][1])
                if re.match(q, bets):
                    numvill = turn[bets][3]
                    pot_odds = float(turn[bets][0]) * 100 / (float(turn[bets][2]) - float(turn[bets][1]) + float(turn[bets][0]))
                poteq = Poteq(numvill, parser.Comm_cards['TURN'], blob)
                TURN[bets] = (round(poteq.poteq(), 2), round(pot_odds, 2))

        if river:
            for bets in river:
                q = r'raise.+'
                numvill = river[bets][2]
                pot_odds = float(river[bets][0]) * 100 / float(river[bets][1])
                if re.match(q, bets):
                    numvill = river[bets][3]
                    pot_odds = float(river[bets][0]) * 100 / (float(river[bets][2]) - float(river[bets][1]) + float(river[bets][0]))
                poteq = Poteq(numvill, parser.Comm_cards['RIVER'], blob)
                RIVER[bets] = (round(poteq.poteq(), 2), round(pot_odds, 2))

        return PREFLOP, FLOP, TURN, RIVER, preflop, flop, turn, river

def analyze_hands(file_content):
    hands_data = []
    lines = file_content.split('\n')
    
    q = r'\^*+\W+\#\W+(\d+)'
    
    for idx, line in enumerate(lines):
        if re.match(q, line):
            Hand_num = re.findall(q, line)[0]
            
            # Find the end of this hand
            hand_end = len(lines)
            for ind, subline in enumerate(lines[idx+1:], start=idx+1):
                if re.match(q, subline) and re.findall(q, subline)[0] != Hand_num:
                    hand_end = ind
                    break
            
            # Extract hand data
            hand_blob = lines[idx+1:hand_end]
            result = finalcalc(hand_blob)
            
            if result != 'Didnt play Hand':
                PREFLOP, FLOP, TURN, RIVER, preflop, flop, turn, river = result
                
                # Get hero's hole cards
                parser = Parser(hand_blob)
                hero_cards = []
                if parser.Hands:
                    for card in parser.Hands:
                        hero_cards.append(get_card_emoji(card))
                
                hand_analysis = {
                    'hand_number': Hand_num,
                    'hero_cards': hero_cards,
                    'preflop': analyze_street(PREFLOP, 'PREFLOP', preflop),
                    'flop': analyze_street(FLOP, 'FLOP', flop, parser.Comm_cards.get('FLOP', [])),
                    'turn': analyze_street(TURN, 'TURN', turn, parser.Comm_cards.get('TURN', [])),
                    'river': analyze_street(RIVER, 'RIVER', river, parser.Comm_cards.get('RIVER', []))
                }
                hands_data.append(hand_analysis)
    
    return hands_data

def get_card_emoji(card):
    """Convert card string to emoji representation"""
    if not card:
        return ""
    
    suit_map = {
        's': '♠️',  # spades
        'h': '♥️',  # hearts  
        'd': '♦️',  # diamonds
        'c': '♣️'   # clubs
    }
    
    if len(card) >= 2:
        rank = card[:-1]
        suit = card[-1].lower()
        return f"{rank}{suit_map.get(suit, suit)}"
    return card

def analyze_street(street_data, street_name, raw_data, comm_cards=None):
    if not street_data:
        return []
    
    analysis = []
    for action, (pot_equity, pot_odds) in street_data.items():
        # Get raw action data for bet amounts and pot size
        raw_action_data = raw_data.get(action, [])
        bet_amount = raw_action_data[0] if len(raw_action_data) > 0 else 0
        pot_after = raw_action_data[1] if len(raw_action_data) > 1 else 0
        
        # Convert action format: call1 -> 1st Call, bet2 -> 2nd Bet, raise1 -> 1st Raise
        if action.startswith('call'):
            number = action.replace('call', '')
            action_display = f"{number}st Call" if number == '1' else f"{number}nd Call" if number == '2' else f"{number}rd Call" if number == '3' else f"{number}th Call"
            action_detail = f"Call ₹{bet_amount}"
        elif action.startswith('bet'):
            number = action.replace('bet', '')
            action_display = f"{number}st Bet" if number == '1' else f"{number}nd Bet" if number == '2' else f"{number}rd Bet" if number == '3' else f"{number}th Bet"
            action_detail = f"Bet ₹{bet_amount}"
        elif action.startswith('raise'):
            number = action.replace('raise', '')
            action_display = f"{number}st Raise" if number == '1' else f"{number}nd Raise" if number == '2' else f"{number}rd Raise" if number == '3' else f"{number}th Raise"
            if len(raw_action_data) > 2:
                raise_to = raw_action_data[2]
                action_detail = f"Raise to ₹{raise_to}"
            else:
                action_detail = f"Raise ₹{bet_amount}"
        else:
            action_display = action
            action_detail = action
        
        if pot_equity > pot_odds:
            justification = f"{action_display} justified"
            color = "success"
        else:
            justification = f"{action_display} not justified"
            color = "danger"
        
        # Get community cards for this street
        street_cards = []
        if comm_cards:
            for card in comm_cards:
                if card:
                    street_cards.append(get_card_emoji(card))
        
        # Get number of active villains for this action
        num_villains = raw_action_data[2] if len(raw_action_data) > 2 else 0
        
        analysis.append({
            'action': action,
            'action_display': action_display,
            'action_detail': action_detail,
            'bet_amount': bet_amount,
            'pot_after': pot_after,
            'pot_equity': pot_equity,
            'pot_odds': pot_odds,
            'justification': justification,
            'color': color,
            'street_cards': street_cards,
            'num_villains': num_villains
        })
    
    return analysis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        try:
            file_content = file.read().decode('utf-8')
            hands_data = analyze_hands(file_content)
            return jsonify({'hands': hands_data})
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
