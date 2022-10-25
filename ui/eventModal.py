import threading

import discord

threadLock = threading.Lock()


class EventModal(discord.ui.Modal):
    def __init__(self, event, update=False, *args, **kwargs) -> None:
        super().__init__(title="Event")
        self.event = event
        self.update = update
        self.add_item(
            discord.ui.InputText(label="Title",
                                 placeholder="Short Description",
                                 style=discord.InputTextStyle.short,
                                 value=event.name))
        self.add_item(
            discord.ui.InputText(label="When",
                                 placeholder="Time",
                                 style=discord.InputTextStyle.short,
                                 value=event.when,
                                 required=False))
        self.add_item(
            discord.ui.InputText(label="Where",
                                 placeholder="Location",
                                 style=discord.InputTextStyle.short,
                                 value=event.where,
                                 required=False))
        self.add_item(
            discord.ui.InputText(label="Date",
                                 placeholder="MM/DD/YYYY",
                                 style=discord.InputTextStyle.short,
                                 max_length=10,
                                 min_length=10,
                                 value=event.date))
        self.add_item(
            discord.ui.InputText(label="Description",
                                 placeholder="Description of event...",
                                 style=discord.InputTextStyle.long,
                                 value=event.description,
                                 required=False))

    async def callback(self, interaction: discord.Interaction):
        self.event.name = None if not self.children[0].value else self.children[0].value
        self.event.when = None if not self.children[1].value else self.children[1].value
        self.event.where = None if not self.children[2].value else self.children[2].value
        self.event.date = None if not self.children[3].value else self.children[3].value
        self.event.description = None if not self.children[4].value else self.children[4].value

        try:
            if self.update:
                print("old event")
                self.event.announced = False
                self.event.save()
                await self.event.refresh(interaction)
            else:
                print("new event")
                await self.event.build(interaction)
        except Exception as e:
            print(e)
            await interaction.response.edit_message(view=None,
                                                    content="Error: Unable to save event.")
