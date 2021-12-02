import unittest
from indexer import *


class testSimilarity(unittest.TestCase):
    def test_volume_1(self):
        database = parse_ratings()
        user_in = {1: 3, 2: 4, 4: 5, 5: 5} # User's movie 
        similar_users = find_sim(user_in, database)
        n_movies = find_similar_movies(similar_users,database,user_in)
        recommendations = compute_movie_recommendation(n_movies, similar_users, database)

        self.assertEqual(find_sim({1: 3, 2: 4, 4: 5, 5: 5}, database), 
            {1: 1.0, 4: 0.3458572319330373})
        self.assertEqual(sorted(union({"a" : 1, "b" : 2}, {"a" : 1, "c" : 2})),
            ['a', 'b', 'c'])
        self.assertEqual(sorted(union({"a" : 1, "b" : 2}, {"d" : 1, "c" : 2})),
            ['a', 'b', 'c', 'd'])
        self.assertEqual(n_movies,
            [3, 6, 7, 8, 10]
        )
        self.assertEqual(recommendations, 
            {3: 4.229062584662965, 6: 4.0, 7: 5.0, 8: 2.0, 10: 2.027916553782713})

if __name__ == '__main__':
    test = testSimilarity()
    test.test_volume_1()