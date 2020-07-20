import neat
import pickle
import pygame as pg
from config import AIConfig
from game import Game
from setuppygame import init_pygame, quit_pygame


class AIDriver:
    def __init__(self, net):
        self.net = net
        self.fitness = 0
    def drive(self, car, player_events):
        gas, turn = self.net.activate(car.radar_lengths)
        gas = (gas + 1) * 0.5
        turn = (turn + 1) * 0.5
        car.drive(gas, turn)

        if car.alive:
            self.fitness += gas - abs(turn-0.5)

        if self.fitness < -10:
            car.alive = False


class AIDriverManager:
    def __init__(self, config_file):
        self.config = neat.config.Config(
            neat.DefaultGenome, 
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet, 
            neat.DefaultStagnation,
            config_file
        )

        self.p = neat.Population(self.config)

        # stdout reporter
        self.p.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.p.add_reporter(self.stats)

    def status(self):
        return 'Population size: {pop_size}\nGenration: {generation}\nAlive: {alive}\nBest fitness: {fitness:.2f}'.format(
                    pop_size=self.p.config.pop_size,
                    generation=self.p.generation,
                    alive=self.game.cars_alive,
                    fitness=self.p.best_genome.fitness if self.p.best_genome is not None else 0
                )

    def eval_genome(self, genomes_numerated, config):
        drivers = []

        for num, genome in genomes_numerated:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            drivers.append(AIDriver(net))

        self.game = Game(self.window, drivers, self.status)
        self.game.start(max_time=600)

        for driver, t in zip(drivers, genomes_numerated):
            num, genome = t
            genome.fitness = driver.fitness


    def study(self, generation_number):
        self.window = init_pygame()
        self.winner = self.p.run(self.eval_genome, generation_number)
        quit_pygame()
        return self.winner


def train_ai():
    ai_driver_manager = AIDriverManager('neat-config.txt')
    ai_driver_manager.study(50)

    print('xxxxxxxxx')
    if AIConfig.save_best_net:
        best_net = neat.nn.FeedForwardNetwork.create(
            ai_driver_manager.winner, 
            ai_driver_manager.config
        )

        with open(AIConfig.best_net_path, 'wb') as f:
            print('saving net')
            pickle.dump(best_net, f)


def load_net(filename):
    with open(filename, 'rb') as f:
        net = pickle.load(f)
        return net
    return None

def run_ai(filenames):
    drivers = []
    for filename in filenames:
        net = load_net(filename)
        if net is not None:
            drivers.append(AIDriver(net))

    window = init_pygame()
    game = Game(window, drivers)
    game.start()
    quit_pygame()


def run_best_ai():
    run_ai([AIConfig.best_net_path])

if __name__ == '__main__':
    #train_ai()
    run_best_ai()
