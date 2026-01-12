#!/usr/bin/env python3
"""Calculate answers for Questions 1-3."""

from collections import namedtuple
import pickle

State = namedtuple(
    'State',
    [
        'name',
        'area_sq_mi',
        'land_area_sq_mi',
        'water_area_sq_mi',
        'population',
        'n_rep_votes',
        'n_senate_votes',
        'n_ec_votes',
    ],
)

CACounty = namedtuple(
    'CACounty', ['name', 'county_seat', 'population', 'area_sq_mi']
)

# Load data
with open('ca_county.pckl', 'rb') as f:
    ca_counties = pickle.load(f)

with open('us_state.pckl', 'rb') as f:
    states = pickle.load(f)

# Filter to 50 US states only (exclude DC and territories)
us_states = [s for s in states if s.n_ec_votes > 0 and s.name != 'District of Columbia']

# QUESTION 1
ca_sorted_by_pop = sorted(ca_counties, key=lambda x: x.population, reverse=True)
sum_3_4_5 = ca_sorted_by_pop[2].population + ca_sorted_by_pop[3].population + ca_sorted_by_pop[4].population
answer_1 = sum(1 for s in us_states if s.population < sum_3_4_5)

print(f"Question 1: {answer_1}")

# QUESTION 2
largest_county = max(ca_counties, key=lambda x: x.area_sq_mi)
answer_2 = sum(1 for s in us_states if s.land_area_sq_mi <= largest_county.area_sq_mi)

print(f"Question 2: {answer_2}")

# QUESTION 3
california = [s for s in states if s.name == 'California'][0]
us_states_no_ca = [s for s in us_states if s.name != 'California']
states_sorted = sorted(us_states_no_ca, key=lambda x: x.population)

min_pop = 37_956_694
max_pop = 41_119_752

cumulative = 0
for i, state in enumerate(states_sorted):
    cumulative += state.population
    if min_pop <= cumulative <= max_pop:
        ec_sum = sum(s.n_ec_votes for s in states_sorted[:i+1])
        answer_3 = ec_sum - california.n_ec_votes
        break

print(f"Question 3: {answer_3}")
