""" Class determine theta_k using any algorithm printing python """
from abc import ABC, abstractmethod
import math
import numpy as np

class Algorithm(ABC):
    """ Algorithm super class """
    def __init__(self, tones: int, theta_k_values=None) -> None:
        self.tones: int = tones
        if theta_k_values is not None:
            self.theta_k_values = theta_k_values

    @abstractmethod
    def calc(self) -> tuple[float]:
        """ calc theta_k abstract method """

class All0(Algorithm):
    """ All 0 Algorithm """
    def calc(self) -> tuple[float]:
        theta_k_values: tuple[float] = tuple(np.zeros(self.tones).tolist())
        return theta_k_values

class Narahashi(Algorithm):
    """ Narahashi Algorithm """
    def calc(self) -> tuple[float]:
        indexes: np.ndarray = np.arange(self.tones)
        theta_k_values: tuple[float] = tuple((((indexes) * (indexes - 1) * math.pi) / (self.tones - 1)).tolist())
        return theta_k_values

class Newman(Algorithm):
    """ Newman Algorithm """
    def calc(self) -> tuple[float]:
        indexes: np.ndarray = np.arange(self.tones)
        theta_k_values: tuple[float] = tuple((((indexes - 1)**2 * math.pi) / (self.tones)).tolist())
        return theta_k_values

class Frank(Algorithm):
    """ Frank Algorithm """
    def calc(self) -> tuple[float]:
        m = np.sqrt(self.tones)
        j_indices, i_indices = np.meshgrid(np.arange(m), np.arange(m))
        theta_k_matrix = (2 * np.pi * (i_indices-1) * (j_indices-1)) / m
        theta_k_values = theta_k_matrix.flatten()
        return theta_k_values

class Random(Algorithm):
    """ Random theta_k_values """
    def calc(self) -> tuple[float]:
        randarr = np.random.rand(self.tones)
        theta_k_values: tuple[float] = tuple(2*np.pi*randarr)
        return theta_k_values

class Manual(Algorithm):
    """ Manual theta_k_values """
    def calc(self) -> tuple[float]:
        return self.theta_k_values

class ManualPi(Algorithm):
    """ Manual theta_k_values """
    def calc(self) -> tuple[float]:
        theta_k_values = np.array(self.theta_k_values)*2*np.pi
        return tuple(theta_k_values)

class AContext:
    """ Algorithm Context """
    def __init__(self, strategy: Algorithm) -> None:
        self._strategy = strategy
        self.theta_k_values: tuple[float] = None

    def calc_algo(self) -> tuple[float]:
        """ Calculation each algorithm """
        if self.theta_k_values is None:
            self.theta_k_values = self._strategy.calc()
        return self.theta_k_values

    def display(self) -> tuple[str]:
        """ Output algorithm process to cli """
        if self.theta_k_values is None:
            self.theta_k_values = self._strategy.calc()
        txt: tuple[str] = tuple(f'theta_k_values[{i}] is {value}' for i, value in enumerate(self.theta_k_values))
        for i, value in enumerate(txt):
            print(value)
        return txt
