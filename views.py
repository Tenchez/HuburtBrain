import discord
import helper as h
import db_utils
import cm
from modals import UpdateModal
from discord.ui import Button, View, Select


class updateEvent(View):

    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.msg = "Update Event:"
        self.hidden = True
        #TODO FIX RETAINING VALUES
        self.selectedEvent = None
        for child in self.children:
            if str(child.type) == 'ComponentType.select':
                self.select = child

    def getEventOptions(self):
        events = db_utils.getEventList()
        options = []
        for event in events:
            option = discord.SelectOption(
                label=event.name,
                value=str(event.id),
                description=
                f"When: {event.when}, Where: {event.where}, Date: {event.hardDate}"
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
        event = db_utils.getEvent(int(self.selectedEvent))
        self.disable_all_items()
        await self.message.edit(view=None, content="Updating event...")
        await interaction.response.send_modal(UpdateModal(event))

    @discord.ui.button(label="Delete",
                       style=discord.ButtonStyle.red,
                       disabled=True)
    async def delete(self, button: Button, interaction: discord.Interaction):
        for option in self.select.options:
            option.default = False
        self.disable_all_items()
        #TODO "Are you sure?" modal or new view
        event = db_utils.getEvent(int(self.selectedEvent))
        await cm.deleteMethod(interaction=interaction,
                              name=event.name,
                              respond=False)
        await interaction.response.edit_message(view=None,
                                                content="Deleted Event...")

    async def send(self, interaction):
        self.select.options = self.getEventOptions()
        if len(self.select.options) == 0:
            await h.respond(interaction, "There are no events... yet. Try /hcreate to make one", True)
            return
        self.m = await h.sendView(interaction, self.msg, self, self.hidden)
