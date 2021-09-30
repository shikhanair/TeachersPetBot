from better_profanity import profanity
profanity.load_censor_words()


def check_profanity(msg):
    ''' check if message contains profanity through profanity module '''
    return profanity.contains_profanity(msg)


def censor_profanity(msg):
    ''' take action on the profanity by censoring it '''
    return profanity.censor(msg)
