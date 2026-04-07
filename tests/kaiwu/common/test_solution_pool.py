import unittest
import numpy as np
from kaiwu.common import HeapUniquePool, ArgpartitionUniquePool, hamiltonian


class TestHeapUniquePool(unittest.TestCase):
    def setUp(self):
        # 构造一个简单的 Ising 模型矩阵
        self.mat = np.array([
            [1, 2, 3],
            [2, 4, 5],
            [3, 5, 6]
        ])
        self.size = 3
        self.size_limit = 2
        self.pool = HeapUniquePool(self.mat, self.size, self.size_limit)

    def test_initialization(self):
        """Test initialization of HeapUniquePool"""
        self.assertEqual(self.pool.size, 3)
        self.assertEqual(self.pool.size_limit, 2)
        self.assertEqual(len(self.pool.minheap_opt), 0)
        self.assertEqual(len(self.pool.opt_set), 0)

    def test_push_unique_solution(self):
        """Test pushing a unique solution"""
        solution1 = np.array([1, -1, 1])
        hamilton1 = hamiltonian(self.mat, solution1.reshape(1, -1))[0]
        self.pool.push(solution1, hamilton1)
        self.assertEqual(len(self.pool.minheap_opt), 1)
        self.assertIn(tuple(solution1), self.pool.opt_set)

    def test_push_duplicate_solution(self):
        """Test pushing a duplicate solution"""
        solution = np.array([1, -1, 1])
        hamilton = hamiltonian(self.mat, solution.reshape(1, -1))[0]
        self.pool.push(solution, hamilton)
        self.pool.push(solution, hamilton)  # Duplicate
        self.assertEqual(len(self.pool.minheap_opt), 1)

    def test_push_exceed_size_limit(self):
        """Test pushing solutions beyond size limit"""
        solution1 = np.array([1, -1, 1])
        solution2 = np.array([-1, 1, -1])
        solution3 = np.array([1, 1, 1])
        h1 = hamiltonian(self.mat, solution1.reshape(1, -1))[0]
        h2 = hamiltonian(self.mat, solution2.reshape(1, -1))[0]
        h3 = hamiltonian(self.mat, solution3.reshape(1, -1))[0]
        
        self.pool.push(solution1, h1)
        self.pool.push(solution2, h2)
        self.pool.push(solution3, h3)
        self.assertEqual(len(self.pool.minheap_opt), 2)  # Should maintain size limit

    def test_extend_solutions(self):
        """Test extending multiple solutions"""
        solutions = np.array([
            [1, -1, 1],
            [-1, 1, -1],
            [1, -1, 1]  # Duplicate
        ])
        self.pool.extend(solutions)
        self.assertEqual(len(self.pool.minheap_opt), 2)

    def test_get_solutions(self):
        """Test getting solutions"""
        solutions = np.array([
            [1, -1, 1],
            [-1, 1, -1]
        ])
        self.pool.extend(solutions)
        result = self.pool.get_solutions()
        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result, np.ndarray))

    def test_clear(self):
        """Test clearing the pool"""
        solution = np.array([1, -1, 1])
        hamilton = hamiltonian(self.mat, solution.reshape(1, -1))[0]
        self.pool.push(solution, hamilton)
        self.pool.clear()
        self.assertEqual(len(self.pool.minheap_opt), 0)
        self.assertEqual(len(self.pool.opt_set), 0)

    def test_json_serialization(self):
        """Test JSON serialization"""
        solution = np.array([1, -1, 1])
        hamilton = hamiltonian(self.mat, solution.reshape(1, -1))[0]
        self.pool.push(solution, hamilton)
        
        json_dict = self.pool.to_json_dict()
        self.assertIn('minheap_opt', json_dict)
        self.assertEqual(len(json_dict['minheap_opt']), 1)
        
        # Test deserialization
        new_pool = HeapUniquePool(self.mat, self.size, self.size_limit)
        new_pool.load_json_dict(json_dict)
        self.assertEqual(len(new_pool.minheap_opt), 1)
        self.assertEqual(len(new_pool.opt_set), 1)


class TestArgpartitionUniquePool(unittest.TestCase):
    def setUp(self):
        self.mat = np.array([
            [1, 2, 3],
            [2, 4, 5],
            [3, 5, 6]
        ])
        self.size = 3
        self.size_limit = 2
        self.pool = ArgpartitionUniquePool(self.mat, self.size, self.size_limit)

    def test_initialization(self):
        """Test initialization of ArgpartitionUniquePool"""
        self.assertEqual(self.pool.size, 3)
        self.assertEqual(self.pool.size_limit, 2)
        self.assertEqual(len(self.pool.opt), 0)
        self.assertEqual(len(self.pool.hamilton), 0)
        self.assertEqual(self.pool.threshold, float('inf'))

    def test_extend_empty_solutions(self):
        """Test extending with empty solutions"""
        empty_solutions = np.array([]).reshape(0, self.size)
        self.pool.extend(empty_solutions)
        self.assertEqual(len(self.pool.opt), 0)
        self.assertEqual(len(self.pool.hamilton), 0)

    def test_extend_unique_solutions(self):
        """Test extending with unique solutions"""
        solutions = np.array([
            [1, -1, 1],
            [-1, 1, -1]
        ])
        self.pool.extend(solutions, final=True)
        self.assertEqual(len(self.pool.opt), 2)
        self.assertEqual(len(self.pool.hamilton), 2)

    def test_extend_duplicate_solutions(self):
        """Test extending with duplicate solutions"""
        solutions = np.array([
            [1, -1, 1],
            [1, -1, 1],  # Duplicate
            [-1, 1, -1]
        ])
        self.pool.extend(solutions, final=True)
        self.assertEqual(len(self.pool.opt), 2)  # Should deduplicate

    def test_extend_exceed_size_limit(self):
        """Test extending beyond size limit"""
        solutions = np.array([
            [1, -1, 1],
            [-1, 1, -1],
            [1, 1, 1]
        ])
        self.pool.extend(solutions, final=True)
        self.assertEqual(len(self.pool.opt), self.size_limit)

    def test_get_solutions_empty(self):
        """Test getting solutions from empty pool"""
        solutions = self.pool.get_solutions()
        self.assertEqual(len(solutions), 0)

    def test_get_solutions_with_data(self):
        """Test getting solutions with data"""
        solutions = np.array([
            [1, -1, 1],
            [-1, 1, -1]
        ])
        self.pool.extend(solutions, final=True)
        result = self.pool.get_solutions()
        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result, np.ndarray))

    def test_clear(self):
        """Test clearing the pool"""
        solutions = np.array([[1, -1, 1], [-1, 1, -1]])
        self.pool.extend(solutions, final=True)
        self.pool.clear()
        self.assertEqual(self.pool.opt.shape[0], 0)
        self.assertEqual(len(self.pool.hamilton), 0)
        self.assertEqual(self.pool.threshold, float('inf'))

    def test_json_serialization(self):
        """Test JSON serialization"""
        solutions = np.array([[1, -1, 1], [-1, 1, -1]])
        self.pool.extend(solutions, final=True)
        
        json_dict = self.pool.to_json_dict()
        self.assertIn('opt', json_dict)
        self.assertIn('hamilton', json_dict)
        
        # Test deserialization
        new_pool = ArgpartitionUniquePool.from_json_dict(json_dict)
        self.assertEqual(len(new_pool.opt), 2)
        self.assertEqual(len(new_pool.hamilton), 2)

    def test_threshold_update(self):
        """Test threshold update mechanism"""
        solutions1 = np.array([[1, -1, 1]])
        self.pool.extend(solutions1, final=True)
        self.assertEqual(self.pool.threshold, float('inf'))  # Not full yet
        
        solutions2 = np.array([[-1, 1, -1], [1, 1, 1]])
        self.pool.extend(solutions2, final=True)
        self.assertNotEqual(self.pool.threshold, float('inf'))  # Should be updated

    def test_incremental_updates(self):
        """Test incremental updates without final flag"""
        solutions1 = np.array([[1, -1, 1]])
        self.pool.extend(solutions1, final=False)
        self.assertEqual(len(self.pool.candidate_solutions), 1)  # Should be in buffer
        
        solutions2 = np.array([[-1, 1, -1]])
        self.pool.extend(solutions2, final=True)  # Now process all solutions
        self.assertEqual(len(self.pool.opt), 2)
        self.assertEqual(len(self.pool.candidate_solutions), 0)  # Buffer should be cleared


if __name__ == '__main__':
    unittest.main()