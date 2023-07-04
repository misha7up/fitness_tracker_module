class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, [duration, distance, speed, calories]):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {str(self.training_type)}; '
                f'Длительность: {str(self.duration)} ч.; '
                f'Дистанция: {str(self.distance)} км; '
                f'Ср. скорость: {str(self.speed)} км/ч; ' # :.3f
                f'Потрачено ккал: {str(self.calories)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self, action: int = None, duration: float = None) -> float:
        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.action, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return message.get_message()


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / super().M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: int):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        return (((0.035 * self.height + (super().get_mean_speed()**2 / self.height) * 0.029 * self.weight) * self.duration))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self, action: int = None, duration: float = None) -> float:
        return self.length_pool * self.count_pool / super().M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed(self.action, self.duration) + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training
    print(info.show_training_info())



if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
