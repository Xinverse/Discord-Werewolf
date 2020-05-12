import enum
import discord

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
        for i in role_obj_list:
            if role_name_str.lower() == str(i).lower():
                return i


class BOTCGameObject:

    class Phase(enum.Enum):
        day = "day"
        night = "night"
        not_in_game = None
    
    def __init__(self):
        self._phase = BOTCGameObject.Phase.not_in_game
    
    def clear(self):
        self.__init__()


class BOTCPlayer:

    def __init__(self, userid_str, role_obj):
        self._userid = userid_str
        self._role = role_obj 
    
