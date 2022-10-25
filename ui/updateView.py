import threading

import discord
from discord.ui import View, Select, Button

from bot import api
from db.event import Event
from ui.eventModal import EventModal

threadLock = threading.Lock()


class UpdateView(View):

    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.msg = "Update Event:"
        self.hidden = True
        self.selectedEvent = None
        for child in self.children:
            if str(child.type) == 'ComponentType.select':
                self.select = child

    def getEventOptions(self):
        events = Event.select()
        options = []
        for event in events:
            option = discord.SelectOption(
                label=event.name,
                value=str(event.id),
                description=
                f"When: {event.when}, Where: {event.where}, Date: {event.date}"
            )
            options.append(option)
        return options

    @discord.ui.select(placeholder="Select Event...")
    async def select(self, select: Select, interaction: discord.Interaction):
        self.selectedEvent = int(select.values[0])
        self.select = select
        for option in select.options:
            option.default = False
            if option.value == str(self.selectedEvent):
                option.default = True
        self.selected = select.values
        for child in self.children:
            child.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Edit",
                       custom_id="event_select",
                       style=discord.ButtonStyle.green,
                       disabled=True)
    async def submit(self, button: Button, interaction: discord.Interaction):
        if self.selectedEvent is None:
            return
        for option in self.select.options:
            option.default = False
        try:
            event = Event.select().where(Event.id == self.selectedEvent).get()
            self.disable_all_items()
            await self.message.delete()
            await interaction.response.send_modal(EventModal(event, update=True))
        except Exception as e:
            print(f"Unable to update {e}")
            await interaction.response.edit_message(view=None,
                                                    content="Error: Unable to update.")

    @discord.ui.button(label="Delete",
                       style=discord.ButtonStyle.red,
                       disabled=True)
    async def delete(self, button: Button, interaction: discord.Interaction):
        for option in self.select.options:
            option.default = False
        self.disable_all_items()
        # TODO "Are you sure?" modal or new view maybe
        try:
            event = Event.get_by_id(self.selectedEvent)
            await event.remove()
            await interaction.response.edit_message(view=None,
                                                    content="Deleted Event...")
        except Exception as e:
            print(f"Unable to delete {e}")
            await interaction.response.edit_message(view=None,
                                                    content="Error: Unable to delete.")

    async def send(self, interaction):
        self.select.options = self.getEventOptions()
        if len(self.select.options) == 0:
            await api.respond(interaction, "There are no events... yet. Try /create to make one", True)
            return
        self.m = await api.sendView(interaction, self.msg, self, self.hidden)
