import json

ID = 0
TIMESTAMP = 1
HANDS = 2
POINTABLES = 3
INTERACTION_BOX = 4

# comes in first leap motion data frame
FRAME_STRUCTURE = json.loads('{"frame":'
                             '["id", "timestamp", {"hands": [["id", "type", "direction", "palmNormal", '
                             '"palmPosition", "palmVelocity", "stabilizedPalmPosition", "pinchStrength", '
                             '"grabStrength", "confidence", "armBasis", "armWidth", "elbow", "wrist"]]}, '
                             '{"pointables": [["id", "direction", "handId", "length", "stabilizedTipPosition", '
                             '"tipPosition", "tipVelocity", "tool", "carpPosition", "mcpPosition", "pipPosition", '
                             '"dipPosition", "btipPosition", "bases", "type"]]}, {"interactionBox": ["center", '
                             '"size"]}]'
                             '}')

test_frame = '[171719, 11086766568, [[87, "right", [-0.0457658, 0.69241, -0.720051], [-0.359249, -0.68399, -0.6349], ' \
             '[39.3046, 166.016, 16.4911], [-0.159124, 0.574626, 0.675342], [41.5582, 163.453, 14.1259], 0, 0, 1, ' \
             'null, null, null, null]], [[870, [-0.595028, 0.296892, -0.746858], 87, 50.4916, [-38.2016, 157.695, ' \
             '-17.4605], [-39.5914, 157.794, -13.9109], [0.926123, 2.99923, 0.784767], false, [20.7346, 127.848, ' \
             '58.2295], [20.7346, 127.848, 58.2295], [-10.491, 143.188, 24.6367], [-30.1464, 152.995, -0.0339627], ' \
             '[-42.4127, 159.228, -18.056], [[[0.687474, 0.654492, 0.314675], [-0.571642, 0.220464, 0.79033], ' \
             '[0.44789, -0.723212, 0.525698]], [[0.406285, 0.912905, 0.0392081], [-0.646559, 0.256899, 0.718307], ' \
             '[0.645673, -0.317188, 0.694621]], [[0.406285, 0.912905, 0.0392081], [-0.693451, 0.280107, 0.663827], ' \
             '[0.595028, -0.296892, 0.746858]], [[0.406285, 0.912905, 0.0392081], [-0.736386, 0.301718, 0.605559], ' \
             '[0.540988, -0.274902, 0.794834]]], null], [871, [-0.273556, 0.326267, -0.90483], 87, 56.9741, ' \
             '[-0.897578, 225.575, -55.3779], [-2.43711, 221.74, -59.3936], [-0.421338, 4.25398, 2.41754], false, ' \
             '[34.3492, 146.189, 60.604], [16.3391, 189.788, 7.17147], [8.19123, 213.282, -26.2072], [1.78541, ' \
             '220.922, -47.3955], [-3.69838, 221.984, -62.9775], [[[0.911202, -0.110104, -0.396973], [0.325366, ' \
             '0.783396, 0.529555], [0.252681, -0.611693, 0.749656]], [[0.928119, -0.157425, -0.337362], [0.316664, ' \
             '0.810324, 0.49305], [0.195754, -0.56444, 0.801928]], [[0.928119, -0.157425, -0.337362], [0.252513, ' \
             '0.932077, 0.25975], [0.273556, -0.326267, 0.90483]], [[0.928119, -0.157425, -0.337362], [0.169836, ' \
             '0.985445, 0.00739203], [0.331288, -0.0641568, 0.941346]]], null], [872, [-0.0286625, 0.344578, ' \
             '-0.93832], 87, 64.9174, [37.9978, 218.592, -77.4892], [38.1309, 222.455, -76.6801], [1.12247, 2.24349, ' \
             '1.40127], false, [45.4948, 146.531, 56.3648], [36.9749, 186.395, 2.44716], [40.8729, 210.924, ' \
             '-37.0979], [40.0832, 220.417, -62.9485], [37.5478, 223.064, -80.7818], [[[0.868056, -0.323659, ' \
             '-0.376463], [0.4802, 0.739884, 0.471148], [0.126047, -0.58976, 0.797681]], [[0.874424, -0.446174, ' \
             '-0.190559], [0.477928, 0.724582, 0.496553], [-0.0834735, -0.525271, 0.846831]], [[0.874424, -0.446174, ' \
             '-0.190559], [0.484316, 0.825951, 0.288519], [0.0286625, -0.344578, 0.93832]], [[0.874424, -0.446174, ' \
             '-0.190559], [0.464747, 0.883053, 0.065022], [0.139262, -0.145418, 0.97952]]], null], [873, [0.0123446, ' \
             '0.411368, -0.911386], 87, 62.4199, [60.7509, 213.511, -73.1947], [61.4945, 216.013, -72.176], [1.0922, ' \
             '4.4344, 3.36652], false, [56.0944, 143.812, 51.683], [56.9971, 177.205, 1.0176], [62.6461, 201.641, ' \
             '-34.2632], [62.9774, 212.681, -58.7233], [61.0516, 217.008, -76.1943], [[[0.838457, -0.461768, ' \
             '-0.289413], [0.544765, 0.695692, 0.468236], [-0.0148741, -0.550257, 0.834863]], [[0.834165, -0.50683, ' \
             '-0.217467], [0.535853, 0.651506, 0.537031], [-0.130503, -0.564502, 0.81505]], [[0.834165, -0.50683, ' \
             '-0.217467], [0.551377, 0.757562, 0.349405], [-0.0123446, -0.411368, 0.911386]], [[0.834165, -0.50683, ' \
             '-0.217467], [0.541156, 0.828245, 0.145465], [0.10639, -0.239025, 0.965167]]], null], [874, [0.155351, ' \
             '0.302727, -0.940331], 87, 48.936, [87.2878, 186.852, -60.9777], [86.6739, 187.167, -60.7722], ' \
             '[-1.99007, 0.587865, 1.05869], false, [64.3283, 134.646, 45.4933], [73.3035, 164.574, -1.19339], ' \
             '[83.7523, 179.394, -30.2577], [86.696, 185.13, -48.076], [86.6673, 187.775, -64.5646], [[[0.729487, ' \
             '-0.630909, -0.264203], [0.665075, 0.564035, 0.489428], [-0.159765, -0.532745, 0.831058]], [[0.690615, ' \
             '-0.713903, -0.115735], [0.655759, 0.550632, 0.516512], [-0.305012, -0.432605, 0.848422]], [[0.690615, ' \
             '-0.713903, -0.115735], [0.706341, 0.631427, 0.319973], [-0.155351, -0.302727, 0.940331]], [[0.690615, ' \
             '-0.713903, -0.115735], [0.723221, 0.682093, 0.108167], [0.00172182, -0.158404, 0.987373]]], null]], ' \
             '[[0, 200, 0], [235.247, 235.247, 147.751]]] '


class Index:
    def __init__(self, frame_str=FRAME_STRUCTURE["frame"]):
        hands_ = frame_str[HANDS]["hands"][0]
        self.hand_item_index = self.index_json(hands_)
        self.hand_index = self.reverse(self.hand_item_index)

        pointables_ = frame_str[POINTABLES]["pointables"][0]
        self.pointables_item_index = self.index_json(pointables_)
        self.pointables_index = self.reverse(self.pointables_item_index)

        self.int_box_item_index = self.index_json(frame_str[INTERACTION_BOX]["interactionBox"])
        self.int_box_index = self.reverse(self.int_box_item_index)

    @staticmethod
    def index_json(frame_str):
        return dict(enumerate(frame_str))

    @staticmethod
    def reverse(index_to_name):
        return {v: k for k, v in index_to_name.items()}


index = Index()


def get_string_template(*args):
    r = range(len(args))
    templ = str(["{{}}".format(x) for x in r])
    formatted = templ.format(*args).replace("'{}'", "{}")[2:-2]\
        .replace("False", "false")\
        .replace("True", "true")
    return formatted


class InteractionBox:
    def __init__(self, json_data=None, interaction_box=None, center=None, size=None):
        if None is not json_data:
            self.center = json_data[index.int_box_index["center"]]
            self.size = json_data[index.int_box_index["size"]]
        else:
            self.center = center
            self.size = size

    def __getitem__(self, key):
        return getattr(self, index.int_box_item_index[key])

    def __str__(self):
        return get_string_template(list(map(lambda x: self[x], range(0, len(index.int_box_index)))))


class Pointables:
    def __init__(self, json_data=None, pointables=None):
        if None is not json_data:
            self.pointables = list(map(lambda j: Pointable(json_data=j), json_data))
        else:
            self.pointables = pointables

    def __str__(self):
        res = "["
        for p in self.pointables:
            res = res + str(p) + ", "
        return res[:-2]+"]"


class Pointable:
    def __init__(self, json_data=None, id=None, direction=None, hand_id=None, length=None, stabilized_tip_position=None,
                 tip_position=None, tip_velocity=None, tool=None, carp_position=None, mcp_position=None, pip_position=None,
                 dip_position=None, btip_position=None, bases=None, pointable_type=None):
        if None is not json_data:
            self.id = json_data[index.pointables_index["id"]]
            self.direction = json_data[index.pointables_index["direction"]]
            self.handId = json_data[index.pointables_index["handId"]]
            self.length = json_data[index.pointables_index["length"]]
            self.stabilizedTipPosition = json_data[index.pointables_index["stabilizedTipPosition"]]
            self.tipPosition = json_data[index.pointables_index["tipPosition"]]
            self.tipVelocity = json_data[index.pointables_index["tipVelocity"]]
            self.tool = json_data[index.pointables_index["tool"]]
            self.carpPosition = json_data[index.pointables_index["carpPosition"]]
            self.mcpPosition = json_data[index.pointables_index["mcpPosition"]]
            self.pipPosition = json_data[index.pointables_index["pipPosition"]]
            self.dipPosition = json_data[index.pointables_index["dipPosition"]]
            self.btipPosition = json_data[index.pointables_index["btipPosition"]]
            self.bases = json_data[index.pointables_index["bases"]]
            self.type = json_data[index.pointables_index["type"]]
        else:
            self.id = id
            self.direction = direction
            self.hand_id = hand_id
            self.length = length
            self.stabilizedTipPosition = stabilized_tip_position
            self.tipPosition = tip_position
            self.tipVelocity = tip_velocity
            self.tool = tool
            self.carpPosition = carp_position
            self.mcpPosition = mcp_position
            self.pipPosition = pip_position
            self.dipPosition = dip_position
            self.btipPosition = btip_position
            self.bases = bases
            self.type = pointable_type

    def __getitem__(self, key):
        return getattr(self, index.pointables_item_index[key])

    def __str__(self):
        res = get_string_template(list(map(lambda x: self[x], range(0, len(index.pointables_item_index)))))
        return res


class Hands:
    def __init__(self, json_data=None, hands=None):
        if None is not json_data:
            self.hands = list(map(lambda j: Hand(json_data=j), json_data))
        else:
            self.hands = hands

    def __str__(self):
        res = "["
        for hand in self.hands:
            res = res + str(hand) + ", "
        return res[:-2]+"]"


class Hand:
    def __init__(self, json_data=None, id=None, type=None, direction=None, palm_normal=None, palm_position=None,
                 palm_velocity=None, stabilized_palm_position=None, pinch_strength=None,
                 grab_strengt=None, confidence=None, arm_basis=None, arm_width=None, elbow=None, wrist=None):
        if None is not json_data:
            self.id = json_data[index.hand_index["id"]]
            self.type = json_data[index.hand_index["type"]]
            self.direction = json_data[index.hand_index["direction"]]
            self.palmNormal = json_data[index.hand_index["palmNormal"]]
            self.palmPosition = json_data[index.hand_index["palmPosition"]]
            self.palmVelocity = json_data[index.hand_index["palmVelocity"]]
            self.stabilizedPalmPosition = json_data[index.hand_index["stabilizedPalmPosition"]]
            self.pinchStrength = json_data[index.hand_index["pinchStrength"]]
            self.grabStrength = json_data[index.hand_index["grabStrength"]]
            self.confidence = json_data[index.hand_index["confidence"]]
            self.armBasis = json_data[index.hand_index["armBasis"]]
            self.armWidth = json_data[index.hand_index["armWidth"]]
            self.elbow = json_data[index.hand_index["elbow"]]
            self.wrist = json_data[index.hand_index["wrist"]]
        else:
            self.id = id
            self.type = type
            self.direction = direction
            self.palmNormal = palm_normal
            self.palmPosition = palm_position
            self.palmVelocity = palm_velocity
            self.stabilizedPalmPosition = stabilized_palm_position
            self.pinchStrength = pinch_strength
            self.grabStrength = grab_strengt
            self.confidence = confidence
            self.armBasis = arm_basis
            self.armWidth = arm_width
            self.elbow = elbow
            self.wrist = wrist

    def __getitem__(self, key):
        return getattr(self, index.hand_item_index[key])

    def __str__(self):
        res = get_string_template(list(map(lambda x: self[x], range(0, len(index.hand_item_index)))))
        return res


class NativeFrame:
    def __init__(self, LeapFrame):
        self.id = LeapFrame.id
        self.timestamp = LeapFrame.timestamp
        self.hands = LeapFrame.hands.hands
        self.pointables = LeapFrame.pointables.pointables
        self.interactionBox = LeapFrame.interactionBox


class LeapFrame:
    def __init__(self, str_data=None, json_data=None, id=None, timestamp=None, hands=None, pointables=None,
                 interaction_box=None):
        if None is not str_data:
            json_data = json.loads('{"x":' + str_data + '}')['x']
        if None is not json_data:
            self.hands = Hands(json_data[HANDS])
            self.pointables = Pointables(json_data[POINTABLES])
            self.interactionBox = InteractionBox(json_data[INTERACTION_BOX])
            self.id = json_data[ID]
            self.timestamp = json_data[TIMESTAMP]
        else:
            self.hands = hands
            self.pointables = pointables
            self.interactionBox = interaction_box
            self.id = id
            self.timestamp = timestamp

    def __str__(self):
        return '[{}, {}, {}, {}, {}]'\
            .format(self.id, self.timestamp, self.hands, self.pointables, self.interactionBox)\
            .replace("'", '"').replace('None', 'null')

    def to_json(self):
        return json.dumps(NativeFrame(self), default=lambda o: o.__dict__,
            sort_keys=False, indent=None)
