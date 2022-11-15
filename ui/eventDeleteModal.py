import discord


class EventDeleteModal(discord.ui.Modal):
    def __init__(self, event, update=False, *args, **kwargs) -> None:
        super().__init__(title="Delete Event...")
        self.event = event
        self.add_item(
            discord.ui.InputText(label="Are you sure you want to delete this event?",placeholder="...",required=False,
                                 style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        await self.event.remove()
        await interaction.response.defer()
