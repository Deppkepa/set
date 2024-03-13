import json

with open("cards2.json", "r") as data:
    word_boy = json.load(data)


def generation_three_card(a, b):
    box2 = []
    if a['color'] == b['color']:
        box2.append(a['color'])
    else:
        box2.append(6 - a['color'] - b['color'])
    if a['shape'] == b['shape']:
        box2.append(a['shape'])
    else:
        box2.append(6 - a['shape'] - b['shape'])
    if a['fill'] == b['fill']:
        box2.append("a['fill']")
    else:
        box2.append(6 - a['fill'] - b['fill'])
    if a['count'] == b['count']:
        box2.append("a['fill']")
    else:
        box2.append(6 - a['count'] - b['count'])
    k = 0
    control = False
    for l in range(len(box2)):
        if box2[l] != 0:
            k += 1
        if k > 1:
            control = True
    if control:
        three_card.update({
            "color": box2[0],
            "shape": box2[1],
            "fill": box2[2],
            "count": box2[3]
        })


def output(one, two, three, b):
    box_color = [0, 'green', 'red', 'blue']
    box_shape = [0, 'romb', 'Tilda', 'oval']
    box_fill = [0, 'streak', 'filled', 'empty']
    box_count = [0, 'one', 'two', 'three']
    print('id:', one['id'], ',', 'color:', box_color[one['color']], ',', 'shape:', box_shape[one['shape']], ',',
          'fill:', box_fill[one['fill']], ',', 'count:', box_count[one['count']])
    print('id:', two['id'], ',', 'color:', box_color[two['color']], ',', 'shape:', box_shape[two['shape']], ',',
          'fill:', box_fill[two['fill']], ',', 'count:', box_count[two['count']])
    print('id:', b[2], ',', 'color:', box_color[three['color']], ',', 'shape:', box_shape[three['shape']], ',',
          'fill:', box_fill[three['fill']], ',', 'count:', box_count[three['count']])


def search(three, arr):
    for o in range(len(arr)):
        if arr[o]['id'] != one_card['id'] and arr[o]['id'] != two_card['id']:
            if three['color'] == arr[o]['color'] \
                    and three['shape'] == arr[o]['shape'] \
                    and three['fill'] == arr[o]['fill'] and three['count'] == arr[o]['count'] \
                    and arr[o]['id'] != one_card['id'] \
                    and arr[o]['id'] != two_card['id']:
                box.append(one_card['id'])
                box.append(two_card['id'])
                box.append(arr[o]['id'])
                if len(box) == 3:
                    print(one_card)
                    print(two_card)
                    print(three_card)
                    output(one_card, two_card, word_boy['cards'][o], box)


one_card = {}
two_card = {}
three_card = {}
box = []
for i in range(len(word_boy['cards'])):
    one_card.update(word_boy['cards'][i])
    for y in range(1, len(word_boy['cards'])):
        if word_boy['cards'][i] != word_boy['cards'][y]:
            two_card.update(word_boy['cards'][y])
            generation_three_card(word_boy['cards'][i], word_boy['cards'][y])
            search(three_card, word_boy['cards'])
if len(box) == 0:
    print("Сета нет")
