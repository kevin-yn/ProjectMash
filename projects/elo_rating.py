import math

def prob_winning(rating1, rating2) :
    prob = 1 / (1 + math.pow(10, (rating2 - rating1)/400))
    return prob

def elo_rating(rating1, rating2, k, actual) :
    # get winning probablities for project1 and project2
    prob_1 = prob_winning(rating1, rating2)
    prob_2 = prob_winning(rating2, rating1)

    # update ratings
    new_rating1 = rating1 + k * (actual - prob_1)
    new_rating2 = rating2 + k * ((1-actual) - prob_2)

    return (new_rating1, new_rating2)
