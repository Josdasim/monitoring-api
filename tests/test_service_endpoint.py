
class TestServiceEndpoints:
    """Tests para los endpoints de servicios."""
    
    def test_create_service(self, client, sample_service_data):
        """Test: Crear un servicio exitosamente."""
        response = client.post("/api/v1/services/", json=sample_service_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["service_name"] == sample_service_data["service_name"]
        assert data["service_url"] == sample_service_data["service_url"]
        assert data["is_active"] is True
        assert "service_id" in data
    
    def test_create_service_duplicate_name(self, client, sample_service_data):
        """Test: No permitir servicios con nombre duplicado."""
        # Crear el primero
        client.post("/api/v1/services/", json=sample_service_data)
        
        # Intentar crear duplicado
        response = client.post("/api/v1/services/", json=sample_service_data)
        assert response.status_code == 400
    
    def test_list_services(self, client, sample_service_data):
        """Test: Listar servicios."""
        # Crear algunos servicios
        client.post("/api/v1/services/", json=sample_service_data)
        
        sample_service_data["service_name"] = "Another Service"
        client.post("/api/v1/services/", json=sample_service_data)
        
        # Listar
        response = client.get("/api/v1/services/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_service_by_id(self, client, sample_service_data):
        """Test: Obtener un servicio por ID."""
        # Crear servicio
        create_response = client.post("/api/v1/services/", json=sample_service_data)
        service_id = create_response.json()["service_id"]
        
        # Obtener por ID
        response = client.get(f"/api/v1/services/{service_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["service_id"] == service_id
        assert data["service_name"] == sample_service_data["service_name"]
    
    def test_get_nonexistent_service(self, client):
        """Test: Intentar obtener servicio que no existe."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/services/{fake_id}")
        assert response.status_code == 404
    
    def test_delete_service(self, client, sample_service_data):
        """Test: Eliminar un servicio."""
        # Crear servicio
        create_response = client.post("/api/v1/services/", json=sample_service_data)
        service_id = create_response.json()["service_id"]
        
        # Eliminar
        response = client.delete(f"/api/v1/services/{service_id}")
        assert response.status_code == 200
        
        # Verificar que ya no existe
        get_response = client.get(f"/api/v1/services/{service_id}")
        assert get_response.status_code == 404
