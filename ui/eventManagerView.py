import discord
from discord.ui import View, Button

from db.event import Event
from db.views import Views
from ui.eventModal import EventModal
from ui.viewType import ViewType


class EventManagerView(View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="📝 Create new event",
                       custom_id="create",
                       style=discord.ButtonStyle.blurple,
                       disabled=False)
    async def create(self, button: Button, interaction: discord.Interaction):
        await interaction.response.send_modal(EventModal(Event()))

    @classmethod
    async def build(self, channel=None, message=None):
        if channel is None:
            return await message.edit(content="Click the button below to create a new event!", view=EventManagerView(), embed=None)
        elif message is None:
            message = await channel.send(content="Click the button below to create a new event!",
                                      view=EventManagerView(), embed=None)
            view = Views.create(guild=channel.guild.id, type=ViewType.CREATE_NEW_EVENT.value, channel=channel.id, message=message.id)
            return message
        else:
            print(f"Error 10 cannot build create event manager")
