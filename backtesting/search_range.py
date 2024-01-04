from backtesting.searcher.range_searcher import RangeSearcher
from backtesting.simulator.simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator(RangeSearcher)
    simulator.run()