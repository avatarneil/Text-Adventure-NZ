"""
Text Based Adventure Game Engine (tbag.py)
A set of classes and methods for creating
player-driven text-based experiences.
"""

import sys
import numpy


class Lang():
    """ Language class that has methods for nice output. """

    @classmethod
    def a(cls, thing):
        """ Returns 'an' if thing starts with a vowel,
        otherwise returns 'a'. """

        return 'an ' + thing if thing[0] in ['a', 'e', 'i', 'o', 'u'] else 'a ' + thing

    @classmethod
    def A(cls, thing):
        """ Returns 'An' if thing starts with a vowel,
        otherwise returns 'A'. """

        return Lang.a(thing).capitalize()

    @classmethod
    def gender(cls, living):
        """ Returns 'Male', 'Female', or an empty string
        depending on the given Living's gender (m/f/x/n). """

        return {'m': 'male', 'f': 'female', 'x': '', 'n': ''}[living.gender]

    @classmethod
    def pronoun(cls, living):
        """ Returns 'he', 'she', 'they', or 'it' depending
        on the given Living's gender (m/f/x/n). """

        return {'m': 'he', 'f': 'she', 'x': 'they', 'n': 'it'}[living.gender]

    @classmethod
    def inputParser(cls, inputData):
        """ Takes inputs and parses into a more convenient datatype """

        if type(inputData) == str:  # if inputData is a string case
            firstWord = inputData.partition(' ')[0]
        else:
            try:
                inputData = str(inputData)
                firstWord = inputData.partition(' ')[0]
            except AttributeError:
                return "Input is not parsable as a string"


class StdObject():
    """ Base object from which all other objects derive from.
    Should never be used directly. """

    def __init__(self, name, longDesc="", shortDesc=""):
        self.name = name
        self.longDesc = longDesc
        self.shortDesc = shortDesc

    def __str__(self):
        return "a StdObject called '{0}'".format(self.name)

    def __repr__(self):
        return "StdObject\nName: {0}\nlongDesc: {1}\nshortDesc: {2}"\
               "\n".format(self.name, self.longDesc, self.shortDesc)


class Living(StdObject):
    """ Base class for all living things.
    Should never be used directly, only derived from. """

    def __init__(self, name, longDesc="", shortDesc="",
                 gender="x", race="human"):
        super().__init__(name, longDesc, shortDesc)
        self.gender = gender
        self.race = race
        self.inventory = Container("{0}'s Inventory".format(self.name))

    def __str__(self):
        return "a {0} {1} Living named '{2}'".format(Lang.gender(self), self.race, self.name)

    def __repr__(self):
        return "Living\nName: {0}\nlongDesc: {1}\nshortDesc: {2}\ngender: {3}\nrace: {4}".format(
            self.name, self.longDesc, self.shortDesc, self.gender, self.race)

    def give_item(self, item):
        """ Inserts the given item into this Living's inventory. """

        self.inventory.insert(item)

    def has_item(self, item) -> bool:
        """ Returns whether or not the Living currently has
        the specified item (true/false). """

        return self.inventory.has_item(item)


class Player(Living):
    """ Controls the Player and handles interaction. """

    def __init__(self, name, longDesc="", shortDesc="",
                 gender="x", race="human"):
        super().__init__(name, longDesc, shortDesc, gender, race)

    def __str__(self):
        return "a {0} {1} Player named '{2}'".format(Lang.gender(self), self.race, self.name)

    def __repr__(self):
        return "Player\nName: {0}\nlongDesc: {1}\nshortDesc: {2}\ngender: {3}\nrace: {4}".format(
            self.name, self.longDesc, self.shortDesc, self.gender, self.race)


class Item(StdObject):
    """ Generic base class for interactible items. """

    def __init__(self, name, longDesc="", shortDesc="", value=0):
        super().__init__(name, longDesc, shortDesc)
        value = value

    def __str__(self):
        return "an Item called '{0}'".format(self.name)

    def __repr__(self):
        return "Item\nName: {0}\nlongDesc: {1}\nshortDesc: {2}"\
            "\n".format(self.name, self.longDesc, self.shortDesc)


class Container(Item):
    """ Game object that is used to store other objects. """

    def __init__(self, name, longDesc="", shortDesc=""):
        super().__init__(name, longDesc, shortDesc)
        self.inventory = []

    def __str__(self):
        return "a Container called '{0}'".format(self.name)

    def __repr__(self):
        return "Container\nName: {0}\nlongDesc: {1}\nshortDesc: {2}"\
               "\n".format(self.name, self.longDesc, self.shortDesc)

    def show_contents(self):
        """ Prints the name of the container followed by
        its contents, each in a new line. """

        print("Contents of {0}:".format(self.name))
        for item in self.inventory:
            print(item)

    def insert(self, item):
        """ Inserts the given item into the Container's inventory """

        self.inventory.append(item)

    def has_item(self, item) -> bool:
        """ Returns whether or not the Container currently contains
        the specified item. """

        return item in self.inventory

    def transfer_to(self, other, item):
        """ Transfers an item from this Container's inventory to another's. """

        if not self.has_item(item):
            return
        other.give_item(self.inventory.pop(item))


class Location(StdObject):
    """ Handles the contents of a certain game location. """

    def __init__(self, name, longDesc, shortDesc):
        super().__init__(self, name, longDesc, shortDesc)
        self.inventory = Container(
            "Contents of Location '{0}'".format(self.name))


class Exit(Item):
    """ Handles moving the Player from one Location to another. """

    def __init__(self, name, longDesc, shortDesc):
        super().__init__(self, name, longDesc, shortDesc)
        self.destination = None
