import discord
import cm
from event import Event
import db_utils


class CreateModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(title="Modal")
        self.add_item(
            discord.ui.InputText(label="Name",
                                 placeholder="Title",
                                 style=discord.InputTextStyle.short))
        self.add_item(
            discord.ui.InputText(label="When",
                                 placeholder="Time",
                                 style=discord.InputTextStyle.short))
        self.add_item(
            discord.ui.InputText(label="Where",
                                 placeholder="Location",
                                 style=discord.InputTextStyle.short))
        self.add_item(
            discord.ui.InputText(label="Date",
                                 placeholder="MM/DD/YYYY",
                                 style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        name = self.children[0].value
        when = self.children[1].value
        where = self.children[2].value
        hardDate = self.children[3].value
        upcomingChannel = discord.utils.get(interaction.channel.guild.channels,
                                            name="upcoming-events")
        await cm.createMethod(interaction.user.id, upcomingChannel,
                              interaction.channel, name, where, when, hardDate)
        await interaction.response.send_message("Hooray! Event created: " +
                                                name + " for: " + when +
                                                " at: " + where)


class UpdateModal(discord.ui.Modal):

    def __init__(self, event: Event, *args, **kwargs) -> None:
        super().__init__(title=str(event.name))
        self.event = event
        self.add_item(
            discord.ui.InputText(label="When",
                                 placeholder="Time",
                                 style=discord.InputTextStyle.short,
                                 value=event.when))
        self.add_item(
            discord.ui.InputText(label="Where",
                                 placeholder="Location",
                                 style=discord.InputTextStyle.short,
                                 value=event.where))
        self.add_item(
            discord.ui.InputText(label="Date",
                                 placeholder="MM/DD/YYYY",
                                 style=discord.InputTextStyle.short,
                                 value=event.hardDate))

    async def callback(self, interaction: discord.Interaction):
        name = self.event.name
        when = self.children[0].value
        where = self.children[1].value
        hardDate = self.children[2].value
        upcomingChannel = discord.utils.get(interaction.channel.guild.channels,
                                            name="upcoming-events")
        print("Editing Event:")
        print(str(self.event.toString()) + "\n\n")
        await db_utils.updateEvent(name, when, where, hardDate)
        await interaction.response.edit_message(view=None,
                                                content="Updated event!")


#class DeleteModal(discord.ui.Modal):
#  def __init__(self, *args, **kwargs)->None:
#    super().__init__(title="Delete an Event")
#    self.add_item(discord.ui.InputText(label="Name of Event to Delete",placeholder="Event Name", #style=discord.InputTextStyle.short))
#
#  async def callback(self, interaction:discord.Interaction):
#    name = self.children[0].value
#    await cm.deleteMethod(interaction=interaction,name=name)
