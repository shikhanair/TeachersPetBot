###########################
# Implements Q and A functionality
###########################
from discord import NotFound

# keep track of next question number
QUESTION_NUMBER = 1

# dictionary of questions with answers
QNA = {}


###########################
# Class: QuestionsAnswers
# Description: object with question details
# Inputs:
#      - q: question text
#      - number: question number
#      - message: id of the message associated with question
#      - ans: answers to the question
# Outputs: None
###########################
class QuestionsAnswers:
    ''' Class containing needed question/answer information and identification '''
    def __init__(self, qs, number, message, ans):
        self.question = qs
        self.number = number
        self.msg = message
        self.answer = ans


###########################
# Function: question
# Description: takes question from user and reposts anonymously and numbered
# Inputs:
#      - ctx: context of the command
#      - q: question text
# Outputs:
#      - User question in new post
###########################
async def question(ctx, qs):
    ''' add a question '''
    global QNA
    global QUESTION_NUMBER

    # format question
    q_str = 'Q' + str(QUESTION_NUMBER) + ': ' + qs + '\n'

    message = await ctx.send(q_str)

    # create QNA object
    new_question = QuestionsAnswers(q, QUESTION_NUMBER, message.id, '')
    # add question to list
    QNA[QUESTION_NUMBER] = new_question

    # increment question number for next question
    QUESTION_NUMBER += 1

    # delete original question
    await ctx.message.delete()


###########################
# Function: answer
# Description: adds user answer to specific question and post anonymously
# Inputs:
#      - ctx: context of the command
#      - num: question number being answered
#      - ans: answer text to question specified in num
# Outputs:
#      - User answer added to question post
###########################
async def answer(ctx, num, ans):
    ''' answer the specific question '''
    global QNA

    # check if question number exists
    if int(num) not in QNA.keys():
        await ctx.author.send('Invalid question number: ' + str(num))
        # delete user msg
        await ctx.message.delete()
        return

    # get question
    q_answered = QNA[int(num)]
    # check if message exists
    try:
        message = await ctx.fetch_message(q_answered.msg)
    except NotFound:
        await ctx.author.send('Invalid question number: ' + str(num))
        # delete user msg
        await ctx.message.delete()
        return

    # generate and edit msg with answer
    if "instructor" in [y.name.lower() for y in ctx.author.roles]:
        role = 'Instructor'
    else:
        role = 'Student'
    new_answer = role + ' Ans: ' + ans

    # store new answer
    if not q_answered.answer == '':
        q_answered.answer += '\n'
    q_answered.answer += new_answer

    # check if message exists and edit
    q_str = 'Q' + str(q_answered.number) + ': ' + q_answered.question
    content = q_str + '\n' + q_answered.answer
    try:
        await message.edit(content=content)
        # message.content = content
    except NotFound:
        await ctx.author.send('Invalid question number: ' + str(num))

    # delete user msg
    await ctx.message.delete()
