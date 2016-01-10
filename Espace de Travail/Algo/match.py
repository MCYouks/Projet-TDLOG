# TDLOG - Projet
# Andréas Blondeau
# Déc 2015

import random
import copy
import unittest
from gender import preferences

guyprefers = preferences().guyprefers
galprefers = preferences().galprefers
capacity = preferences().capacity

guys = sorted(guyprefers.keys())
gals = sorted(galprefers.keys())

# guyprefers= {
#  'abe':  ['abi', 'cath', 'bea'],
#  'bob':  ['cath', 'abi', 'bea'],
#  'col':  ['abi', 'bea', 'cath'],
#  'dan':  ['bea', 'cath', 'abi'],
#  'ed':   ['bea', 'cath', 'abi'],
#  'fred': ['bea', 'abi', 'cath'],
#  'gav':  ['bea', 'cath', 'abi'],
#  'hal':  ['abi', 'cath', 'bea'],
#  'ian':  ['cath', 'bea', 'abi'],
#  'jon':  ['abi', 'bea', 'cath'],
#  }

# galprefers = {
#  'abi':  ['bob', 'fred', 'jon', 'gav', 'ian', 'abe', 'dan', 'ed', 'col', 'hal'],
#  'bea':  ['bob', 'abe', 'col', 'fred', 'gav', 'dan', 'ian', 'ed', 'jon', 'hal'],
#  'cath': ['fred', 'bob', 'ed', 'gav', 'hal', 'col', 'ian', 'abe', 'dan', 'jon'],
#  }

# capacity = {
#     'abi':  4,
#     'bea':  3,
#     'cath': 1,
# }




def inversedict(dico):
    inversedico = {}
    for she,they in dico.items():
        for he in they:
            inversedico[he] = she
    return inversedico
 
def check(engaged):
    inverseengaged = inversedict(engaged)
    for she, they in engaged.items():
        for he in they:
            shelikes = galprefers[she]
            shelikesbetter = shelikes[:shelikes.index(he)]
            helikes = guyprefers[he]
            helikesbetter = helikes[:helikes.index(she)]
            for guy in shelikesbetter:
                if guy not in engaged[she]:
                    guysgirl = inverseengaged[guy]
                    guylikes = guyprefers[guy]
                    if guylikes.index(guysgirl) > guylikes.index(she):
                        print("%s and %s like each other better than "
                              "their present partners: %s and %s, respectively"
                              % (she, guy, he, guysgirl))
                        return False
        for gal in helikesbetter:
            gallikes = galprefers[gal]
            girlsthey = engaged[gal]
            for girlsguy in girlsthey:
                if gallikes.index(girlsguy) > gallikes.index(he):
                    print("%s and %s like each other better than "
                          "their present partners: %s and %s, respectively"
                          % (he, gal, she, girlsguy))
                    return False
    return True

def orderlist(she, fiances):
    """ordonne la liste des fiances dans l'ordre de preference"""
    liste = []
    for guy in galprefers[she]:
        if guy in fiances:
            liste.append(guy)
    return liste

def matchmaker():
    guysfree = guys[:]
    engaged  = dict((she,[]) for she in gals)
    guyprefers2 = copy.deepcopy(guyprefers)
    galprefers2 = copy.deepcopy(galprefers)
    print('\nEngagements:')
    while guysfree:
        guy = guysfree.pop(0)
        guyslist = guyprefers2[guy]
        gal = guyslist.pop(0)
        fiances = engaged.get(gal)
        if len(fiances) < capacity[gal]:
            # She still has places
            engaged[gal].append(guy)
            engaged[gal] = orderlist(gal, engaged[gal])
            print("  %s and %s" % (guy, gal))
        else:
            # The bounder proposes to an engaged lass!
            lastfiance = engaged[gal][-1]
            galslist = galprefers2[gal]
            if galslist.index(lastfiance) > galslist.index(guy):
                # She prefers new guy
                del engaged[gal][-1]
                    # Remove lastfiance
                engaged[gal].append(guy)
                engaged[gal] = orderlist(gal, engaged[gal])
                print("  %s dumped %s for %s" % (gal, lastfiance, guy))
                if guyprefers2[lastfiance]:
                    # Ex has more girls to try
                    guysfree.append(lastfiance)
            else:
                # She is faithful to old fiance
                if guyslist:
                    # Look again
                    guysfree.append(guy)
    return engaged

def displayCouples(engaged):     
    print('\nCouples:')
    for she,they in sorted(engaged.items()):
        print('  ' + ',\n  '.join('%s is engaged to %s' % (she,he)
                                  for he in they))
    print()


        
