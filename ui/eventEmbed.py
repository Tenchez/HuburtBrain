from discord import Embed


class EventEmbed(Embed):
    def __init__(self, event ):
        super().__init__()
        self.title = event.name
        if event.description:
            self.description=event.description
        if event.where:
            self.add_field(name="Where", value=event.where, inline=True)
        if event.when:
            self.add_field(name="When", value=event.when, inline=True)
        self.add_field(name="Date", value=event.date, inline=True)
        sum = 0 if str(event.going) == "None" else len(str(event.going).split(','))
        self.add_field(name=f"Attendees ({sum})", value=event.going, inline=False)
        self.set_image(url="https://i.imgur.com/OdwAGeL.png")
        self.set_footer(text=f"Created by: {str(event.createdBy).rsplit('#')[0]}")
        self.color=event.color

