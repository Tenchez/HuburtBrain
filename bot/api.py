from bot.constants import bot, my_secret


def startBot():
    try:
        bot.run(my_secret)
    except Exception as e:
        print(f"Error 6 {e}")


async def message(ctx, msg, view=None):
    try:
        return await ctx.send(msg, view=view)
    except Exception as e:
        print("Cannot send message: {}".format(e))


async def sendView(interaction, msg, view, hidden):
    try:
        return await interaction.response.send_message(view=view,
                                                       ephemeral=hidden)
    except Exception as e:
        print("Cannot send view: {}".format(e))


async def respond(interaction, msg, hidden):
    try:
        return await interaction.response.send_message(msg, ephemeral=hidden)
    except Exception as e:
        print("Cannot send response: {}".format(e))


async def deleteMessage(msg):
    try:
        return await msg.delete()
    except Exception as e:
        print("Cannot delete message: {}".format(e))
