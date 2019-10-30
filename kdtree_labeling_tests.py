import pytest
import numpy as np
from kdtree_labeling import KDTreeLabeling


def test_fail_on_negative_r():
    with pytest.raises(ValueError):
        KDTreeLabeling(r=-3, bound=2)


def test_fail_on_negative_bound():
    with pytest.raises(ValueError):
        KDTreeLabeling(r=3, bound=-2)


def test_fail_on_empty_space():
    labeling = KDTreeLabeling(r=1, bound=2)
    space = np.array([])
    classes = np.array([])
    with pytest.raises(ValueError):
        labeling.fit_predict(space, classes)


def test_fail_on_space_with_nans():
    labeling = KDTreeLabeling(r=1, bound=2)
    space = np.array([[np.inf, np.nan], [5, 4]])
    classes = np.array([0, 1])
    with pytest.raises(ValueError):
        labeling.fit_predict(space, classes)


def test_fail_on_empty_classes():
    labeling = KDTreeLabeling(r=1, bound=2)
    space = np.array([[5, 5]])
    classes = np.array([])
    with pytest.raises(ValueError):
        labeling.fit_predict(space, classes)


def test_fail_on_classes_with_nans():
    labeling = KDTreeLabeling(r=1, bound=2)
    space = np.array([5, 3])
    classes = np.array([np.nan])
    with pytest.raises(ValueError):
        labeling.fit_predict(space, classes)


@pytest.mark.parametrize("space, classes, expected_labels", [
    (np.array([[5, 5]]), np.array([0]), [0]),
    (np.array([[5, 5], [4, 4]]), np.array([0, 0]), [0, 0]),
    (np.array([[5, 5], [4, 4], [10, 10], [20, 20]]), np.array([0, 0, 1, 1]), [0, 0, 1, 1]),
    (np.array([[5, 5], [4, 4], [10, 10], [15, 15], [150, 200], [350, 150]]),
     np.array([0, 0, 1, 1, 2, 2]), [0, 0, 1, 1, 2, 2])
], ids=['one_point', 'two_points_from_one_class', 'four_points_from_two_classes', 'six_points_from_three_classes'])
def test_on_points_that_do_not_mix(space, classes, expected_labels):
    labeling = KDTreeLabeling(r=2, bound=6)
    assert np.array_equal(labeling.fit_predict(space, classes), expected_labels)


@pytest.mark.parametrize("space, classes, expected_labels", [
    (np.array([[5, 5], [4, 4]]), np.array([0, 1]), [-1, -1])
], ids=['two_mixed_points'])
def test_on_mixed_points(space, classes, expected_labels):
    labeling = KDTreeLabeling(r=2, bound=0)
    assert np.array_equal(labeling.fit_predict(space, classes), expected_labels)

