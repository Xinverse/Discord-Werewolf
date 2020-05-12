import enum
import discord
import random
import bot
import botc_troublebrewing
import datetime

MIN_PLAYERS = 5
MAX_PLAYERS = 15

random.seed(datetime.datetime.now())

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


# ============================== Utility functions ======================
# -----------------------------------------------------------------------

class BOTCUtils:

    @staticmethod
    def find_role_by_name(role_name_str, role_obj_list):
        for role in role_obj_list:
            if role_name_str.lower() == str(role).lower():
                return role


class BOTCGameObject:

    class Phase(enum.Enum):
        day = "day"
        night = "night"
        idle = "idle"
    
    class IncorrectNumberPlayers(Exception):
        pass

    class NotBOTCGame(Exception):
        pass

    def distribute_roles(self, role_obj_list, player_id_list):
        pass
    
    def generate_role_set(self, num_player):
        if num_player > MAX_PLAYERS or num_player < MIN_PLAYERS:
            raise BOTCGameObject.IncorrectNumberPlayers("Must be between 5 and 15 players.")
        else:
            role_guide_chart_temp = bot.gamemodes[self._gamemode.value.lower()]["improved_guide"]
            role_guide_chart = role_guide_chart_temp[str(num_player)]
            nb_townsfolk = role_guide_chart[0]
            nb_outsider = role_guide_chart[1]
            nb_minion = role_guide_chart[2]
            nb_demon = role_guide_chart[3]
            # Trouble brewing mode
            if self.gamemode == BOTCGamemode.tb:

                tb_townsfolk_all = [role_obj() for role_obj in botc_troublebrewing.Townsfolk.__subclasses__()]
                tb_outsider_all = [role_obj() for role_obj in botc_troublebrewing.Outsider.__subclasses__()]
                tb_minion_all = [role_obj() for role_obj in botc_troublebrewing.Minion.__subclasses__()]
                tb_demon_all = [role_obj() for role_obj in botc_troublebrewing.Demon.__subclasses__()]

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
            
                self.distribute_roles(setup, self.player_id_list)

            # Bad moon rising mode
            elif self.gamemode == BOTCGamemode.bmr:
                pass
            # Sects and violets mode
            elif self.gamemode == BOTCGamemode.sv:
                pass
            else:
                raise BOTCGameObject.NotBOTCGame("Gamemode is not one of BoTC editions.")
    
    def __init__(self, gamemode, player_id_list):
        if gamemode not in BOTCGamemode:
            raise BOTCGameObject.NotBOTCGame("Gamemode is not one of BoTC editions.")
        self._phase = BOTCGameObject.Phase.idle
        self._gamemode = gamemode  # enum.Enum object here
        self._player_id_list = player_id_list  # list object
        self._player_obj_list = []  # list object
        self.generate_role_set(len(self._player_id_list))
    
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

    
