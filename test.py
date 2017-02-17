import Emulator_Classes as ec
import Emulator_Classes_2 as ec2
reload(ec)
reload(ec2)
import random
import numpy as np

date_range = (2, 1, 1, 8)  # providers, weeks, days, slots

patients = ec2.generate_patients(20, 60, 20, date_range)

s = ec.Schedule()
s.initialize(date_range[0], date_range[1], date_range[2], date_range[3])
availabilities = [(0, 0, 0, list(range(8))), (1, 0, 0, list(range(8)))]  # Both providers, week 1, day 1, all slots

for availability in availabilities:
    s.set_open_slots(availability, start=1, max_p=2)  # Start = Can we start an app? max_p = max p per physician


t = ec.TestAlgorithm()
t.input(s)

for patient in patients:
    t.schedule(patient)

p = ec2.PostProcessor(t)
overtime = p.overtime()