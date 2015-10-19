import sys

class Person:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.next_unasked_index = 0
        self.partner = None

    @property
    def preferences(self):
        return self.preferences

    @property
    def name(self):
        return self.name

    def is_free(self):
        return self.partner is None

    def clear_partner(self):
        self.partner = None

    @preferences.setter
    def partner(self, value):
        self.partner = value

    def get_next_unasked(self):
        next_unasked = self.preferences[self.next_unasked_index]
        self.next_unasked_index += 1
        return next_unasked

    def prefers(self, person):
        if self.partner is None:
            return True

        return self.preferences.index(person) < \
            self.preferences.index(self.partner)


def gale_shaplin(men, women):
    men = [Person(name, preferences) for name, preferences in men.items()]
    women = [Person(name, preferences) for name, preferences in women.items()]

    every_man_taken = False
    while not every_man_taken:
        print_pairs(men, women)

        free_men = sorted((man for man in men if man.is_free()),
                          key=lambda x: x.name)

        man_to_match = next(iter(free_men))
        name_preferred_woman = man_to_match.get_next_unasked()
        woman = get_person_with_name(women, name_preferred_woman)
        if woman.prefers(man_to_match.name):
            if not woman.is_free():
                partner = get_person_with_name(men, woman.partner)
                partner.clear_partner()
                free_men.append(partner)

            man_to_match.partner = woman.name
            woman.partner = man_to_match.name
            print('\nAssigned woman {} to man {}'.format(
                woman.name, man_to_match.name))
            free_men.remove(man_to_match)

        print('\n')
        every_man_taken = len(free_men) == 0


def get_person_with_name(persons, name):
    return next(iter([pers for pers in persons if pers.name == name]))


def print_pairs(men, women):
    matched_men = [man for man in men if not man.is_free()]
    sys.stdout.write('Current pairs are: ')

    if not matched_men:
        print('None')
        return
    for pers in matched_men:
        partner = get_person_with_name(women, pers.partner)
        sys.stdout.write('{{{0} {1}}} '.format(man.name, partner.name))


def main():
    men = {
        'm1': ['f1', 'f2', 'f3', 'f4', 'f5'],
        'm2': ['f2', 'f3', 'f4', 'f1', 'f5'],
        'm3': ['f3', 'f4', 'f1', 'f2', 'f5'],
        'm4': ['f4', 'f1', 'f2', 'f3', 'f5'],
        'm5': ['f1', 'f2', 'f3', 'f4', 'f5']}

    women = {
        'f1': ['m2', 'm3', 'm4', 'm5', 'm1'],
        'f2': ['m3', 'm4', 'm5', 'm1', 'm2'],
        'f3': ['m4', 'm5', 'm1', 'm2', 'm3'],
        'f4': ['m5', 'm1', 'm2', 'm3', 'm4'],
        'f5': ['m1', 'm2', 'm3', 'm4', 'm5']}

    gale_shaplin(men, women)

if __name__ == "__main__":
    main()
