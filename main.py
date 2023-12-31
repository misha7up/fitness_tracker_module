from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
              'Определите get_spent_calories в %s.' % (self.__class__.__name__)
              )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий, если активность – Бег."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / super().M_IN_KM
                * (self.duration
                * super().MIN_IN_HR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER: float = 0.035
    SPEED_HEIGHT_SQUARE: float = 0.029
    KMH_TO_MS_CONST: float = 0.278
    CM_TO_M_CONST: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий,
        если активность – спортивная ходьба."""
        return ((self.WEIGHT_MULTIPLIER * self.weight
                + (super().get_mean_speed() * self.KMH_TO_MS_CONST) ** 2
                / (self.height / self.CM_TO_M_CONST)
                * self.SPEED_HEIGHT_SQUARE * self.weight)
                * (self.duration * super().MIN_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_OFFSET: float = 1.1
    SPEED_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (self.length_pool * self.count_pool
                / super().M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий,
        если активность – плавание."""
        return ((self.get_mean_speed()
                + self.SPEED_OFFSET) * self.SPEED_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: dict[str, type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking}
    if workout_type in workouts:
        return workouts[workout_type](*data)
    raise KeyError(f'Тип тренировки "{workout_type}" не найден!')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
