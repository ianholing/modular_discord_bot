###
# GLOBAL CONSTANTS AND CONFIG SETTINGS
###

DISCORD_TOKEN = "TOKEN.FROM.DISCORD"
TEST_CHANNEL = 999999999999999999 # BOT TEST
SKIP_LEADERBOARD_WEEKEND = True

########## TACO MODULE #########

DAILY_TACOS = 5
RESET_HOUR = 9  # UTC
SHOW_LEADERBOARD_CHANNEL = 999999999999999998 # 833671405630652429 # GENERAL
GROUP_NAME = "Comunidad test"
TACO_NAME = "testpoints"
TACO_EMOJI = ":taco:"
RESET_DAY_OFFSET = 4 # Friday is our day to show tacos list (Offset from first day of the week starting from 0)
TACO = {":taco:": 1, ":broccoli:": 1.5, ":medio_taco:": 0.5, ":beer:": 2, ":beer_mug:":2, ":-1:": -1, ":thumbs_down:": -1, ":cucumber:": 2, ":hot_pepper:": 1, ":test_tube:": 0}

########## CHATBOT MODULE #########

MIN_RANDOM_REPLY_COUNTER = 5
MAX_RANDOM_REPLY_COUNTER = 50
CHATBOT_TOKEN = "sk-..."
CHATBOT_NAME = "Godofredo"
CHATBOT_ROLE = "A beautiful assistant called " + CHATBOT_NAME

########## PARROT MODULE #########

SHOW_PARROT_CHANNEL = 999999999999999999

########## REMINDER MODULE #########

MIN_REMINDER_TIME = 60 * 60
SHOW_REMINDER_CHANNEL = 999999999999999999
HELP_TEXT = "La forma correcta de usar el bot de recuerdos es:  \r\n\
```AYUDA: @Bot recuerda ayuda\r\n\
INSERTAR: @Bot recuerda [userto], [text], [tag], [interval], [interval_launch_time], [counter]\r\n\
ELIMINAR: @Bot recuerda borrar [userto | channel | tag | id]```  \r\n\
EJEMPLOS:\r\n\
@Bot recuerda[ a ] @manolo, ir a por patatas, #compra, 1w, 9:00, 0\r\n\
@Bot recuerda[ a ] #general, Recordad que el viernes hay charla de , #alerts, 1d, 9:00, 5\r\n\
@Bot recuerda[ a ] @maria, Vete a casa <-- Implicit launch only once: (#general, -, 18:00, 1)\r\n\
@Bot recuerda[ a ] borrar 1245\r\n\
@Bot recuerda[ a ] borrar #compra\r\n"