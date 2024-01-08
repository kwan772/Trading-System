from backtesting.searcher import RangeSearcher, MaBreakout, Gaps
from backtesting.simulator.simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator(Gaps)
    simulator.run()