# Functionality related to Q & A
from discord import NotFound

question_number = 1
qna = {}


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

    q_str = 'Q' + str(question_number) + ': ' + q + '\n'

    message = await ctx.send(q_str)

    # create qna object
    new_question = QuestionsAnswers(q, question_number, message, '')
    # add question to list
    qna[question_number] = new_question

    # increment question number for next question
    question_number += 1

    # delete original question
    await ctx.message.delete()


# Answers question specified in num
async def answer(ctx, num, ans):
    global qna

    print('context: \n', ctx)

    # check if question number exists
    if int(num) not in qna.keys():
        await ctx.author.send('Invalid question number: ' + str(num))
        # delete user msg
        await ctx.message.delete()
        return

    # get question
    q_answered = qna[int(num)]
    message = q_answered.msg

    # generate and edit msg with answer
    content = message.content + '\n'
    if "instructor" in [y.name.lower() for y in ctx.author.roles]:
        role = 'Instructor'
    else:
        role = 'Student'
    content = message.content + '\n' + role + ' Ans: ' + ans

    # check if message exists
    try:
        await message.edit(content=content)
    except NotFound:
        await ctx.author.send('Invalid question number: ' + str(num))

    # delete user msg
    await ctx.message.delete()

