from utils.data_generator import DataGenerator


class TestMovies:

    def test_get_movies(self, api_manager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert "movies" in data
        assert "count" in data
        assert isinstance(data["movies"], list)

    def test_get_movies_pagination(self, api_manager):
        response = api_manager.movies_api.get_movies(params={"page": 1, "pageSize": 3})
        data = response.json()

        assert data["page"] == 1
        assert data["pageSize"] == 3
        assert len(data["movies"]) <= 3

    def test_get_movies_filter_by_genre(self, api_manager):
        genre_id = 1
        response = api_manager.movies_api.get_movies(params={"genreId": genre_id})
        data = response.json()

        assert len(data["movies"]) > 0
        for movie in data["movies"]:
            assert movie["genreId"] == genre_id

    def test_create_movie(self, admin_api_manager):
        movie_data = DataGenerator.generate_movie_data()
        response = admin_api_manager.movies_api.create_movie(movie_data)
        response_data = response.json()

        assert "id" in response_data
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
        assert response_data["description"] == movie_data["description"]
        assert response_data["location"] == movie_data["location"]
        assert response_data["genreId"] == movie_data["genreId"]
        assert response_data["published"] == movie_data["published"]

        admin_api_manager.movies_api.delete_movie(response_data["id"])

    def test_get_movie_by_id(self, api_manager, created_movie):
        response = api_manager.movies_api.get_movie_by_id(created_movie["id"])
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]

    def test_get_movie_not_found(self, api_manager):
        api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

    def test_create_movie_without_auth(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)

        assert response.json()["statusCode"] == 401

    def test_update_movie(self, admin_api_manager, created_movie):
        update_data = {
            "name": f"Updated {DataGenerator.generate_random_name()}",
            "price": 777
        }
        response = admin_api_manager.movies_api.update_movie(created_movie["id"], update_data)
        data = response.json()

        assert data["name"] == update_data["name"]
        assert data["price"] == update_data["price"]

    def test_delete_movie(self, admin_api_manager):
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_api_manager.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        admin_api_manager.movies_api.delete_movie(movie_id)
        admin_api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
