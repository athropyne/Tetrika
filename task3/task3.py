def appearance(intervals: dict[str, list[int]]) -> int:
    case = intervals
    min_time = min(case["lesson"][0], case["pupil"][0], case["tutor"][0])
    max_time = max(case["lesson"][-1], case["pupil"][-1], case["tutor"][-1])
    lesson_times = {
        time: True
        for time
        in range(case["lesson"][0] + 1, case["lesson"][-1] + 1)
    }

    def person_activity_map(timestamps: list[int]) -> dict[int, bool]:
        return {
            second: True  # секунда в которую персонаж был онлайн
            for entry_timestamp  # запись времени входа
            in range(0, len(timestamps), 2)  # идем только по входам
            for second
            in range(
                timestamps[entry_timestamp] + 1,  # не включаем нулевую секунду времени входа
                timestamps[entry_timestamp + 1] + 1  # включаем последнюю секунду времени выхода
            )
        }

    common_times = {
        time: True  # помечаем секунду в которой на уроке были и ученик и учитель если:
        if all(
            (
                lesson_times.get(time),  # урок уже идет
                person_activity_map(case["pupil"]).get(time),  # ученик в сети
                person_activity_map(case["tutor"]).get(time)  # учитель в сети
            )
        )
        else False  # если кого то не было или урок не начался/закончился
        for time
        in range(min_time, max_time + 1)
    }
    common_times = list(filter(
        lambda x: common_times[x],
        common_times)
    )  # оставляем только секунды в которых и учитель и ученик были на уроке
    return len(common_times)  # вот столько времени всего оба были на уроке одновременно


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
