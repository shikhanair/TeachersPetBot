from profanity_filter import ProfanityFilter
pf = ProfanityFilter()
def check_profanity(msg):
    pf.censor_char = '*'
    return pf.censor(msg)