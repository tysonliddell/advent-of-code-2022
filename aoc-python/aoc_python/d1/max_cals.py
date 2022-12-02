from typing import List


def total_cal_reader(calorie_list: List[int]):
    sum_ = 0
    for cal in calorie_list:
        if cal is None:
            yield sum_
            sum_ = 0
        else:
            sum_ += cal


def get_most_cals(calorie_list: List[int]):
    return max(total_cal_reader(calorie_list))


def get_top_three_cals(calorie_list: List[int]):
    top_three = sorted(list(total_cal_reader(calorie_list)))[-3:]
    return sum(top_three)
