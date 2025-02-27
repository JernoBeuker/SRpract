import random as rd

LH_NATURAL = {"body.arms.left.lower.roll": -0.6,"body.arms.left.upper.pitch": -0.1}
RH_NATURAL = {"body.arms.right.lower.roll": -0.6,"body.arms.right.upper.pitch": -0.1}
HEAD_NATURAL = {"body.head.roll": 0, "body.head.pitch": 0, "body.head.yaw": 0}

FRAMES_RH_GESTURE = [
            {"time": 400, "data": RH_NATURAL},
            {"time": 1000, "data": {"body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0,7)}},
            {"time": 1600, "data": RH_NATURAL}
            ]

FRAMES_LH_GESTURE = [
        	{"time": 400, "data": LH_NATURAL},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL}
            ]

FRAMES_LH_RH_GESTURE = [
        	{"time": 400, "data": LH_NATURAL | RH_NATURAL},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | RH_NATURAL}
            ]

FRAMES_HEAD_L_GESTURE = [
            {"time": 400, "data": HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0}},
            {"time": 1600, "data": HEAD_NATURAL}
            ]

FRAMES_HEAD_R_GESTURE = [
            {"time": 400, "data": HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0}},
            {"time": 1600, "data": HEAD_NATURAL}
            ]

FRAMES_LEFT_HEAD_GESTURE = [
            {"time": 400, "data": LH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_RIGHT_HEAD_GESTURE = [
            {"time": 400, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_LEFT_HEAD_GESTURE2 = [
            {"time": 400, "data": LH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_RIGHT_HEAD_GESTURE2 = [
            {"time": 400, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

# Iconic gestures
CELEBRATE = [
        	{"time": 0, "data": LH_NATURAL | RH_NATURAL | {"body.torso.yaw": 0}},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(-0.5, -0.3)}},
            {"time": 1600, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": rd.uniform(-0.9, -0.7)}},
            {"time": 2200, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(-0.5, -0.3)}},
            {"time": 2800, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": 0}},
            {"time": 3400, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(0.3, 0.5),}},
            {"time": 4000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": 0.8}},
            {"time": 4600, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(0.3, 0.5),}},
            {"time": 5600, "data": LH_NATURAL | RH_NATURAL | {"body.torso.yaw": 0}}
            ]

EUREKA = [
            {"time": 0, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 1400, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 2000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 2600, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 3200, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 3800, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 4400, "data": {"body.head.roll": 0.0,
                                    "body.head.yaw": 0.0,
                                    "body.head.pitch": rd.uniform(-0,4, -0.2),
                                    "body.arms.right.lower.roll": rd.uniform(-0,6, -0.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9)}},
            {"time": 5000, "data": {"body.head.roll": 0.0,
                                    "body.head.yaw": 0.0,
                                    "body.head.pitch": rd.uniform(-0,4, -0.2),
                                    "body.arms.right.lower.roll": rd.uniform(-0,6, -0.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9)}},
            {"time": 5600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

GESTURES = [
    FRAMES_RH_GESTURE, 
    FRAMES_LH_GESTURE, 
    FRAMES_LH_RH_GESTURE, 
    FRAMES_HEAD_L_GESTURE,
    FRAMES_HEAD_R_GESTURE,
    FRAMES_LEFT_HEAD_GESTURE, 
    FRAMES_RIGHT_HEAD_GESTURE, 
    FRAMES_LEFT_HEAD_GESTURE2, 
    FRAMES_RIGHT_HEAD_GESTURE2
]

NATURAL_POS = [{"time": 400, "data": LH_NATURAL | RH_NATURAL | HEAD_NATURAL}]
