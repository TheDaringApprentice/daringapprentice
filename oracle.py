# -*- coding: utf-8 -*-
# Copyright The Daring Apprentice 2009 --- thedaringapprentice@gmail.com
# http://github.com/TheDaringApprentice/daringapprentice/tree/master
# git://github.com/TheDaringApprentice/daringapprentice.git

def loadOraclefile(fileparameter):
    '''
    This function loads an oracletext file into a dictionary with the cardname as key, and
    a card dictionary of values:  (so we have a dictionary of dictionaries)
        'Name': 'Darksteel Colossus',
        'Type': 'Artifact Creature \xe2\x80\x94 Golem',
        'Converted Cost': 11,
        'Cost': '11',
        'Mono colored': True,
        'Colors': ['Colorless'],
        'Rules Text': "Trample Darksteel Colossus is indestructible. If Darksteel Colossus would be put into a graveyard from anywhere, reveal Darksteel Colossus and shuffle it into its owner's library instead.",
        'Set': ['Magic 2010', 'Darksteel'],
        'Rarity': 'Rare',
        'Rarity': ['Mythic Rare', 'Rare'],
        'Pow/Tgh': '(11/11)',
        'Power': '11',
        'Toughness': '11',   
        'Url': 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191312'
    '''

    # split the data into "cards" --- Split with the "Name: \t" substring
    data = file(fileparameter).read()\
            .replace('Name: \t','<---NewCard--->Name: \t')\
            .replace('Æ','Ae')\
            .split('<---NewCard--->')
            
            
    print 'Total Cards: ' + str(len(data))
    
    def GetCard(cardno):
        ''' GetCard reads and converts a card read from Oracle.txt to
        a dictionary called card.
        '''    
        
        # read the whole card data into a string
        s = data[cardno]
        
        # initialize the two lists
        Heads = []
        Tails = []
        
        # While there is a Key identifier {colon}{space}{tab} --- NB: this is assumed!
        while s.find(': \t') > 0:
            
            # Read the part before the Key Identifier
            aHead = s.partition(': \t')[0]
            
            # Take everything after the last newline char
            Heads.append(aHead.split('\n').pop())
            
            # Read the part after the Key Identifier, upto (and excl) the next Key Identifier
            aTail = s.partition(': \t')[2].partition(': \t')[0].rpartition('\n')[0]
            
            s = s.partition(': \t')[2]
            
            # Find the last newline
            lastchar = aTail.rfind('\n')
            if lastchar == -1 or s.find(': \t') >= len(aTail):
                lastchar = len(aTail)
            
            # Take everything up to the last newline (or all if no more newlines were found)
            Tails.append(aTail[0:lastchar].replace('\n',' '))
            # This kinda sucks... some \n chars are intentional, and some are just the break.
            # We either take it with the line breaks, and get weird breaks, or without them
            # and we sit with activation costs not at the start of the card.  Maybe some
            # more data cleaning before we run?  
            
            
        
        # Empty dictionary
        card = {}
        for item in Heads:
            card[item] = Tails[Heads.index(item)]
        
        if 'Name' in card:
            # Split the name and the url
            card['Url'] = "http://gatherer.wizards.com/Pages/" + card['Name'].partition('<../')[2].strip('>')
            card['Name'] = card['Name'].partition('<..')[0].strip()
            
        if 'Cost' in card:
            # Calculate the color(s) of a card, and the converted casting cost
            color = set([])
            aS = ''
            if card['Cost'].find('W') >= 0 or (card['Name'] + ' is white') in card['Rules Text'] >= 0:
                color = color | set(['White'])
            if card['Cost'].find('R') >= 0 or (card['Name'] + ' is red') in card['Rules Text'] >= 0:
                color = color | set(['Red'])
            if card['Cost'].find('G') >= 0 or (card['Name'] + ' is green') in card['Rules Text'] >= 0:
                color = color | set(['Green'])
            if card['Cost'].find('B') >= 0 or (card['Name'] + ' is black') in card['Rules Text'] >= 0:
                color = color | set(['Black'])
            if card['Cost'].find('U') >= 0 or (card['Name'] + ' is blue') in card['Rules Text'] >= 0:
                color = color | set(['Blue'])
                    
            if len(color) > 1:
                color = color | set(['Gold'])
                    
            if 'Type' in card:
                if card['Type'].find('Land') >= 0:
                    color = color | set(['Land'])
                '''
                # Artifacts are strictly colorless
                if card['Type'].find('Artifact') >= 0:
                    color = color | set(['Artifact'])
                '''
                
            if len(color) == 0:
                color = color | set(['Colorless'])
            
            # Assign the calculated colors    
            card['Colors'] = color
            
            
            # Do we need mono colored?  It may be useful in searching
            if len(color) == 1:
                card['Mono colored'] = True
            else:
                card['Mono colored'] = False
            
            # Calculate Converted Cost
            '''
                In this part we cycle through each character.  If the character is a digit
                we remember it,  to see if the next is  a  digit ( for cards above casting 
                cost 10).  1 is added for alpha characters.
                
                We  also check for multi mana,  and then only  the  first  alpha character 
                counts as 1. 
            '''
            cc = 0
            inmulti = False
            firstinmulti = True
            cs = ''
            for i, ch in enumerate(card['Cost']):
                if ch in '0123456789':
                    cs = cs + ch  #  not sure about += or =+ ?
                else:
                    if cs != '':
                        cc += int(cs)
                        cs = ''
                        firstinmulti = False
                    if ch.isalpha:
                        if ch not in ['x','X','(',')','{','}','/','\\']:
                            if inmulti:
                                if firstinmulti:
                                    cc += 1
                                    firstinmulti = False
                            else:
                                cc += 1
                        if ch in ['(','{']:
                            inmulti = True
                            firstinmulti = True
                        if ch in [')',')']:
                            inmulti = False
            if cs != '':
                cc += int(cs)
            card['Converted Cost'] = cc
                
        if 'Set/Rarity' in card:
            # For MTG, do some special work around Mythic Rares and Timeshifted Special cards
            s = card['Set/Rarity']\
                .replace('Mythic Rare','Mythic_Rare')\
                .replace('"Timeshifted" Special','"Timeshifted"_Special')\
                .split(',')
            Sets = []
            Rarities = []
            for aSet in s:
                Sets = Sets + [aSet.rpartition(' ')[0].strip()]
                Rarities = Rarities + [aSet.rpartition(' ')[2].strip().replace('_',' ')]
            card['Sets'] = Sets
            card['Rarities'] = Rarities
            # card['Rarity'] = Rarities[len(Rarities)-1]  # I decided I don't need a latest Rarity
            del card['Set/Rarity']
        
        if 'Pow/Tgh' in card:
            if card['Pow/Tgh'].find('/') > 0 :
                s = card['Pow/Tgh'].strip('()[]{}').split('/')
                card['Power'],card['Toughness'] = s[0],s[1]
            else:
                card['Power'],card['Toughness'] = '0','0'  # Assumed?!  Is there any cards without the / in the P/T?
            # Delete the P/T?  
        return card
    
    # Main loop - gets all the cards, and runs "GetCard" to get all the info
    # Should I start at -1 or 0? 0 seems to have nothing in current test data
    i = -1
    Cards = {}  # the master database!
    for card in data:
        i += 1
        aCard = GetCard(i)
        if 'Name' in aCard:
            Cards[aCard['Name']] = aCard
        else:
            print "Error at card no " + str(i)
    

    # A way to handle split cards - Might need refining!
    def CreateSplitcard(SplitCardName):
        cardname = SplitCardName.rpartition('(')[0].strip()
        if cardname in Cards:
            return
        card1 = cardname + ' (' + cardname.split('//')[0].strip() + ')'
        card2 = cardname + ' (' + cardname.split('//')[1].strip() + ')'
        card = {}
        card['Name'] = cardname.strip()
        card['Cost'] = Cards[card1]['Cost'] + ' // ' + Cards[card2]['Cost']
        card['Type'] = Cards[card1]['Type'] + ' // ' + Cards[card2]['Type']
        card['Converted Cost'] = Cards[card1]['Converted Cost'] + Cards[card2]['Converted Cost']
        card['Mono colored'] = Cards[card1]['Mono colored'] and Cards[card2]['Mono colored']
        card['Colors'] = set(Cards[card1]['Colors']) | set(Cards[card2]['Colors'])
        card['Rules Text'] = Cards[card1]['Rules Text'] + '\n---Split---\n' + Cards[card2]['Rules Text']
        card['Sets'] = Cards[card1]['Sets'] # Or should I just add the 2 sets together?
        card['Rarities'] = Cards[card1]['Rarities'] # Or should I just add the 2 rarities together?
        card['Pow/Tgh'] = Cards[card1]['Pow/Tgh'] + ' // ' + Cards[card2]['Pow/Tgh'] # Looks silly on spells
        card['Power'] = Cards[card1]['Power'] + ' // ' + Cards[card2]['Power'] # Max maybe?
        card['Toughness'] = Cards[card1]['Toughness'] + ' // ' + Cards[card2]['Toughness'] # Max maybe?
        card['Url'] = Cards[card1]['Url'] # + ', ' + Cards[card2]['Url'] # They have the same URL...
        Cards[cardname.strip()] = card
        # Should I delete the single cards? 
        del Cards[card1]
        del Cards[card2]
            

    # Do split cards --- good to know Cards.keys() is only evaluated once
    for aName in Cards.keys():
        if aName.find('//') >= 0:
            CreateSplitcard(aName)
    
    # Return the dictionary of cards
    print len(Cards)
    return Cards
    
# OracleCards = loadOraclefile('g:\pyDA\Oracle.txt')

# Some test cases
'''
print OracleCards['Evermind']                           # Funny colored cards
print OracleCards['Court Hussar']                       # Just a power and toughness test
print OracleCards['Darksteel Colossus']                 # Funny mana cost, Mythic Rare
print OracleCards['Craw Giant']                         # Timeshifted special
print OracleCards['Flame Javelin']                      # Funny casting costs
print OracleCards['Crime // Punishment (Crime)']        # Split cards 1 side
print OracleCards['Crime // Punishment (Punishment)']   # Split cards other side
print OracleCards['Crime // Punishment']                # Manually combined split card
print OracleCards['Wrath of God']['Cost']               # How to reference a key within the dictionary
'''
# print len(OracleCards)
