import pytest
from PruebaPython import app


class TestCotizacion(object):

    def test_cotizacion_sin_esmerilado(self):
        # Arrange
        request_data = dict(
            estilo='O',
            acabado='Pulido',
            vidrio='Transparente',
            cantidad=1,
            ancho=12,
            alto=15
        )

        # Act
        response = app.test_client().post('/', data=request_data, follow_redirects=True)

        # Assert
        assert response.status_code == 200
        assert b'49541.0' in response.data

    def test_cotizacion_con_esmerilado(self):
        # Arrange
        request_data = dict(
            estilo='O',
            acabado='Pulido',
            vidrio='Transparente',
            cantidad=1,
            ancho=12,
            alto=15
        )

        # Act
        response = app.test_client().post('/', data=request_data, follow_redirects=True)

        # Assert
        assert response.status_code == 200
        assert b'49541.0' in response.data


if __name__ == '__main__':
    pytest.main()
