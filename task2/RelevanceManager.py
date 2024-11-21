class RelevanceManager:
    DOCUMENT_INDEX_OFFSET: int = 1
    GET_MOST_RELEVANT_DOCUMENTS_QUERY: int = 1
    CHANGE_ATTRIBUTE_OF_DOCUMENT_QUERY: int = 2

    class Document:
        __id: int
        __attributes: list[int]
        __cached_relevance_value: int = -1

        def __init__(self, id: int, attributes: list[int]):
            self.__id = id
            self.attributes = attributes

        def __str__(self) -> str:
            return str(self.__id)

        def __repr__(self) -> str:
            return str(self.__id)

        def get_relevance_value_by_params(self, params: list[int]) -> int:
            if len(self.attributes) != len(params):
                raise ValueError(
                    'number of document attributes is not equal to the number of parameters'
                )

            if self.__cached_relevance_value < 0:
                self.__cached_relevance_value = self.__calculate_relevance(params)

            return self.__cached_relevance_value

        def __calculate_relevance(self, params: list[int]) -> int:
            result = 0

            for i in range(len(params)):
                result += self.attributes[i] * params[i]

            return result

        def change_attribute_of_document(
                self,
                attribute_index: int,
                new_value: int
        ):
            self.attributes[attribute_index] = new_value
            self.__cached_relevance_value = -1

    __params: list[int]
    __documents: list[Document]

    def __init__(self):
        num_params = int(input())

        if not 0 < num_params < 100:
            raise Exception('Invalid range params')

        self.__params = list(map(int, input().split(' ')))

        if num_params != len(self.__params):
            raise Exception(
                'number of parameters is not equal to the number of parameters entered'
            )

        num_documents = int(input())

        self.__documents = []

        for document_index in range(num_documents):
            attributes = list(map(int, input().split(' ')))

            if len(attributes) != num_params:
                raise Exception(
                    'number of document attributes is not equal to the number of parameters entered'
                )

            self.__documents.append(RelevanceManager.Document(document_index + self.DOCUMENT_INDEX_OFFSET, attributes))

        num_queries = int(input())

        for i in range(num_queries):
            query = list(map(int, input().split(' ')))

            match query[0]:
                case self.GET_MOST_RELEVANT_DOCUMENTS_QUERY:
                     print(self.__get_most_relevant_documents(int(query[1])))
                case self.CHANGE_ATTRIBUTE_OF_DOCUMENT_QUERY:
                     self.__change_attribute_of_document(int(query[1]) - self.DOCUMENT_INDEX_OFFSET, int(query[2]), int(query[3]))
                case _:
                    raise Exception('A non-existent menu item is selected')

    def __get_most_relevant_documents(
            self,
            count: int = 10
    ) -> list[Document]:
        return sorted(
            self.__documents,
            key=lambda document: document.get_relevance_value_by_params(self.__params),
            reverse=True
        )[:count]

    def __change_attribute_of_document(
            self,
            document_index: int,
            attribute_index: int,
            new_value: int
    ) -> None:
        self.__documents[document_index].change_attribute_of_document(
            attribute_index,
            new_value
        )


RelevanceManager()
