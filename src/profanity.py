from better_profanity import profanity
profanity.load_censor_words()


def check_profanity(msg):
    return(profanity.contains_profanity(msg))


def censor_profanity(msg):
    return profanity.censor(msg)