# layer 0: Background Objects
# layer 1: Foreground Objects
# Layer 2: ShortSword Swing Objects
# Layer 3: PickaxeRed Swing Objects
# Layer 4: Arrow Objects
# Layer 5: Bullet Objects

objects = [[], [], [], [], [], []]
collision_group = dict()

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol


def remove_object(o):
    for layer in objects:
        try:
            if o in layer:
                layer.remove(o)
                # remove_collision_object(o)
                del o
                return
        except:
            pass
    raise ValueError('Trying destroy non existing object')


def all_objects():
    for layer in objects:
        for o in layer:
            yield o

def add_collision_pairs(a, b, group):
    if group not in collision_group:
        print('Create New Group')
        collision_group[group] = [[], []]
        
    if a:
        if type(b) is list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)
            
    if b:
        if type(a) is list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)
            
def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group

def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
            
def remove_collision_pairs(a, b, group):
    if group not in collision_group:
        assert('group is not in collision_group')
        
    if a:
        if type(b) is list:
            collision_group[group][1] -= b
        else:
            collision_group[group][1].remove(b)
            
    if b:
        if type(a) is list:
            collision_group[group][0] -= a
        else:
            collision_group[group][0].remove(a)
            
    del group

def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()

def update():
    for game_object in all_objects():
        game_object.update()


