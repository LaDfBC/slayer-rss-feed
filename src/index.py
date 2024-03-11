import praw
from dhooks import Embed, Webhook
import datetime
import time

#Don't Touch
search_term = 'Slayers'



# This is the only part you have to touch
#  To generate a client ID and secret, go here: https://www.reddit.com/prefs/apps scroll all the way to the bottom, and
#  hit the create an app button. Enter something for name and redirect URL, and make sure the script radio button is
#  selected. Hit the create app button, and then paste the client ID and secret below. The user_agent string literally 
#  just needs to have some text in it, does not matter what.

# If you haven't made one of these before, use 127.0.0.1 for the url and http://localhost for the redirect url
reddit = praw.Reddit(
    client_id='E0s_QzllJ8H4MVexsSZl4Q',
    client_secret='-th8R70ElDD0W8vY3oIeABrvgb1KOw',
    user_agent='slayer-rss-token'
)


# Don't change anything after here.

#DO NOT TOUCH
def parse_comments():
    for comment in reddit.subreddit('BaseballbytheNumbers').stream.comments(skip_existing=True):
        if search_term.lower() in comment.link_title.lower():

            #No touchy, this was the one that either Mike, Cash, or Sonar gave me, idr.
            hook = Webhook('https://discord.com/api/webhooks/474218985525870601/tM2lAv3vhvzsndDdSZgw1WzRbyB2mnH3TlVBb7U3reVQxoqQKh7DiNLUyvwDrg2hMjLf')

# Set this to the appropriate team abbreviation to say "New Pitch" when your team is batting instead of "New Update"
            #Don't Touch
            isping = comment.body.count('SUN')
            isresult = comment.body.count('Pitch:')
            numouts = comment.body.count('Outs')
            bodytext = comment.body.replace('**', '')


            update = '----------------------------------------------------------------------------\n'
            if isping > 1:
                #FOR THE LOVE OF BUFFY, DO NOT TOUCH
                update += '**Sunnydale Ping'
            elif isresult > 0:
                pitchindex = comment.body.index('Pitch:')
                pitch = comment.body[pitchindex+9:pitchindex+13]
                update += '**Pitch %s resulted' % (pitch)
            else:
                update += '**New Post'
                
            name = comment.author.name
            update += ' posted by ' + name
            update += ' at (<https://www.reddit.com%s>)**\n\n\n' % comment.permalink

                


# Remove the playbarcode URL            
            update = update.split('[.]')[0]

# Manipulate the reddit markdown into discord markdown
            update = update.replace('\t', '')
            update = update.replace('\n\n', '\n')
            update = update.replace('    ', '```    ',1)

            if numouts > 0:
                update = update.replace('Outs', 'Outs```',1)
            else:
                update = update.replace('Out', 'Out```',1)
            
            print("I've got the update set to " + update)

            print("Sending to discord now")
# Send the update to discord webhook            
            hook.send(update)
            em1 = Embed(description = "Play Overview", color=0x800080)
            em1.add_field(name = "Reddit Text", value = bodytext)
            em1.set_thumbnail(url='https://cdn.discordapp.com/attachments/643871298023325718/684806598014795850/UpdatedSlayerLogoFinal.png')
            hook.send(embed = em1)



while True:
    try:
        parse_comments()
    except Exception as e:
        print(e)
        time.sleep(60)
    else:
        time.sleep(360)
