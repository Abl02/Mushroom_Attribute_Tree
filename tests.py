import unittest
from project import *

class TestMushroomDataLoading(unittest.TestCase):
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')

    def test_load_dataset(self):
        m1 = self.mushrooms[0]
        self.assertFalse(m1.is_edible(), "Le premier champignon devrait être non comestible.")
        self.assertEqual(m1.get_attribute('cap-shape'), 'Convex')
        self.assertEqual(m1.get_attribute('odor'), 'Pungent')

        m2 = self.mushrooms[1]
        self.assertTrue(m2.is_edible(), "Le deuxième champignon devrait être comestible.")
        self.assertEqual(m2.get_attribute('cap-color'), 'Yellow')
        self.assertEqual(m2.get_attribute('odor'), 'Almond')

        m3 = self.mushrooms[2]
        self.assertTrue(m3.is_edible(), "Le troisième champignon devrait être comestible.")
        self.assertEqual(m3.get_attribute('cap-shape'), 'Bell')
        self.assertEqual(m3.get_attribute('odor'), 'Anise')

    def test_no_attribute(self):
        data = [Mushroom(True), Mushroom(True), Mushroom(False), Mushroom(True)]
        with self.assertRaises(ValueError):
            main(data)


def make_mushroom(attributes):
    ret = Mushroom(None)
    for k, v in attributes.items():
        ret.add_attribute(k, v)
    return ret

class TestBuildTree(unittest.TestCase):
    def setUp(self):
        self.data = load_dataset('mushrooms.csv')
        self.test_tree_root = build_decision_tree(self.data)

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            self.data[0].add_attribute('habitat', 0)
            self.data[0].add_attribute(0, 'good')
            self.data[1].add_attribute(True, 0.0)
            self.data[0].add_attribute(None, None)
            build_decision_tree(self.data)

    def test_tree_main_attribute(self):
        self.assertEqual(self.test_tree_root.criterion_, 'odor', "Le premier critère de division doit être 'odor'")
        nos = ['Pungent', 'Creosote', 'Foul', 'Fishy', 'Spicy', 'Musty']
        odors = {edge.label_: edge.child_ for edge in self.test_tree_root.edges_}
        for odor in nos:
            self.assertTrue(
                odors[odor].is_leaf() and odors[odor].criterion_ == 'No',
                f'Les champignons avec une odeur \'{odor}\' doivent être non-comestibles'
            )
    def test_tree_prediction(self):
        root = self.test_tree_root
        self.assertTrue(is_edible(root, make_mushroom({'odor': 'Almond'})))
        self.assertFalse(is_edible(root, make_mushroom({'odor': 'None', 'spore-print-color': 'Green'})))

    def test_boolean_convertion(self):
        expression = [('odor', 'Almond'), ('odor', 'Anise'), ('odor', 'None'),
                     [('spore-print-color', 'Brown'), ('spore-print-color', 'Black'),
                     ('spore-print-color', 'White'), [('habitat', 'Waste'), ('habitat', 'Leaves'),
                     [('cap-color', 'Cinnamon'), ('cap-color', 'Brown')],
                     ('habitat', 'Woods'), [('gill-size', 'Broad')],
                     ('habitat', 'Grasses'), ('habitat', 'Paths')],
                     ('spore-print-color', 'Chocolate'), ('spore-print-color', 'Orange'),
                     ('spore-print-color', 'Yellow'), ('spore-print-color', 'Buff')]]
        self.assertEqual(to_boolean_expression(self.test_tree_root, []), expression)

if __name__ == '__main__':
    unittest.main()
