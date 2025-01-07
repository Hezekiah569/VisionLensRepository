# Objects available in identify mode
IDENTIFY_MODE_OBJECTS = [
    '1', '5', '10', '20', '20 coin', '50', '100', '200', '500', '1000',
    'phone', 'bookshelf', 'chair', 'desktop', 'door', 'keyboard', 'people',
    'table', 'bag', 'cup', 'electricfan', 'laptop', 'water dispenser'
]

# Objects available in navigate mode
NAVIGATE_MODE_OBJECTS = [
    'bookshelf', 'chair', 'desktop', 'door', 'handrail', 'people', 'table',
    'walls', 'downstairs', 'electricfan', 'upstairs', 'water dispenser'
]

# Responses for identify mode with spatial direction
IDENTIFY_MODE_RESPONSES = {
    # 💰 Currency
    '1': {  # 🪙 One Peso Coin
        'front': "That's a one peso coin in front of you.",
        'left': "That's a one peso coin to your left.",
        'right': "That's a one peso coin to your right."
    },
    '5': {  # 🪙 Five Peso Coin
        'front': "Looks like a five peso coin in front of you.",
        'left': "Looks like a five peso coin to your left.",
        'right': "Looks like a five peso coin to your right."
    },
    '10': {  # 🪙 Ten Peso Coin
        'front': "I see a ten peso coin in front of you.",
        'left': "I see a ten peso coin to your left.",
        'right': "I see a ten peso coin to your right."
    },
    '20': {  # 💵 Twenty Peso Bill
        'front': "That's a twenty peso bill in front of you.",
        'left': "That's a twenty peso bill to your left.",
        'right': "That's a twenty peso bill to your right."
    },
    '20 coin': {  # 🪙 Twenty Peso Coin
        'front': "It seems to be a twenty peso coin in front of you.",
        'left': "It seems to be a twenty peso coin to your left.",
        'right': "It seems to be a twenty peso coin to your right."
    },
    '50': {  # 💵 Fifty Peso Bill
        'front': "This is a fifty peso bill in front of you.",
        'left': "This is a fifty peso bill to your left.",
        'right': "This is a fifty peso bill to your right."
    },
    '100': {  # 💵 One Hundred Peso Bill
        'front': "That's a one hundred peso bill in front of you.",
        'left': "That's a one hundred peso bill to your left.",
        'right': "That's a one hundred peso bill to your right."
    },
    '200': {  # 💵 Two Hundred Peso Bill
        'front': "I see a two hundred peso bill in front of you.",
        'left': "I see a two hundred peso bill to your left.",
        'right': "I see a two hundred peso bill to your right."
    },
    '500': {  # 💵 Five Hundred Peso Bill
        'front': "That's a five hundred peso bill in front of you.",
        'left': "That's a five hundred peso bill to your left.",
        'right': "That's a five hundred peso bill to your right."
    },
    '1000': {  # 💵 One Thousand Peso Bill
        'front': "I see a one thousand peso bill in front of you.",
        'left': "I see a one thousand peso bill to your left.",
        'right': "I see a one thousand peso bill to your right."
    },

    # 📱 Electronics
    'phone': {  # 📱 Phone
        'front': "There's a phone in front of you.",
        'left': "There's a phone to your left.",
        'right': "There's a phone to your right."
    },
    'desktop': {  # 🖥️ Desktop
        'front': "I see a desktop computer in front of you.",
        'left': "I see a desktop computer to your left.",
        'right': "I see a desktop computer to your right."
    },
    'keyboard': {  # ⌨️ Keyboard
        'front': "That looks like a keyboard in front of you.",
        'left': "That looks like a keyboard to your left.",
        'right': "That looks like a keyboard to your right."
    },
    'laptop': {  # 💻 Laptop
        'front': "There's a laptop in front of you.",
        'left': "There's a laptop to your left.",
        'right': "There's a laptop to your right."
    },
    'electricfan': {  # 🌀 Electric Fan
        'front': "I see an electric fan in front of you.",
        'left': "I see an electric fan to your left.",
        'right': "I see an electric fan to your right."
    },
    'water dispenser': {  # 🚰 Water Dispenser
        'front': "That's a water dispenser in front of you.",
        'left': "That's a water dispenser to your left.",
        'right': "That's a water dispenser to your right."
    },

    # 🪑 Furniture
    'bookshelf': {  # 📚 Bookshelf
        'front': "There's a bookshelf ahead.",
        'left': "There's a bookshelf to your left.",
        'right': "There's a bookshelf to your right."
    },
    'chair': {  # 🪑 Chair
        'front': "I see a chair in front of you.",
        'left': "I see a chair to your left.",
        'right': "I see a chair to your right."
    },
    'table': {  # 🛋️ Table
        'front': "That's a table in front of you.",
        'left': "That's a table to your left.",
        'right': "That's a table to your right."
    },
    'door': {  # 🚪 Door
        'front': "I notice a door ahead.",
        'left': "I notice a door to your left.",
        'right': "I notice a door to your right."
    },
    'bag': {  # 🎒 Bag
        'front': "There's a bag in front of you.",
        'left': "There's a bag to your left.",
        'right': "There's a bag to your right."
    },
    'cup': {  # 🥤 Cup
        'front': "I see a cup in front of you.",
        'left': "I see a cup to your left.",
        'right': "I see a cup to your right."
    },

    # 🧑 People
    'people': {  # 🧍 People
        'front': "There's someone in front of you.",
        'left': "There's someone to your left.",
        'right': "There's someone to your right."
    }
}

# Responses for navigate mode with spatial direction
NAVIGATE_MODE_RESPONSES = {

    # 📚 Bookshelf
    'bookshelf': {
        'front': "There's a bookshelf in front of you. Move carefully.",
        'left': "There's a bookshelf to your left. Be cautious.",
        'right': "There's a bookshelf to your right. Watch your step."
    },

    # 🪑 Chair
    'chair': {
        'front': "There's a chair in front of you. Step carefully.",
        'left': "There's a chair to your left. Watch out.",
        'right': "There's a chair to your right. Be mindful."
    },

    # 🖥️ Desktop
    'desktop': {
        'front': "A desktop computer is directly in front of you.",
        'left': "There's a desktop computer to your left.",
        'right': "There's a desktop computer to your right."
    },

    # 🚪 Door
    'door': {
        'front': "There's a door in front of you. Proceed cautiously.",
        'left': "There's a door to your left.",
        'right': "There's a door to your right."
    },

    # 🤲 Handrail
    'handrail': {
        'front': "There's a handrail in front of you. You can use it for support.",
        'left': "There's a handrail to your left.",
        'right': "There's a handrail to your right."
    },

    # 👥 People
    'people': {
        'front': "There are people in front of you. Move carefully.",
        'left': "There are people to your left. Give them space.",
        'right': "There are people to your right. Be cautious."
    },

    # 🛋️ Table
    'table': {
        'front': "There's a table in front of you. Navigate carefully.",
        'left': "There's a table to your left. Mind your step.",
        'right': "There's a table to your right. Be careful."
    },

    # 🧱 Walls
    'walls': {
        'front': "There's a wall directly in front of you.",
        'left': "There's a wall to your left.",
        'right': "There's a wall to your right."
    },

    # ⬇️ Downstairs
    'downstairs': {
        'front': "Stairs leading down are in front of you. Step cautiously.",
        'left': "Stairs going down are to your left.",
        'right': "Stairs going down are to your right."
    },

    # ⬆️ Upstairs
    'upstairs': {
        'front': "Stairs leading up are in front of you. Move carefully.",
        'left': "Stairs going up are to your left.",
        'right': "Stairs going up are to your right."
    },

    # 🌬️ Electric Fan
    'electricfan': {
        'front': "There's an electric fan in front of you.",
        'left': "There's an electric fan to your left.",
        'right': "There's an electric fan to your right."
    },

    # 🚰 Water Dispenser
    'water_dispenser': {
        'front': "There's a water dispenser in front of you.",
        'left': "There's a water dispenser to your left.",
        'right': "There's a water dispenser to your right."
    }
}

# Default responses for unidentified objects
DEFAULT_IDENTIFY_RESPONSE = "I see a {object_name} to your {direction}. It's something I can identify."
DEFAULT_NAVIGATE_RESPONSE = "Be careful around the {object_name} to your {direction}."
