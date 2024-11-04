
import discord 
from discord.ext import commands, tasks
import random
import asyncio
import pytz 
import time
from discord.ui import View,  Select
from datetime import datetime, timedelta
from discord.utils import get
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)

timer_active = False
timer_seconds = 0
timer_message = None

#Bot Ready!

@client.event
async def on_ready():
    current_time = datetime.now(pytz.timezone('Europe/Athens')).strftime("%H:%M:%S")
    logschannel = client.get_channel(1116792893957484625)
    await client.change_presence(activity=discord.Game(name="EmeraldOG SMP"))
    if logschannel:
        embed = discord.Embed(title='Bot is ONLINE!', description='', colour=0x00FF00)
        embed.add_field(name='Ready', value='Bot is ready!', inline=False)
        embed.add_field(name='Version:', value='Python Version: 3.10.11', inline=False)
        embed.add_field(name='Connected At:', value=f'{current_time}', inline=False) 
        await logschannel.send(embed=embed) 



#---------------------------------------------------------------------------------------------Classic Commands---------------------------------------------------------------------------------------------#



    #Application Embed command 

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label='📚 Manager For Buy', url='https://docs.google.com/forms/d/e/1FAIpQLSdyhitZ68bAWKYYfXsGweqxlJcfQODZPxKTWBqeegTrkku8wA/viewform?usp=sf_link'))

    async def on_timeout(self):
        pass

@client.command()
async def application(ctx):
    embed = discord.Embed(title='Application', description='Πατήστε ένα από τα παρακάτω κουμπιά για να υποβάλετε μια αίτηση', color=0x800080)

    view = MyView()

    await ctx.send(embed=embed, view=view)


  #say  
@client.command()
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)



 #Add_Role command

@client.command()
async def add_role(ctx, member: discord.Member, *roles: discord.Role):
    for role in roles:
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f'{role.name} added to {member.display_name}', delete_after=3)
        else:
            await ctx.send(f'{member.display_name} already has the {role.name} role',ephemeral=True)

#Romeve_Role command 

@client.command()
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    required_role = discord.utils.get(ctx.guild.roles, id= 1115921947163893860) 

    if not ctx.author.guild_permissions.manage_roles and role != required_role:
        await ctx.send("You don't have the necessary permissions to remove roles from this member.",ephemeral=True)
        return

    if role not in member.roles:
        await ctx.send(f"{member.mention} doesn't have the {role.name} role.",ephemeral=True)
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"Successfully removed the {role.name} role from {member.mention}.",ephemeral=True)
    except discord.Forbidden:
        await ctx.send("I don't have the necessary permissions to remove roles.",ephemeral=True)
    except discord.HTTPException:
        await ctx.send("An error occurred while removing the role.",ephemeral=True)





        #Support Move

@client.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined the channel with code 1111
    if before.channel != after.channel and after.channel is not None and after.channel.name == "📞Waiting For Support":
        guild = member.guild
        category = discord.utils.get(guild.categories, name='📞Waiting For Support')

        # Create a new voice channel with the desired name format
        channel_name = f'📞 Support 24/7 Online - {member.display_name}'
        new_channel = await guild.create_voice_channel(channel_name, category=category)

        # Move the member to the new channel
        await member.move_to(new_channel)
        print(f'Moved {member.display_name} to {new_channel.name}')

        # Send a message to the support-ntf channel mentioning specific roles
        support_ntf_channel = discord.utils.get(guild.channels, name='📞notifications')
        if support_ntf_channel:
            founder_role = discord.utils.get(guild.roles, name='💼Management™')
            donator_manager_role = discord.utils.get(guild.roles, name='💎Staff™')

            mention_roles = ''
            if founder_role:
                mention_roles += founder_role.mention
            if donator_manager_role:
                mention_roles += ' ' + donator_manager_role.mention

            await support_ntf_channel.send(f'Go to Support room and help {member.mention}. {mention_roles}')

    # Check if the member who created the channel leaves
    if before.channel is not None and before.channel.name.startswith('📞 Support 24/7 Online - ') and before.channel.members == []:
        # Delete the channel when the member leaves
        print(f'Deleting channel {before.channel.name}')
        await before.channel.delete()




#embed feedcback  

@client.command() 
async def feedbackembed(ctx): 
    embed=discord.Embed(title='**Οδηγίες:**', description='**Για να μας στείλετε μια αξιολόγηση, παρακαλώ γράψτε !feedback (Perfect,good,awful).**', color=0x8A1E05) 
    embed.set_footer(text='`Εάν σε περίπτωση που κάποιος σπαμάρει ή γράφει ανοησίες θα αποκλείστεί από το server!`') 
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1288087748762275963/1301751200181522484/New_Project_14.gif?ex=67259dc7&is=67244c47&hm=404ef534f02841871274cca52b88500c82c50a6b9b1cae1ce0b2c6f83b68adf8&=&width=671&height=671') 

    await ctx.send(embed=embed)


#Feedback

babis2_message = None 

@client.command()
async def feedback(ctx, *, feedback):
    global babis2_message
    babis_message = await ctx.send(f"{ctx.author.mention}, The feedback sent to the staff team!",delete_after=3)

    feedback_channel = client.get_channel(1302816950354710579)

    member = ctx.author

    embed = discord.Embed(title="**New Feedback**", description='', color=0x00F892)
    embed.add_field(name='Όνομα:', value=member.mention, inline=True)
    embed.add_field(name='Feedback:', value=feedback, inline=True)
    embed.set_thumbnail(url=member.avatar.url)  

    await feedback_channel.send(embed=embed)



#Embed Command 

@client.command()
async def staffrules(ctx):
    embed = discord.Embed(title='**Staff Rules**', description='**1)Όταν έχει γίνει κάποιο Report δεν παμε και κατεβαίνουμε απο Noclip όποιος το κάνει αυτό θα υπάρχει ποινή\n\n2) Όταν είμασται στο On Duty εχουμε PUSH TO TALK\n\n3) Όταν ειμασται στο On Duty παίζουμε μόνο στον Lion Roleplay Fivem\n\n4) Όταν πάμε σε κάποιο Report οπος και να σας μιλήσει ο user του μιλάτε ευγενικά\n\n5) Στο Support πάει μόνο ενα άτομο και άμα ειναι για σκηνικό παει κάποιος πάνω απο την θέση Server Supporter \n\n6) Δεν βρίζουμε οποιοδήποτε Staff όταν είμαστε σε κανάλι On Duty \n\n7) Απαγορεύεται το spam στα voice και text channels\n\n8) Απαγορεύεται να στέλνετε μυνηματα που δεν αφορούν τον Server στο κανάλι Staff Chat \n\n9) Απαγορεύεται να στέλνετε μηνύματα που περιέχουν κακόβουλο υλικό (ip grαb1fy, t0κkeν grαbbεr , faκe nιtrοs κλπ.**', colour=0x00eeff)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1288087748762275963/1301751200181522484/New_Project_14.gif?ex=67259dc7&is=67244c47&hm=404ef534f02841871274cca52b88500c82c50a6b9b1cae1ce0b2c6f83b68adf8&=&width=671&height=671')
    embed.set_footer(text='Lion Roleplay')
    await ctx.send(embed=embed)


#Userinfo 

@client.command() 
async def userinfo(ctx, user:discord.Member=None): 
    if user is None: 
        user=ctx.author 
    elif user is not None: 
        user=user    

    info_embed= discord.Embed(title=f'{user.name}`s Information', color=0x000000) 
    info_embed.set_thumbnail(url=user.avatar)  
    info_embed.add_field(name='NAME:    ', value=user.name, inline=False) 
    info_embed.add_field(name='NICK NAME:', value=user.display_name, inline=False)
    info_embed.add_field(name='ID:', value=user.id, inline=False)
    info_embed.add_field(name='DISCRIMINATOR:', value=user.discriminator, inline=False)
    info_embed.add_field(name='TOP ROLE:', value=user.top_role, inline=False)
    info_embed.add_field(name='STATUS:', value=user.status, inline=False)  
    info_embed.add_field(name='CREATION DATE:', value=user.created_at.__format__("%A, %d. %B %Y  %H:%M:%S"), inline=False)  

    await ctx.send(embed=info_embed) 

#Avatar 
@client.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    avatar_url = member.avatar.url
    embed = discord.Embed(title="Avatar", description=f"Avatar of {member.name}", color=0x8A1E05)
    embed.set_image(url=avatar_url)
    await ctx.send(embed=embed)






 #clear command  
@client.command() 
async def clear(ctx, amount=10000000):    
    await ctx.send(f'{amount} messages have been deleted!', ephemeral=False)

    #Application Embed command 


class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label='📚 Manager For Buy', url='https://docs.google.com/forms/d/e/1FAIpQLSe4zryN4Fb4III1Ay2CeshhQ-yKmCJpfUG7qUJ_OG10_SxMrg/viewform'))



    async def on_timeout(self):
        pass

@client.command()
async def app1(ctx):
    embed = discord.Embed(title='Application', description='Πατήστε ένα από τα παρακάτω κουμπιά για να υποβάλετε μια αίτηση', color=0x00ffdd)

    view = MyView()

    await ctx.send(embed=embed, view=view)

    #---------------------------------------------------------------------------------------------RP BOT------------------------------------------------------------#

#Ip SYSTEM
@client.command()
async def ip(ctx):
    embed = discord.Embed(title='**IP SYSTEM**', description='', color=0xFFFF00)
    embed.add_field(name='IP:', value='soon...', inline=True) 
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1288087748762275963/1301751200181522484/New_Project_14.gif?ex=67259dc7&is=67244c47&hm=404ef534f02841871274cca52b88500c82c50a6b9b1cae1ce0b2c6f83b68adf8&=&width=671&height=671')
    embed.set_footer(text='Lion Roleplay')

    await ctx.send(embed=embed)

#Connect System 

@client.command() 
async def connect(ctx): 
    embed=discord.Embed(title='Connect System', description='', color=0xFFFF00) 
    embed.add_field(name='Connect:', value='connect soon...', inline=False)
    embed.set_thumbnail (url='https://media.discordapp.net/attachments/1288087748762275963/1301751200181522484/New_Project_14.gif?   ex=67259dc7&is=67244c47&hm=404ef534f02841871274cca52b88500c82c50a6b9b1cae1ce0b2c6f83b68adf8&=&width=671&height=671')
    embed.set_footer(text='Lion Roleplay')

    await ctx.send(embed=embed)






#--------------------------------------------------TESTING------------------------------------------------#


client.run('MTMwMjgyMjU3NjgyODk3MzE4Nw.Gvu4tA.jjnlUOXZGafJztkgYQZFiSHx-s_mqWVO5DABnY')
