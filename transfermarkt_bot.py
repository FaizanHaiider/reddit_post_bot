import requests, re
from lxml import html

# info needed to request page
headers = {'User-Agent' : 'transfermarkt_bot'}
url = "http://www.transfermarkt.com/premier-league/letztetransfers/wettbewerb/GB1/plus/1"

# request page 
webpage = requests.get(url, headers=headers)
tree = html.fromstring(webpage.content)

# collect raw data
rows = tree.xpath('//*[@id="yw1"]//tr/td[2]//a//text()')
age_date = tree.xpath('//*[@class="zentriert"]//text()')
transfer_type = tree.xpath('//*[@class="rechts hauptlink"]//text()')

# remove irrelavent data
for i in range(0, 3):
	age_date.pop(0)

# filter raw data
players = []
club_from = []
club_to = []
player_age = []

i_rows = 0
for elmnt in rows:
	if i_rows % 3 == 0:
		players.append(elmnt.encode("utf-8"))
	elif i_rows % 3 == 1:
		club_from.append(elmnt.encode("utf-8"))
	elif i_rows % 3 == 2:
		club_to.append(elmnt.encode("utf-8"))
	i_rows += 1

i_rows = 0
for elmnt in age_date:
	if i_rows % 2 == 0:
		player_age.append(elmnt.encode("utf-8"))
	i_rows += 1


# create final message
manutd_related = []
transfer_related = []
loan_related = []
free_agent_related = []


# player transferred to x from y for $
# player signed for x, originally a free agent
# player loaned to x from y
# player returned from loan to x from y
# player became free agent from x

for i in range(0, len(players)):
	final_message = players[i] + " (" + player_age[i] +" y/o) "

	if re.search("free agent", club_to[i], re.IGNORECASE):
		final_message += "became a free agent from " + club_from[i] 
	elif re.search("loan", transfer_type[i], re.IGNORECASE):
		final_message += "loaned to " + club_to[i] + " from " + club_from[i]
	elif re.search("end of loan", transfer_type[i].encode("utf-8"), re.IGNORECASE):
		final_message += "returned from loan to " + club_to[i] + " from " + club_from[i]
	elif re.search("free agent", club_from[i], re.IGNORECASE):
		final_message += "signed for " + club_to[i] + ", originally a free agent"
	else:
		final_message += "transferred to " + club_to[i] + " from " + club_from[i]
	
	if re.search("-", transfer_type[i]) and not re.search("free agent", club_to[i], re.IGNORECASE) and not re.search("free agent", club_from[i], re.IGNORECASE):
		final_message += " for an undisclosed fee"
	elif re.search("free transfer", transfer_type[i], re.IGNORECASE):
		final_message += " on a free transfer"
	elif not re.search("end of loan", transfer_type[i].encode("utf-8"), re.IGNORECASE) and not re.search("loan", transfer_type[i], re.IGNORECASE) and not re.search("-", transfer_type[i]):
		final_message += " for " + transfer_type[i].encode("utf-8")
	
	if re.search("manchester united", final_message, re.IGNORECASE):
		manutd_related.append(final_message)
	elif re.search("transferred to", final_message, re.IGNORECASE):
		transfer_related.append(final_message)
	elif re.search("free agent", club_to[i], re.IGNORECASE) or re.search("free agent", club_from[i], re.IGNORECASE):
		free_agent_related.append(final_message)
	else:
		loan_related.append(final_message)

print "Manchester United related:\n------------------------"
if len(manutd_related) == 0:
	print "None\n"
else:
	for message in manutd_related:
		print message

print "\nTransfers:\n-----------------"
if len(transfer_related) == 0:
	print "None\n"
else:
	for message in transfer_related:
		print message

print "\nLoans:\n-----------------"
if len(transfer_related) == 0:
	print "None\n"
else:
	for message in loan_related:
		print message

print "\nFree Agents:\n-----------------"
if len(free_agent_related) == 0:
	print "None\n"
else:
	for message in free_agent_related:
		print message

