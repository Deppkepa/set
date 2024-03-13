from flask import Flask, request, jsonify
import json
import secrets
import random

app = Flask(__name__)
box = []


def proverka_a(a, set_cards):
    for i in range(len(set_cards)):
        if set_cards == a:
            a = random.randint(1, 81)
    return a


def create_gameid(text):
    count = 0
    for t in range(len(text['games'])):
        print(text['games'][t]['id'])
        if text['games'][t]['id'] > count:
            count = text['games'][t]['id']
    return count


def test_identity_token(token, text):
    for t in range(len(text)):
        if len(text[t]) > 1:
            if token == text[t]['accessToken']:
                return True

    return False


@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    text = json.load(open('users.json'))  # файл в котором хранятся пользователи
    username = data.get('nickname')
    password = data.get('password')
    if not username or not password:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both username and password'}}), 400
    for i in range(len(text['users'])):
        if text['users'][i]['nickname'] == username:
            return jsonify({"success": 'false', "exception": {"message": 'Nickname is already occupied.'}}), 400
    token = secrets.token_hex(6)
    flag = True
    while flag:
        flag = test_identity_token(token, text['users'])
        if flag:
            token = secrets.token_hex(6)
    text['users'].append({'nickname': username, 'password': password, 'accessToken': token})
    json.dump(text, open('users.json', 'w'))
    return jsonify({'nickname': username, 'accessToken': token, "success": 'true', "exception": 'null'}), 200


@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    text = json.load(open('users.json'))
    username = data.get('nickname')
    password = data.get('password')
    if not username or not password:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both username and password'}}), 400
    for i in range(len(text['users'])):
        if text['users'][i]['nickname'] == username:
            return jsonify({'nickname': username, 'accessToken': text['users'][i]['accessToken']}), 400
    return jsonify({"success": 'false', "exception": {
        'error': 'You are not in the database.Please provide both username and password'}}), 400


@app.route('/set/room/create', methods=['POST'])
def create_room():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    id = create_gameid(text) + 1
    text['games'].append(
        {"id": id, 'cards_id': [], 'score': 0, 'status': "ended", 'set_cards_id': [], 'accessToken': ''})
    json.dump(text, open('users.json', 'w'))
    return jsonify({"success": 'true', "exception": 'null', "gameId": id})


@app.route('/set/room/list', methods=['POST'])
def list_games():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    for i in range(len(text['games'])):
        if text['games'][i]['status'] == "ended":
            box.append({'id': text['games'][i]['id']})
    if len(box) == 0:
        return jsonify({"success": 'false', "exception": {'error': 'Please create game room'}}), 400
    return jsonify({'games': box})


@app.route('/set/room/enter', methods=['POST'])
def enter_game():
    data = request.get_json()
    text = json.load(open('users.json'))
    gameid = data.get('gameId')
    if type(gameid) != int:
        return jsonify({"success": 'false', "exception": {'error': 'Please input gameId integer number'}}), 400
    token = data.get('accessToken')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    flag = test_identity_token(token, text['games'])
    if flag:
        for i in range(len(text['games'])):
            if text['games'][i]['accessToken'] == token and text['games'][i]["id"] != gameid:
                return jsonify({"success": 'false', "exception": {
                    'error': "User's token is registered for a game with id: " + str(text['games'][i]['id'])},
                                'gameId': gameid})
            else:
                return jsonify({"success": 'true', "exception": 'null', 'gameId': gameid})
    for i in range(len(text['games'])):
        if text['games'][i]['id'] == gameid and text['games'][i]['accessToken'] != "" and text['games'][i]["id"] != gameid:
            return jsonify(
                {"success": 'false', "exception": {'error': 'Game is busy, check the gameId'}, 'gameId': gameid})
    for i in range(len(text['games'])):
        if text['games'][i]['id'] == gameid:
            text['games'][i]['accessToken'] = token
            text['games'][i]['status'] = "ongoing"
    json.dump(text, open('users.json', 'w'))
    return jsonify({"success": 'true', "exception": 'null', 'gameId': gameid})


@app.route('/set/field', methods=['POST'])
def field():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    id = []
    flag = test_identity_token(token, text['games'])
    if not flag or not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    for i in range(len(text["games"])):
        if text["games"][i]['accessToken'] == token:
            if len(text["games"][i]['cards_id']) != 0:
                return jsonify({"success": 'false', "exception": {'error': 'This field is created'}}), 400
    for i in range(8):
        a = random.randint(1, 81)
        id.append(a)
    for i in range(len(id)):
        for y in range(i, len(id)):
            if id[i] == id[y] and i != y:
                id[i] = random.randint(1, 81)
    for i in range(len(text['games'])):
        if text['games'][i]['accessToken'] == token:
            text['games'][i]["cards_id"] = id
            json.dump(text, open('users.json', 'w'))
    for y in range(len(id)):
        for i in range(len(text['cards'])):
            if id[y] == text['cards'][i]['id']:
                box.append(text['cards'][i])
    return jsonify({'cards': box, "status": "ongoing", "score": 0})


@app.route('/set/pick', methods=['POST'])
def pick():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    cards = data.get('cards')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    id = []
    game_number = 0
    for y in range(len(cards)):
        if type(cards[y]) != int:
            return jsonify({"success": 'false', "exception": {'error': 'Please input cards id as integer number'}}), 400
    for i in range(len(text['games'])):
        if text['games'][i]['accessToken'] == token:
            id = text['games'][i]['cards_id']
            game_number = i
    for y in range(len(id)):
        for i in range(len(text['cards'])):
            if id[y] == text['cards'][i]['id']:
                box.append(text['cards'][i])
    count = 0
    for i in range(len(id)):
        for y in range(len(cards)):
            if id[i] == cards[y]:
                count += 1
    if count < 3:
        count = 0
        return jsonify({"success": 'false', "exception": {'error': 'There is no card with this id'}})
    else:
        count = 0
    card_one = {}
    card_two = {}
    card_three = {}
    for i in range(len(box)):
        if box[i]['id'] == cards[0]:
            card_one = box[i]
        if box[i]['id'] == cards[1]:
            card_two = box[i]
        if box[i]['id'] == cards[2]:
            card_three = box[i]
    key = ['color', 'shape', 'fill', 'count']
    k = 1
    proverka = [0, 0, 0, 0]
    for i in range(4):
        for t in range(1):
            if card_one[key[i]] != card_three[key[i]] and card_two[key[i]] != card_three[key[i]] and card_one[key[i]] != \
                    card_two[key[i]]:
                proverka[i] = 1
            if card_one[key[i]] == card_two[key[i]]:
                proverka[i] = card_one[key[i]] + card_two[key[i]]
                if card_two[key[i]] == card_three[key[i]]:
                    proverka[i] = 1
                else:
                    proverka[i] = 0
            elif card_two[key[i]] == card_three[key[i]]:
                proverka[i] = card_two[key[i]] + card_three[key[i]]
                if card_one[key[i]] == card_three[key[i]]:
                    proverka[i] = 1
                else:
                    proverka[i] = 0
            elif card_one[key[i]] == card_three[key[i]]:
                proverka[i] = card_one[key[i]] + card_three[key[i]]
                if card_one[key[i]] == card_two[key[i]]:
                    proverka[i] = 1
                else:
                    proverka[i] = 0
    count_one = 0
    for i in range(len(proverka)):
        if proverka[i] == 1:
            count_one += 1
    k = 0
    if count_one == 4:
        for i in text['games'][game_number]['set_cards_id']:
            for y in cards:
                if i == y:
                    k += 1
        if k == 0:
            text['games'][game_number]['score'] += 1
        else:
            k = 0
        for i in range(len(cards)):
            text['games'][game_number]['cards_id'].remove(cards[i])
        a = random.randint(1, 81)
        count = 0
        if len(text['games'][game_number]['set_cards_id']) > 3:
            for i in range(len(text['games'][game_number]['set_cards_id'])):
                for LLL in range(len(cards)):
                    if text['games'][game_number]['set_cards_id'][i] != cards[LLL] and count < 3:
                        text['games'][game_number]['set_cards_id'].append(cards[LLL])
                        count += 1
        else:
            for LLL in range(len(cards)):
                text['games'][game_number]['set_cards_id'].append(cards[LLL])
        x = 0
        while len(text['games'][game_number]['cards_id']) <= 7:
            a = proverka_a(a, text['games'][game_number]['set_cards_id'])
            if text['games'][game_number]['cards_id'][x] != a:
                if text['games'][game_number]['set_cards_id'][x] != a:
                    a = random.randint(1, 81)
                    text['games'][game_number]['cards_id'].append(a)
            x += 1
        box.clear()
        for y in range(len(text['games'][game_number]['cards_id'])):
            for i in range(len(text['cards'])):
                if text['games'][game_number]['cards_id'][y] == text['cards'][i]['id']:
                    box.append(text['cards'][i])
        json.dump(text, open('users.json', 'w'))
        return jsonify({'isSet': 'true', "score": text['games'][game_number]['score'], 'cards': box})
    else:
        return jsonify({'isSet': 'false', "score": text['games'][game_number]['score'], 'cards': box})


@app.route('/set/add', methods=['POST'])
def add():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    id_not = []
    game_number = 0
    flag = 0
    for i in range(len(text['games'])):
        if text['games'][i]['accessToken'] == token:
            for lll in text['games'][i]['cards_id']:
                id_not.append(lll)
            for lll in text['games'][i]['set_cards_id']:
                id_not.append(lll)
            game_number = i
            flag += 1
    if flag == 0:
        return jsonify(
            {"success": 'false', "exception": {'error': 'There is no game with such a token. Check the token'}}), 400
    a = random.randint(1, 81)
    a = proverka_a(a, id_not)
    for i in range(len(id_not)):
        while id_not[i] == a:
            a = random.randint(1, 81)
            a = proverka_a(a, id_not)
    text['games'][game_number]['cards_id'].append(a)
    for y in range(len(text['games'][game_number]['cards_id'])):
        for i in range(len(text['cards'])):
            if text['games'][game_number]['cards_id'][y] == text['cards'][i]['id']:
                box.append(text['cards'][i])
    json.dump(text, open('users.json', 'w'))
    return jsonify({'cards': box, "success": 'true', "exception": 'null'})


@app.route('/set/scores', methods=['POST'])
def scores():
    data = request.get_json()
    text = json.load(open('users.json'))
    token = data.get('accessToken')
    if not token or len(token) != 12:
        return jsonify({"success": 'false', "exception": {'error': 'Please provide both token'}}), 400
    token_users = []
    for i in range(len(text['games'])):
        if text['games'][i]['accessToken'] != '':
            token_users.append(
                {'accessToken': text['games'][i]['accessToken'], 'score': text['games'][i]['score'], "nickname": ''})
    for x in range(len(text['users'])):
        for y in range(len(token_users)):
            if text['users'][x]['accessToken'] == token_users[y]['accessToken']:
                token_users[y]["nickname"] = text['users'][x]['nickname']
    index = 0
    for i in range(len(token_users)):
        if token_users[i - index]['nickname'] == "":
            del token_users[i - index]
            index += 1
    for i in range(len(token_users)):
        del token_users[i - index]['accessToken']
    return jsonify({'users': token_users, "success": 'true', "exception": 'null'})


if __name__ == '__main__':
    app.run(debug=True)
