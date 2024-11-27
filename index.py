import discord
from discord.ext import commands
import os

# Remplace par ton token
TOKEN = os.getenv("DISCORD_TOKEN")

# Préfixe des commandes
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# ID du message "Règlement" et du rôle
REGLEMENT_MESSAGE_ID = None  # Remplace après avoir envoyé ton message
ROLE_ID = None               # Remplace par l'ID du rôle "Membre"

# Événement : Ajout de réaction
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == REGLEMENT_MESSAGE_ID:  # Vérifie que c'est le bon message
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)  # Récupère le rôle
        member = guild.get_member(payload.user_id)  # Récupère l'utilisateur

        if role and member:
            await member.add_roles(role)  # Attribue le rôle
            print(f"Rôle {role.name} attribué à {member.name}")

# Commande pour envoyer le message de règlement
@bot.command()
@commands.has_permissions(administrator=True)
async def règles(ctx):
    # ID du salon textuel "rules"
    rules_channel_id = 1168583831184478239
    rules_channel = ctx.guild.get_channel(rules_channel_id)

    # Envoie un message avec les règles
    if rules_channel and isinstance(rules_channel, discord.TextChannel):
        message = await ctx.send(
            f"**Bienvenue sur le serveur !**\n"
            f"Merci de lire et d'accepter les règles dans {rules_channel.mention}.\n"
            f"Réagissez avec ✅ sous le message dans ce canal pour obtenir l'accès au serveur."
        )
        await message.add_reaction("✅")  # Ajoute l'emoji ✅
        
        global REGLEMENT_MESSAGE_ID
        REGLEMENT_MESSAGE_ID = message.id  # Sauvegarde l'ID du message
    else:
        await ctx.send("Le salon textuel 'rules' est introuvable. Vérifiez son ID.")

@bot.event
async def on_raw_reaction_add(payload):
    # On vérifie si la réaction vient du canal #rules
    if payload.channel_id != 1168583831184478239:  # Remplace par l'ID du canal #rules
        return
    
    # Vérifie si la réaction est un ✅
    if str(payload.emoji) == '✅':
        # On récupère le membre qui a réagi
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        # On vérifie si le membre a bien réagi au message du #rules (on prend le message spécifique)
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        
        # On vérifie si c'est le dernier message de #rules, ici tu peux ajuster en fonction de ton message spécifique
        if message.id == 1311333597239578696:  # Remplace par l'ID du message #rules
            # On récupère le rôle "Moule" (assure-toi que ce rôle existe)
            role_moule = discord.utils.get(guild.roles, name="Moule")
            role_plebien = discord.utils.get(guild.roles, name="Plébéien")
            
            # Si le rôle 'Moule' existe, on l'attribue
            if role_moule:
                await member.add_roles(role_moule)
                print(f"Le rôle 'Moule' a été attribué à {member.name}")
            
            # Si le rôle 'plébéien' existe, on le retire
            if role_plebien:
                await member.remove_roles(role_plebien)
                print(f"Le rôle 'plébéien' a été retiré à {member.name}")
            else:
                print("Le rôle 'plébéien' n'a pas été trouvé.")


# Événement : Le bot est prêt
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

# Commande simple
@bot.command()
async def ping(ctx):
    await ctx.send("tu t'es pris pour un chinois fdp!?")

# Commande pour répéter un message
@bot.command()
async def say(ctx):
    await ctx.send('Salut les connards, comment ça va !? pensez a faire un tour sur le stream ou jte nique ta mère!')

import asyncio

# commande pour le !Status 
@bot.command()
async def status(ctx):
    # Message initial
    await ctx.send('TEST SISMIQUE!!!!!!')

    # Vérifie si l'utilisateur est dans un salon vocal
    if not ctx.author.voice:
        await ctx.send("Tu dois être connecté à un salon vocal pour exécuter cette commande !")
        return

    # Liste des salons vocaux disponibles dans le serveur
    voice_channels = [channel for channel in ctx.guild.voice_channels]

    if not voice_channels:
        await ctx.send("Aucun salon vocal disponible pour exécuter cette commande.")
        return

    try:
        # Récupère le salon vocal actuel de l'utilisateur
        current_channel = ctx.author.voice.channel

        # Déplacement dans chaque salon vocal pendant 5 secondes
        for channel in voice_channels:
            if channel != current_channel:  # Ignore le salon actuel
                await ctx.author.move_to(channel)  # Déplace l'utilisateur
                await asyncio.sleep(1)  # Attend 1 seconde dans chaque salon

        # Retourne l'utilisateur dans son salon vocal initial
        await ctx.author.move_to(current_channel)
        await ctx.send(f"Fin du test sismique, {ctx.author.mention} est de retour dans son salon initial.")

    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions nécessaires pour déplacer cet utilisateur.")
    except discord.HTTPException as e:
        await ctx.send(f"Une erreur s'est produite lors du déplacement : {e}")


import asyncio

# commande troll de notre ami dobby
@bot.command()
async def roles(ctx):
    role_plebeien_name = "Plébéien"  # Nom du rôle temporaire "Plébéien"

    # Envoie un message de troll
    await ctx.send("Non mais sérieusement gros, y'a vraiment des gens comme toi qui tappent des commandes de merde comme ça que le dev qui m'a créé a clairement pas envie de coder!? Allez hop ça retourne en plébéien pendant 120 secondes, raz le cul des casse couilles !")

    # Recherche le rôle "Plébéien" dans le serveur
    role_plebeien = discord.utils.get(ctx.guild.roles, name=role_plebeien_name)

    if not role_plebeien:
        await ctx.send(f"Désolé, le rôle '{role_plebeien_name}' n'existe pas.")
        return

    try:
        # Sauvegarde les rôles actuels de l'utilisateur
        user_roles = ctx.author.roles[1:]  # Ignore @everyone (toujours présent)

        # Retire tous les rôles de l'utilisateur
        await ctx.author.edit(roles=[])
        # Assigne le rôle "Plébéien" à l'utilisateur
        await ctx.author.add_roles(role_plebeien)

        # Attendre 5 secondes avant de restaurer les rôles initiaux
        await asyncio.sleep(120)
        # Retirer le rôle "Plébéien"
        await ctx.author.remove_roles(role_plebeien)
        # Restaurer les rôles initiaux
        await ctx.author.edit(roles=user_roles)

    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions pour modifier les rôles de cet utilisateur.")
    except discord.HTTPException as e:
        await ctx.send(f"Une erreur s'est produite : {e}")
   
# commande pour donner des infos sur les membres du discord
@bot.command()
async def info(ctx):
    # Récupère les informations du serveur
    guild = ctx.guild
    total_members = guild.member_count  # Nombre total de membres
    online_members = len([member for member in guild.members if member.status != discord.Status.offline])  # Membres en ligne
    server_name = guild.name
    server_creation_date = guild.created_at.strftime("%d/%m/%Y")  # Date de création du serveur
    
    # Création du message à envoyer
    info_message = f"""
    **Informations sur le serveur** : {server_name}
    
    🗓️ **Date de création** : {server_creation_date}
    👥 **Membres totaux** : {total_members}
    💬 **Membres en ligne** : {online_members}
    
    **Quelques chiffres intéressants** :
    - **Salons** : {len(guild.text_channels) + len(guild.voice_channels)}
    - **Rôles** : {len(guild.roles)}
    - **Emojis personnalisés** : {len(guild.emojis)}
    
    **Ressources disponibles** :
    - Consultez les règles du serveur dans le canal #règles.
    - Si vous avez des questions, le canal #aide est à votre disposition.
    """
    
    # Envoie le message dans le canal
    await ctx.send(info_message)


# commande Hello   
@bot.command()
async def hello(ctx):
    await ctx.send('salut abonnes toi pitié... connard')
    
# commande cachée   
@bot.command()
async def chaussette(ctx):
    # Nom des rôles à gérer
    role_name_super_moule = "Super Moule"
    role_name_moule = "Moule"
    
    # Recherche les rôles dans le serveur
    role_super_moule = discord.utils.get(ctx.guild.roles, name=role_name_super_moule)
    role_moule = discord.utils.get(ctx.guild.roles, name=role_name_moule)
    
    # Retirer le rôle 'Moule' s'il existe
    if role_moule:
        await ctx.author.remove_roles(role_moule)
        print(f"{ctx.author.name} a perdu le rôle '{role_name_moule}'")
    
    if role_super_moule:
        # Ajouter le rôle 'Super Moule'
        await ctx.author.add_roles(role_super_moule)
        await ctx.send(f"{ctx.author.mention}, tu as maintenant le rôle '{role_name_super_moule}' !")
    else:
        # Si le rôle 'Super Moule' n'existe pas
        await ctx.send(f"Désolé {ctx.author.mention}, le rôle '{role_name_super_moule}' n'existe pas.")
    
    # Supprimer le message de l'utilisateur (le message "!chaussette")
    await ctx.message.delete()


@bot.command()
async def msg(ctx):
    await ctx.send('Bienvenue sur le serveur! :tada:\n\n'
                   'Nous sommes ravis de t’accueillir dans notre communauté. Avant de commencer à discuter, voici quelques informations importantes pour bien démarrer :\n\n'
                   '**Lisez les règles :** Assurez-vous d’avoir pris connaissance de nos règles de serveur dans le canal #règles. Le respect et la convivialité sont essentiels ici !\n\n'
                   '**Présentation :** N’hésitez pas à vous présenter dans le canal #présentations et à dire quelques mots sur vous. C’est toujours agréable de connaître les nouveaux membres !\n\n'
                   '**Ressources utiles :** Si vous avez des questions, n’hésitez pas à utiliser le canal #aide ou à contacter un membre de l’équipe de modération.\n\n'
                   '**Commandes du Bot :** Voici la liste des commandes disponibles pour interagir avec notre bot dans le canal #general et profiter pleinement du serveur :\n\n'
                   '`!hello` : Le bot vous dira bonjour et vous présentera quelques informations de base.\n'
                   '`!règles` : Vous rappelle les règles du serveur. Assurez-vous de les lire !\n'
                   '`!info` : Donne des informations sur le serveur, les membres, et plus encore.\n'
                   '`!roles` : Liste les rôles disponibles et permet de vous auto-assigner certains rôles spécifiques.\n'
                   '`!quiz` : Lance un quiz rapide pour tester vos connaissances sur des sujets variés !\n'
                   '`!status` : Affiche l’état actuel du serveur et des bots.\n'
                   '`!ping` : Vérifie la latence du bot et assure que tout fonctionne bien.\n\n'
                   '**Il existe quelques commandes cachées... A toi de les trouver **\n\n'
                   '**Conseils pour bien démarrer :**\n'
                   '- Assurez-vous de lire les règles et de réagir au message de bienvenue pour obtenir l\'accès complet aux canaux.\n'
                   '- Respectez les autres membres et gardez une ambiance chill, café et détente !\n'
                   '- Si vous avez des questions ou des préoccupations, n’hésitez pas à solliciter un modérateur.\n\n'
                   'Nous espérons que vous passerez un bon moment avec nous. Si vous avez des suggestions ou des idées pour améliorer le serveur, faites-le nous savoir !\n\n'
                   '**Bonne aventure et amusez-vous bien sur La Bourriche!**')
    
# Supprime l'ancienne commande si elle existe
bot.remove_command("msgRules")

@bot.command()
async def msgRules(ctx):
    parts = [
        "**📜 Règles du Serveur Discord :**\n\n"
        "**Bienvenue sur notre serveur !**\n"
        "Nous sommes ici pour échanger, discuter, et passer un bon moment ensemble. "
        "Nous vous demandons simplement de respecter quelques règles pour maintenir une ambiance agréable et respectueuse pour tous.\n\n"
        "**1️⃣ Respectez les autres membres.**\n"
        "Chacun mérite d’être traité avec respect. Les attaques personnelles, insultes et discriminations de toute sorte sont interdites. "
        "Gardez toujours à l’esprit que derrière chaque pseudo se trouve une personne réelle.\n\n"
        "**2️⃣ Pas de contenu explicite.**\n"
        "Ce serveur est un espace de discussion respectueux. Aucun contenu pornographique, violent ou choquant n’est toléré.\n\n"
        "**3️⃣ La politique, oui, mais avec responsabilité.**\n"
        "Les discussions politiques sont autorisées, mais elles doivent rester respectueuses. Si vous avancez des arguments, soyez prêt à les assumer pleinement.\n\n",
        
        "**4️⃣ Les harceleurs seront bannis.**\n"
        "Politique de tolérance zéro envers le harcèlement. Si vous harcelez quelqu’un (sur le serveur ou en privé), vous serez immédiatement banni.\n\n"
        "**5️⃣ Ambiance chill café, pas de drama.**\n"
        "Ce serveur est un lieu de détente et d’amusement. Évitez les dramas inutiles.\n\n"
        "**6️⃣ Utilisez les canaux comme il se doit.**\n"
        "Chaque canal a un but précis : gardez les discussions pertinentes à chaque sujet.\n\n"
        "**7️⃣ Aucun spam ni flood.**\n"
        "Ne spammez pas les messages ou les notifications.\n\n",

        "**8️⃣ Les publicités, c’est en privé.**\n"
        "Les publicités non sollicitées sont interdites dans les canaux publics.\n\n"
        "**9️⃣ Respect de la vie privée.**\n"
        "Ne partagez jamais des informations personnelles d’autres membres.\n\n"
        "**🔟 Soyez courtois avec les modérateurs.**\n"
        "Respectez leurs décisions et contactez-les en cas de problème.\n\n"
        "**🔢 Les bots, c’est avec modération.**\n"
        "N’abusez pas des commandes de bots.\n\n"
        "**🚫 Pas de comportements toxiques.**\n"
        "Évitez les comportements nuisibles qui perturbent l’ambiance.\n\n"
        "click sur ✅ sur ce message pour accepter les règles et gagner un rôle différent. \n\n"
        "Merci de faire partie de notre communauté, et bonne discussion ! 🎉"
    ]

    # Envoie chaque partie une seule fois
    for part in parts:
        await ctx.send(part)


# Commande pour supprimer des messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} messages supprimés.", delete_after=5)

# Démarrer le bot
bot.run(TOKEN)
