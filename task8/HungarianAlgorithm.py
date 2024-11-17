import numpy as np

class HungarianAlgorithm:

    @staticmethod
    def execute(
            weight_matrix: np.array,
            is_maximization: bool = False
    ) -> np.array:

        weight_matrix = np.array(weight_matrix)

        rows_count, columns_count = weight_matrix.shape

        if rows_count != columns_count:
            raise ValueError("Matrix must be square!")

        reduced_matrix = HungarianAlgorithm.__reduce_matrix(
            weight_matrix,
            rows_count,
            columns_count,
            is_maximization
        )

        marked_matrix = HungarianAlgorithm.__get_marked_matrix(
            reduced_matrix,
            rows_count,
            columns_count
        )

        return HungarianAlgorithm.__extract_marked_elements(
            weight_matrix,
            marked_matrix
        )

    @staticmethod
    def __extract_marked_elements(
            weight_matrix: np.array,
            marked_matrix: np.array,
    ) -> np.array:
        if marked_matrix.shape != weight_matrix.shape:
            raise Exception("Matrix must be square!")

        return weight_matrix[marked_matrix].tolist()

    @staticmethod
    def get_minimal_line_cover(
            reduced_matrix: np.array,
            marked_matrix: np.array,
            rows_count: int,
            columns_count: int
    ) -> np.array:
        row_cover = np.zeros(rows_count, dtype=bool)
        col_cover = np.zeros(columns_count, dtype=bool)

        for i in range(rows_count):
            for j in range(columns_count):
                if marked_matrix[i, j] and not row_cover[i] and not col_cover[j]:
                    row_zeros = np.sum((reduced_matrix[i, :] == 0) & ~col_cover)
                    col_zeros = np.sum((reduced_matrix[:, j] == 0) & ~row_cover)

                    if row_zeros >= col_zeros:
                        row_cover[i] = True
                    else:
                        col_cover[j] = True

        while True:
            uncovered_zeros = np.argwhere((reduced_matrix == 0) & ~row_cover[:, None] & ~col_cover)
            if len(uncovered_zeros) == 0:
                break

            for i, j in uncovered_zeros:
                if not row_cover[i] and not col_cover[j]:
                    row_zeros = np.sum((reduced_matrix[i, :] == 0) & ~col_cover)
                    col_zeros = np.sum((reduced_matrix[:, j] == 0) & ~row_cover)

                    if row_zeros >= col_zeros:
                        row_cover[i] = True
                    else:
                        col_cover[j] = True

        return row_cover, col_cover

    @staticmethod
    def __get_marked_matrix(
            reduced_matrix: np.array,
            rows_count: int,
            columns_count: int
    ) -> np.array:
        row_cover = np.zeros(rows_count, dtype=bool)
        col_cover = np.zeros(columns_count, dtype=bool)
        marked_matrix = np.zeros((rows_count, columns_count), dtype=bool)

        zero_counts = [(i, np.sum(reduced_matrix[i] == 0)) for i in range(rows_count)]
        zero_counts.sort(key=lambda x: x[1])

        for i, _ in zero_counts:
            for j in range(columns_count):
                if reduced_matrix[i, j] == 0 and not row_cover[i] and not col_cover[j]:
                    marked_matrix[i, j] = True
                    row_cover[i] = True
                    col_cover[j] = True

        if np.all(row_cover) and np.all(col_cover):
            return marked_matrix

        corrected_matrix = HungarianAlgorithm.__get_corrected_matrix(
            reduced_matrix,
            marked_matrix,
            rows_count,
            columns_count
        )

        return HungarianAlgorithm.__get_marked_matrix(
            corrected_matrix,
            rows_count,
            columns_count
        )

    @staticmethod
    def __get_corrected_matrix(
            reduced_matrix: np.array,
            marked_matrix: np.array,
            rows_count: int,
            columns_count: int
    ) -> np.array:
        row_cover, col_cover = HungarianAlgorithm.get_minimal_line_cover(
            reduced_matrix,
            marked_matrix,
            rows_count,
            columns_count
        )

        min_uncovered = np.min(reduced_matrix[~row_cover[:, None] & ~col_cover])

        for i in range(rows_count):
            for j in range(columns_count):
                if not row_cover[i] and not col_cover[j]:
                    reduced_matrix[i, j] -= min_uncovered
                elif row_cover[i] and col_cover[j]:
                    reduced_matrix[i, j] += min_uncovered

        return reduced_matrix

    @staticmethod
    def __reduce_matrix(
            weight_matrix: np.array,
            rows_count: int,
            columns_count: int,
            is_maximization: bool = False
    ) -> np.array:
        weight_matrix_copy = weight_matrix.copy()

        if is_maximization:
            weight_matrix_copy = HungarianAlgorithm.__subtract_max_elem_from_rows_and_negate(
                weight_matrix_copy,
                rows_count
            )

        return HungarianAlgorithm.__subtract_min_elem_from_columns(
            HungarianAlgorithm.__subtract_min_elem_from_rows(
                weight_matrix_copy,
                rows_count
            ), columns_count)

    @staticmethod
    def __subtract_min_elem_from_rows(
            weight_matrix: np.array,
            rows_count: int
    ) -> np.array:
        for i in range(rows_count):
            weight_matrix[i] -= weight_matrix[i].min()

        return weight_matrix

    @staticmethod
    def __subtract_min_elem_from_columns(
            weight_matrix: np.array,
            columns_count: int
    ) -> np.array:
        for i in range(columns_count):
            weight_matrix[:, i] -= weight_matrix[:, i].min()

        return weight_matrix

    @staticmethod
    def __subtract_max_elem_from_rows_and_negate(
            weight_matrix: np.array,
            rows_count: int
    ) -> np.array:
        for i in range(rows_count):
            weight_matrix[i] -= weight_matrix[i].max()

        weight_matrix *= -1

        return weight_matrix


weight_matrix = [
    [7, 3, 6, 9, 5],
    [7, 5, 7, 5, 6],
    [7, 6, 8, 8, 9],
    [3, 1, 6, 5, 7],
    [2, 4, 9, 9, 5]
]

# weight_matrix = [
#         [4, 1, 3],
#         [2, 0, 5],
#         [3, 2, 2]
#     ]

# result = HungarianAlgorithm.execute(weight_matrix)
result = HungarianAlgorithm.execute(weight_matrix, is_maximization=True)

print(result)
print(np.sum(result))

