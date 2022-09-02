import config
from neo4j import GraphDatabase


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def get_names(self):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._get_movie_names)
            movie_names = []
            for movie_info in result:
                movie_names.append(movie_info[0])
            return movie_names

    @staticmethod
    def _get_movie_names(tx):
        query = (
            """
            MATCH (m:Movie) RETURN m.title
                                """
        )
        result = tx.run(query)
        return [row for row in result]

    def get_recommendation(self, id):
        with self.driver.session() as session:
            ##DUZENLE
            result = session.read_transaction(self._recommend_gkdw, id)
            gkd_result = session.read_transaction(self._recommend_gkd, id)
            gk_result = session.read_transaction(self._recommend_gk, id)
            if result:
                if id in result[0][0][0][0].get("title"):
                    result = gk_result
                if gkd_result:
                    if gkd_result[0][0][0][1] > result[0][0][0][1]:
                        result = gkd_result
                if gk_result:
                    if gk_result[0][0][0][1] > result[0][0][0][1]:
                        result = gk_result
            else:
                result = gk_result
            #     print("aaa")
            # print(result[0][0][0][0].get("title"))
            if result:
                recommendation_data = result[0][0]
                recommended_movies = []
                for movies in recommendation_data:
                    recommended_movies.append(movies[0])
                    print(movies[0].get('title'), '   Rat', movies[0].get('average_rating'), "   Sim", movies[1],
                          movies[0].get('imdb_id'))

                return recommended_movies

                # for movie in recommended_movies:
                #     print(movie.get('title'), movie.get('average_rating'))
            else:
                print('Similar movie not found!')

            # for row in result:
            # print(row.get('overview'))
            # print(row)
            # print("Found movie: {row}".format(row=row))

    @staticmethod
    def _recommend_gkdw(tx, id):
        id = "(?i)" + id
        query = (
            """
            MATCH (c1:Movie)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(c2:Movie)
            MATCH (c1:Movie)-[:HAS]->(k:Keyword)<-[:HAS]-(c2:Movie)
            MATCH (c1:Movie)-[:DIRECTED_BY]->(d:Person)<-[:DIRECTED_BY]-(c2:Movie)
            MATCH (c1:Movie)-[:WROTE_BY]->(w:Person)<-[:WROTE_BY]-(c2:Movie)
            WHERE c1 <> c2 AND c1.title =~ $id
            WITH c1, c2, COUNT(DISTINCT g)*2 + COUNT(DISTINCT k) + COUNT(DISTINCT d) + COUNT(DISTINCT w) as intersection_count

            WITH c1, c2, intersection_count
            ORDER BY intersection_count DESC, c2.average_rating DESC
            WITH c1, COLLECT([c2, intersection_count])[0..5] as neighbors
            return neighbors
                                """
        )
        result = tx.run(query, id=id)
        return [row for row in result]

    @staticmethod
    def _recommend_gkd(tx, id):
        id = "(?i)" + id
        query = (
            """
            MATCH (c1:Movie)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(c2:Movie)
            MATCH (c1:Movie)-[:HAS]->(k:Keyword)<-[:HAS]-(c2:Movie)
            MATCH (c1:Movie)-[:DIRECTED_BY]->(d:Person)<-[:DIRECTED_BY]-(c2:Movie)
            WHERE c1 <> c2 AND c1.title =~ $id
            WITH c1, c2, COUNT(DISTINCT g)*2 + COUNT(DISTINCT k) + COUNT(DISTINCT d)  as intersection_count

            WITH c1, c2, intersection_count
            ORDER BY intersection_count DESC, c2.average_rating DESC
            WITH c1, COLLECT([c2, intersection_count])[0..5] as neighbors
            return neighbors
                                """
        )
        result = tx.run(query, id=id)
        return [row for row in result]

    @staticmethod
    def _recommend_gk(tx, id):
        id = "(?i)" + id
        query = (
            """
            MATCH (c1:Movie)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(c2:Movie)
            MATCH (c1:Movie)-[:HAS]->(k:Keyword)<-[:HAS]-(c2:Movie)
            WHERE c1 <> c2 AND c1.title =~ $id
            WITH c1, c2, COUNT(DISTINCT g)*2 + COUNT(DISTINCT k) as intersection_count

            WITH c1, c2, intersection_count
            ORDER BY intersection_count DESC, c2.average_rating DESC
            WITH c1, COLLECT([c2, intersection_count])[0..5] as neighbors
            return neighbors
                                """
        )
        result = tx.run(query, id=id)
        return [row for row in result]


if __name__ == "__main__":
    uri = config.NEO4J_URI
    user = "neo4j"
    password = config.NEO4J_API_KEY
    app = App(uri, user, password)
    # print(app.get_names())
    app.close()
