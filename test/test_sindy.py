import sys
import os
import pytest
import numpy as np

from scipy.integrate import odeint
from sklearn.exceptions import NotFittedError

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from sindy import SINDy


@pytest.fixture
def data_lorenz():

    def lorenz(z, t):
        return [
            10*(z[1] - z[0]),
            z[0]*(28 - z[2]) - z[1],
            z[0]*z[1] - 8/3*z[2]
        ]

    t = np.linspace(0, 5, 100)
    x0 = [8, 27, -7]
    x = odeint(lorenz, x0, t)

    return x, t


@pytest.fixture
def data_1d():
    t = np.linspace(0, 5, 100)
    x = 2 * t.reshape(-1, 1)
    return x, t


def test_get_feature_names_len(data_lorenz):
    x, t = data_lorenz

    model = SINDy()
    model.fit(x, t)

    # Assumes default library is polynomial features of degree 2
    assert len(model.get_feature_names()) == 10


def test_predict_not_fitted(data_1d):
    x, t = data_1d
    model = SINDy()
    with pytest.raises(NotFittedError):
        model.predict(x)


def test_coefficient_not_fitted():
    model = SINDy()
    with pytest.raises(NotFittedError):
        model.coefficients()


def test_equation_not_fitted():
    model = SINDy()
    with pytest.raises(NotFittedError):
        model.equations()


def test_predict_bad_input(data_1d):
    x, t = data_1d
    model = SINDy()
    model.fit(x, t)
    with pytest.raises(ValueError):
        model.predict(x.flatten())