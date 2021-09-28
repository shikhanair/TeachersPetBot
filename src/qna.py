# Functionality related to Q & A
from discord import NotFound

# keep track of next question number
question_number = 1

# dictionary of questions with answers
qna = {}


# object with question details
class QuestionsAnswers:
    def __init__(self, q, number, message, ans):
        self.question = q
        self.number = number
        self.msg = message
        self.answer = ans


# Ask question
async def question(ctx, q):
    global qna
    global question_number

    # format question
    q_str = 'Q' + str(question_number) + ': ' + q + '\n'

    message = await ctx.send(q_str)

    # create qna object
    new_question = QuestionsAnswers(q, question_number, message.id, '')
    # add question to list
    qna[question_number] = new_question

    # increment question number for next question
    question_number += 1

    # delete original question
    await ctx.message.delete()


# Answers question specified in num
async def answer(ctx, num, ans):
    global qna

    # check if question number exists
    if int(num) not in qna.keys():
        await ctx.author.send('Invalid question number: ' + str(num))
        # delete user msg
        await ctx.message.delete()
        return

    # get question
    q_answered = qna[int(num)]
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
    content = message.content + '\n' + new_answer
    try:
        await message.edit(content=content)
    except NotFound:
        await ctx.author.send('Invalid question number: ' + str(num))

    # delete user msg
    await ctx.message.delete()

