import enum
import random
import discord
import datetime

random.seed(datetime.datetime.now())

# =======================================================================
# ---------- ASSETS (settings, lore) ------------------------------------
# -----------------------------------------------------------------------

MIN_PLAYERS = 5
MAX_PLAYERS = 15

gamemode = {
    'trouble-brewing' : {
        'description' : "Trouble Brewing has a little bit of everything. Some characters passively receive " \
                        "information, some need to take action to learn who is who, while some simply want to " \
                        "bait the Demon into attacking them. Both good and evil can gain the upper hand by " \
                        "making well-timed sacrifices. Trouble Brewing is a relatively straightforward " \
                        "Demon-hunt, but evil has a number of dastardly misinformation tricks up their " \
                        "sleeves, so the good players best question what they think they know if they hope to " \
                        "survive.",
        'min_players' : MIN_PLAYERS,
        'max_players' : MAX_PLAYERS,
        'chance' : 0,
        'game' : 'botc',
        'roles' : {
            #4, 5, 6, 7, 8, 9, 10,11,12,13,14,15
            "Townsfolk" :
            [0, 3, 3, 5, 5, 5, 7, 7, 7, 9, 9, 9],
            "Outsider" :
            [0, 0, 1, 0, 1, 2, 0, 1, 2, 0, 1, 2],
            "Minion" :
            [0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            "Demon" :
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        },
        'improved_guide' : {
            #p     t  o  m  d
            '5' : [3, 0, 1, 1],
            '6' : [3, 1, 1, 1],
            '7' : [5, 0, 1, 1],
            '8' : [5, 1, 1, 1],
            '9' : [5, 2, 1, 1],
            '10': [7, 0, 2, 1],
            '11': [7, 1, 2, 1],
            '12': [7, 2, 2, 1],
            '13': [9, 0, 3, 1],
            '14': [9, 1, 3, 1],
            '15': [9, 2, 3, 1]
        }
    }
}

lore_text = {

    "game_start_lore" : "Clouds roll in over Ravenswood Bluff, engulfing this sleepy town and its superstitious " \
                        "inhabitants in foreboding shadow. Freshly-washed clothes dance eerily on lines strung " \
                        "between cottages. Chimneys cough plumes of smoke into the air. Exotic scents waft " \
                        "through cracks in windows and under doors, as hidden cauldrons lay bubbling. An " \
                        "unusually warm Autumn breeze wraps around vine-covered walls and whispers ominously to " \
                        "those brave enough to walk the cobbled streets. Those who can read the signs know there " \
                        "is **Trouble Brewing**.",
    "day_end_warning" : "Anxious mothers call their children home from play, as thunder begins to clap on the horizon."

}

# =======================================================================
# ---------- UTILITY (game object, player object) -----------------------
# -----------------------------------------------------------------------

class BOTCUtils:

    @staticmethod
    def find_role_by_name(role_name_str, role_obj_list):
        for role in role_obj_list:
            if role_name_str.lower() == str(role).lower():
                return role
    
    @staticmethod
    def get_tb_townsfolk_list():
        tb_townsfolk_all = [role_obj() for role_obj in Townsfolk.__subclasses__()]
        return tb_townsfolk_all
    
    @staticmethod
    def get_tb_outsider_list():
        tb_outsider_all = [role_obj() for role_obj in Outsider.__subclasses__()]
        return tb_outsider_all
    
    @staticmethod
    def get_tb_minion_list():
        tb_minion_all = [role_obj() for role_obj in Minion.__subclasses__()]
        return tb_minion_all
    
    @staticmethod
    def get_tb_demon_list():
        tb_demon_all = [role_obj() for role_obj in Demon.__subclasses__()]
        return tb_demon_all
    
    @staticmethod
    def get_tb_all_list():
        tb_all = BOTCUtils.get_tb_townsfolk_list() + BOTCUtils.get_tb_outsider_list() + \
                 BOTCUtils.get_tb_minion_list() + BOTCUtils.get_tb_demon_list()
        return tb_all


class BOTCRole:

    def __init__(self):
        self._desc_string = None  # Role description -> string
        self._instr_string = None  # Character text -> string
        self._role_name = None  # Role name -> enum.Enum
        self._art_link = None  # Character art url -> string 
        self._wiki_link = None  # Character wiki url -> string
        self._main_wiki_link = "http://bloodontheclocktower.com/wiki/Main_Page"  # Main page url -> string
        self._gm_art_link = None  # Gamemode wiki url -> string
        self._botc_demon_link = "https://bloodontheclocktower.com/img/website/demon-head.png?" \
                              "rel=1589188746616"  # Demon head art url -> string
        self._botc_logo_link = "http://bloodontheclocktower.com/wiki/images/logo.png"  
                               # Logo art url -> string
        self.gm_of_appearance = None  # Gamemode of appearance -> enum.Enum

    def __str__(self):
        return self._role_name.value
    
    def __repr__(self):
        return self._role_name.value + " Obj"

    def get_role_desc(self):
        return self._desc_string

    def get_role_player_instr(self):
        return self._instr_string
    
    def get_category(self):
        raise NotImplementedError
    
    def get_team(self):
        raise NotImplementedError

    def exec_init_setup(self, townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list):
        return [townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list] 
    
    def exec_init_flags(self):
        return
    
    def make_role_card_embed(self):

        TOWNSFOLK_COLOR = 0x00f8fb
        OUTSIDER_COLOR = 0x00f8fb
        MINION_COLOR = 0xe10600
        DEMON_COLOR = 0xe10600

        def make_embed(role_name, role_category, card_color, gm, gm_art_link, desc_str, char_str, pic_link, 
                       wiki_link):
            embed = discord.Embed(title = role_name, description = "[{}]".format(role_category), 
                                  color = card_color)
            embed.set_author(name = "Blood on the Clocktower - {}".format(gm), icon_url = gm_art_link)
            embed.set_thumbnail(url = pic_link)
            embed.add_field(name = "Description", value = desc_str, inline = False)
            embed.add_field(name = "Character Text", value = char_str + "\n" + wiki_link, inline = False)
            embed.set_footer(text = "Copyrights of BoTC belong to the Pandemonium Institute. " \
                                    "The Devs are not affiliated with them in any way.")
            return embed

        if self.get_category() == BOTCCategory.townsfolk:
            color = TOWNSFOLK_COLOR
        elif self.get_category() == BOTCCategory.outsider:
            color = OUTSIDER_COLOR
        elif self.get_category() == BOTCCategory.minion:
            color = MINION_COLOR
        elif self.get_category() == BOTCCategory.demon:
            color = DEMON_COLOR
        gm_art_link = self._gm_art_link if self._gm_art_link else self._botc_logo_link
        pic_link = self._art_link if self._art_link else self._botc_demon_link
        wiki_link = self._wiki_link if self._wiki_link else self._main_wiki_link
        embed = make_embed(self.__str__(), self.get_category().value, color, self.gm_of_appearance.value, 
                           gm_art_link, self.get_role_desc(), self.get_role_player_instr(), pic_link, 
                           wiki_link)
        return embed


class BOTCGameObject:

    class Phase(enum.Enum):
        day = "day"
        night = "night"
        idle = "idle"
    
    class IncorrectNumberPlayers(Exception):
        pass

    class NotBOTCGame(Exception):
        pass

    def __init__(self, gamemode, player_id_list):
        if gamemode not in BOTCGamemode:
            raise BOTCGameObject.NotBOTCGame("Gamemode is not one of BoTC editions.")
        self._phase = BOTCGameObject.Phase.idle
        self._gamemode = gamemode  # enum.Enum object here
        self._player_id_list = player_id_list  # list object
        self._player_obj_list = []  # list object
        self.generate_role_set(len(self._player_id_list))
    
    def generate_role_set(self, num_player):
        if num_player > MAX_PLAYERS or num_player < MIN_PLAYERS:
            raise BOTCGameObject.IncorrectNumberPlayers("Must be between 5 and 15 players.")
        else:
            role_guide_chart_temp = gamemode[self._gamemode.value.lower()]["improved_guide"]
            role_guide_chart = role_guide_chart_temp[str(num_player)]
            nb_townsfolk = role_guide_chart[0]
            nb_outsider = role_guide_chart[1]
            nb_minion = role_guide_chart[2]
            nb_demon = role_guide_chart[3]
            # Trouble brewing mode
            if self.gamemode == BOTCGamemode.tb:
                
                tb_townsfolk_all = BOTCUtils.get_tb_townsfolk_list()
                tb_outsider_all = BOTCUtils.get_tb_outsider_list()
                tb_minion_all = BOTCUtils.get_tb_minion_list()
                tb_demon_all = BOTCUtils.get_tb_demon_list()

                ret_townsfolk = random.sample(tb_townsfolk_all, nb_townsfolk)
                ret_outsider = random.sample(tb_outsider_all, nb_outsider)
                ret_minion = random.sample(tb_minion_all, nb_minion)
                ret_demon = random.sample(tb_demon_all, nb_demon)

                final_townsfolk = ret_townsfolk.copy()
                final_outsider = ret_outsider.copy()
                final_minion = ret_minion.copy()
                final_demon = ret_demon.copy()

                prelim = ret_townsfolk + ret_outsider + ret_minion + ret_demon

                for role in prelim:
                    setup_next = role.exec_init_setup(final_townsfolk, final_outsider, final_minion, final_demon)
                    final_townsfolk = setup_next[0]
                    final_outsider = setup_next[1]
                    final_minion = setup_next[2]
                    final_demon = setup_next[3]
                
                setup = final_townsfolk + final_outsider + final_minion + final_demon
                random.shuffle(setup)
                print(setup)
                self.distribute_roles(setup, self.player_id_list)
                return

            # Bad moon rising mode
            elif self.gamemode == BOTCGamemode.bmr:
                pass
            # Sects and violets mode
            elif self.gamemode == BOTCGamemode.sv:
                pass
            else:
                raise BOTCGameObject.NotBOTCGame("Gamemode is not one of BoTC editions.")
        
    def distribute_roles(self, role_obj_list, player_id_list):
        pass
    
    @property
    def gamemode(self):
        return self._gamemode
    
    @property
    def player_id_list(self):
        return self._player_id_list


class BOTCPlayer:

    class PlayerState(enum.Enum):
        alive = "alive"
        dead = "dead"
        fleaved = "fleaved"

    def __init__(self, userid_str, role_obj):
        self._userid = userid_str
        self._role = role_obj 
        self._state = BOTCPlayer.PlayerState.alive
    
    @property
    def role(self):
        return self._role
    
    @property
    def userid(self):
        return self._userid
    
    @property
    def state(self):
        return self._state
    
    def exec_death(self):
        self._state = BOTCPlayer.PlayerState.dead

    def exec_fleave(self):
        self._state = BOTCPlayer.PlayerState.fleaved


# =======================================================================
# ---------- BLOOD ON THE CLOCKTOWER (general, parent classes) ----------
# -----------------------------------------------------------------------

class BOTCGamemode(enum.Enum):

    tb = "Trouble-Brewing"
    bmr = "Bad-Moon-Rising"
    sv = "Sects-&-Violets"


class BOTCCategory(enum.Enum):

    townsfolk = "Townsfolk"
    outsider = "Outsider"
    minion = "Minion"
    demon = "Demon"


class BOTCTeam(enum.Enum):

    good = "Good"
    evil = "Evil"


class Townsfolk:
    
    def get_category(self):
        return BOTCCategory.townsfolk
    
    def get_team(self):
        return BOTCTeam.good


class Outsider:

    def get_category(self):
        return BOTCCategory.outsider
    
    def get_team(self):
        return BOTCTeam.good


class Minion:

    def get_category(self):
        return BOTCCategory.minion
    
    def get_team(self):
        return BOTCTeam.evil


class Demon:
    
    def get_category(self):
        return BOTCCategory.demon
    
    def get_team(self):
        return BOTCTeam.evil


# =======================================================================
# ---------- TROUBLE BREWING EDITION (roles and lists) ------------------
# -----------------------------------------------------------------------

# ---------- Parent classes [Trouble Brewiding Edition] ----------

class TBRole(enum.Enum):
    """Enum object for all Trouble Brewing edition roles"""

    washerwoman = "Washerwoman"
    librarian = "Librarian"
    investigator = "Investigator"
    chef = "Chef"
    empath = "Empath"
    fortuneteller = "Fortune Teller"
    undertaker = "Undertaker"
    monk = "Monk"
    ravenkeeper = "Ravenkeeper"
    virgin = "Virgin"
    slayer = "Slayer"
    soldier = "Soldier"
    mayor = "Mayor"
    butler = "Butler"
    drunk = "Drunk"
    recluse = "Recluse"
    saint = "Saint"
    poisoner = "Poisoner"
    scarletwoman = "Scarlet Woman"
    baron = "Baron"
    imp = "Imp"


class TroubleBrewing:
    """Parent class for all Trouble Brewing edition roles"""

    def __init__(self):
        self.gm_of_appearance = BOTCGamemode.tb
        self._gm_art_link = "http://bloodontheclocktower.com/wiki/images/9/92/TB_Logo.png"


# ---------- Townsfolk [Trouble Brewiding Edition] ----------

class Washerwoman(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Washerwoman learns that a particular Townsfolk character is in play, " \
                            "but not exactly which player it is."
        self._instr_string = "You start knowing 1 of 2 players is a particular Townsfolk."
        self._role_name = TBRole.washerwoman
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4d/Washerwoman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Washerwoman"


class Librarian(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Librarian learns that a particular Outsider character is in play, " \
                            "but not exactly which player it is."
        self._instr_string = "You start knowing that 1 of 2 players is a particular Outsider." \
                             "(Or that zero are in play)"
        self._role_name = TBRole.librarian
        self._art_link = "http://bloodontheclocktower.com/wiki/images/8/86/Librarian_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Librarian"


class Investigator(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Investigator learns that a particular Minion character is in play, " \
                            "but not exactly which player it is."
        self._instr_string = "You start knowing 1 of 2 players is a particular Minion."
        self._role_name = TBRole.investigator
        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ec/Investigator_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Investigator"


class Chef(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Chef knows if evil players are sitting next to each other."
        self._instr_string = "You start knowing how many pairs of evil players there are."
        self._role_name = TBRole.chef
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4c/Chef_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Chef"


class Empath(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Empath keeps learning if their living neighbors are good or evil."
        self._instr_string = "Each night, you learn how many of your 2 alive neighbors are evil."
        self._role_name = TBRole.empath
        self._art_link = "http://bloodontheclocktower.com/wiki/images/6/61/Empath_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Empath"


class FortuneTeller(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Fortune Teller detects who the Demon is, " \
                            "but sometimes thinks good players are Demons."
        self._instr_string = "Each night, choose 2 players: you learn if either is a Demon. " \
                             "There is 1 good player that registers falsely to you."
        self._role_name = TBRole.fortuneteller
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/3a/Fortune_Teller_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Fortune_Teller"


class Undertaker(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Undertaker learns which character was executed today."
        self._instr_string = "Each night, you learn which character died by execution today."
        self._role_name = TBRole.undertaker
        self._art_link = "http://bloodontheclocktower.com/wiki/images/f/fe/Undertaker_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Undertaker"


class Monk(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Monk protects other people from the Demon."
        self._instr_string = "Each night*, choose a player (not yourself): " \
                             "they are safe from the Demon tonight."
        self._role_name = TBRole.monk
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1b/Monk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Monk"


class Ravenkeeper(Townsfolk, BOTCRole, TroubleBrewing):
    
    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Ravenkeeper learns any player's character, but only if they die at night."
        self._instr_string = "If you die at night, you are woken to choose a player: " \
                             "you learn their character."
        self._role_name = TBRole.ravenkeeper
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/45/Ravenkeeper_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Ravenkeeper"


class Virgin(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Virgin is safe from execution... perhaps. " \
                            "In the process, they confirm which players are Townsfolk."
        self._instr_string = "The 1st time you are nominated, if the nominator is a Townsfolk, " \
                             "they are executed immediately."
        self._role_name = TBRole.virgin
        self._art_link = "http://bloodontheclocktower.com/wiki/images/5/5e/Virgin_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Virgin"


class Slayer(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Slayer can kill the Demon by guessing who it is."
        self._instr_string = "Once per game, during the day, publicly choose a player: " \
                             "if they are the Demon, they die."
        self._role_name = TBRole.slayer
        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2f/Slayer_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Slayer"


class Soldier(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Soldier can not be killed by the Demon."
        self._instr_string = "You are safe from the Demon."
        self._role_name = TBRole.soldier
        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9e/Soldier_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Soldier"


class Mayor(Townsfolk, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)
        self._desc_string = "The Mayor can win by peaceful means on the final day."
        self._instr_string = "If only 3 players live & no execution occurs, your team wins. " \
                             "If you die at night, another player might die instead."
        self._role_name = TBRole.mayor
        self._art_link = "http://bloodontheclocktower.com/wiki/images/c/c4/Mayor_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Mayor"


# ---------- Outsider [Trouble Brewiding Edition] ----------

class Butler(Outsider, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)
        self._desc_string = "The Butler may only vote when their Master (another player) votes."
        self._instr_string = "Each night, choose a player (not yourself): " \
                             "tomorrow, you may only vote if they are voting too."
        self._role_name = TBRole.butler
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1a/Butler_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Butler"


class Drunk(Outsider, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)
        self._desc_string = "The Drunk player thinks that they are a Townsfolk, " \
                            "and has no idea that they are actually the Drunk."
        self._instr_string = "You do not know you are the Drunk. " \
                             "You think you are a Townsfolk, but your ability malfunctions."
        self._role_name = TBRole.drunk
        self._art_link = "http://bloodontheclocktower.com/wiki/images/0/03/Drunk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Drunk"


class Recluse(Outsider, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)
        self._desc_string = "The Recluse might appear to be an evil character, but is actually good."
        self._instr_string = "You might register as evil & as a Minion or Demon, even if dead."
        self._role_name = TBRole.recluse
        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/bb/Recluse_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Recluse"


class Saint(Outsider, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)
        self._desc_string = "The Saint ends the game if they are executed."
        self._instr_string = "If you die by execution, your team loses."
        self._role_name = TBRole.saint
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/77/Saint_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Saint"


# ---------- Minion [Trouble Brewiding Edition] ----------

class Poisoner(Minion, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)
        self._desc_string = "The Poisoner secretly disrupts character abilities."
        self._instr_string = "Each night, choose a player: their ability malfunctions " \
                             "tonight and tomorrow day."
        self._role_name = TBRole.poisoner
        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/af/Poisoner_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Poisoner"


class ScarletWoman(Minion, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)
        self._desc_string = "The Scarlet Woman becomes the Demon when the Demon dies."
        self._instr_string = "If there are 5 or more players alive & the Demon dies, you become the Demon."
        self._role_name = TBRole.scarletwoman
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/7c/Scarlet_Woman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Scarlet_Woman"


class Baron(Minion, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)
        self._desc_string = "The Baron changes the number of Outsiders present in the game."
        self._instr_string = "There are extra Outsiders in play. [+2 Outsiders]"
        self._role_name = TBRole.baron
        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/ba/Baron_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Baron"
    
    def exec_init_setup(self, townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list):
        random.shuffle(townsfolk_obj_list)
        townsfolk_obj_list.pop()
        townsfolk_obj_list.pop()
        tb_outsider_all = [role_obj() for role_obj in Outsider.__subclasses__()]
        random.shuffle(tb_outsider_all)
        count = 0
        for outsider in tb_outsider_all:
            if count >= 2:
                break
            else:
                if str(outsider) not in [str(role) for role in outsider_obj_list]:
                    outsider_obj_list.append(outsider)
                    count += 1
        return [townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list]


# ---------- Demon [Trouble Brewiding Edition] ----------

class Imp(Demon, BOTCRole, TroubleBrewing):

    def __init__(self):
        BOTCRole.__init__(self)
        TroubleBrewing.__init__(self)
        Demon.__init__(self)
        self._desc_string = "The Imp kills a player each night, and can make copies of itself... " \
                            "for a terrible price."
        self._instr_string = "Each night*, choose a player: they die. " \
                             "If you kill yourself this way, a Minion becomes the Imp."
        self._role_name = TBRole.imp
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/42/Imp_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Imp"


# ---------- Others [Trouble Brewing Edition] ----------

tb_roles_list = [role() for role in Townsfolk.__subclasses__() + 
                                    Outsider.__subclasses__() + 
                                    Minion.__subclasses__() + 
                                    Demon.__subclasses__()]

# {role name : [team, plural, description]}
tb_roles_dict = {str(role).lower(): [role.get_category().value, str(role), 
                             role.get_role_desc() + " " + role.get_role_player_instr()] for role in tb_roles_list}




a = BOTCGameObject(BOTCGamemode.tb, ["1", "2", "3", "4", "5", "6", "7"])

