
class TestHealthCheckEndpoints:
    """Tests para los endpoints de health checks."""
    
    def test_get_latest_check_no_checks(self, client, sample_service_data):
        """Test: Error cuando no hay health checks todavía."""
        # Crear servicio
        create_response = client.post("/api/v1/services/", json=sample_service_data)
        service_id = create_response.json()["service_id"]
        
        # Intentar obtener checks (no debería haber ninguno)
        response = client.get(f"/api/v1/health/{service_id}/latest")
        assert response.status_code == 404
    
    def test_get_history_empty(self, client, sample_service_data):
        """Test: Historial vacío cuando no hay checks."""
        # Crear servicio
        create_response = client.post("/api/v1/services/", json=sample_service_data)
        service_id = create_response.json()["service_id"]
        
        # Obtener historial vacío
        response = client.get(f"/api/v1/health/{service_id}/history")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_summary_no_checks(self, client, sample_service_data):
        """Test: Error en summary cuando no hay checks."""
        # Crear servicio
        create_response = client.post("/api/v1/services/", json=sample_service_data)
        service_id = create_response.json()["service_id"]
        
        # Intentar obtener summary
        response = client.get(f"/api/v1/health/{service_id}/summary")
        assert response.status_code == 404


class TestRootEndpoints:
    """Tests para endpoints raíz."""
    
    def test_root(self, client):
        """Test: Endpoint raíz funciona."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Monitoring API is running"
    
    def test_health_check(self, client):
        """Test: Health check de la API."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"