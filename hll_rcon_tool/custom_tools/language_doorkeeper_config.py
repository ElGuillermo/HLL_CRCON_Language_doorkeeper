"""
language_doorkeeper_config.py

A plugin for HLL CRCON (https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.

It has been designed for french servers, you'll have to adapt it to your language.

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
# Available : 0 english, 1 french, 2 german, 3 Spanish
LANG = 1

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
WHITELIST_PSEUDO_REGEX = r"(^|[^a-z0-9])FR(A|E|(ANCE)|(ENCH))?([^a-z0-9]|$)"

# Steam profile country codes whitelist
# Note : you can't really rely on this, as Steam API may not answer requests
# and we can't access GamePass, nor Epic users profiles
WHITELIST_STEAM_COUNTRY = True

# (Pays et régions francophones)
WHITELIST_STEAM_COUNTRIES = {
    "BE",  # Belgique
    "BF",  # Burkina Faso
    "BI",  # Burundi
    "BJ",  # Bénin
    "BL",  # Saint-Barthélemy
    # "CA",  # Canada
    # "CD",  # Congo (Kinshasa)
    # "CF",  # République d'Afrique centrale
    # "CG",  # Congo (Brazzaville)
    # "CH",  # Confédération helvétique
    "CI",  # Côte d'Ivoire
    "CM",  # Cameroun
    "DJ",  # Djibouti
    "DZ",  # Algérie
    "FR",  # France métropolitaine
    "GA",  # Gabon
    "GF",  # Guyane française
    "GN",  # Guinée
    "GP",  # Guadeloupe
    # "GQ",  # Guinée équatoriale
    # "HT",  # Haïti
    # "KM",  # Comores
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
    # "RW",  # Rwanda
    # "SC",  # Seychelles
    "SN",  # Sénégal
    # "TD",  # Tchad
    "TF",  # Terres australes et antarctiques françaises
    "TG",  # Togo
    "TN",  # Tunisie
    "VU",  # Vanuatu
    "WF",  # Wallis et Futuna
    "YT",  # Mayotte
}

# CRCON profile flag whitelist
# Players tagged with any of these flags won't be tested
WHITELIST_CRCON_EMOJI_FLAGS = {
    "🇧🇪",  # Belgique
    # "🇧🇱",  # Saint-Barthélemy
    # "🇨🇦",  # Canada
    # "🇨🇭",  # Confédération helvétique
    # "🇨🇵",  # Clipperton Island (FR) (identique au drapeau FR)
    # "🇩🇿",  # Algérie
    "🇫🇷",  # France
    # "🇬🇵",  # Guadeloupe
    # "🇲🇦",  # Maroc
    # "🇲🇨",  # Monaco
    # "🇲🇫",  # Saint-Martin (FR) (identique au drapeau FR)
    # "🇲🇶",  # Martinique
    # "🇵🇫",  # Polynésie française
    # "🇵🇲",  # Saint-Pierre et Miquelon
    # "🇹🇳",  # Tunisie
    # "🇻🇺",  # Vanuatu
    # "🇼🇫",  # Wallis et Futuna
}


# Random question that will be asked to the player
# -------------------------------------

# Explain to the player why (s)he has been punished and give instructions to answer.
# ie : "You've been killed by a bot.\nEnter the second word of the following sentence in chat :"
# Note : the random question sentence will be added to the end of this text.
# Hint : do not use digits (2, 3, 4, ...), as they help to guess the answer.
GENERIC_QUESTION_INTRO = (
    "\n\n[ Vérification automatique ]\n"
    "\n"
    "French *speaking* only server\n"
    "(from 9am to 9pm UTC)\n"
    "\n"
    "Tape dans le chat le deuxième mot de la phrase\n"
    "(tel qu'il apparaît et sans rien ajouter) :\n\n"
)

# The sentence the player will have to "decode"
# The four {} {} {} {} random items will be displayed in this order :
# FIRST_WORDS_LIST, SECOND_WORDS_LIST, THIRD_WORDS_LIST and FOURTH_WORDS_LIST
# The player will have to enter the word randomly chosen in FIRST_WORDS_LIST
# ie : "'Did the {} {} {} jumped over the lazy {} ?' (Y/N)"
# Hint : keep the question mark (?) and the (Y/N) at end for an extra trap !
GENERIC_QUESTION = "'Le {} {} {} {} ?' (O/N)\n\n"

# One of these words will replace the first {} in GENERIC_QUESTION
# Note : this is the one the player will have to enter in chat
# hint : use accents if you have them in your language,
#        as they're not easy to enter with a foreign keyboard
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
    "abimé", "âgé", "bleuté", "brisé", "cabossé", "cassé", "dirigé", "dégradé",
    "épais", "étalé", "foncé", "fracassé", "grisé", "guidé",
    "hébété", "humidifié", "idéal", "illuminé", "jeté", "jalousé",
    "kaki", "kamikaze", "lésé", "lancé", "mouillé", "modéré", "nacré", "noyé",
    "orangé", "ovalisé", "paré", "paumé", "qualifié", "quantifié",
    "raté", "rapiécé", "salé", "sédentaire", "tourmenté", "trempé", "unifié", "usé",
    "validé", "vérolé", "wallon", "wallisien", "xénophile", "xénophobe",
    "yankee", "yéménite", "zébré", "zélé"
)


# The player gave a valid answer
# -------------------------------------

# This emoji flag will be added to the validated player's CRCON profile
# IMPORTANT : do not forget to add it to the WHITELIST_CRCON_EMOJI_FLAGS above
# Find your flag code : https://emojipedia.org/
# Copy-paste it in there as it is, like "🇫🇷", NOT in Discord's format (":flag_fr:")
VERIFIED_PLAYER_FLAG = "🇫🇷"

# This flag will be used to illustrate the player's success in a Discord embed
# You can use you country flag or any emoji, like : ":white_check_mark:" or ":heart:"
VERIFIED_PLAYER_FLAG_EMBED = ":flag_fr:"

# Send a message to inform the players they passed the test
# Default : True
SUCCESS_MESSAGE_DISPLAY = True

# The message that will be sent
# ie : "Good answer !\nYou have been registered as an english speaker.\nHave a good game !"
SUCCESS_MESSAGE_TEXT = (
    "Bonne réponse !\n"
    "\n"
    "Tu as été marqué(e) 'FR' dans notre base.\n"
    "Le bot ne t'embêtera plus.\n"
    "\n"
    "Bon jeu !"
)


# The player gave a bad answer or didn't answer at all
# -------------------------------------

# This text will be displayed on the kick screen
# Note : CLAN_URL is defined in CRCON's UI (Settings / Others / Discord Invite Url)
KICK_MESSAGE_TEXT = (
    "\nSorry, fellow HLL player,\n"
    "\n"
    "you can be from anywhere in the world,\n"
    "but you have to *speak* french\n"
    "to play on this server\n"
    "from 9am to 9pm UTC.\n"
    "\n"
    "Tu as été exclu(e) par un bot\n"
    "car tu n'as pas (ou mal) écrit\n"
    "le mot demandé dans le chat.\n"
    "\n"
    "Réclamations :\n"
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
    "Tu as décidé de tuer un coéquipier\n"
    "parce qu'un bot testait ta capacité à comprendre le français.\n"
    "Ce type de comportement n'est pas toléré sur notre serveur.\n"
    "\n"
    "Réclamations :\n"
    f"{CLAN_URL}\n\n"
)


# Discord
# -------------------------------------

# False : the only output will be the log file
USE_DISCORD = True

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
