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
    """ Inverse la clef et la valeur d'un dico """
    inversedico = {}
    for she,they in dico.items():
        for he in they:
            inversedico[he] = she
    return inversedico
 
def check(engaged):
    """ Teste la stability du dictionnaire de match 'engaged' 
        Le dictionnaire engaged est de la forme {'fille' : ['garçon1', 'garçon2', 'garçon3']}
    """
    # On commence par créer le dictionnaire de match réciproque
    # Il est de la forme {'garçon': 'fille'}
    inverseengaged = inversedict(engaged)
    for she, they in engaged.items():
        # pour chaque garcon dans sa liste de partenaires
        for he in they:
            # on regarde la liste de préférences de la fille 'she'
            shelikes = galprefers[she]
            # on regarde parmi sa liste de préférence lesquelles sont mieux classés que son partenaire actuel 'he'
            shelikesbetter = shelikes[:shelikes.index(he)]
            # on regarde la liste de préférence de 'he'
            helikes = guyprefers[he]
            # on regarde parmi sa liste de préférence lesquelles sont mieux classées que sa partenaire actuel 'she'
            helikesbetter = helikes[:helikes.index(she)]
            # pour chaque garçon qu'elle préfère plus que son partenaire actuel 'he'
            for guy in shelikesbetter:
                # s'il ne figure pas dans la liste de ses partenaires actuels
                if guy not in engaged[she]:
                    # on regarde qui est la partenaire actuelle de ce garçon 'guy'
                    guysgirl = inverseengaged[guy]
                    # On regarde sa liste de préférence de filles
                    guylikes = guyprefers[guy]
                    # si sa partenaire actuelle est moins bien classée que 'she' dans sa liste de préférence
                    # cela signifie qu'ils pourraient respectivement lâcher leur partenaire actuel pour se mettre
                    # en couple tous les 2 car ils s'aiment plus qu'ils n'aiment leur partenaire actuel
                    if guylikes.index(guysgirl) > guylikes.index(she):
                        print("%s and %s like each other better than "
                              "their present partners: %s and %s, respectively"
                              % (she, guy, he, guysgirl))
                        # le match est donc instable
                        return False
        # pour chaque fille qu'il préfère à sa partenaire actuelle 'she'
        for gal in helikesbetter:
            # on regarde le partenaire actuel de cette fille 'gal'
            girlsthey = engaged[gal]
            # on regarde la liste de préférence de cette fille 'gal'
            gallikes = galprefers[gal]
            # pour chaque garçon 'girlsguy' dans sa liste de partenaires actuels
            for girlsguy in girlsthey:
                # si son partenaire actuel 'girlsguy' est moins bien classé que 'he' dans sa liste de préférence
                # cela signifie qu'ils pourraient respectivement lâcher leur partenaire actuel pour se mettre
                # en couple tous les 2 car ils s'aiment plus qu'ils n'aiment leur partenaire actuel
                if gallikes.index(girlsguy) > gallikes.index(he):
                    print("%s and %s like each other better than "
                          "their present partners: %s and %s, respectively"
                          % (he, gal, she, girlsguy))
                    # le match est donc instable
                    return False
    return True

def orderlist(she, fiances):
    """ordonne la liste des fiancés dans l'ordre de preference"""
    liste = []
    for guy in galprefers[she]:
        if guy in fiances:
            liste.append(guy)
    return liste

def matchmaker():
    # on injecte tous les garçons dans la boucle de match
    guysfree = guys[:]
    # on initialise le dictionnaire de match
    engaged  = dict((she,[]) for she in gals)
    guyprefers2 = copy.deepcopy(guyprefers)
    galprefers2 = copy.deepcopy(galprefers)
    # tant qu'il y a des garçon dans la boucle de match, on continue
    while guysfree:
        # on sort le premier garçon de la boucle
        guy = guysfree.pop(0)
        # on regarde sa liste de préférences
        guyslist = guyprefers2[guy]
        # il se dirige vers la fille qu'il n'a jamais encore rencontré et qui est située le plus haut sur sa liste de préférence
        gal = guyslist.pop(0)
        # on regarde la liste des fiances actuels de cette fille 'gal'
        fiances = engaged.get(gal)
        # si la fille a moins de fiances qu'elle n'aimerait en avoir
        if len(fiances) < capacity[gal]:
            # alors on engage 'guy' avec 'gal'
            engaged[gal].append(guy)
            # et on réordonne sa liste de fiancés dans l'ordre de ses préférences
            engaged[gal] = orderlist(gal, engaged[gal])
            print("  %s and %s" % (guy, gal))
        # si la fille a déjà atteint sont nombre limite de fiancés
        else:
            # on regarde parmi ses fiancés celui qu'elle préfère le moins
            lastfiance = engaged[gal][-1]
            # on regarde sa liste de préférences
            galslist = galprefers2[gal]
            # si elle préfère le nouveau garçon 'guy' à 'lastfiances'
            if galslist.index(lastfiance) > galslist.index(guy):
                # alors elle retire 'lastfiances' de sa liste de fiances
                del engaged[gal][-1]
                # pour se fiancer avec 'guy'
                engaged[gal].append(guy)
                # puis elle remet de l'ordre dans sa liste de fiancés
                engaged[gal] = orderlist(gal, engaged[gal])
                print("  %s dumped %s for %s" % (gal, lastfiance, guy))

                # si 'lastfiances' a encore des filles à aller voir
                if guyprefers2[lastfiance]:
                    # alors on le réinjecte dans la boucle de match
                    guysfree.append(lastfiance)

            # sinon, si la fille reste fidèle à sa liste de fiancés
            else:
                # si 'guy' a encore des filles à aller voir
                if guyslist:
                    # alors on le réinjecte dans la boucle de match
                    guysfree.append(guy)
    return engaged

def displayCouples(engaged):     
    print('\nCouples:')
    for she,they in sorted(engaged.items()):
        print('  ' + ',\n  '.join('%s is engaged to %s' % (she,he)
                                  for he in they))
    print()


class TestDeCase(unittest.TestCase):
    """Test la fiabilite du match"""
    
    def test_1_check_stability(self):
        """Verifie que la stabilite du match"""
        self.assertTrue(check(engaged))
        print('Engagement stability check PASSED'
          if check(engaged) else 'Engagement stability check FAILED')
        print()

    def test_2_check_instability(self):
        """Verifie l'instabilite du match si l'on introduit volontairement une erreur"""
        engaged2 = copy.deepcopy(engaged)
        she1,she2 = random.sample(gals, 2)
        index1 = random.randint(0, len(engaged[she1])-1)
        index2 = random.randint(0, len(engaged[she2])-1)
        print('\n\nSwapping two fiances to introduce an error')
        engaged2[she1][index1], engaged2[she2][index2] = engaged2[she2][index2], engaged2[she1][index1]
        for gal in (she1,she2):
            for guy in engaged2[gal]:
                if guy not in engaged[gal]:
                    print('  %s is now engaged to %s' % (gal, guy))
        print()
        self.assertTrue(not check(engaged2))
        print('Engagement instability check PASSED'
              if not check(engaged2) else 'Engagement instability check FAILED')


###################################### MAIN ########################################
if __name__ == '__main__':
    print('\nEngagements:')
    engaged = matchmaker()
    displayCouples(engaged)
    unittest.main()



        
