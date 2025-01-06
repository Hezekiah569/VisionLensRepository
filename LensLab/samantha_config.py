IDENTIFY_MODE_OBJECTS = ['1', '5', '10', '20', '20 coin', '50', '100', '200', '500', '1000',
                         'phone', 'bookshelf', 'chair', 'desktop', 'door','keyboard', 'people',
                         'table', 'bag', 'cup', 'electricfan', 'laptop', 'water dispenser']

NAVIGATE_MODE_OBJECTS = ['bookshelf', 'chair', 'desktop', 'door', 'handrail', 'people', 'table',
                         'walls', 'downstairs', 'electricfan', 'upstairs', 'water dispenser']

IDENTIFY_MODE_RESPONSES = {

    '1': "I see a one peso coin.",
    '5': "I see a five peso coin.",
    '10': "I see a ten peso coin.",
    '20': "That's a 20 peso bill",
    '20 coin': "I see a 20 peso coin",
    '50': "I see a fifty peso bill",
    '100': "I see a one hundred peso bill.",
    '200': "I see a two hundred peso bill",
    '500': "I see a five hundred peso bill",
    '1000': "I see a one thousand peso bill",
    'phone': "I see a phone.",
    'bookshelf': "That's a bookshelf.",
    'chair': "I see a chair.",
    'desktop': "I see a desktop.",
    'door': "I can see a door.",
    'keyboard': "I see a keyboard",
    'people': "I see dead people.",
    'table': "I see a table",
    'bag': "I see a bag.",
    'cup': "I see a cup.",
    'electricfan': "I see an electric fan",
    'laptop': "I see a laptop.",
    'water dispenser': "I see a water dispenser.",

}

NAVIGATE_MODE_RESPONSES = {

    'bookshelf': "Watch out, there's a bookshelf ahead. You might want to move carefully.",
    'chair': "There's a chair nearby. Be cautious not to bump into it.",
    'desktop': "I see a desktop computer. Might be part of a workstation.",
    'door': "There's a door in your path. It could be an exit or an entrance.",
    'handrail': "A handrail is nearby. You can use it for support.",
    'people': "I see people nearby. Mind your step and give them space.",
    'table': "Careful. You might run into a table nearby.",
    'walls': "Careful. There's a wall nearby.",
    'downstairs': "Walk slowly. There's a downstairs in front of you.",
    'electricfan': "Careful. There's an electric fan in front.",
    'upstairs': "Walk slowly. There's an upstairs in front of you.",
    'water dispenser': "Careful. You might run into a water dispenser.",

}

DEFAULT_IDENTIFY_RESPONSE = "I see a {object_name}. It's something I can identify."
DEFAULT_NAVIGATE_RESPONSE = "Be careful around the {object_name}. It's in your path."
