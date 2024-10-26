"""
automod_verif_fr

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.
(preconfigured with french parameters, you can adapt it to your language)

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""
import logging
from datetime import datetime, timezone, timedelta
from multiprocessing.pool import ThreadPool
import random
import re
from time import sleep
from typing import Literal, List
import discord  # type: ignore
from rcon.blacklist import add_record_to_blacklist
from rcon.game_logs import get_recent_logs
from rcon.player_history import add_flag_to_player
from rcon.rcon import Rcon
from rcon.settings import SERVER_INFO
from custom_tools.custom_common import (
    CLAN_URL,
    DISCORD_EMBED_AUTHOR_URL,
    DISCORD_EMBED_AUTHOR_ICON_URL,
    get_avatar_url,
    get_external_profile_url,
    seconds_until_start
)


# Configuration (you must change these)
# -----------------------------------------------------------------------------

# Don't forget you have some parameters to set in 'custom_common.py' too !

# Simulation mode : no *real* action (messsage/punish/kick/ban) will be done
TEST_MODE = False

# The script can work without any Discord output
# If "False", the only output would be the log file
USE_DISCORD = True

# Dedicated Discord's channel webhook
DISCORD_WEBHOOK = (
    "https://discord.com/api/webhooks/..."
)

# Activity schedule
# Hours are in UTC (heure d'hiver : UTC = FR-1 ; heure d'été : UTC = FR-2)
# ie : "0: (4, 30, 21, 15)" means "active on mondays, from 4:30am to 9:15pm
# ie : "3: (0, 0, 23, 59)" means "active on thursdays, from 0:00am to 11:59pm"
SCHEDULE = {
    0: (3, 1, 20, 0),  # Monday
    1: (3, 1, 20, 0),  # Tuesday
    2: (3, 1, 20, 0),  # Wednesday
    3: (3, 1, 20, 0),  # Thursday
    4: (3, 1, 20, 0),  # Friday
    5: (3, 1, 20, 0),  # Saturday
    6: (3, 1, 20, 0)  # Sunday
}

# Don't run if the total players number would drop below (seed limit).
DONT_KICK_BELOW = 45


# Configuration (default settings)
# -----------------------------------------------------------------------------

# The interval between watch turns (in seconds)
# Recommended : as the stats are to be gathered for all the players,
#               requiring a big amount of data from the game server,
#               you may encounter slowdowns if done too frequently.
# Recommended : not less than 30 secs
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
# Note : Do not forget to add it to the CRCON_EMOJI_FLAGS_WHITELIST below !
# Find your flag code : https://emojipedia.org/
VERIFIED_PLAYER_FLAG = "🇫🇷"
VERIFIED_PLAYER_FLAG_COMMENT = "A bien répondu à la question du bot verif_fr."

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
EXPECTED_ANSWER_COMMENT = "Réponse attendue"
RECEIVED_ANSWER_COMMENT = "Réponse reçue"
NOANSWER_DEFAULT_TXT = "(rien)"
ACTION_RESULT_COMMENT = "Résultat"

# ghost : player disconnected before being punished/seeing the question
DISCORD_GHOST_EMOJI = ":airplane_departure:"
DISCORD_GHOST_COMMENT = "est parti avant la question."
DISCORD_GHOST_EMBED_DISPLAY = False
DISCORD_GHOST_EMBED_COLOR = 0xffff00
# coward : player disconnected after seeing the question, but before the kick
DISCORD_COWARD_EMOJI = ":chicken:"
DISCORD_COWARD_COMMENT = "est parti avant le kick."
DISCORD_COWARD_EMBED_DISPLAY = True
DISCORD_COWARD_EMBED_COLOR = 0xff8000
# kick : player has been kicked (he gave no/a bad answer or TKed)
DISCORD_KICK_EMOJI = ":no_entry:"
DISCORD_KICK_COMMENT = "a été kické du serveur."
DISCORD_KICK_EMBED_DISPLAY = True
DISCORD_KICK_EMBED_COLOR = 0xff0000
# valid : player has been flagged as 'verified' (gave a correct answer)
DISCORD_VALID_EMOJI = ":flag_fr:"
DISCORD_VALID_COMMENT = "a été flaggé 'FR'."
DISCORD_VALID_EMBED_DISPLAY = True
DISCORD_VALID_EMBED_COLOR = 0x00ff00

# Display the random sentence sent to the player (True/False)
DISCORD_EMBED_QUESTION_DISPLAY = True
# Display the processing time before disconnect/good answer/kick (True/False)
DISCORD_EMBED_FOOTER_DISPLAY = True
# Caption before the processing time display
DISCORD_EMBED_FOOTER_INTRO_TXT = "Temps de traitement (secs) : "


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
BOT_NAME = "CRCON_automod_verif_fr"

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


# (End of configuration)
# -----------------------------------------------------------------------------


def should_we_run():
    """
    Test various running conditions before monitoring players
    """
    # Don't run : outside activity schedule
    seconds_before_start = seconds_until_start(SCHEDULE)
    if seconds_before_start != 0:
        if seconds_before_start < WATCH_INTERVAL_SECS:
            return
        logger.info(
            "Waiting for %s (%s secs).",
            str(timedelta(seconds = (seconds_before_start + WATCH_INTERVAL_SECS))),
            str(seconds_before_start + WATCH_INTERVAL_SECS)
        )
        sleep(seconds_before_start)
        return

    # Get server infos
    rcon = Rcon(SERVER_INFO)
    try:
        gamestate_request = rcon.get_gamestate()
    except Exception as error:
        logger.error("Gamestate can't be read - %s", error)
        return

    if WATCH_INTERVAL_SECS < 300:
        sleep_time = 300 - WATCH_INTERVAL_SECS
    else:
        sleep_time = 0

    # Don't run : there's no more than DONT_KICK_BELOW players on map
    players_count = (
        gamestate_request["num_allied_players"]
        + gamestate_request["num_axis_players"]
    )
    if players_count <= DONT_KICK_BELOW:
        logger.info(
            "Not enough players on map (%s/%s). Next check in %s minutes.",
            str(players_count),
            str(DONT_KICK_BELOW),
            str(round((sleep_time + WATCH_INTERVAL_SECS) / 60))
        )
        sleep(sleep_time)
        return

    # Don't run : the game is ending in less than 90 secs
    remain_hours, remain_mins, remain_secs = (
        gamestate_request["raw_time_remaining"].split(':')
    )
    remain_time_secs = (
        int(remain_hours) * 3600 + int(remain_mins) * 60 + int(remain_secs)
    )
    if remain_time_secs < 90:
        logger.info(
            "Game is ending (%s secs remaining). Next check in %s minutes.",
            remain_time_secs, round((sleep_time + WATCH_INTERVAL_SECS) / 60)
        )
        sleep(sleep_time)
        return

    # Let's run !
    filter_players(
        rcon=rcon,
        players_count=players_count
    )


def filter_players(
    rcon: Rcon,
    players_count: int
):
    """
    Find the players whom language isn't known/guessable
    """
    try:
        players = rcon.get_players()
    except Exception as error:
        logger.error("get_players() failed - %s", error)
        return

    # Multithreading init
    to_check = []
    max_players_in_batch = min(
        players_count - DONT_KICK_BELOW, MAX_PLAYERS_TO_CHECK
    )

    for player in players:

        try:
            profile = player.get("profile")
        except Exception as error:
            logger.error(
                "'%s' - Profile can't be read - %s", player["name"],
                error
            )
            continue

        # A whitelisted flag has been set on the CRCON profile
        flags = profile.get("flags", []) if profile else []
        if any(f["flag"] in CRCON_EMOJI_FLAGS_WHITELIST for f in flags):
            continue

        # The player's pseudo contains 'FR', 'FRA', 'FRE', 'FRANCE' or 'FRENCH'
        if re.findall(
            r"(^|[^a-z0-9])FR(A|E|(ANCE)|(ENCH))?([^a-z0-9]|$)",
            player["name"],
            re.IGNORECASE
        ):
            continue

        # Connected since less than 50s (not on map yet : can't be punished)
        try:
            current_playtime_seconds = (
                profile.get("current_playtime_seconds") if profile else 0
            )
            if (
                current_playtime_seconds < 50
                or current_playtime_seconds > 86400
            ):
                continue
        except Exception as error:
            logger.error(
                "'%s' - Can't get current_playtime_seconds - %s",
                player["name"], error
            )

        # A whitelisted country is set on the player's Steam profile
        if USE_STEAM_COUNTRIES_WHITELIST:
            try:
                if player["country"] in STEAM_COUNTRIES_WHITELIST:
                    continue
            except Exception as error:
                logger.warning(
                    "'%s' - Can't get Steam profile country - %s",
                    player["name"],
                    error
                )

        # The player has a "real" VIP (not <24h : seeder's or gameplay reward)
        if player["is_vip"]:
            try:
                vips = profile.get("vips", []) if profile else []
                if vips is not None and len(vips) != 0:
                    for vip in vips:
                        exp_secs = int(
                            (
                                vip["expiration"] - datetime.now(timezone.utc)
                            ).total_seconds()
                        )
                        if exp_secs > 86400:
                            continue
            except Exception as error:
                logger.warning(
                    "'%s' - Can't get VIP expiration - %s",
                    player["name"],
                    error
                )

        # No exemption could be found : this player will be tested

        if len(to_check) < max_players_in_batch:

            if TEST_MODE:
                dry_run_warning = "(TEST MODE) - "
            else:
                dry_run_warning = ""

            logger.info(
                "%s'%s' - Will be verified - connected for %s - %s",
                dry_run_warning,
                player["name"],
                str(timedelta(seconds=current_playtime_seconds)),
                get_external_profile_url(player["player_id"], player["name"])
            )

            generic_question = GENERIC_QUESTION
            question_first_word_random = random.choice(FIRST_WORDS_LIST)
            question_sentence = generic_question.format(
                question_first_word_random,
                random.choice(SECOND_WORDS_LIST),
                random.choice(THIRD_WORDS_LIST),
                random.choice(FOURTH_WORDS_LIST)
            )

            # Add the player to the batch
            to_check.append(
                dict(
                    player_name=player["name"],
                    player_id=player["player_id"],
                    question_sentence=question_sentence,
                    expected_answers_list=[question_first_word_random]
                )
            )

        # Batch now contains max_players_in_batch : process them
        else:
            break

    # Batch processing
    try:
        if len(to_check) > 0:
            logger.info(
                "\n\n--- New batch - %s player(s) to check ---"
                "---------------------------------------",
                len(to_check)
            )

            with ThreadPool(processes=len(to_check)) as thread:
                thread.map(_process_security_question, to_check)

            logger.info(
                "\n--- End of batch processing ------------"
                "---------------------------------------\n"
            )
    except Exception as error:
        logger.error("Can't launch _process_security_question() : %s", error)


def _process_security_question(item):
    ask_security_question(**item)


def still_there_or_not(
    rcon: Rcon,
    player_name: str
) -> bool:
    """
    Checks if the player is still connected to the game server
    returns True if yes, False if no
    """
    try:
        players_ingame_list = rcon.get_players()
        for player_ingame in players_ingame_list:
            if player_ingame["name"] == player_name:
                return True
    except Exception as error:
        logger.error("Can't get players list - %s", error)
    return False


def ask_security_question(
    player_name: str,
    player_id: str,
    question_sentence: str,
    expected_answers_list: List[str]
):
    """
    Displays the question within a "punish" screen
    """
    if TEST_MODE:
        logger.info(
            "(DRY RUN) -  '%s' - Would have been tested.",
            player_name
        )
        return

    rcon = Rcon(SERVER_INFO)
    max_punish_retries = MAX_PUNISH_RETRIES
    punish_success = False

    while max_punish_retries >= 0:

        try:
            rcon.punish(
                player_name=player_name,
                reason=GENERIC_QUESTION_INTRO + question_sentence,
                by=BOT_NAME
            )

        # Can't be punished - player may be in the lobby, already dead, or gone
        except Exception:

            # Player is still connected
            if still_there_or_not(rcon, player_name):
                if max_punish_retries > 0:
                    logger.warning(
                        "'%s' - Can't be punished. Will retry %s time(s)",
                        player_name, max_punish_retries
                    )
                    sleep(PUNISH_RETRIES_INTERVAL)
                max_punish_retries = max_punish_retries - 1
                continue

            # Player has disconnected before being punished
            report(
                report_mode="ghost",
                player_id=player_id,
                player_name=player_name,
                question_sentence=question_sentence,
                expected_answers_list=expected_answers_list
            )
            return

        # Player has been punished
        else:
            punish_success = True
            logger.info(
                "'%s' - Saw the question.",
                player_name
            )
            break

    # No retries left - player couldn't be punished
    if not punish_success:
        logger.warning(
            "'%s' - Couldn't be punished. Will be tested in next batch.",
            player_name
        )
        return

    # Player has been punished
    watch_logs(
        rcon=rcon,
        player_name=player_name,
        player_id=player_id,
        question_sentence=question_sentence,
        expected_answers_list=expected_answers_list
    )


def watch_logs(
    rcon: Rcon,
    player_name: str,
    player_id: str,
    question_sentence: str,
    expected_answers_list: List[str]
):
    """
    Player has been punished (saw the question)
    Monitor server logs :
    - wait for "TEAM KILL"
    - wait for "DISCONNECTED"
    - wait for a valid answer in "CHAT"
    """
    if not ANSWER_CASE_SENSITIVE:
        expected_answers_list = [
            answer.upper() for answer in expected_answers_list
        ]
    his_answers_list = []
    answered_with_tk = False
    disconnected = False
    correct_answer = False
    start = datetime.now(timezone.utc)
    start_timestamp_int = int(start.timestamp())

    # Monitoring logs, expecting an answer in chat
    while (
        datetime.now(timezone.utc) - start
    ).total_seconds() <= TIME_TO_ANSWER_SEC:
        try:
            logs = get_recent_logs(
                # start=0,  # Default : 0
                end=300,  # Default : 100000
                player_search=player_name,
                action_filter=["CHAT", "DISCONNECTED", "TEAM KILL"],
                min_timestamp=start_timestamp_int,
                exact_player_match=True,  # Default : False
                # exact_action=False,  # Won't work because "CHAT[Axis][Team]"
                # inclusive_filter=True,  # Default : True
            )
        except Exception:
            logger.error("'%s' - Couldn't get the logs", player_name)
            sleep(5)
            continue  # Will retry until TIME_TO_ANSWER_SEC expires

        # Analyzing logs
        for log in logs["logs"]:

            if (
                log["action"] == "TEAM KILL"
                and log["player_name_1"] == player_name
            ):
                answered_with_tk = True
                break

            if log["action"] == "DISCONNECTED":
                disconnected = True
                break

            # log["action"] == "CHAT"
            if log["sub_content"] and len(log["sub_content"]) != 0:

                if log["sub_content"] not in his_answers_list:
                    his_answers_list.append(log["sub_content"])

                if ANSWER_EXACT_MATCH:
                    if not ANSWER_CASE_SENSITIVE:
                        if log["sub_content"].upper() in expected_answers_list:
                            correct_answer = True
                            break
                    else:
                        if log["sub_content"] in expected_answers_list:
                            correct_answer = True
                            break
                else:
                    if not ANSWER_CASE_SENSITIVE:
                        for answer in expected_answers_list:
                            if re.findall(
                                answer, log["sub_content"],
                                re.IGNORECASE
                            ):
                                correct_answer = True
                                break
                    else:
                        for answer in expected_answers_list:
                            if re.findall(answer, log["sub_content"]):
                                correct_answer = True
                                break

        # Player committed a TK
        if answered_with_tk:
            total_answer_time_secs = int(
                (datetime.now(timezone.utc) - start).total_seconds()
            )
            logger.info(
                "'%s' - Committed a TK in %s secs.",
                player_name,
                total_answer_time_secs
            )
            break

        # Player has disconnected
        if disconnected:
            total_answer_time_secs = int(
                (datetime.now(timezone.utc) - start).total_seconds()
            )
            logger.info(
                "'%s' - Has disconnected in %s secs.",
                player_name,
                total_answer_time_secs
            )
            break

        # Player gave a valid answer
        if correct_answer:
            total_answer_time_secs = int(
                (datetime.now(timezone.utc) - start).total_seconds()
            )
            logger.info(
                "'%s' - Gave a valid answer in %s secs.",
                player_name,
                total_answer_time_secs
            )
            success(
                rcon=rcon,
                player_name=player_name,
                player_id=player_id,
                question_sentence=question_sentence,
                expected_answers_list=expected_answers_list,
                his_answers_list=his_answers_list,
                total_answer_time_secs=total_answer_time_secs
            )
            return

        # Answering time isn't over. No valid response yet...
        # Sleep time to avoid a fast loop that consumes a lot of CPU time
        sleep(1)

    # Player committed a TK / disconnected / didn't give the right answer

    # Time is up and player gave no/bad answer(s)
    if not answered_with_tk and not disconnected:
        total_answer_time_secs = int(
            (datetime.now(timezone.utc) - start).total_seconds()
        )

    # Giving a default value to the answer if player didn't answered at all
    if len(his_answers_list) == 0:
        his_answers_list.append(NOANSWER_DEFAULT_TXT)

    failure(
        rcon=rcon,
        player_name=player_name,
        player_id=player_id,
        question_sentence=question_sentence,
        expected_answers_list=expected_answers_list,
        his_answers_list=his_answers_list,
        answered_with_tk=answered_with_tk,
        disconnected=disconnected,
        total_answer_time_secs=total_answer_time_secs
    )


def success(
    rcon: Rcon,
    player_name: str,
    player_id: str,
    question_sentence: str,
    expected_answers_list: List[str],
    his_answers_list: List[str],
    total_answer_time_secs: int
):
    """
    Player gave a valid answer
    - set a 'validated' tag on its CRCON profile
    - send Discord embed
    - send a 'success' ingame message
    """
    # Flags player's CRCON profile
    flag_success = False
    retries = 3  # hardcoded
    while retries >= 0:
        try:
            add_flag_to_player(
                player_id=player_id,
                flag=VERIFIED_PLAYER_FLAG,
                comment=VERIFIED_PLAYER_FLAG_COMMENT
            )
        except Exception as error:
            logger.warning(
                "'%s' - Can't be flagged. Will retry %s time(s) - %s",
                player_name, retries, error
            )
            retries = retries - 1
            sleep(5)  # Wait for the CRCON to restore connections (?)
            continue
        else:
            flag_success = True
            break

    # Player's CRCON profile couldn't be flagged
    if not flag_success:
        logger.error(
            "\n--------------------\n"
            "|  CRITICAL ERROR  |\n"
            "--------------------\n"
            "'%s' - Couldn't be flagged.",
            player_name
        )
        return

    # Player's CRCON profile has been flagged

    report(
        report_mode="valid",
        player_id=player_id,
        player_name=player_name,
        question_sentence=question_sentence,
        expected_answers_list=expected_answers_list,
        his_answers_list=his_answers_list,
        total_answer_time_secs=total_answer_time_secs
    )

    if SUCCESS_MESSAGE_DISPLAY:
        try:
            rcon.message_player(
                player_name=player_name,
                player_id=player_id,
                message=SUCCESS_MESSAGE_TEXT,
                by=BOT_NAME,
                # save_message=False  # default = False
            )
        except Exception as error:
            logger.warning(
                "'%s' - Success message couldn't be sent - %s",
                player_name,
                error
            )

    # Sleep time to be sure the flag will be active on the next loop
    # (avoids the player to be tested again)
    sleep(5)


def failure(
    rcon: Rcon,
    player_name: str,
    player_id: str,
    question_sentence: str,
    expected_answers_list: List[str],
    his_answers_list: List[str],
    answered_with_tk: bool,
    disconnected: bool,
    total_answer_time_secs: int
):
    """
    - Player didn't give any answer, or a bad one : kick
    - Player answered with a TK : kick or blacklist
    - send Discord embed
    """
    if answered_with_tk:

        if TK_ACTION == "blacklist":
            try:
                if TK_BLACKLIST_EXPIRATION is not None:
                    expires_at = (
                        datetime.now(timezone.utc)
                        + timedelta(TK_BLACKLIST_EXPIRATION)
                    )
                else:
                    expires_at = None
                add_record_to_blacklist(
                    player_id=player_id,
                    blacklist_id=TK_BLACKLIST_ID,
                    reason=TK_BAN_MESSAGE,
                    expires_at=expires_at,
                    admin_name=BOT_NAME
                )
                logger.info(
                    "'%s' - %s (until %s)",
                    player_name,
                    TK_ACTION,
                    expires_at
                )
            except Exception as error:
                logger.error("'%s' - %s - %s", player_name, TK_ACTION, error)

        elif TK_ACTION == "kickonly":
            logger.info("'%s' - %s", player_name, TK_ACTION)

    if disconnected:
        report(
            report_mode="coward",
            player_id=player_id,
            player_name=player_name,
            question_sentence=question_sentence,
            expected_answers_list=expected_answers_list,
            his_answers_list=his_answers_list,
            total_answer_time_secs=total_answer_time_secs
        )
        return

    kick_success = False
    retries = 3  # hardcoded
    while retries >= 0:
        try:
            rcon.kick(
                player_name=player_name,
                reason=KICK_MESSAGE_TEXT,
                by=BOT_NAME,
                player_id=player_id
            )

        # Kick failed
        except Exception:
            # Player is still connected
            if still_there_or_not(rcon, player_name):
                logger.warning(
                    "'%s' - Can't be kicked. Will retry %s time(s).",
                    player_name,
                    retries
                )
                retries = retries - 1
                sleep(5)
                continue

            # Player left the server
            report(
                report_mode="coward",
                player_id=player_id,
                player_name=player_name,
                question_sentence=question_sentence,
                expected_answers_list=expected_answers_list,
                his_answers_list=his_answers_list,
                total_answer_time_secs=total_answer_time_secs,
            )
            return

        kick_success = True
        break

    # Kick failed, player is still connected
    if not kick_success:
        logger.error(
            "\n--------------------\n"
            "|  CRITICAL ERROR  |\n"
            "--------------------\n"
            "'%s' - Couldn't be kicked.",
            player_name
        )
        return

    # Player has been kicked
    report(
        report_mode="kick",
        player_id=player_id,
        player_name=player_name,
        question_sentence=question_sentence,
        expected_answers_list=expected_answers_list,
        his_answers_list=his_answers_list,
        total_answer_time_secs=total_answer_time_secs
    )


def report(
    report_mode: Literal["coward", "ghost", "kick", "valid"],
    player_id: str,
    player_name: str,
    question_sentence: str,
    expected_answers_list: List[str],
    his_answers_list: List[str] = [],
    total_answer_time_secs: int = 0
):
    """
    Sends Discord embed (ghost/coward/valid/kicked)
    """
    if report_mode == "coward":
        comment = DISCORD_COWARD_COMMENT
        embed_display = DISCORD_COWARD_EMBED_DISPLAY
        emoji = DISCORD_COWARD_EMOJI
        embed_color = DISCORD_COWARD_EMBED_COLOR
    elif report_mode == "ghost":
        comment = DISCORD_GHOST_COMMENT
        embed_display = DISCORD_GHOST_EMBED_DISPLAY
        emoji = DISCORD_GHOST_EMOJI
        embed_color = DISCORD_GHOST_EMBED_COLOR
    elif report_mode == "kick":
        comment = DISCORD_KICK_COMMENT
        embed_display = DISCORD_KICK_EMBED_DISPLAY
        emoji = DISCORD_KICK_EMOJI
        embed_color = DISCORD_KICK_EMBED_COLOR
    elif report_mode == "valid":
        comment = DISCORD_VALID_COMMENT
        embed_display = DISCORD_VALID_EMBED_DISPLAY
        emoji = DISCORD_VALID_EMOJI
        embed_color = DISCORD_VALID_EMBED_COLOR

    # "ghost" default
    # his_answers_list = [] if his_answers_list is None else his_answers_list
    if len(his_answers_list) == 0:
        his_answers_list.append(NOANSWER_DEFAULT_TXT)

    logger.info(
        "'%s' - %s - %s : '%s' - %s : '%s'",
        player_name,
        comment,
        EXPECTED_ANSWER_COMMENT,
        " ; ".join(expected_answers_list),
        RECEIVED_ANSWER_COMMENT,
        " ; ".join(his_answers_list)
    )

    # Discord
    if USE_DISCORD and embed_display:
        send_discord_embed(
            embed_title=player_name,
            embed_title_url=get_external_profile_url(player_id, player_name),
            avatar_url=get_avatar_url(player_id),
            embed_desc_txt=question_sentence,
            embed_color=embed_color,
            embed_answer_expected="\n".join(expected_answers_list),
            embed_answer_received="\n".join(his_answers_list),
            embed_answer_result=emoji + " " + comment,
            embed_footer_txt=(
                DISCORD_EMBED_FOOTER_INTRO_TXT + str(total_answer_time_secs)
            )
        )


def send_discord_embed(
    embed_title: str,
    embed_title_url: str,
    avatar_url: str,
    embed_desc_txt: str,
    embed_color,
    embed_answer_expected: str,
    embed_answer_received: str,
    embed_answer_result: str,
    embed_footer_txt: str
):
    """
    Sends an embed message to Discord
    """
    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK)
    if DISCORD_EMBED_QUESTION_DISPLAY:
        embed = discord.Embed(
            title=embed_title,
            url=embed_title_url,
            description=embed_desc_txt,
            color=embed_color
        )
    else:
        embed = discord.Embed(
            title=embed_title,
            url=embed_title_url,
            color=embed_color
        )
    embed.set_author(
        name=BOT_NAME,
        url=DISCORD_EMBED_AUTHOR_URL,
        icon_url=DISCORD_EMBED_AUTHOR_ICON_URL
    )
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(
        name=EXPECTED_ANSWER_COMMENT, value=embed_answer_expected, inline=True
    )
    embed.add_field(
        name=RECEIVED_ANSWER_COMMENT, value=embed_answer_received, inline=True
    )
    embed.add_field(
        name=ACTION_RESULT_COMMENT, value=embed_answer_result, inline=True
    )
    if DISCORD_EMBED_FOOTER_DISPLAY:
        embed.set_footer(text=embed_footer_txt)
    embeds = []
    embeds.append(embed)
    webhook.send(embeds=embeds, wait=True)


# Launching - initial pause : wait to be sure the CRCON is fully started
sleep(60)

logger = logging.getLogger('rcon')

logger.info(
    "\n-------------------------------------------------------------------------------\n"
    "%s (started)\n"
    "-------------------------------------------------------------------------------",
    BOT_NAME
)

if TEST_MODE:
    logger.info(
        "NOTE : Test mode enabled. No real action will be engaged\n"
        "-------------------------------------------------------------------------------"
    )

# Launching (infinite loop)
if __name__ == "__main__":
    while True:
        should_we_run()
        # Sleep time to avoid a super-fast infinite loop
        # if no player has to be checked during bot activity time
        sleep(WATCH_INTERVAL_SECS)
