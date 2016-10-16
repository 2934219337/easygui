

try:
    from . import utils as ut
except (SystemError, ValueError, ImportError):
    import utils as ut

import collections


class Choices(object):
    def __init__(self, input_choices, default_choice, cancel_choice):
        """
        User can enter choices as a single string, a list of strings and a dictionary
        Here we transform them all into a dicrionary
        """
        dict_choices = self.input_choices_to_dict(input_choices)
        dict_choices['No choice'] = None
        self.choices = self.dict_2_abstract_data_class(dict_choices)
        unique_choices = ut.uniquify_list_of_strings(self.choices.keys())

        for uc, choice in zip(unique_choices, self.choices.values()):
            choice.unique_text = uc

        if default_choice in self.choices:
            self.default_choice =self.choices[default_choice]

        if cancel_choice:
            if cancel_choice in self.choices:
                self.choices[cancel_choice].is_cancel = True
            else:
                err_msg = "Cancel choice <{}> is not part of choices".format(cancel_choice)
                raise ValueError(err_msg)

        self.selected_choice = self.choices['No choice']

    def unselect_choice(self):
        self.selected_choice = self.choices['No choice']

    def select_choice_from_hotkey(self, hotkey):
        success = False
        for choice in self.choices.values():
            if choice.hotkey == hotkey:
                self.selected_choice = choice
                success = True
        return success


    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.
    def input_choices_to_dict(self, choices):
        if isinstance(choices, collections.Mapping):  # If it is dictionary-like
            choices_dict = choices
        else:
            try:
                # Try to convert to OrderedDict, it will succeed if it is a list of lists or list or tuples...
                # http://stackoverflow.com/questions/25480089/initializing-an-ordereddict-using-its-constructor
                choices_dict = collections.OrderedDict(choices)
            except:
                # Convert into a dictionary of equal key and values
                choices_list = list(choices)
                choices_dict = collections.OrderedDict()
                for choice in choices_list:
                    choices_dict[choice] = choice
        return choices_dict

    def dict_2_abstract_data_class(self, choices_dict):
        choices = collections.OrderedDict()
        for text, result in choices_dict.items():
            choices[text] = Choice(text, result)
        return choices

    def __repr__(self):
        return repr(self.choices)

class Choice(object):
    def __init__(self, text, result):
        self.original_text = text
        self.result = result
        self.clean_text, self.hotkey, self.hotkey_position = ut.parse_hotkey(self.original_text)
        self.default = False
        self.is_cancel = False