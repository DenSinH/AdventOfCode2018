import copy
import time

t0 = time.time()

# lists containing groups
# first is immune system, second is infection
groups = [[], []]


class Group(object):

    def __init__(self, no_units, hp, immune, weak, atk, atk_typ, initiative, typ, id):
        self.no_units = no_units
        self.hp = hp
        self.immune = immune
        self.weak = weak
        self.atk = atk
        self.atk_typ = atk_typ
        self.initiative = initiative
        self.typ = typ  # immune system or infection
        self.id = id  # id for keeping track

        self.alive = True

        self.target_i = -1  # target of the other group, none chosen is -1

    def effective_power(self):
        # returns groups effective power
        return self.no_units * self.atk

    def target_selection(self):
        # can only select target if we are alive
        if not self.alive:
            return

        # keeping track of the maximum damage we can deal so far
        max_dmg_dealt = 0
        for i in xrange(len(groups[1 - self.typ])):
            # can only target alive groups
            if not groups[1 - self.typ][i].alive:
                continue

            # can only target groups that aren't targeted yet
            if i in [g.target_i for g in groups[self.typ]]:
                continue

            # can only target groups we can deal damage to
            if self.atk_typ in groups[1 - self.typ][i].immune:
                continue
            else:
                # damage dealt to this group
                dmg_dealt = self.effective_power()
                if self.atk_typ in groups[1 - self.typ][i].weak:
                    dmg_dealt *= 2

            # checking if it is the first one we find we can target, or if it is the highest one so far
            if self.target_i < 0:
                self.target_i = int(i)
                max_dmg_dealt = int(dmg_dealt)
            elif dmg_dealt == max_dmg_dealt:
                diff = groups[1 - self.typ][i].effective_power() - groups[1 - self.typ][self.target_i].effective_power()
                if diff > 0:
                    self.target_i = int(i)
                elif diff == 0:
                    if groups[1 - self.typ][i].initiative > groups[1 - self.typ][self.target_i].initiative:
                        self.target_i = int(i)
            elif dmg_dealt > max_dmg_dealt:
                self.target_i = int(i)
                max_dmg_dealt = int(dmg_dealt)

    def get_hit(self, dmg, typ, report=False):
        # get hit with a certain amount of damage from a certain type
        assert self.alive, "Something went wrong: only alive units can get hit"
        if typ in self.weak:
            dmg *= 2
        self.no_units -= dmg // self.hp

        # check if group is alive
        if self.no_units <= 0:
            self.alive = False

        # report the damage done
        if report:
            print dmg, "to", ["Immune", "Infection"][self.typ], self.id + 1, "killing", dmg // self.hp, \
                  "units", "immune to", self.immune, "weak to", self.weak

        return dmg // self.hp > 0

    def attack(self, report=False):
        # only attack if we are alive and have a target
        if not self.alive:
            self.target_i = -1
            return False
        elif self.target_i < 0:
            return False

        # report if desired
        elif report:
            print ["Immune", "Infection"][self.typ], self.id + 1, "deals",

        # resetting target
        to_return = groups[1 - self.typ][self.target_i].get_hit(int(self.effective_power()), self.atk_typ, report=report)
        self.target_i = -1
        return to_return


with open("input.txt", "r") as f:
    current_type = -1  # 0: immune system, 1: infection
    for line in f.readlines():
        if line == "\n":  # skip empty lines
            continue
        elif ":\n" in line:  # if line ends with a colon, we go to the next army
            current_type += 1
        else:
            # find all stats in the line
            split = line.split()
            stats = [immune, weak] = [[], []]
            mode = -1
            for word in split:
                if "immune" in word:
                    mode = 0
                elif "weak" in word:
                    mode = 1
                elif mode >= 0 and word != "to":
                    stats[mode].append(word.replace(",", "").replace(")", "").replace(";", ""))
                    if ")" in word:
                        mode = -1

            no_units = int(split[0])
            hp = int(split[4])
            atk = int(split[-6])
            atk_typ = split[-5]
            initiative = int(split[-1])

            # add a group
            groups[current_type].append(Group(no_units, hp, immune, weak, atk, atk_typ,
                                              initiative, current_type, len(groups[current_type])))

# check group parameters
"""
for i in xrange(2):
    print ""
    for g in groups[i]:
        print g.no_units, g.hp, g.atk, g.atk_typ, g.weak, g.immune, g.initiative
"""

# copy of the groups we started with
start_groups = copy.deepcopy(groups)
boost = 0

# I tried to speed up the process by changing the step in which the boost goes up/down
# it didn't really work though, as there were a lot of scenarios with ties
for step in [100, -10, 1]:
    end_condition = True
    while end_condition:
        # reset the groups
        groups = copy.deepcopy(start_groups)

        # add boost
        for g in groups[0]:
            g.atk += boost

        # keep going until only one army is left
        while any([g.alive for g in groups[0]]) and any([g.alive for g in groups[1]]):

            # target selection
            for typ in xrange(2):
                for g in sorted(groups[typ], key=lambda g: (g.effective_power(), g.initiative), reverse=True):
                    g.target_selection()

            # attacking, checking if any units are killed
            # if no units are killed, we have reached an equilibrium situation, and must break as there is a tie
            u_killed = False
            for g in sorted(groups[0] + groups[1], key=lambda g: g.initiative, reverse=True):
                if g.attack():
                    u_killed = True

            if not u_killed:
                # tie, so we need to break
                break

        else:
            # if some army has won, report part 1 and 2 (if immune system won)
            if not boost:
                for i in xrange(2):
                    if any([g.alive for g in groups[i]]):
                        print "PART 1:", sum([g.no_units for g in groups[i] if g.no_units > 0])

            if any([g.alive for g in groups[0 if step > 0 else 1]]):
                if step == 1:
                    print "@ boost:", boost
                    print "PART 2:", sum([g.no_units for g in groups[0] if g.no_units > 0])
                break

        boost += step

print time.time() - t0
