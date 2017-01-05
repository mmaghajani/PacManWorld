class Person:
    population = 0

    def __init__(self, age):
        self.age = age
        Person.population += 1

    def get_age(self):
        return self.age

    @staticmethod
    def get_population():
        return Person.population
