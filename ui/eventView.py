import discord
from discord.ui import View, Button
from bot import api


class EventView(View):
    def __init__(self, event, *, timeout=None):
        super().__init__(timeout=timeout)
        self.event = event

    @discord.ui.button(label="✔ Going",
                       custom_id="attend",
                       style=discord.ButtonStyle.green,
                       disabled=False)
    async def attend(self, button: Button, interaction: discord.Interaction):
        self.disable_all_items()
        if "None" in str(self.event.going):
            going = []
        else:
            going = str(self.event.going).split(", ")
        if str(interaction.user.id) in going:
            return await self.event.refresh(interaction)
        print(f"{interaction.user.name} is attending {self.event.name}")
        going.append(str(interaction.user.id))
        self.event.going = str.join(", ", going)
        await self.event.refresh(interaction)
        try:
            print(f"adding {interaction.user.name} to thread for {self.event.name}")
            await api.bot.get_channel(self.event.thread).add_user(interaction.user)
        except Exception as e:
            print(f"unable to add {interaction.user.name} to thread: {e}")

    @discord.ui.button(label="✖ Not Going",
                       custom_id="notAttending",
                       style=discord.ButtonStyle.gray,
                       disabled=False)
    async def notAttending(self, button: Button, interaction: discord.Interaction):
        self.disable_all_items()
        if "None" in str(self.event.going):
            going = []
        else:
            going = str(self.event.going).split(", ")
        if str(interaction.user.id) not in going:
            return await self.event.refresh(interaction)
        print(f"{interaction.user.name} is not attending {self.event.name}")
        i = going.index(str(interaction.user.id))
        if i >= 0:
            del going[i]
        self.event.going = str.join(", ", going)
        if not self.event.going:
            self.event.going = "None"
        await self.event.refresh(interaction)
        try:
            print(f"removing {interaction.user.name} from thread for {self.event.name}")
            await api.bot.get_channel(self.event.thread).remove_user(interaction.user)
        except Exception as e:
            print(f"unable to remove {interaction.user.name} from thread: {e}")

    @discord.ui.button(label="📝 Edit",
                       custom_id="edit",
                       style=discord.ButtonStyle.blurple,
                       disabled=False)
    async def edit(self, button: Button, interaction: discord.Interaction):
        self.disable_all_items()
        await self.event.edit(interaction)

    @discord.ui.button(label="🗑️ Delete",
                       custom_id="delete",
                       style=discord.ButtonStyle.danger,
                       disabled=False)
    async def delete(self, button: Button, interaction: discord.Interaction):
        self.disable_all_items()
        await self.event.deleteEvent(interaction)
