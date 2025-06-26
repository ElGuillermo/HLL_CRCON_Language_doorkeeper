"""
language_doorkeeper_config.py

A plugin for HLL CRCON (https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.

This version has been designed to be used on ES (spanish) servers.

Unfortunately, english servers can't really use it,
as many people in the world will understand the question and defeat the test.

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""

from custom_tools.common_functions import CLAN_URL

# Configuration (you must review/change these)
# -----------------------------------------------------------------------------

# Simulation mode : no *real* action (messsage/punish/kick/ban) will be engaged
# True : you'll only see in logs what could have been done
TEST_MODE = False

# Discord embeds strings translations
# Available : 0 english, 1 french, 2 german, 3 spanish
LANG = 3

# Activity schedule (UTC time)
# FR setting : (heure d'hiver = UTC+1 ; heure d'été = UTC+2)
# specified hours : "0: (4, 30, 21, 15)" means "active on mondays, from 4:30am to 9:15pm"
# all day long : "3: (0, 0, 23, 59)" means "active on thursdays, from 0:00am to 11:59pm"
SCHEDULE = {
    0: (9, 1, 21, 0),  # Monday
    1: (9, 1, 21, 0),  # Tuesday
    2: (9, 1, 21, 0),  # Wednesday
    3: (9, 1, 21, 0),  # Thursday
    4: (9, 1, 21, 0),  # Friday
    5: (9, 1, 21, 0),  # Saturday
    6: (9, 1, 21, 0)  # Sunday
}

# Don't run if the connected players number would drop below X.
# Default : your seed limit
# 0
DONT_KICK_BELOW = 50

# True : the answer must be the expected word *only*
# False : the expected word can be found in a sentence
# Default : True (some foreigners *will* try to enter the whole sentence)
ANSWER_EXACT_MATCH = True

# Analyze the answer's text capitalization
# True : capitals matter (Bob is not the same as BOB)
# False : cApItAlS dOn'T mAtTeR (Bob, BOB ans bOb are considered the same)
ANSWER_CASE_SENSITIVE = True

# Whitelists
# -------------------------------------

# Don't test the player if he has more than X hours of VIP
# Default : 0 (disabled)
WHITELIST_VIP_HOURS = 25

# Don't test the player if his pseudo contains a pattern
# This is a regular expression, test yours here : https://regex101.com/
# ie (german) : r"(^|[^a-z0-9])(GER|GERMAN|GERMANY|DE|DEUTSCH|DEUTSCHLAND)([^a-z0-9]|$)"
WHITELIST_PSEUDO_ENABLE = True
WHITELIST_PSEUDO_REGEX = r"(^|[^a-z0-9])(ES|ESP|ESPAÑA|SPANISH|SPAN|ESPAÑOL|CASTELLANO)([^a-z0-9]|$)"

# Steam profile country codes whitelist
# Note : you can't really rely on this, as Steam API may not answer requests
# and we can't access GamePass, nor Epic users profiles
WHITELIST_STEAM_COUNTRY = True

# (Pays et régions francophones)
WHITELIST_STEAM_COUNTRIES = {
    "AR",  # Argentina
    "BO",  # Bolivia
    "CL",  # Chile
    "CO",  # Colombia
    "CR",  # Costa Rica
    "CU",  # Cuba
    "DO",  # República Dominicana
    "EC",  # Ecuador
    "ES",  # España
    "GT",  # Guatemala
    "HN",  # Honduras
    "MX",  # México
    "NI",  # Nicaragua
    "PA",  # Panamá
    "PE",  # Perú
    "PY",  # Paraguay
    "SV",  # El Salvador
    "UY",  # Uruguay
    "VE"  # Venezuela
}

# CRCON profile flag whitelist
# Players tagged with any of these flags won't be tested
WHITELIST_CRCON_EMOJI_FLAGS = {
    "🇦🇷",  # Argentina
    "🇧🇴",  # Bolivia
    "🇨🇱",  # Chile
    "🇨🇴",  # Colombia
    "🇨🇷",  # Costa Rica
    "🇨🇺",  # Cuba
    "🇩🇴",  # República Dominicana
    "🇪🇨",  # Ecuador
    "🇪🇸",  # España
    "🇬🇹",  # Guatemala
    "🇭🇳",  # Honduras
    "🇲🇽",  # México
    "🇳🇮",  # Nicaragua
    "🇵🇦",  # Panamá
    "🇵🇪",  # Perú
    "🇵🇾",  # Paraguay
    "🇸🇻",  # El Salvador
    "🇺🇾",  # Uruguay
    "🇻🇪"  # Venezuela
}

# Random question that will be asked to the player
# -------------------------------------

# Explain to the player why (s)he has been punished and give instructions to answer.
# ie : "You've been killed by a bot.\nEnter the second word of the following sentence in chat :"
# Note : the random question sentence will be added to the end of this text.
# Hint : do not use digits (2, 3, 4, ...), as they help to guess the answer.
GENERIC_QUESTION_INTRO = (
    "\n\n[ Bot de verificación ]\n"
    "\n"
    "Servidor solo para *hablantes de español*\n"
    "(de 9am a 9pm UTC)\n"
    "\n"
    "Escribe en el chat la segunda palabra que se te muestra\n"
    "(tal y como aparece y sin añadir nada más) :\n\n"
)

# The sentence the player will have to "decode"
# The four {} {} {} {} random items will be displayed in this order :
# FIRST_WORDS_LIST, SECOND_WORDS_LIST, THIRD_WORDS_LIST and FOURTH_WORDS_LIST
# The player will have to enter the word randomly chosen in FIRST_WORDS_LIST
# ie : "'Did the {} {} {} jumped over the lazy {} ?' (Y/N)"
# Hint : keep the question mark (?) and the (Y/N) at end for an extra trap !
GENERIC_QUESTION = "'El {} de {} {} {}' (O/N)\n\n"

# One of these words will replace the first {} in GENERIC_QUESTION
# Note : this is the one the player will have to enter in chat
# hint : use accents if you have them in your language,
#        as they're not easy to enter with a foreign keyboard
FIRST_WORDS_LIST = (
    "niño", "cuñado", "coñazo"
)

# One of these words will replace the second {} in GENERIC_QUESTION
SECOND_WORDS_LIST = (
    "Pepe", "Paco", "Pedro", "Santi"
)

# One of these words will replace the third {} in GENERIC_QUESTION
THIRD_WORDS_LIST = (
    "esta", "estará", "estuvo"
)

# One of these words will replace the fourth {} in GENERIC_QUESTION
FOURTH_WORDS_LIST = (
    "imputado", "detenido", "enchufado"
)


# The player gave a valid answer
# -------------------------------------

# This emoji flag will be added to the validated player's CRCON profile
# IMPORTANT : do not forget to add it to the WHITELIST_CRCON_EMOJI_FLAGS above
# Find your flag code : https://emojipedia.org/
# Copy-paste it in there as it is, like "🇫🇷", NOT in Discord's format (":flag_fr:")
VERIFIED_PLAYER_FLAG = "🇪🇸"

# This flag will be used to illustrate the player's success in a Discord embed
# You can use you country flag or any emoji, like : ":white_check_mark:" or ":heart:"
VERIFIED_PLAYER_FLAG_EMBED = ":flag_es:"

# Send a message to inform the players they passed the test
# Default : True
SUCCESS_MESSAGE_DISPLAY = True

# The message that will be sent
# ie : "Good answer !\nYou have been registered as an english speaker.\nHave a good game !"
SUCCESS_MESSAGE_TEXT = (
    "¡Respuesta correcta!\n"
    "\n"
    "Has sido marcado(a) como 'ES' en nuestra base de datos.\n"
    "El bot no te molestará más.\n"
    "\n"
    "¡Buen juego!"
)

# The player gave a bad answer or didn't answer at all
# -------------------------------------

# This text will be displayed on the kick screen
# Note : CLAN_URL is defined in CRCON's UI (Settings / Others / Discord Invite Url)
KICK_MESSAGE_TEXT = (
    "\nLo siento, compañero jugador de HLL,\n"
    "\n"
    "puedes ser de cualquier parte del mundo,\n"
    "pero debes *hablar* español\n"
    "para jugar en este servidor\n"
    "de 9am a 9pm UTC.\n"
    "\n"
    "Has sido expulsado(a) por un bot\n"
    "porque no escribiste (o escribiste mal)\n"
    "la palabra solicitada en el chat.\n"
    "\n"
    "Reclamaciones:\n"
    f"{CLAN_URL}\n\n"
)

# The player committed a TK while being tested
# -------------------------------------

# Action
# Available : "blacklist" (default) and "kickonly"
TK_ACTION = "blacklist"

# Blacklist id
# Default : 0 (the default and always available blacklist)
TK_BLACKLIST_ID = 0

# Blacklist duration
# ie : "hours=2" or "days=7"
# Default : None (never expires)
TK_BLACKLIST_EXPIRATION = None

# The message the player will see when blacklisted
# Note : CLAN_URL is defined in CRCON's UI (Settings / Others / Discord Invite Url)
TK_BAN_MESSAGE = (
    "\nYou decided to kill a teammate\n"
    "because a bot was testing your ability to understand french.\n"
    "This kind of behavior is not tolerated on our server.\n"
    "\n"
    "Decidiste matar a un compañero de equipo\n"
    "porque un bot estaba probando tu capacidad para entender español.\n"
    "Este tipo de comportamiento no es tolerado en nuestro servidor.\n"
    "\n"
    "Reclamaciones:\n"
    f"{CLAN_URL}\n\n"
)

# Discord
# -------------------------------------

# False : the only output will be the log file
USE_DISCORD = False

# Dedicated Discord's channel webhook
SERVER_CONFIG = [
    ["https://discord.com/api/webhooks/...", True],  # Server 1
    ["https://discord.com/api/webhooks/...", False],  # Server 2
    ["https://discord.com/api/webhooks/...", False],  # Server 3
    ["https://discord.com/api/webhooks/...", False],  # Server 4
    ["https://discord.com/api/webhooks/...", False],  # Server 5
    ["https://discord.com/api/webhooks/...", False],  # Server 6
    ["https://discord.com/api/webhooks/...", False],  # Server 7
    ["https://discord.com/api/webhooks/...", False],  # Server 8
    ["https://discord.com/api/webhooks/...", False],  # Server 9
    ["https://discord.com/api/webhooks/...", False]  # Server 10
]

# Display in Discord the random sentence sent to the player
DISCORD_EMBED_QUESTION_DISPLAY = True

# ghost : player disconnected before being tested
DISCORD_GHOST_EMOJI = ":airplane_departure:"
DISCORD_GHOST_EMBED_DISPLAY = False
DISCORD_GHOST_EMBED_COLOR = 0xffff00

# coward : player disconnected after seeing the question, but before being kicked
DISCORD_COWARD_EMOJI = ":chicken:"
DISCORD_COWARD_EMBED_DISPLAY = True
DISCORD_COWARD_EMBED_COLOR = 0xff8000

# kick : player has been kicked (he gave no/bad answer or commited a TK)
DISCORD_KICK_EMOJI = ":no_entry:"
DISCORD_KICK_EMBED_DISPLAY = True
DISCORD_KICK_EMBED_COLOR = 0xff0000

# valid : player gave a valid answer
DISCORD_VALID_EMBED_DISPLAY = True
DISCORD_VALID_EMBED_COLOR = 0x00ff00

# Display in Discord the processing time before disconnect/good answer/kick
DISCORD_EMBED_FOOTER_DISPLAY = True

# Miscellaneous (you should not change these)
# -------------------------------------

# Bot name that will be displayed in CRCON "audit logs" and Discord embeds
BOT_NAME = "CRCON_language_doorkeeper"

# The interval between watch turns (in seconds)
# Recommended : as the stats are to be gathered for all the players,
#               requiring a big amount of data from the game server,
#               you may encounter slowdowns if done too frequently.
# Recommended : not less than 60
# Default : 60
WATCH_INTERVAL_SECS = 60

# Time (seconds) the player has to enter the expected word in chat
# Note : you should expect a correct answer in ~15-45 secs
# Recommended : not less than 60
# Default : 60
TIME_TO_ANSWER_SEC = 60

# The maximum number of players the bot can test in a batch.
# A thread will be created for each one, so mind the CPU/RAM/network resources.
# Recommended : no more than 5. Expect connexion errors if set above.
# Default : 3
MAX_PLAYERS_TO_CHECK = 5

# We use the "punish" screen to display the question
# But : a player can't be punished if he's not in game (on map)
# Retrying to punish them until they enter the map.
# Recommended : no more than 5, as it will delay the next batch
# Default : 3
MAX_PUNISH_RETRIES = 3

# Waiting time (seconds) between each failed punish try
# Recommended : no more than 10, as it will delay the next batch
# Default : 10
PUNISH_RETRIES_INTERVAL = 10
