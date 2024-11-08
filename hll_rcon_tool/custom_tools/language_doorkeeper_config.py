"""
language_doorkeeper_config

A plugin for HLL CRCON (https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.

(preconfigured for french servers, you'll have to adapt it to your language)

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""

from custom_tools.common_functions import CLAN_URL


# Configuration (you must review/change these)
# -----------------------------------------------------------------------------

# Simulation mode : no *real* action (messsage/punish/kick/ban) will be done
TEST_MODE = False

# The script can work without any Discord output
# If "False", the only output would be the log file
USE_DISCORD = True

# Dedicated Discord's channel webhook
# ServerNumber, Webhook, Enabled
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

# Activity schedule
# Hours are in UTC (heure d'hiver : UTC = FR-1 ; heure d'été : UTC = FR-2)
# ie : "0: (4, 30, 21, 15)" means "active on mondays, from 4:30am to 9:15pm
# ie : "3: (0, 0, 23, 59)" means "active on thursdays, from 0:00am to 11:59pm"
SCHEDULE = {
    0: (4, 1, 21, 0),  # Monday
    1: (4, 1, 21, 0),  # Tuesday
    2: (4, 1, 21, 0),  # Wednesday
    3: (4, 1, 21, 0),  # Thursday
    4: (4, 1, 21, 0),  # Friday
    5: (4, 1, 21, 0),  # Saturday
    6: (4, 1, 21, 0)  # Sunday
}

# Don't run if the total players number would drop below (seed limit).
DONT_KICK_BELOW = 45


# Configuration (default settings)
# -----------------------------------------------------------------------------

# The interval between watch turns (in seconds)
# Recommended : as the stats are to be gathered for all the players,
#               requiring a big amount of data from the game server,
#               you may encounter slowdowns if done too frequently.
# Recommended : not less than 60 secs
# Default : 60
WATCH_INTERVAL_SECS = 60

# Time (seconds) the player has to enter the expected word in chat
# Note : you should expect a correct answer in ~15-45 secs
# Recommended : not less than 60 secs
# Default : 60
TIME_TO_ANSWER_SEC = 60

# True : the answer must be the expected word *only*
# False : the expected word can be found in a sentence
# Hint : use "True" (some foreigners *will* try to enter the whole sentence)
ANSWER_EXACT_MATCH = True
# True : capitals matter (Bob != BOB)
# False : cApItAlS dOn'T mAtTeR (Bob == BOB == bOb)
ANSWER_CASE_SENSITIVE = True

# What should we do with those who TK after being punished by the bot ?
# Available actions : "blacklist", "kickonly"
# Default : "blacklist"
TK_ACTION = "blacklist"

# Only applies if TK_ACTION = "blacklist"
# Default : 0 (the default and always available blacklist)
TK_BLACKLIST_ID = 2
# A duration. ie : "hours=2" or "days=7"
# Default : None (never expires)
TK_BLACKLIST_EXPIRATION = None


# Messages
# -------------------------------------

# Question sentence intro
# Explain to the player why (s)he has been punished
# and give instructions to answer the question.
# ie : "you've been killed by a bot,\n"
#      "enter the nth word of the following sentence in chat :"
# Hint : do not use digits (2,3,4,...) : they help to guess the answer.
# Note : the random question sentence will be added to the end of this text.
GENERIC_QUESTION_INTRO = (
    "\n\n[ Bot de vérification ]\n"
    "\n"
    "French *speaking* only server\n"
    "(from 3am to 8pm UTC)\n"
    "\n"
    "Tape dans le chat le deuxième mot de la phrase\n"
    "(tel qu'il apparaît et sans rien ajouter) :\n\n"
)

# The sentence the player will have to "decode"
# There is four {} {} {} {} random items that will be displayed in this order :
# FIRST_WORDS_LIST, SECOND_WORDS_LIST, THIRD_WORDS_LIST and FOURTH_WORDS_LIST
# The player will have to enter the word randomly chosen in FIRST_WORDS_LIST
# ie : "'Did the {} {} {} jumped over the lazy {} ?' (Y/N)"
# Hint : keep the question mark (?) and the (Y/N) at end for an extra trap !
GENERIC_QUESTION = "'Le {} {} {} {} ?' (O/N)\n\n"

# This message will be displayed on the kick screen
KICK_MESSAGE_TEXT = (
    "\nSorry, fellow HLL player,\n"
    "\n"
    "you can be from anywhere in the world,\n"
    "but you have to *speak* french\n"
    "to play on this server\n"
    "from 3am to 8pm UTC.\n"
    "\n"
    "Tu as été exclu(e) par un bot\n"
    "car tu n'as pas (ou mal) écrit\n"
    "le mot demandé dans le chat.\n"
    "\n"
    "Réclamations :\n"
    f"{CLAN_URL}\n\n"
)

# The ingame message sent to inform the players they passed the test
# Default : True (let's be cool : we killed them just before)
SUCCESS_MESSAGE_DISPLAY = True
SUCCESS_MESSAGE_TEXT = (
    "Bonne réponse !\n"
    "\n"
    "Tu as été marqué(e) 'FR' dans notre base.\n"
    "Le bot ne t'embêtera plus.\n"
    "\n"
    "Bon jeu !"
)

# This flag will be added to the validated player's CRCON profile
# Note : do not forget to add it to the CRCON_EMOJI_FLAGS_WHITELIST below !
# Find your flag code : https://emojipedia.org/
VERIFIED_PLAYER_FLAG = "🇫🇷"
VERIFIED_PLAYER_FLAG_COMMENT = "A bien répondu à la question du bot."

# In case of TK : the message the player will see when blacklisted
TK_BAN_MESSAGE = (
    "\nYou decided to kill a teammate\n"
    "because a bot was testing your ability to understand french.\n"
    "This kind of behavior is not tolerated on our server.\n"
    "\n"
    "Tu as décidé de tuer un coéquipier\n"
    "parce qu'un bot testait ta capacité à comprendre le français.\n"
    "Ce type de comportement n'est pas toléré sur notre serveur.\n"
    "\n"
    "Réclamations :\n"
    f"{CLAN_URL}\n\n"
)


# Random question elements
# -------------------------------------

# One of these words will replace the first {} in GENERIC_QUESTION
# Note : This is the one the player will have to enter in chat
# hint : use accents : they're not easy to enter with a foreign keyboard
FIRST_WORDS_LIST = (
    "béret", "béton", "blé", "boléro", "café", "canapé", "ciné", "côté",
    "dé", "décor", "débat", "degré", "fémur", "flétan", "fléau", "fossé",
    "géant", "génépi", "génie", "gué", "haché", "henné", "héron", "héros",
    "jéroboam", "jésuite", "jubilé", "karaté", "kébab", "képi", "kérosène",
    "laqué", "légume", "lézard", "lycée", "mégot", "mérou", "métal", "métro",
    "narguilé", "naufragé", "néon", "numéro", "passé", "pavé", "pépin", "pré",
    "quarté", "quinté", "récif", "résumé", "rodéo", "rosé",
    "saké", "schéma", "séchoir", "sérum",
    "télex", "thé", "tiercé", "traité", "trésor",
    "ukulélé", "vélo", "vélin", "velouté", "vérin", "wattmètre",
    "xénon", "xérès", "yéyé", "zèbre", "zébu", "zénith", "zéro"
)
# One of these words will replace the second {} in GENERIC_QUESTION
SECOND_WORDS_LIST = (
    "d'Anne", "de Benoît", "de Carole", "de Dominique", "d'Elliot", "de Félix",
    "de Guillaume", "d'Horace", "d'Isabelle", "de Jeanne", "de Karl",
    "de Luna", "de Medhi", "de Noé", "d'Oscar", "de Pierre", "de Quentin",
    "de Rita", "de Sam", "de Théo", "d'Ulysse", "de Vincent", "de Willy",
    "de Xavier", "de Yann", "de Zoé"
)
# One of these words will replace the third {} in GENERIC_QUESTION
THIRD_WORDS_LIST = (
    "apparaissait-il", "est-il apparu", "apparaît-il", "apparaîtra-t-il",
    "devenait-il", "est-il devenu", "devient-il", "deviendra-t-il",
    "était-il", "a-t-il été", "est-il", "sera-t-il",
    "se montrait-il", "s'est-il montré", "se montre-t-il", "se montrera-t-il",
    "paraissait-il", "a-t-il paru", "paraît-il", "paraîtra-t-il",
    "semblait-il", "a-t-il semblé", "semble-t-il", "semblera-t-il"
)
# One of these words will replace the fourth {} in GENERIC_QUESTION
FOURTH_WORDS_LIST = (
    "abimé", "âgé", "bleu", "brisé", "cabossé", "cassé", "dirigé", "droit",
    "épais", "étalé", "foncé", "fracassé", "gris", "guidé",
    "haut", "humidifié", "idéal", "illuminé", "joli", "juste",
    "kaki", "kamikaze", "lent", "lustré", "marron", "mou", "nacré", "neuf",
    "orange", "ovale", "plat", "pourri", "qualitatif", "quelconque",
    "raté", "rouge", "sale", "solaire", "torride", "trempé", "unique", "usé",
    "vieux", "violet", "wallon", "wallisien", "xénophile", "xénophobe",
    "yankee", "yéménite", "zébré", "zélé"
)


# Logs and Discord
# -------------------------------------

# Common strings (logs/embeds)
EXPECTED_ANSWER_COMMENT = "Réponse attendue"  # "Expected answer"
RECEIVED_ANSWER_COMMENT = "Réponse reçue"  # "Received answer"
NOANSWER_DEFAULT_TXT = "(rien)"  # "(nothing)"
ACTION_RESULT_COMMENT = "Résultat"  # "Result"

# ghost : player disconnected before being punished/seeing the question
DISCORD_GHOST_EMOJI = ":airplane_departure:"
DISCORD_GHOST_COMMENT = "est parti avant la question."  # "Leaved before the test"
DISCORD_GHOST_EMBED_DISPLAY = False
DISCORD_GHOST_EMBED_COLOR = 0xffff00
# coward : player disconnected after seeing the question, but before the kick
DISCORD_COWARD_EMOJI = ":chicken:"
DISCORD_COWARD_COMMENT = "est parti avant le kick."  # "Leaved before the kick"
DISCORD_COWARD_EMBED_DISPLAY = True
DISCORD_COWARD_EMBED_COLOR = 0xff8000
# kick : player has been kicked (he gave no/a bad answer or TKed)
DISCORD_KICK_EMOJI = ":no_entry:"
DISCORD_KICK_COMMENT = "a été kické du serveur."  # "has been kicked"
DISCORD_KICK_EMBED_DISPLAY = True
DISCORD_KICK_EMBED_COLOR = 0xff0000
# valid : player has been flagged as 'verified' (gave a correct answer)
DISCORD_VALID_EMOJI = ":flag_fr:"  # Use the Discord emoji syntax (":emoji:")
DISCORD_VALID_COMMENT = "a été flaggé 'FR'."  # "passed the test"
DISCORD_VALID_EMBED_DISPLAY = True
DISCORD_VALID_EMBED_COLOR = 0x00ff00

# Display in Discord the random sentence sent to the player (True/False)
DISCORD_EMBED_QUESTION_DISPLAY = True
# Display in Discord the processing time before disconnect/good answer/kick (True/False)
DISCORD_EMBED_FOOTER_DISPLAY = True
# Caption before the processing time display
DISCORD_EMBED_FOOTER_INTRO_TXT = "Temps de traitement (secs) : "  # "Processing time (secs) : "


# Whitelists
# -------------------------------------

# Steam profile country codes whitelist
# Note : you can't really rely on this, as Steam API may not answer requests
# and GamePass users have no specified country
USE_STEAM_COUNTRIES_WHITELIST = True
# (Pays et régions francophones)
STEAM_COUNTRIES_WHITELIST = {
    "BE",  # Belgique
    "BF",  # Burkina Faso
    "BI",  # Burundi
    "BJ",  # Bénin
    "BL",  # Saint-Barthélemy
    # "CA",  # Canada
    # "CD",  # Congo (Kinshasa)
    # "CF",  # République d'Afrique centrale
    # "CG",  # Congo (Brazzaville)
    "CH",  # Confédération helvétique
    "CI",  # Côte d'Ivoire
    "CM",  # Cameroun
    "DJ",  # Djibouti
    "DZ",  # Algérie
    "FR",  # France
    "GA",  # Gabon
    "GF",  # Guyane française
    "GN",  # Guinée
    "GP",  # Guadeloupe
    "GQ",  # Guinée équatoriale
    "HT",  # Haïti
    "KM",  # Comores
    # "LB",  # Liban
    # "LU",  # Luxembourg
    "MA",  # Maroc
    "MC",  # Monaco
    "MF",  # Saint-Martin
    "MG",  # Madagascar
    "ML",  # Mali
    "MQ",  # Martinique
    "MR",  # Mauritanie
    "MU",  # Île Maurice
    # "NC",  # Nouvelle Calédonie
    "NE",  # Niger
    "PF",  # Polynésie française
    "PM",  # Saint-Pierre et Miquelon
    "QC",  # Québec
    "RE",  # La Réunion
    "RW",  # Rwanda
    # "SC",  # Seychelles
    "SN",  # Sénégal
    "TD",  # Tchad
    "TF",  # Terres australes et antarctiques françaises
    "TG",  # Togo
    "TN",  # Tunisie
    "VU",  # Vanuatu
    "WF",  # Wallis et Futuna
    "YT",  # Mayotte
}

# CRCON profile flag whitelist
# Players tagged with any of these won't be tested
CRCON_EMOJI_FLAGS_WHITELIST = {
    "🇧🇪",  # Belgique
    "🇧🇱",  # Saint-Barthélemy
    "🇨🇦",  # Canada
    "🇨🇭",  # Confédération helvétique
    "🇨🇵",  # Clipperton Island (FR) (identique au drapeau FR)
    "🇩🇿",  # Algérie
    "🇫🇷",  # France
    "🇬🇵",  # Guadeloupe
    "🇲🇦",  # Maroc
    "🇲🇨",  # Monaco
    "🇲🇫",  # Saint-Martin (FR) (identique au drapeau FR)
    "🇲🇶",  # Martinique
    "🇵🇫",  # Polynésie française
    "🇵🇲",  # Saint-Pierre et Miquelon
    "🇹🇳",  # Tunisie
    "🇻🇺",  # Vanuatu
    "🇼🇫",  # Wallis et Futuna
}


# Miscellaneous
# -------------------------------------

# Bot name that will be displayed in CRCON "audit logs" and Discord embeds
BOT_NAME = "CRCON_language_doorkeeper"

# The maximum number of players the bot can test in a batch.
# A new thread will be created for each one, so mind the CPU/RAM resources !
# Recommended : no more than 5
# Default : 5
MAX_PLAYERS_TO_CHECK = 5

# We use the "punish" screen to display the question
# But : a player can't be punished if he's not in game (on map)
# Retrying to punish them until they enter the map.
# Recommended : no more than 5, as it will delay the next batch
# Default : 5
MAX_PUNISH_RETRIES = 5

# Waiting time (seconds) between each failed punish try
# Recommended : no more than 10, as it will delay the next batch
# Default : 10
PUNISH_RETRIES_INTERVAL = 10
