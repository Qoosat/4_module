from utils.data_generator import DataGenerator


class TestMovies:
    created_movie_id = None

    def test_get_movies(self, api_manager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert response.status_code == 200
        assert "movies" in data
        assert "count" in data
        assert isinstance(data["movies"], list)

    def test_get_movies_pagination(self, api_manager):
        response = api_manager.movies_api.get_movies(params={"page": 1, "pageSize": 3})
        data = response.json()

        assert response.status_code == 200
        assert data["page"] == 1
        assert data["pageSize"] == 3
        assert len(data["movies"]) <= 3

    def test_a_create_movie(self, admin_api_manager):
        movie_data = DataGenerator.generate_movie_data()
        response = admin_api_manager.movies_api.create_movie(movie_data)
        response_data = response.json()

        assert response.status_code == 201
        assert "id" in response_data

        TestMovies.created_movie_id = response_data["id"]

    def test_b_get_movie_by_id(self, api_manager):
        assert TestMovies.created_movie_id is not None

        response = api_manager.movies_api.get_movie_by_id(TestMovies.created_movie_id)
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == TestMovies.created_movie_id

    def test_get_movie_not_found(self, api_manager):
        response = api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

        assert response.status_code == 404

    def test_create_movie_without_auth(self, api_manager):
        movie_data = DataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)

        assert response.status_code in (401, 403)

    def test_update_movie(self, admin_api_manager, created_movie):
        update_data = {
            "name": f"Updated {DataGenerator.generate_random_name()}",
            "price": 777
        }
        response = admin_api_manager.movies_api.update_movie(created_movie["id"], update_data)
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == update_data["name"]
        assert data["price"] == update_data["price"]

    def test_delete_movie(self, admin_api_manager):
        movie_data = DataGenerator.generate_movie_data()
        create_response = admin_api_manager.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        response = admin_api_manager.movies_api.delete_movie(movie_id)

        assert response.status_code == 200
