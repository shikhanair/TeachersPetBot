# Functionality related to Q & A

question_number = 1
qna = {}


class QuestionsAnswers:
    def __init__(self, q, number, message_id, ans):
        self.question = q
        self.number = number
        self.message_id = message_id
        self.answer = ans


async def question(ctx, q):
    global qna
    global question_number

    message = 'Q' + str(question_number) + ': ' + q + '\n'

    message_id = await ctx.send(message)

    # create qna object
    new_question = QuestionsAnswers(q, question_number, message_id, '')
    # add question to list
    qna[question_number] = new_question

    # increment question number for next question
    question_number += 1

    # delete original question
    await ctx.message.delete()


async def answer(ctx, num, ans):
    # get question
    global qna
    q_answered = qna[int(num)]
    message = q_answered.message_id

    # generate and edit msg with answer
    content = message.content + '\n' + 'A: ' + ans
    await message.edit(content=content)

    # delete user msg
    await ctx.message.delete()

