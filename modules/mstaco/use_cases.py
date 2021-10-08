import operator
import modules.mstaco.persistence as persistence

from config import SKIP_LEADERBOARD_WEEKEND, DAILY_TACOS, GROUP_NAME
from utils.time_utils import get_today, get_time_left, is_weekend, is_final_day


def give_tacos(giver_id, receiver_id, given_tacos, reaction=False, channel=None, emoji="🌮"):
    giver = persistence.DBUser(giver_id)
    receiver = persistence.DBUser(receiver_id)

    if giver.remaining_tacos() >= abs(given_tacos):
        receiver.add_tacos(given_tacos)
        giver.remove_tacos(given_tacos)

        giver_message = _notify_tacos_sent(receiver.user_id, given_tacos, giver.remaining_tacos(), emoji)
        receiver_message = _notify_tacos_received(giver.user_id, given_tacos, receiver.owned_tacos(), channel, emoji)
        _log_taco_transaction(giver.user_id, receiver.user_id, given_tacos, reaction, get_today())
        return giver_message, receiver_message
    else:
        giver_message = _notify_not_enough_tacos(get_time_left())
        return giver_message, None


def give_bonus_taco_if_required(user_id):
    user = persistence.DBUser(user_id)
    

    if user.requires_bonus_taco():
        user.add_tacos(1, bonus=True)

        _log_bonus_taco(user.user_id, get_today())
        return _notify_bonus_taco(user.owned_tacos())

def reset_daily_tacos():
    persistence.DBUser.reset_daily_tacos()

    # Compute all the tacos from yesterday.
    daily_taco_count = persistence.daily_taco_count()
    
    return print_weekly_leaderboard()


def print_leaderboard():
    # Compute all the tacos from yesterday.
    daily_taco_count = persistence.daily_taco_count()

    message = f"**¡DIVINE-INFO!** El número total de tacos repartidos ayer en la comunidad es de **{daily_taco_count}x :taco: \n\n**"

    message += '**' + GROUP_NAME + ' Leaderboard de Tacos :taco:**\n'
    db_list = persistence.DBUser.get_top_ranking()
    bots_id = [None, 'UGMETH49H']

    i = 1
    top_n = 10

    # Top 10 elements
    for l in db_list:
        if i <= min(len(db_list), top_n):
            if l['user_id'] not in bots_id:
                message += str(i) + "). " + "<@!" + str(l['user_id']) + "> `" + str(l['owned_tacos']) + "`\n"
                i += 1
        else:
            break

    return message

def print_weekly_leaderboard():
    if SKIP_LEADERBOARD_WEEKEND and is_weekend():
        print("IS WEEKEND, LEADERBOARD SKIPPED")
        return ""

    # Compute all the tacos from yesterday.
    daily_taco_count = persistence.daily_taco_count()

    message = f"**¡DIVINE-INFO!** El número total de tacos repartidos esta semana es de **{daily_taco_count}x :taco: **\n"

    db_list = persistence.DBUser.get_weekly_info()
    bots_id = [None, 'UGMETH49H']

    is_final = is_final_day() # Is the final leaderboard?
    if is_final:
        message += '**' + GROUP_NAME + ' Leaderboard Final de Tacos :taco:**\n'
        db_list  = persistence.DBUser.get_prev_weekly_info()
    else:
        message += '**' + GROUP_NAME + ' Leaderboard Semanal de Tacos :taco:**\n'

    i = 1
    top_n = 10

    week_logs = {}

    # Reduce weekly logs to get the total number of tacos per user.
    for log in db_list:
        user = log['receiver_user']
        if user != None:
            if user in week_logs:
                week_logs[user] = week_logs[user] + log['n_tacos']
            else:
                week_logs.update({user: log['n_tacos']})

    week_logs = sorted(week_logs.items(), key=operator.itemgetter(1), reverse=True)

    # Top 10 elements
    for user_id, n_tacos in week_logs:
        if i <= min(len(db_list), top_n):
            if user_id not in bots_id:
                if (is_final and i < 4):
                    medals = [":first_place_medal:", ":second_place_medal:", ":third_place_medal:"]
                    message +=  medals[i-1] + " " + "<@!" + str(user_id) + "> `" + str(n_tacos).replace('.0','') + "`\n"
                else:
                    message +=     str(i) + "). " + "<@!" + str(user_id) + "> `" + str(n_tacos).replace('.0', '') + "`\n"

                i += 1
        else:
            break

    if is_final:
        message += "\n**¡Este ranking semanal de tacos está basado en milagros bíblicos inexplicables y ha sido reiniciado!**"

    return message


def print_leaderboard_me(user):
    db_list = persistence.DBUser.get_top_ranking()

    # Find user in ranking
    users_generator = ({'pos':i + 1, 'info':db_info} for i, db_info in enumerate(db_list) if db_info['user_id'] == user.id)

    user_taco = next(users_generator)

    # If not in ranking, maybe it's a error or the user doesn't have tacos
    if user_taco is None:
        message = '**No apareces en nuestro registro de tacos :sad_parrot:. ¿Has recibido algún taco?**\n'

    else:
        message = ":taco: Stats de <@!" + str(user.id) + ">:\n"
        message += "\t\t**Posición: ** `" +  str(user_taco['pos']) + "` \n"
        message += "\t\t**Tacos:    ** `" +  str(user_taco['info']['owned_tacos']) + "`  \n"

    return message


def _log_taco_transaction(giver_id, reciver_id, amount, reaction, date):
    print ("TACO TRANSACTION DATE: ", date)
    persistence.save_log({
        'giving_user': giver_id,
        'receiver_user': reciver_id,
        'n_tacos': amount,
        'type': 'reaction' if reaction else 'message',
        'date': date
    })


def _log_bonus_taco(user_id, date):
    print ("TACO BONUS DATE: ", date)
    persistence.save_log({
        'giving_user': None,
        'receiver_user': user_id,
        'n_tacos': 1,
        'type': 'bonus',
        'date': date
    })


def _notify_tacos_sent(receiver_id, amount, remaining, emoji):
    extra_text = ""
    if emoji != "🌮":
        extra_text = f"(equivalente a {amount} taco(s)) "
    message = f"¡<@!{receiver_id}> **ha recibido 1 x {emoji}** {extra_text}de tu parte! Te quedan {remaining} tacos para repartir hoy."
    return message


def _notify_tacos_received(giver_id, amount, total, channel, emoji):
    extra_text = ""
    if emoji != "🌮":
        extra_text = f"(equivalente a {amount} taco(s))"
    message = f"¡**Has recibido 1 x {emoji}** {extra_text}de <@!{giver_id}> en el canal <#{channel}>! Ya tienes **{total}x :taco:**"
    return message


def _notify_not_enough_tacos(time_before_reset):
    message = f"**¡No tienes suficientes tacos!** Recibirás {DAILY_TACOS} TACOS NUEVOS :taco: recién cocinados en **{time_before_reset} horas.**"
    return message


def _notify_bonus_taco(total):
    message = f"¡Toma! Aquí tienes **1 TACO de premio por participar hoy en la comunidad**. Ya tienes **{total}x :taco: ** ¡Vuelve mañana a por más!"
    return message